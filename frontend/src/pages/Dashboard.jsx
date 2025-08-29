import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../api/client'

function Dashboard() {
  const [stats, setStats] = useState({
    narratives: 0,
    entities: 0,
    signals: 0,
    rules: 0
  })
  const [recentNarratives, setRecentNarratives] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      
      // Load recent narratives
      const narratives = await apiClient.get('/narratives?limit=5')
      setRecentNarratives(narratives)
      
      // Load basic stats
      const entities = await apiClient.get('/entities?limit=1')
      const signals = await apiClient.get('/signals?limit=1')
      const rules = await apiClient.get('/playbooks?limit=1')
      
      setStats({
        narratives: narratives.length,
        entities: entities.length,
        signals: signals.length,
        rules: rules.length
      })
      
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Overview of your narrative intelligence platform
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid" style={{ marginBottom: '3rem' }}>
        <div className="card">
          <h3 style={{ marginBottom: '1rem', color: '#3b82f6' }}>Narratives</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.narratives}</div>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '0.5rem' }}>
            Generated insights
          </p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem', color: '#10b981' }}>Entities</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.entities}</div>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '0.5rem' }}>
            Resolved entities
          </p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem', color: '#f59e0b' }}>Signals</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.signals}</div>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '0.5rem' }}>
            Active signals
          </p>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1rem', color: '#8b5cf6' }}>Rules</h3>
          <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.rules}</div>
          <p style={{ color: 'rgba(255,255,255,0.7)', marginTop: '0.5rem' }}>
            Active rules
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3 style={{ marginBottom: '1.5rem' }}>Quick Actions</h3>
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
          <Link to="/sources" className="btn-primary" style={{ textAlign: 'center', display: 'block' }}>
            Upload Data
          </Link>
          <Link to="/signals" className="btn-primary" style={{ textAlign: 'center', display: 'block' }}>
            Compute Signals
          </Link>
          <Link to="/playbooks" className="btn-primary" style={{ textAlign: 'center', display: 'block' }}>
            Evaluate Rules
          </Link>
          <Link to="/narratives" className="btn-primary" style={{ textAlign: 'center', display: 'block' }}>
            Generate Narratives
          </Link>
        </div>
      </div>

      {/* Recent Narratives */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Recent Narratives</h3>
          <Link to="/narratives" className="btn-primary">
            View All
          </Link>
        </div>

        {recentNarratives.length > 0 ? (
          <div className="grid" style={{ gridTemplateColumns: '1fr' }}>
            {recentNarratives.map((narrative) => (
              <div key={narrative.id} className="card" style={{ margin: '0.5rem 0' }}>
                <h4 style={{ marginBottom: '0.5rem', color: '#3b82f6' }}>
                  {narrative.title}
                </h4>
                <p style={{ color: 'rgba(255,255,255,0.8)', marginBottom: '1rem' }}>
                  {narrative.summary}
                </p>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {JSON.parse(narrative.actions || '[]').slice(0, 2).map((action, index) => (
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
              </div>
            ))}
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'rgba(255,255,255,0.7)' }}>
            <p>No narratives generated yet.</p>
            <p style={{ marginTop: '0.5rem' }}>
              <Link to="/narratives" className="btn-primary" style={{ display: 'inline-block' }}>
                Generate Your First Narrative
              </Link>
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
