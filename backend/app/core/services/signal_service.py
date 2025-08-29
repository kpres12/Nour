from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import pandas as pd
from app.core.models import Signal, RawRecord, Dataset


class SignalService:
    """Service for computing business signals and metrics"""
    
    def compute_signals(self, org_id: int, period_start: datetime, period_end: datetime, 
                       dataset_id: int = None, db: Session = None) -> List[Signal]:
        """Compute signals for the organization"""
        signals = []
        
        # Compute pipeline velocity delta
        velocity_signal = self._compute_pipeline_velocity_delta(org_id, period_start, period_end, db)
        if velocity_signal:
            signals.append(velocity_signal)
        
        # Compute late invoice risk
        invoice_signal = self._compute_late_invoice_risk(org_id, period_start, period_end, db)
        if invoice_signal:
            signals.append(invoice_signal)
        
        # Compute stalled deal motif
        deal_signal = self._compute_stalled_deal_motif(org_id, period_start, period_end, db)
        if deal_signal:
            signals.append(deal_signal)
        
        # Compute support churn flag
        support_signal = self._compute_support_churn_flag(org_id, period_start, period_end, db)
        if support_signal:
            signals.append(support_signal)
        
        return signals
    
    def _compute_pipeline_velocity_delta(self, org_id: int, period_start: datetime, 
                                       period_end: datetime, db: Session) -> Signal:
        """Compute pipeline velocity change"""
        try:
            # Get deals data from raw records
            deals_data = self._get_deals_data(org_id, period_start, period_end, db)
            
            if not deals_data:
                return None
            
            # Calculate velocity metrics
            current_period_velocity = self._calculate_deal_velocity(deals_data, period_start, period_end)
            previous_period_start = period_start - (period_end - period_start)
            previous_period_end = period_start
            previous_period_velocity = self._calculate_deal_velocity(deals_data, previous_period_start, previous_period_end)
            
            # Calculate delta
            if previous_period_velocity > 0:
                velocity_delta = (current_period_velocity - previous_period_velocity) / previous_period_velocity
            else:
                velocity_delta = 0
            
            # Normalize score (-1 to 1, where 0 is no change)
            score = max(-1, min(1, velocity_delta))
            
            signal = Signal(
                org_id=org_id,
                kind="pipeline_velocity_delta",
                period_start=period_start,
                period_end=period_end,
                payload=json.dumps({
                    "current_velocity": current_period_velocity,
                    "previous_velocity": previous_period_velocity,
                    "delta": velocity_delta,
                    "deals_count": len(deals_data)
                }),
                score=score,
                threshold=0.1
            )
            
            db.add(signal)
            db.commit()
            db.refresh(signal)
            
            return signal
            
        except Exception as e:
            print(f"Error computing pipeline velocity: {str(e)}")
            return None
    
    def _compute_late_invoice_risk(self, org_id: int, period_start: datetime, 
                                 period_end: datetime, db: Session) -> Signal:
        """Compute late invoice risk"""
        try:
            # Get invoices data
            invoices_data = self._get_invoices_data(org_id, period_start, period_end, db)
            
            if not invoices_data:
                return None
            
            # Calculate risk metrics
            total_invoices = len(invoices_data)
            late_invoices = sum(1 for inv in invoices_data if self._is_invoice_late(inv))
            late_percentage = late_invoices / total_invoices if total_invoices > 0 else 0
            
            # Calculate total late amount
            late_amount = sum(float(inv.get('amount', 0)) for inv in invoices_data if self._is_invoice_late(inv))
            
            # Risk score based on percentage and amount
            risk_score = min(1.0, (late_percentage * 0.7) + (min(late_amount / 10000, 1.0) * 0.3))
            
            signal = Signal(
                org_id=org_id,
                kind="late_invoice_risk",
                period_start=period_start,
                period_end=period_end,
                payload=json.dumps({
                    "total_invoices": total_invoices,
                    "late_invoices": late_invoices,
                    "late_percentage": late_percentage,
                    "late_amount": late_amount,
                    "risk_score": risk_score
                }),
                score=risk_score,
                threshold=0.3
            )
            
            db.add(signal)
            db.commit()
            db.refresh(signal)
            
            return signal
            
        except Exception as e:
            print(f"Error computing late invoice risk: {str(e)}")
            return None
    
    def _compute_stalled_deal_motif(self, org_id: int, period_start: datetime, 
                                  period_end: datetime, db: Session) -> Signal:
        """Compute stalled deal patterns"""
        try:
            # Get deals data
            deals_data = self._get_deals_data(org_id, period_start, period_end, db)
            
            if not deals_data:
                return None
            
            # Find stalled deals (no stage change in 30+ days)
            stalled_deals = []
            for deal in deals_data:
                if self._is_deal_stalled(deal):
                    stalled_deals.append(deal)
            
            stalled_count = len(stalled_deals)
            total_deals = len(deals_data)
            stalled_percentage = stalled_count / total_deals if total_deals > 0 else 0
            
            # Calculate average stall duration
            stall_durations = [self._get_deal_stall_duration(deal) for deal in stalled_deals]
            avg_stall_duration = sum(stall_durations) / len(stall_durations) if stall_durations else 0
            
            # Score based on percentage and duration
            score = min(1.0, (stalled_percentage * 0.6) + (min(avg_stall_duration / 60, 1.0) * 0.4))
            
            signal = Signal(
                org_id=org_id,
                kind="stalled_deal_motif",
                period_start=period_start,
                period_end=period_end,
                payload=json.dumps({
                    "total_deals": total_deals,
                    "stalled_deals": stalled_count,
                    "stalled_percentage": stalled_percentage,
                    "avg_stall_duration": avg_stall_duration,
                    "stalled_deal_ids": [deal.get('deal_id', 'unknown') for deal in stalled_deals]
                }),
                score=score,
                threshold=0.4
            )
            
            db.add(signal)
            db.commit()
            db.refresh(signal)
            
            return signal
            
        except Exception as e:
            print(f"Error computing stalled deal motif: {str(e)}")
            return None
    
    def _compute_support_churn_flag(self, org_id: int, period_start: datetime, 
                                  period_end: datetime, db: Session) -> Signal:
        """Compute support churn indicators"""
        try:
            # Get support tickets data
            tickets_data = self._get_tickets_data(org_id, period_start, period_end, db)
            
            if not tickets_data:
                return None
            
            # Calculate churn indicators
            high_severity_tickets = sum(1 for ticket in tickets_data if ticket.get('severity') in ['high', 'critical'])
            unresolved_tickets = sum(1 for ticket in tickets_data if ticket.get('status') not in ['resolved', 'closed'])
            
            total_tickets = len(tickets_data)
            
            # Churn risk factors
            severity_risk = high_severity_tickets / total_tickets if total_tickets > 0 else 0
            resolution_risk = unresolved_tickets / total_tickets if total_tickets > 0 else 0
            
            # Combined churn score
            churn_score = (severity_risk * 0.6) + (resolution_risk * 0.4)
            
            signal = Signal(
                org_id=org_id,
                kind="support_churn_flag",
                period_start=period_start,
                period_end=period_end,
                payload=json.dumps({
                    "total_tickets": total_tickets,
                    "high_severity_tickets": high_severity_tickets,
                    "unresolved_tickets": unresolved_tickets,
                    "severity_risk": severity_risk,
                    "resolution_risk": resolution_risk,
                    "churn_score": churn_score
                }),
                score=churn_score,
                threshold=0.5
            )
            
            db.add(signal)
            db.commit()
            db.refresh(signal)
            
            return signal
            
        except Exception as e:
            print(f"Error computing support churn flag: {str(e)}")
            return None
    
    def _get_deals_data(self, org_id: int, period_start: datetime, period_end: datetime, db: Session) -> List[Dict]:
        """Get deals data from raw records"""
        # This would typically query a deals dataset
        # For MVP, we'll return sample data
        return []
    
    def _get_invoices_data(self, org_id: int, period_start: datetime, period_end: datetime, db: Session) -> List[Dict]:
        """Get invoices data from raw records"""
        # This would typically query an invoices dataset
        # For MVP, we'll return sample data
        return []
    
    def _get_tickets_data(self, org_id: int, period_start: datetime, period_end: datetime, db: Session) -> List[Dict]:
        """Get support tickets data from raw records"""
        # This would typically query a tickets dataset
        # For MVP, we'll return sample data
        return []
    
    def _calculate_deal_velocity(self, deals_data: List[Dict], start: datetime, end: datetime) -> float:
        """Calculate average deal velocity in days"""
        # Placeholder implementation
        return 30.0
    
    def _is_invoice_late(self, invoice: Dict) -> bool:
        """Check if invoice is late"""
        due_date = invoice.get('due_date')
        if not due_date:
            return False
        
        try:
            due_date = pd.to_datetime(due_date)
            return due_date < datetime.utcnow()
        except:
            return False
    
    def _is_deal_stalled(self, deal: Dict) -> bool:
        """Check if deal is stalled"""
        # Placeholder implementation
        return False
    
    def _get_deal_stall_duration(self, deal: Dict) -> int:
        """Get deal stall duration in days"""
        # Placeholder implementation
        return 45
