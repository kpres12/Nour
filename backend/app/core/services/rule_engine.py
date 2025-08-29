from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import yaml
from app.core.models import Rule, Signal, Entity


class RuleEngine:
    """Service for evaluating business rules and generating insights"""
    
    def evaluate_rules(self, rules: List[Rule], signals: List[Signal], db: Session) -> List[Dict]:
        """Evaluate all rules against current signals"""
        results = []
        
        for rule in rules:
            try:
                rule_result = self._evaluate_single_rule(rule, signals, db)
                if rule_result:
                    results.append(rule_result)
            except Exception as e:
                print(f"Error evaluating rule {rule.id}: {str(e)}")
                continue
        
        return results
    
    def _evaluate_single_rule(self, rule: Rule, signals: List[Signal], db: Session) -> Dict:
        """Evaluate a single rule against signals"""
        try:
            rule_def = json.loads(rule.definition)
            
            # Check if rule conditions are met
            conditions_met = self._check_conditions(rule_def.get('when', {}), signals)
            
            if conditions_met:
                # Rule triggered - generate narrative
                narrative = self._generate_rule_narrative(rule_def, signals, db)
                
                return {
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "triggered": True,
                    "narrative": narrative,
                    "severity": rule_def.get('severity', 'medium'),
                    "category": rule.category
                }
            else:
                return {
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "triggered": False,
                    "severity": rule_def.get('severity', 'medium'),
                    "category": rule.category
                }
                
        except Exception as e:
            print(f"Error evaluating rule {rule.id}: {str(e)}")
            return None
    
    def _check_conditions(self, conditions: Dict, signals: List[Signal]) -> bool:
        """Check if rule conditions are met"""
        if not conditions:
            return True
        
        # Handle 'all' conditions (AND logic)
        if 'all' in conditions:
            all_conditions = conditions['all']
            for condition in all_conditions:
                if not self._evaluate_condition(condition, signals):
                    return False
            return True
        
        # Handle 'any' conditions (OR logic)
        elif 'any' in conditions:
            any_conditions = conditions['any']
            for condition in any_conditions:
                if self._evaluate_condition(condition, signals):
                    return True
            return False
        
        # Single condition
        else:
            return self._evaluate_condition(conditions, signals)
    
    def _evaluate_condition(self, condition: Dict, signals: List[Signal]) -> bool:
        """Evaluate a single condition"""
        signal_kind = condition.get('signal')
        if not signal_kind:
            return False
        
        # Find matching signals
        matching_signals = [s for s in signals if s.kind == signal_kind]
        
        if not matching_signals:
            return False
        
        # Check where clause
        where_clause = condition.get('where', {})
        if not where_clause:
            return True
        
        # Evaluate where conditions
        for field, criteria in where_clause.items():
            if not self._evaluate_where_clause(field, criteria, matching_signals):
                return False
        
        return True
    
    def _evaluate_where_clause(self, field: str, criteria: Dict, signals: List[Signal]) -> bool:
        """Evaluate where clause criteria"""
        for signal in signals:
            try:
                payload = json.loads(signal.payload)
                value = payload.get(field)
                
                if value is None:
                    continue
                
                # Check if value meets criteria
                if self._check_value_criteria(value, criteria):
                    return True
                    
            except Exception as e:
                print(f"Error evaluating where clause: {str(e)}")
                continue
        
        return False
    
    def _check_value_criteria(self, value: Any, criteria: Dict) -> bool:
        """Check if a value meets the criteria"""
        for operator, threshold in criteria.items():
            if operator == 'gte':
                if not (value >= threshold):
                    return False
            elif operator == 'lte':
                if not (value <= threshold):
                    return False
            elif operator == 'gt':
                if not (value > threshold):
                    return False
            elif operator == 'lt':
                if not (value < threshold):
                    return False
            elif operator == 'eq':
                if not (value == threshold):
                    return False
            elif operator == 'ne':
                if not (value != threshold):
                    return False
            elif operator == 'in':
                if not (value in threshold):
                    return False
            elif operator == 'count':
                # Special case for count-based criteria
                if isinstance(value, (list, tuple)):
                    count = len(value)
                else:
                    count = 1
                
                if not self._check_value_criteria(count, threshold):
                    return False
        
        return True
    
    def _generate_rule_narrative(self, rule_def: Dict, signals: List[Signal], db: Session) -> Dict:
        """Generate narrative from rule definition and signals"""
        template = rule_def.get('narrative_template', '')
        actions = rule_def.get('actions', [])
        
        # Extract values from signals for template substitution
        template_vars = self._extract_template_variables(rule_def, signals)
        
        # Apply template variables
        narrative_text = template
        for var_name, var_value in template_vars.items():
            placeholder = f"{{{var_name}}}"
            narrative_text = narrative_text.replace(placeholder, str(var_value))
        
        return {
            "title": rule_def.get('name', 'Rule Triggered'),
            "summary": narrative_text,
            "actions": actions,
            "evidence": template_vars,
            "severity": rule_def.get('severity', 'medium')
        }
    
    def _extract_template_variables(self, rule_def: Dict, signals: List[Signal]) -> Dict:
        """Extract variables for template substitution"""
        variables = {}
        
        # Extract from signals
        for signal in signals:
            try:
                payload = json.loads(signal.payload)
                
                # Add signal data to variables
                signal_key = f"{signal.kind}_data"
                variables[signal_key] = payload
                
                # Add specific fields
                for key, value in payload.items():
                    variables[f"{signal.kind}_{key}"] = value
                    
            except Exception as e:
                print(f"Error extracting template variables: {str(e)}")
                continue
        
        # Add rule-specific variables
        variables['rule_name'] = rule_def.get('name', 'Unknown Rule')
        variables['severity'] = rule_def.get('severity', 'medium')
        
        return variables
    
    def create_rule_from_yaml(self, yaml_content: str) -> Dict:
        """Create rule definition from YAML"""
        try:
            rule_def = yaml.safe_load(yaml_content)
            return rule_def
        except Exception as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")
    
    def validate_rule_definition(self, rule_def: Dict) -> bool:
        """Validate rule definition structure"""
        required_fields = ['name', 'when', 'then']
        
        for field in required_fields:
            if field not in rule_def:
                return False
        
        # Validate 'when' clause
        when_clause = rule_def['when']
        if not isinstance(when_clause, dict):
            return False
        
        # Validate 'then' clause
        then_clause = rule_def['then']
        if not isinstance(then_clause, dict):
            return False
        
        if 'narrative_template' not in then_clause:
            return False
        
        return True
