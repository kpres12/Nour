import React, { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

function Narratives() {
  const [narratives, setNarratives] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedNarrative, setSelectedNarrative] = useState(null)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    loadNarratives()
  }, [])

  const loadNarratives = async () => {
    try {
      setLoading(true)
      const data = await apiClient.get('/narratives')
      setNarratives(data)
    } catch (error) {
      console.error('Error loading narratives:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAutoGenerate = async () => {
    try {
      setLoading(true)
      const result = await apiClient.post('/narratives/auto-generate')
      console.log('Auto-generated narratives:', result)
      await loadNarratives() // Reload to show new narratives
    } catch (error) {
      console.error('Error auto-generating narratives:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (narrativeId, format = 'markdown') => {
    try {
      const result = await apiClient.post(`/narratives/export/${narrativeId}?format=${format}`)
      
      if (format === 'markdown') {
        // Download as markdown file
        const blob = new Blob([result.content], { type: 'text/markdown' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `narrative-${narrativeId}.md`
        a.click()
        URL.revokeObjectURL(url)
      } else if (format === 'json') {
        // Download as JSON file
        const blob = new Blob([JSON.stringify(result.content, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `narrative-${narrativeId}.json`
        a.click()
        URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Error exporting narrative:', error)
    }
  }

  const openNarrativeDetail = (narrative) => {
    setSelectedNarrative(narrative)
    setShowModal(true)
  }

  if (loading) {
    return <div className="loading">Loading narratives...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Narratives</h1>
        <p className="page-subtitle">
          AI-generated insights and actionable recommendations
        </p>
      </div>

      {/* Actions */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <button 
            onClick={handleAutoGenerate} 
            className="btn-primary"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Auto-Generate Narratives'}
          </button>
        </div>
      </div>

      {/* Narratives List */}
      {narratives.length > 0 ? (
        <div className="grid">
          {narratives.map((narrative) => (
            <div key={narrative.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <h3 style={{ color: '#3b82f6', flex: 1 }}>{narrative.title}</h3>
                <span style={{
                  background: narrative.status === 'active' ? 'rgba(34, 197, 94, 0.2)' : 'rgba(156, 163, 175, 0.2)',
                  color: narrative.status === 'active' ? '#22c55e' : '#9ca3af',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '0.25rem',
                  fontSize: '0.75rem',
                  textTransform: 'uppercase'
                }}>
                  {narrative.status}
                </span>
              </div>
              
              <p style={{ color: 'rgba(255,255,255,0.8)', marginBottom: '1rem', lineHeight: '1.6' }}>
                {narrative.summary}
              </p>
              
              {/* Actions */}
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1rem' }}>
                {JSON.parse(narrative.actions || '[]').slice(0, 3).map((action, index) => (
                  <span 
                    key={index}
                    style={{
                      background: 'rgba(59, 130, 246, 0.2)',
                      padding: '0.25rem 0.5rem',
                      borderRadius: '0.25rem',
                      fontSize: '0.875rem',
                      color: '#3b82f6'
                    }}
                  >
                    {action}
                  </span>
                ))}
              </div>
              
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                fontSize: '0.875rem',
                color: 'rgba(255,255,255,0.6)'
              }}>
                <span>Generated: {new Date(narrative.generated_at).toLocaleDateString()}</span>
                <span>By: {narrative.author}</span>
              </div>
              
              <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
                <button 
                  onClick={() => openNarrativeDetail(narrative)}
                  className="btn-primary"
                  style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                >
                  View Details
                </button>
                <button 
                  onClick={() => handleExport(narrative.id, 'markdown')}
                  className="btn-primary"
                  style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                >
                  Export MD
                </button>
                <button 
                  onClick={() => handleExport(narrative.id, 'json')}
                  className="btn-primary"
                  style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                >
                  Export JSON
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
            No Narratives Yet
          </h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '2rem' }}>
            Generate your first narrative by uploading data and computing signals.
          </p>
          <button onClick={handleAutoGenerate} className="btn-primary">
            Generate Narratives
          </button>
        </div>
      )}

      {/* Narrative Detail Modal */}
      {showModal && selectedNarrative && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.8)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          padding: '1rem'
        }}>
          <div className="card" style={{ maxWidth: '800px', maxHeight: '90vh', overflow: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2>{selectedNarrative.title}</h2>
              <button 
                onClick={() => setShowModal(false)}
                style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: 'rgba(255,255,255,0.7)' }}
              >
                ×
              </button>
            </div>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#3b82f6' }}>Summary</h4>
              <p style={{ lineHeight: '1.6' }}>{selectedNarrative.summary}</p>
            </div>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#3b82f6' }}>Actions</h4>
              <ul style={{ paddingLeft: '1.5rem' }}>
                {JSON.parse(selectedNarrative.actions || '[]').map((action, index) => (
                  <li key={index} style={{ marginBottom: '0.5rem' }}>{action}</li>
                ))}
              </ul>
            </div>
            
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: '#3b82f6' }}>Evidence</h4>
              <pre style={{ 
                background: 'rgba(0,0,0,0.3)', 
                padding: '1rem', 
                borderRadius: '0.5rem',
                overflow: 'auto',
                fontSize: '0.875rem'
              }}>
                {JSON.stringify(JSON.parse(selectedNarrative.evidence || '{}'), null, 2)}
              </pre>
            </div>
            
            <div style={{ 
              display: 'flex', 
              gap: '0.5rem', 
              justifyContent: 'flex-end',
              borderTop: '1px solid rgba(255,255,255,0.1)',
              paddingTop: '1rem'
            }}>
              <button 
                onClick={() => handleExport(selectedNarrative.id, 'markdown')}
                className="btn-primary"
              >
                Export Markdown
              </button>
              <button 
                onClick={() => handleExport(selectedNarrative.id, 'json')}
                className="btn-primary"
              >
                Export JSON
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Narratives
