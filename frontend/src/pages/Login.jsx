import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'

function Login() {
  const [email, setEmail] = useState('demo@nour.com')
  const [password, setPassword] = useState('demo123')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const result = await login(email, password)
      if (!result.success) {
        setError(result.error || 'Login failed')
      }
    } catch (err) {
      setError('An unexpected error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="page-header">
        <h1 className="page-title">Welcome to Nour</h1>
        <p className="page-subtitle">
          Narrative Intelligence Platform - Transform your data into actionable insights
        </p>
      </div>

      <div className="card" style={{ maxWidth: '400px', margin: '0 auto' }}>
        <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Demo Login</h2>
        
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn-primary" 
            style={{ width: '100%' }}
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div style={{ marginTop: '2rem', textAlign: 'center', color: 'rgba(255,255,255,0.7)' }}>
          <p>This is a demo application. Use any email/password to login.</p>
          <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
            The system will create a demo organization automatically.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login
