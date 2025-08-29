from .base import BaseModel
from .org import Organization
from .dataset import Dataset
from .entity import Entity
from .link import Link
from .event import Event
from .narrative import Narrative
from .rule import Rule
from .signal import Signal
from .audit import AuditLog
from .raw_record import RawRecord

# Establish relationships
Organization.datasets = relationship("Dataset", back_populates="organization")
Organization.entities = relationship("Entity", back_populates="organization")
Organization.links = relationship("Link", back_populates="organization")
Organization.events = relationship("Event", back_populates="organization")
Organization.narratives = relationship("Narrative", back_populates="organization")
Organization.rules = relationship("Rule", back_populates="organization")
Organization.signals = relationship("Signal", back_populates="organization")
Organization.audit_logs = relationship("AuditLog", back_populates="organization")

Entity.audit_actions = relationship("AuditLog", back_populates="actor")

__all__ = [
    "BaseModel",
    "Organization", 
    "Dataset",
    "Entity",
    "Link",
    "Event",
    "Narrative",
    "Rule",
    "Signal",
    "AuditLog",
    "RawRecord"
]
