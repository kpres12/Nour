from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from rapidfuzz import fuzz
from app.core.models import Entity, RawRecord


class EntityResolver:
    """Service for resolving entities from raw data"""
    
    def __init__(self):
        self.name_threshold = 0.8
        self.email_threshold = 0.9
        self.phone_threshold = 0.85
    
    def resolve_entities(self, raw_records: List[RawRecord], org_id: int, db: Session) -> List[Entity]:
        """Resolve entities from raw records"""
        entities = []
        
        for record in raw_records:
            try:
                data = json.loads(record.payload)
                
                # Extract entity type based on data structure
                entity_type = self._detect_entity_type(data)
                
                if entity_type:
                    # Check if entity already exists
                    existing_entity = self._find_existing_entity(data, entity_type, org_id, db)
                    
                    if existing_entity:
                        # Update existing entity
                        self._update_entity(existing_entity, data, db)
                        entities.append(existing_entity)
                    else:
                        # Create new entity
                        new_entity = self._create_entity(data, entity_type, org_id, db)
                        entities.append(new_entity)
                        
            except Exception as e:
                print(f"Error processing record {record.id}: {str(e)}")
                continue
        
        return entities
    
    def _detect_entity_type(self, data: Dict[str, Any]) -> str:
        """Detect entity type from data structure"""
        if 'account' in data or 'company' in data:
            return 'company'
        elif 'name' in data and ('email' in data or 'phone' in data):
            return 'person'
        elif 'deal_id' in data or 'opportunity' in data:
            return 'deal'
        elif 'invoice_id' in data or 'invoice_number' in data:
            return 'invoice'
        elif 'ticket_id' in data or 'case_id' in data:
            return 'ticket'
        else:
            return 'generic'
    
    def _find_existing_entity(self, data: Dict[str, Any], entity_type: str, org_id: int, db: Session) -> Entity:
        """Find existing entity using fuzzy matching"""
        existing_entities = db.query(Entity).filter(
            Entity.org_id == org_id,
            Entity.type == entity_type
        ).all()
        
        best_match = None
        best_score = 0
        
        for entity in existing_entities:
            canonical = json.loads(entity.canonical)
            score = self._calculate_similarity(data, canonical)
            
            if score > best_score and score > self._get_threshold_for_field(data):
                best_score = score
                best_match = entity
        
        return best_match
    
    def _calculate_similarity(self, data1: Dict[str, Any], data2: Dict[str, Any]) -> float:
        """Calculate similarity between two data records"""
        scores = []
        
        # Compare names
        if 'name' in data1 and 'name' in data2:
            name_score = fuzz.ratio(data1['name'].lower(), data2['name'].lower()) / 100
            scores.append(name_score)
        
        # Compare emails
        if 'email' in data1 and 'email' in data2:
            email_score = fuzz.ratio(data1['email'].lower(), data2['email'].lower()) / 100
            scores.append(email_score)
        
        # Compare phone numbers
        if 'phone' in data1 and 'phone' in data2:
            phone_score = fuzz.ratio(data1['phone'], data2['phone']) / 100
            scores.append(phone_score)
        
        # Compare company names
        if 'company' in data1 and 'company' in data2:
            company_score = fuzz.ratio(data1['company'].lower(), data2['company'].lower()) / 100
            scores.append(company_score)
        
        return max(scores) if scores else 0
    
    def _get_threshold_for_field(self, data: Dict[str, Any]) -> float:
        """Get threshold based on data type"""
        if 'email' in data:
            return self.email_threshold
        elif 'phone' in data:
            return self.phone_threshold
        else:
            return self.name_threshold
    
    def _create_entity(self, data: Dict[str, Any], entity_type: str, org_id: int, db: Session) -> Entity:
        """Create new entity"""
        entity = Entity(
            org_id=org_id,
            type=entity_type,
            canonical=json.dumps(data),
            confidence=1.0,
            provenance=json.dumps({"source": "raw_record"})
        )
        
        db.add(entity)
        db.commit()
        db.refresh(entity)
        
        return entity
    
    def _update_entity(self, entity: Entity, new_data: Dict[str, Any], db: Session):
        """Update existing entity with new data"""
        canonical = json.loads(entity.canonical)
        
        # Merge data, preferring newer values
        merged_data = {**canonical, **new_data}
        entity.canonical = json.dumps(merged_data)
        
        # Update confidence based on data quality
        entity.confidence = min(1.0, entity.confidence + 0.1)
        
        db.commit()
