import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'mechanic' | 'customer' | 'inspector'
  aircraft_ids?: string[]
}

interface AuthContextType {
  user: User | null
  login: (email: string, password?: string) => Promise<boolean>
  logout: () => void
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_BASE_URL = 'http://localhost:8200'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password?: string): Promise<boolean> => {
    try {
      setError(null)
      setLoading(true)
      
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        email,
        password: password || 'default',
      })
      
      const { token, user } = response.data
      
      setToken(token)
      setUser(user)
      localStorage.setItem('authToken', token)
      localStorage.setItem('user', JSON.stringify(user))
      
      setLoading(false)
      return true
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed')
      setLoading(false)
      return false
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user, loading, error }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export async function apiRequest(method: string, endpoint: string, data?: any) {
  const token = localStorage.getItem('authToken')
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }

  const response = await axios({
    method,
    url: `${API_BASE_URL}${endpoint}`,
    data,
    headers,
  })

  return response.data
}
