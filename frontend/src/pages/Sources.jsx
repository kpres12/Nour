import React, { useState, useEffect } from 'react'
import { apiClient } from '../api/client'

function Sources() {
  const [datasets, setDatasets] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newDataset, setNewDataset] = useState({
    name: '',
    source_type: 'csv',
    acl_tag: 'default',
    description: ''
  })

  useEffect(() => {
    loadDatasets()
  }, [])

  const loadDatasets = async () => {
    try {
      setLoading(true)
      const data = await apiClient.get('/sources')
      setDatasets(data)
    } catch (error) {
      console.error('Error loading datasets:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateDataset = async (e) => {
    e.preventDefault()
    try {
      await apiClient.post('/sources', newDataset)
      setShowCreateForm(false)
      setNewDataset({ name: '', source_type: 'csv', acl_tag: 'default', description: '' })
      await loadDatasets()
    } catch (error) {
      console.error('Error creating dataset:', error)
    }
  }

  const handleFileUpload = async (datasetId, file) => {
    try {
      await apiClient.upload(`/sources/upload/${datasetId}`, file)
      alert('File uploaded successfully!')
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Error uploading file')
    }
  }

  const handleIngest = async (datasetId) => {
    try {
      await apiClient.post(`/ingest/run/${datasetId}`)
      alert('Ingestion started!')
    } catch (error) {
      console.error('Error starting ingestion:', error)
      alert('Error starting ingestion')
    }
  }

  if (loading) {
    return <div className="loading">Loading sources...</div>
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Data Sources</h1>
        <p className="page-subtitle">
          Manage your data sources and upload files for processing
        </p>
      </div>

      {/* Create Dataset */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>Data Sources</h3>
          <button 
            onClick={() => setShowCreateForm(!showCreateForm)}
            className="btn-primary"
          >
            {showCreateForm ? 'Cancel' : 'Add Source'}
          </button>
        </div>

        {showCreateForm && (
          <form onSubmit={handleCreateDataset} style={{ marginTop: '1rem' }}>
            <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
              <div className="form-group">
                <label className="form-label">Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={newDataset.name}
                  onChange={(e) => setNewDataset({ ...newDataset, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Source Type</label>
                <select
                  className="form-input"
                  value={newDataset.source_type}
                  onChange={(e) => setNewDataset({ ...newDataset, source_type: e.target.value })}
                >
                  <option value="csv">CSV</option>
                  <option value="api">API</option>
                  <option value="webhook">Webhook</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">ACL Tag</label>
                <input
                  type="text"
                  className="form-input"
                  value={newDataset.acl_tag}
                  onChange={(e) => setNewDataset({ ...newDataset, acl_tag: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description</label>
                <input
                  type="text"
                  className="form-input"
                  value={newDataset.description}
                  onChange={(e) => setNewDataset({ ...newDataset, description: e.target.value })}
                />
              </div>
            </div>

            <button type="submit" className="btn-primary">
              Create Dataset
            </button>
          </form>
        )}
      </div>

      {/* Datasets List */}
      {datasets.length > 0 ? (
        <div className="grid">
          {datasets.map((dataset) => (
            <div key={dataset.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ color: '#3b82f6', marginBottom: '0.5rem' }}>{dataset.name}</h3>
                  <p style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.875rem' }}>
                    {dataset.description || 'No description'}
                  </p>
                </div>
                <span style={{
                  background: dataset.is_active ? 'rgba(34, 197, 94, 0.2)' : 'rgba(156, 163, 175, 0.2)',
                  color: dataset.is_active ? '#22c55e' : '#9ca3af',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '0.25rem',
                  fontSize: '0.75rem',
                  textTransform: 'uppercase'
                }}>
                  {dataset.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>

              <div style={{ 
                display: 'flex', 
                gap: '0.5rem', 
                flexWrap: 'wrap', 
                marginBottom: '1rem',
                fontSize: '0.875rem'
              }}>
                <span style={{
                  background: 'rgba(59, 130, 246, 0.2)',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '0.25rem',
                  color: '#3b82f6'
                }}>
                  {dataset.source_type.toUpperCase()}
                </span>
                <span style={{
                  background: 'rgba(139, 92, 246, 0.2)',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '0.25rem',
                  color: '#8b5cf6'
                }}>
                  {dataset.acl_tag}
                </span>
              </div>

              {/* File Upload */}
              <div style={{ marginBottom: '1rem' }}>
                <label className="form-label">Upload File</label>
                <input
                  type="file"
                  accept=".csv,.json,.xlsx"
                  onChange={(e) => {
                    if (e.target.files[0]) {
                      handleFileUpload(dataset.id, e.target.files[0])
                    }
                  }}
                  style={{ 
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '0.5rem',
                    padding: '0.5rem',
                    color: 'white',
                    width: '100%'
                  }}
                />
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  onClick={() => handleIngest(dataset.id)}
                  className="btn-primary"
                  style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                >
                  Start Ingestion
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h3 style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
            No Data Sources Yet
          </h3>
          <p style={{ color: 'rgba(255,255,255,0.6)', marginBottom: '2rem' }}>
            Create your first data source to start uploading and processing data.
          </p>
          <button onClick={() => setShowCreateForm(true)} className="btn-primary">
            Create Data Source
          </button>
        </div>
      )}
    </div>
  )
}

export default Sources
