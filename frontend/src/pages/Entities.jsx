import React, { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

function Entities() {
  const [entities, setEntities] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [entityType, setEntityType] = useState('')

  useEffect(() => {
    loadEntities()
  }, [searchQuery, entityType])

  const loadEntities = async () => {
    try {
      setLoading(true)
      let url = '/entities'
      const params = new URLSearchParams()
      
      if (searchQuery) params.append('query', searchQuery)
      if (entityType) params.append('type', entityType)
      
      if (params.toString()) {
        url += '?' + params.toString()
      }
      
      const data = await apiClient.get(url)
      setEntities(data)
    } catch (error) {
      console.error('Error loading entities:', error)
    } finally {
      setLoading(false)
    }
  }

  const getEntityIcon = (type) => {
    switch (type) {
      case 'person': return '👤'
      case 'company': return '🏢'
      case 'deal': return '💼'
      case 'invoice': return '📄'
      case 'ticket': return '🎫'
      default: return '🔗'
    }
  }

  const getEntityColor = (type) => {
    switch (type) {
      case 'person': return '#10b981'
      case 'company': return '#3b82f6'
      case 'deal': return '#f59e0b'
      case 'invoice': return '#8b5cf6'
      case 'ticket': return '#ef4444'
      default: return '#6b7280'
    }
  }

  if (loading) {
    return <div className="loading">Loading entities...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Entities</h1>
        <p className="page-subtitle">
          View and manage resolved business entities from your data
        </p>
      </div>

      {/* Search and Filters */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
          <div className="form-group">
            <label className="form-label">Search Entities</label>
            <input
              type="text"
              className="form-input"
              placeholder="Search by name, email, or other fields..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Entity Type</label>
            <select
              className="form-input"
              value={entityType}
              onChange={(e) => setEntityType(e.target.value)}
            >
              <option value="">All Types</option>
              <option value="person">Person</option>
              <option value="company">Company</option>
              <option value="deal">Deal</option>
              <option value="invoice">Invoice</option>
              <option value="ticket">Ticket</option>
            </select>
          </div>
        </div>
      </div>

      {/* Entities List */}
      {entities.length > 0 ? (
        <div className="grid">
          {entities.map((entity) => {
            const canonical = JSON.parse(entity.canonical || '{}')
            const icon = getEntityIcon(entity.type)
            const color = getEntityColor(entity.type)
            
            return (
              <div key={entity.id} className="card">
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
                      {canonical.name || canonical.company || canonical.deal_id || `Entity ${entity.id}`}
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
                        color: '#3b82f6',
                        textTransform: 'capitalize'
                      }}>
                        {entity.type}
                      </span>
                      
                      <span style={{
                        background: 'rgba(139, 92, 246, 0.2)',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        color: '#8b5cf6'
                      }}>
                        {Math.round(entity.confidence * 100)}% confidence
                      </span>
                    </div>
                  </div>
                </div>

                {/* Entity Details */}
                <div style={{ marginBottom: '1rem' }}>
                  {Object.entries(canonical).slice(0, 5).map(([key, value]) => (
                    <div key={key} style={{ 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      padding: '0.25rem 0',
                      borderBottom: '1px solid rgba(255,255,255,0.1)'
                    }}>
                      <span style={{ 
                        color: 'rgba(255,255,255,0.7)', 
                        fontSize: '0.875rem',
                        textTransform: 'capitalize'
                      }}>
                        {key.replace(/_/g, ' ')}:
                      </span>
                      <span style={{ 
                        color: 'rgba(255,255,255,0.9)', 
                        fontSize: '0.875rem',
                        maxWidth: '200px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap'
                      }}>
                        {String(value)}
                      </span>
                    </div>
                  ))}
                </div>

                {/* External ID */}
                {entity.external_id && (
                  <div style={{ 
                    fontSize: '0.875rem', 
                    color: 'rgba(255,255,255,0.6)',
                    marginBottom: '1rem'
                  }}>
                    External ID: {entity.external_id}
                  </div>
                )}

                {/* Created Date */}
                <div style={{ 
                  fontSize: '0.875rem', 
                  color: 'rgba(255,255,255,0.6)',
                  textAlign: 'right'
                }}>
                  Created: {new Date(entity.created_at).toLocaleDateString()}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
            No Entities Found
          </h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '2rem' }}>
            {searchQuery || entityType 
              ? 'No entities match your search criteria. Try adjusting your filters.'
              : 'No entities have been resolved yet. Upload data and run entity resolution to get started.'
            }
          </p>
          {!searchQuery && !entityType && (
            <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.875rem' }}>
              Entities are automatically created when you ingest data and run entity resolution.
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default Entities
