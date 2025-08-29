import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

function Navbar() {
  const { logout } = useAuth()
  const location = useLocation()

  const navItems = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/narratives', label: 'Narratives' },
    { path: '/entities', label: 'Entities' },
    { path: '/sources', label: 'Sources' },
    { path: '/signals', label: 'Signals' },
    { path: '/playbooks', label: 'Playbooks' }
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/dashboard" className="logo">
          Nour
        </Link>
        
        <ul className="nav-links">
          {navItems.map((item) => (
            <li key={item.path}>
              <Link 
                to={item.path}
                className={isActive(item.path) ? 'active' : ''}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
        
        <button onClick={logout} className="btn-primary">
          Logout
        </button>
      </div>
    </nav>
  )
}

export default Navbar
