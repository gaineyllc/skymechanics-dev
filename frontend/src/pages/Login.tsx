import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const LoginContainer = {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
  backgroundColor: '#f5f5f5',
}

const LoginForm = {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '40px',
  boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  width: '100%',
  maxWidth: '400px',
}

const Title = {
  fontSize: '24px',
  fontWeight: '600',
  marginBottom: '32px',
  textAlign: 'center',
  color: '#1a1a1a',
}

const SectionTitle = {
  fontSize: '18px',
  fontWeight: '600',
  marginBottom: '24px',
  color: '#333',
}

const FormLabel = {
  display: 'block',
  marginBottom: '8px',
  fontWeight: '600',
  color: '#555',
  fontSize: '14px',
}

const InputField = {
  width: '100%',
  padding: '12px 16px',
  borderRadius: '8px',
  border: '1px solid #e0e0e0',
  fontSize: '14px',
  marginBottom: '16px',
  boxSizing: 'border-box',
}

const PrimaryButton = {
  width: '100%',
  padding: '14px',
  backgroundColor: '#0066cc',
  border: 'none',
  borderRadius: '8px',
  fontSize: '16px',
  fontWeight: '600',
  cursor: 'pointer',
  color: '#fff',
  marginBottom: '16px',
}

const ErrorMessage = {
  backgroundColor: '#fde8e8',
  color: '#c53030',
  padding: '12px',
  borderRadius: '8px',
  marginBottom: '16px',
  fontSize: '14px',
}

const Link = {
  color: '#0066cc',
  textDecoration: 'none',
}

export function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const success = await login(email, password)

    if (success) {
      navigate('/dashboard')
    } else {
      setError('Invalid email or password')
    }

    setLoading(false)
  }

  return (
    <div style={LoginContainer}>
      <div style={LoginForm}>
        <h1 style={Title}>SkyMechanics</h1>
        <h2 style={SectionTitle}>Login</h2>

        {error && <div style={ErrorMessage}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <label style={FormLabel}>Email Address</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={InputField}
            placeholder="Enter your email"
            required
          />

          <label style={FormLabel}>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={InputField}
            placeholder="Enter your password"
            required
          />

          <button type="submit" style={PrimaryButton} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p style={{ textAlign: 'center', fontSize: '14px', color: '#666' }}>
          Don't have an account?
        </p>
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center' }}>
          <a href="/register/owner" style={{ ...Link, textDecoration: 'underline' }}>
            Create Owner Account
          </a>
          <span style={{ color: '#999' }}>or</span>
          <a href="/register/mechanic" style={{ ...Link, textDecoration: 'underline' }}>
            Create Mechanic Account
          </a>
        </div>
      </div>
    </div>
  )
}

export default Login
