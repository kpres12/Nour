from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
import json
from app.core.models import Narrative, Signal, Rule, Entity
from app.core.services.rule_engine import RuleEngine


class NarrativeService:
    """Service for generating narratives and insights"""
    
    def __init__(self):
        self.rule_engine = RuleEngine()
    
    def generate_narrative(self, title: str, summary: str, evidence: Dict, 
                          actions: List[str], org_id: int, db: Session) -> Narrative:
        """Generate a new narrative"""
        narrative = Narrative(
            org_id=org_id,
            title=title,
            summary=summary,
            evidence=json.dumps(evidence),
            actions=json.dumps(actions),
            generated_at=datetime.utcnow(),
            author="ai"
        )
        
        db.add(narrative)
        db.commit()
        db.refresh(narrative)
        
        return narrative
    
    def auto_generate_narratives(self, signals: List[Signal], rules: List[Rule], 
                               org_id: int, db: Session) -> List[Narrative]:
        """Automatically generate narratives based on signals and rules"""
        narratives = []
        
        # Evaluate rules to find triggered ones
        rule_results = self.rule_engine.evaluate_rules(rules, signals, db)
        
        for result in rule_results:
            if result.get('triggered', False):
                narrative_data = result['narrative']
                
                # Create narrative from rule result
                narrative = self.generate_narrative(
                    title=narrative_data['title'],
                    summary=narrative_data['summary'],
                    evidence=narrative_data['evidence'],
                    actions=narrative_data['actions'],
                    org_id=org_id,
                    db=db
                )
                
                narratives.append(narrative)
        
        # Generate additional narratives based on signal patterns
        signal_narratives = self._generate_signal_based_narratives(signals, org_id, db)
        narratives.extend(signal_narratives)
        
        return narratives
    
    def _generate_signal_based_narratives(self, signals: List[Signal], org_id: int, db: Session) -> List[Narrative]:
        """Generate narratives based on signal patterns"""
        narratives = []
        
        # Group signals by type
        signal_groups = {}
        for signal in signals:
            if signal.kind not in signal_groups:
                signal_groups[signal.kind] = []
            signal_groups[signal.kind].append(signal)
        
        # Generate narratives for high-scoring signals
        for signal_kind, signal_list in signal_groups.items():
            high_score_signals = [s for s in signal_list if s.score > s.threshold]
            
            if high_score_signals:
                narrative = self._create_signal_narrative(signal_kind, high_score_signals, org_id, db)
                if narrative:
                    narratives.append(narrative)
        
        return narratives
    
    def _create_signal_narrative(self, signal_kind: str, signals: List[Signal], 
                                org_id: int, db: Session) -> Narrative:
        """Create a narrative for a specific signal type"""
        if not signals:
            return None
        
        # Get the highest scoring signal
        top_signal = max(signals, key=lambda x: x.score)
        
        try:
            payload = json.loads(top_signal.payload)
            
            # Generate title and summary based on signal type
            title, summary, actions = self._generate_signal_content(signal_kind, payload, top_signal.score)
            
            # Create narrative
            narrative = self.generate_narrative(
                title=title,
                summary=summary,
                evidence={
                    "signal_type": signal_kind,
                    "signal_score": top_signal.score,
                    "signal_data": payload,
                    "signals_count": len(signals)
                },
                actions=actions,
                org_id=org_id,
                db=db
            )
            
            return narrative
            
        except Exception as e:
            print(f"Error creating signal narrative: {str(e)}")
            return None
    
    def _generate_signal_content(self, signal_kind: str, payload: Dict, score: float) -> tuple:
        """Generate title, summary, and actions for a signal"""
        if signal_kind == "pipeline_velocity_delta":
            delta = payload.get('delta', 0)
            if delta > 0:
                title = "Pipeline Velocity Improving"
                summary = f"Sales pipeline velocity has improved by {delta:.1%} compared to the previous period."
                actions = [
                    "Continue current sales practices",
                    "Share best practices with team",
                    "Monitor for sustained improvement"
                ]
            else:
                title = "Pipeline Velocity Declining"
                summary = f"Sales pipeline velocity has declined by {abs(delta):.1%} compared to the previous period."
                actions = [
                    "Review sales process bottlenecks",
                    "Analyze deal stage progression",
                    "Implement velocity improvement initiatives"
                ]
        
        elif signal_kind == "late_invoice_risk":
            late_percentage = payload.get('late_percentage', 0)
            late_amount = payload.get('late_amount', 0)
            
            title = "High Late Invoice Risk"
            summary = f"{late_percentage:.1%} of invoices are late, representing ${late_amount:,.0f} in overdue payments."
            actions = [
                "Implement stricter payment terms",
                "Automate payment reminders",
                "Review credit policies for high-risk customers"
            ]
        
        elif signal_kind == "stalled_deal_motif":
            stalled_count = payload.get('stalled_deals', 0)
            avg_duration = payload.get('avg_stall_duration', 0)
            
            title = "Deals Stalled in Pipeline"
            summary = f"{stalled_count} deals are stalled with an average stall duration of {avg_duration:.0f} days."
            actions = [
                "Review stalled deal strategies",
                "Implement deal acceleration programs",
                "Provide additional sales support resources"
            ]
        
        elif signal_kind == "support_churn_flag":
            churn_score = payload.get('churn_score', 0)
            
            title = "Customer Support Churn Risk"
            summary = f"Customer support metrics indicate a churn risk score of {churn_score:.1%}."
            actions = [
                "Review support ticket resolution times",
                "Implement customer satisfaction surveys",
                "Develop proactive customer success programs"
            ]
        
        else:
            title = f"{signal_kind.replace('_', ' ').title()} Alert"
            summary = f"Signal {signal_kind} has been triggered with a score of {score:.2f}."
            actions = [
                "Review signal details",
                "Investigate root causes",
                "Develop mitigation strategies"
            ]
        
        return title, summary, actions
    
    def get_narrative_insights(self, narrative_id: int, org_id: int, db: Session) -> Dict:
        """Get detailed insights for a narrative"""
        narrative = db.query(Narrative).filter(
            Narrative.id == narrative_id,
            Narrative.org_id == org_id
        ).first()
        
        if not narrative:
            return None
        
        try:
            evidence = json.loads(narrative.evidence)
            actions = json.loads(narrative.actions)
            
            insights = {
                "id": narrative.id,
                "title": narrative.title,
                "summary": narrative.summary,
                "evidence": evidence,
                "actions": actions,
                "generated_at": narrative.generated_at.isoformat(),
                "author": narrative.author,
                "confidence": self._calculate_narrative_confidence(evidence),
                "priority": self._calculate_narrative_priority(evidence, actions)
            }
            
            return insights
            
        except Exception as e:
            print(f"Error getting narrative insights: {str(e)}")
            return None
    
    def _calculate_narrative_confidence(self, evidence: Dict) -> float:
        """Calculate confidence score for narrative"""
        # Simple confidence calculation based on evidence quality
        confidence_factors = []
        
        if 'signal_score' in evidence:
            confidence_factors.append(evidence['signal_score'])
        
        if 'signals_count' in evidence:
            confidence_factors.append(min(evidence['signals_count'] / 5, 1.0))
        
        if 'signal_data' in evidence:
            data_quality = len(evidence['signal_data']) / 10
            confidence_factors.append(min(data_quality, 1.0))
        
        if confidence_factors:
            return sum(confidence_factors) / len(confidence_factors)
        else:
            return 0.5
    
    def _calculate_narrative_priority(self, evidence: Dict, actions: List[str]) -> str:
        """Calculate priority level for narrative"""
        # Simple priority calculation
        if 'signal_score' in evidence and evidence['signal_score'] > 0.8:
            return "high"
        elif 'signal_score' in evidence and evidence['signal_score'] > 0.5:
            return "medium"
        else:
            return "low"
