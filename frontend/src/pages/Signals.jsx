import React, { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

function Signals() {
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)
  const [computing, setComputing] = useState(false)
  const [signalKind, setSignalKind] = useState('')
  const [periodDays, setPeriodDays] = useState(90)

  useEffect(() => {
    loadSignals()
  }, [signalKind])

  const loadSignals = async () => {
    try {
      setLoading(true)
      let url = '/signals'
      const params = new URLSearchParams()
      
      if (signalKind) params.append('kind', signalKind)
      
      if (params.toString()) {
        url += '?' + params.toString()
      }
      
      const data = await apiClient.get(url)
      setSignals(data)
    } catch (error) {
      console.error('Error loading signals:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleComputeSignals = async () => {
    try {
      setComputing(true)
      await apiClient.post(`/signals/compute?period_days=${periodDays}`)
      await loadSignals() // Reload to show new signals
      alert('Signals computed successfully!')
    } catch (error) {
      console.error('Error computing signals:', error)
      alert('Error computing signals')
    } finally {
      setComputing(false)
    }
  }

  const getSignalIcon = (kind) => {
    switch (kind) {
      case 'pipeline_velocity_delta': return '📈'
      case 'late_invoice_risk': return '⚠️'
      case 'stalled_deal_motif': return '⏸️'
      case 'support_churn_flag': return '🔴'
      case 'market_headwind': return '🌪️'
      case 'revenue_trend': return '💰'
      case 'customer_satisfaction': return '😊'
      case 'operational_efficiency': return '⚡'
      default: return '📊'
    }
  }

  const getSignalColor = (score, threshold) => {
    if (score > threshold) {
      if (score > 0.8) return '#ef4444' // Red for high risk
      if (score > 0.6) return '#f59e0b' // Orange for medium risk
      return '#10b981' // Green for low risk
    }
    return '#6b7280' // Gray for below threshold
  }

  const formatSignalValue = (kind, payload) => {
    try {
      const data = JSON.parse(payload)
      
      switch (kind) {
        case 'pipeline_velocity_delta':
          const delta = data.delta || 0
          return `${delta > 0 ? '+' : ''}${(delta * 100).toFixed(1)}%`
        
        case 'late_invoice_risk':
          return `${(data.late_percentage * 100).toFixed(1)}% (${data.late_invoices}/${data.total_invoices})`
        
        case 'stalled_deal_motif':
          return `${data.stalled_deals}/${data.total_deals} (${(data.stalled_percentage * 100).toFixed(1)}%)`
        
        case 'support_churn_flag':
          return `${(data.churn_score * 100).toFixed(1)}%`
        
        default:
          return data.score ? `${(data.score * 100).toFixed(1)}%` : 'N/A'
      }
    } catch {
      return 'N/A'
    }
  }

  if (loading) {
    return <div className="loading">Loading signals...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Signals</h1>
        <p className="page-subtitle">
          Monitor business metrics and automated anomaly detection
        </p>
      </div>

      {/* Compute Signals */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1.5rem' }}>Compute Signals</h3>
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
          <div className="form-group">
            <label className="form-label">Period (Days)</label>
            <select
              className="form-input"
              value={periodDays}
              onChange={(e) => setPeriodDays(parseInt(e.target.value))}
            >
              <option value={30}>30 days</option>
              <option value={60}>60 days</option>
              <option value={90}>90 days</option>
              <option value={180}>180 days</option>
              <option value={365}>365 days</option>
            </select>
          </div>
          
          <div className="form-group" style={{ display: 'flex', alignItems: 'end' }}>
            <button 
              onClick={handleComputeSignals}
              className="btn-primary"
              disabled={computing}
            >
              {computing ? 'Computing...' : 'Compute Signals'}
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
          <div className="form-group">
            <label className="form-label">Signal Type</label>
            <select
              className="form-input"
              value={signalKind}
              onChange={(e) => setSignalKind(e.target.value)}
            >
              <option value="">All Types</option>
              <option value="pipeline_velocity_delta">Pipeline Velocity Delta</option>
              <option value="late_invoice_risk">Late Invoice Risk</option>
              <option value="stalled_deal_motif">Stalled Deal Motif</option>
              <option value="support_churn_flag">Support Churn Flag</option>
              <option value="market_headwind">Market Headwind</option>
              <option value="revenue_trend">Revenue Trend</option>
              <option value="customer_satisfaction">Customer Satisfaction</option>
              <option value="operational_efficiency">Operational Efficiency</option>
            </select>
          </div>
        </div>
      </div>

      {/* Signals List */}
      {signals.length > 0 ? (
        <div className="grid">
          {signals.map((signal) => {
            const icon = getSignalIcon(signal.kind)
            const color = getSignalColor(signal.score, signal.threshold)
            const value = formatSignalValue(signal.kind, signal.payload)
            
            return (
              <div key={signal.id} className="card">
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', marginBottom: '1rem' }}>
                  <div style={{ 
                    fontSize: '2rem',
                    background: `${color}20`,
                    padding: '0.5rem',
                    borderRadius: '0.5rem',
                    border: `1px solid ${color}40`
                  }}>
                    {icon}
                  </div>
                  
                  <div style={{ flex: 1 }}>
                    <h3 style={{ color, marginBottom: '0.5rem' }}>
                      {signal.kind.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </h3>
                    
                    <div style={{ 
                      display: 'flex', 
                      gap: '0.5rem', 
                      flexWrap: 'wrap', 
                      marginBottom: '0.5rem',
                      fontSize: '0.875rem'
                    }}>
                      <span style={{
                        background: 'rgba(59, 130, 246, 0.2)',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        color: '#3b82f6'
                      }}>
                        Score: {(signal.score * 100).toFixed(1)}%
                      </span>
                      
                      <span style={{
                        background: 'rgba(139, 92, 246, 0.2)',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        color: '#8b5cf6'
                      }}>
                        Threshold: {(signal.threshold * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                {/* Signal Value */}
                <div style={{ 
                  background: 'rgba(255,255,255,0.05)',
                  padding: '1rem',
                  borderRadius: '0.5rem',
                  marginBottom: '1rem',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: color }}>
                    {value}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.7)' }}>
                    Current Value
                  </div>
                </div>

                {/* Period */}
                <div style={{ 
                  fontSize: '0.875rem', 
                  color: 'rgba(255,255,255,0.6)',
                  marginBottom: '1rem'
                }}>
                  Period: {new Date(signal.period_start).toLocaleDateString()} - {new Date(signal.period_end).toLocaleDateString()}
                </div>

                {/* Status */}
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  paddingTop: '1rem',
                  borderTop: '1px solid rgba(255,255,255,0.1)'
                }}>
                  <span style={{
                    background: signal.score > signal.threshold ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.2)',
                    color: signal.score > signal.threshold ? '#ef4444' : '#22c55e',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '0.25rem',
                    fontSize: '0.75rem',
                    textTransform: 'uppercase'
                  }}>
                    {signal.score > signal.threshold ? 'Triggered' : 'Normal'}
                  </span>
                  
                  <span style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.6)' }}>
                    Created: {new Date(signal.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
            No Signals Found
          </h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '2rem' }}>
            {signalKind 
              ? 'No signals of this type found. Try computing signals or adjusting your filters.'
              : 'No signals have been computed yet. Compute signals to start monitoring your business metrics.'
            }
          </p>
          {!signalKind && (
            <button onClick={handleComputeSignals} className="btn-primary" disabled={computing}>
              {computing ? 'Computing...' : 'Compute Your First Signals'}
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export default Signals
