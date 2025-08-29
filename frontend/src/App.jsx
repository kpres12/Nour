import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Layout/Navbar'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Narratives from './pages/Narratives'
import Entities from './pages/Entities'
import Sources from './pages/Sources'
import Signals from './pages/Signals'
import Playbooks from './pages/Playbooks'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import './App.css'

function AppContent() {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Login />
  }

  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/narratives" element={<Narratives />} />
            <Route path="/entities" element={<Entities />} />
            <Route path="/sources" element={<Sources />} />
            <Route path="/signals" element={<Signals />} />
            <Route path="/playbooks" element={<Playbooks />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
