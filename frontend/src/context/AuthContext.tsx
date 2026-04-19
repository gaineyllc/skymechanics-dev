import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'mechanic' | 'customer'
}

interface AuthContextType {
  user: User | null
  login: (email: string) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_BASE_URL = 'http://localhost:8080'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)

  useEffect(() => {
    const storedToken = localStorage.getItem('authToken')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const login = (email: string) => {
    // Simulated login - will be replaced with actual API call
    const mockUser: User = {
      id: '1',
      email,
      name: 'Test User',
      role: 'admin',
    }
    
    const mockToken = 'mock-jwt-token'
    
    setUser(mockUser)
    setToken(mockToken)
    
    localStorage.setItem('authToken', mockToken)
    localStorage.setItem('user', JSON.stringify(mockUser))
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
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
