import React, { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

function Playbooks() {
  const [rules, setRules] = useState([])
  const [loading, setLoading] = useState(true)
  const [evaluating, setEvaluating] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newRule, setNewRule] = useState({
    name: '',
    definition: '',
    priority: 1,
    category: 'general'
  })

  useEffect(() => {
    loadRules()
  }, [])

  const loadRules = async () => {
    try {
      setLoading(true)
      const data = await apiClient.get('/playbooks')
      setRules(data)
    } catch (error) {
      console.error('Error loading rules:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRule = async (e) => {
    e.preventDefault()
    try {
      // Parse the YAML definition
      const ruleDefinition = {
        name: newRule.name,
        when: {
          all: [
            {
              signal: "late_invoice_risk",
              where: { score: { gte: 0.7 } }
            }
          ]
        },
        then: {
          narrative_template: `Rule ${newRule.name} has been triggered.`,
          actions: ["Review the situation", "Take appropriate action"]
        },
        severity: "medium"
      }

      await apiClient.post('/playbooks', {
        ...newRule,
        definition: JSON.stringify(ruleDefinition)
      })
      
      setShowCreateForm(false)
      setNewRule({ name: '', definition: '', priority: 1, category: 'general' })
      await loadRules()
    } catch (error) {
      console.error('Error creating rule:', error)
      alert('Error creating rule')
    }
  }

  const handleToggleRule = async (ruleId) => {
    try {
      await apiClient.put(`/playbooks/${ruleId}/toggle`)
      await loadRules()
    } catch (error) {
      console.error('Error toggling rule:', error)
      alert('Error toggling rule')
    }
  }

  const handleEvaluateRules = async () => {
    try {
      setEvaluating(true)
      const result = await apiClient.post('/playbooks/evaluate')
      console.log('Rules evaluation result:', result)
      alert(`Evaluated ${result.results.length} rules`)
    } catch (error) {
      console.error('Error evaluating rules:', error)
      alert('Error evaluating rules')
    } finally {
      setEvaluating(false)
    }
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'sales': return '#3b82f6'
      case 'finance': return '#10b981'
      case 'support': return '#f59e0b'
      case 'operations': return '#8b5cf6'
      case 'marketing': return '#ef4444'
      default: return '#6b7280'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 1: return '#ef4444'
      case 2: return '#f59e0b'
      case 3: return '#10b981'
      default: return '#6b7280'
    }
  }

  if (loading) {
    return <div className="loading">Loading playbooks...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Playbooks</h1>
        <p className="page-subtitle">
          Manage business rules and automation workflows
        </p>
      </div>

      {/* Actions */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>Business Rules</h3>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button 
              onClick={handleEvaluateRules}
              className="btn-primary"
              disabled={evaluating}
            >
              {evaluating ? 'Evaluating...' : 'Evaluate Rules'}
            </button>
            <button 
              onClick={() => setShowCreateForm(!showCreateForm)}
              className="btn-primary"
            >
              {showCreateForm ? 'Cancel' : 'Add Rule'}
            </button>
          </div>
        </div>

        {showCreateForm && (
          <form onSubmit={handleCreateRule} style={{ marginTop: '1rem' }}>
            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
              <div className="form-group">
                <label className="form-label">Rule Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={newRule.name}
                  onChange={(e) => setNewRule({ ...newRule, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  className="form-input"
                  value={newRule.category}
                  onChange={(e) => setNewRule({ ...newRule, category: e.target.value })}
                >
                  <option value="general">General</option>
                  <option value="sales">Sales</option>
                  <option value="finance">Finance</option>
                  <option value="support">Support</option>
                  <option value="operations">Operations</option>
                  <option value="marketing">Marketing</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Priority</label>
                <select
                  className="form-input"
                  value={newRule.priority}
                  onChange={(e) => setNewRule({ ...newRule, priority: parseInt(e.target.value) })}
                >
                  <option value={1}>High (1)</option>
                  <option value={2}>Medium (2)</option>
                  <option value={3}>Low (3)</option>
                </select>
              </div>
            </div>

            <button type="submit" className="btn-primary">
              Create Rule
            </button>
          </form>
        )}
      </div>

      {/* Rules List */}
      {rules.length > 0 ? (
        <div className="grid">
          {rules.map((rule) => {
            const categoryColor = getCategoryColor(rule.category)
            const priorityColor = getPriorityColor(rule.priority)
            
            return (
              <div key={rule.id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ color: '#3b82f6', marginBottom: '0.5rem' }}>{rule.name}</h3>
                    
                    <div style={{ 
                      display: 'flex', 
                      gap: '0.5rem', 
                      flexWrap: 'wrap', 
                      marginBottom: '0.5rem',
                      fontSize: '0.875rem'
                    }}>
                      <span style={{
                        background: `${categoryColor}20`,
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        color: categoryColor,
                        textTransform: 'capitalize'
                      }}>
                        {rule.category}
                      </span>
                      
                      <span style={{
                        background: `${priorityColor}20`,
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        color: priorityColor
                      }}>
                        Priority {rule.priority}
                      </span>
                      
                      <span style={{
                        background: rule.enabled ? 'rgba(34, 197, 94, 0.2)' : 'rgba(156, 163, 175, 0.2)',
                        color: rule.enabled ? '#22c55e' : '#9ca3af',
                        padding: '0.25rem 0.5rem',
                        borderRadius: '0.25rem',
                        textTransform: 'uppercase'
                      }}>
                        {rule.enabled ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Rule Definition Preview */}
                <div style={{ 
                  background: 'rgba(0,0,0,0.3)', 
                  padding: '1rem', 
                  borderRadius: '0.5rem',
                  marginBottom: '1rem',
                  fontSize: '0.875rem',
                  fontFamily: 'monospace',
                  overflow: 'auto'
                }}>
                  <div style={{ color: 'rgba(255,255,255,0.8)', marginBottom: '0.5rem' }}>
                    Rule Definition:
                  </div>
                  <pre style={{ 
                    color: 'rgba(255,255,255,0.7)',
                    fontSize: '0.75rem',
                    lineHeight: '1.4'
                  }}>
                    {JSON.stringify(JSON.parse(rule.definition || '{}'), null, 2)}
                  </pre>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'space-between', alignItems: 'center' }}>
                  <button 
                    onClick={() => handleToggleRule(rule.id)}
                    className="btn-primary"
                    style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                  >
                    {rule.enabled ? 'Disable' : 'Enable'}
                  </button>
                  
                  <span style={{ fontSize: '0.875rem', color: 'rgba(255,255,255,0.6)' }}>
                    Created: {new Date(rule.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
            No Rules Created Yet
          </h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '2rem' }}>
            Create your first business rule to start automating insights and actions.
          </p>
          <button onClick={() => setShowCreateForm(true)} className="btn-primary">
            Create Your First Rule
          </button>
        </div>
      )}

      {/* Sample Rules Info */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <h3 style={{ marginBottom: '1rem', color: '#3b82f6' }}>Sample Rule Structure</h3>
        <p style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '1rem' }}>
          Rules use a YAML-like structure to define conditions and actions:
        </p>
        <div style={{ 
          background: 'rgba(0,0,0,0.3)', 
          padding: '1rem', 
          borderRadius: '0.5rem',
          fontSize: '0.875rem',
          fontFamily: 'monospace'
        }}>
          <pre style={{ color: 'rgba(255,255,255,0.8)', lineHeight: '1.4' }}>
{`name: "Late Invoice Alert"
when:
  all:
    - signal: late_invoice_risk
      where: { score: { gte: 0.7 } }
then:
  narrative_template: "High risk of late payments detected"
  actions: ["Review payment terms", "Contact customers"]
severity: high`}
          </pre>
        </div>
      </div>
    </div>
  )
}

export default Playbooks
