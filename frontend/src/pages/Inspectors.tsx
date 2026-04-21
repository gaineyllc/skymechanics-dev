import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { styled } from '../utils/styled'
import { apiRequest } from '../context/AuthContext'

interface Inspector {
  id: number
  name: string
  email: string
  phone: string
  license_number: string
  certifications: string[]
  availability: Record<string, any>
  current_location: { lat: number; lng: number }
}

export function Inspectors() {
  const [inspectors, setInspectors] = useState<Inspector[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    const loadInspectors = async () => {
      try {
        const data: Inspector[] = await apiRequest('GET', '/inspectors')
        setInspectors(Array.isArray(data) ? data : [data])
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to load inspectors')
      } finally {
        setLoading(false)
      }
    }
    loadInspectors()
  }, [])

  const handleCreateInspector = async () => {
    setIsModalOpen(true)
  }

  const handleDeleteInspector = async (id: number) => {
    if (confirm('Are you sure you want to delete this inspector?')) {
      try {
        await apiRequest('DELETE', `/inspectors/${id}`)
        setInspectors((prev) => prev.filter((inspector) => inspector.id !== id))
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to delete inspector')
      }
    }
  }

  if (loading) {
    return (
      <div style={{ padding: '24px' }}>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading inspectors...</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '600' }}>Inspectors ({inspectors.length})</h1>
        <button
          onClick={handleCreateInspector}
          style={{
            padding: '12px 24px',
            backgroundColor: '#007AFF',
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: '600',
            cursor: 'pointer',
          }}
        >
          + New Inspector
        </button>
      </div>

      {error && (
        <div
          style={{
            backgroundColor: '#ffe5e5',
            color: '#d00',
            padding: '16px',
            borderRadius: '8px',
            marginBottom: '16px',
          }}
        >
          {error}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
        {inspectors.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', gridColumn: '1 / -1', color: '#666' }}>
            No inspectors yet. Create one to get started.
          </div>
        ) : (
          inspectors.map((inspector) => (
            <div
              key={inspector.id}
              style={{
                backgroundColor: '#fff',
                borderRadius: '12px',
                padding: '20px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>{inspector.name}</h3>
                  <p style={{ margin: '4px 0 0 0', color: '#666', fontSize: '14px' }}>{inspector.email}</p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Link
                    to={`/inspectors/${inspector.id}`}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: '#f0f0f0',
                      color: '#333',
                      textDecoration: 'none',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '500',
                    }}
                  >
                    View
                  </Link>
                  <button
                    onClick={() => handleDeleteInspector(inspector.id)}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: '#ff4d4d',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '500',
                      cursor: 'pointer',
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '12px' }}>
                <strong>Phone:</strong> {inspector.phone}
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '12px' }}>
                <strong>License:</strong> {inspector.license_number}
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '12px' }}>
                <strong>Certifications:</strong> {inspector.certifications.length} total
              </div>

              <div style={{ fontSize: '14px', color: '#333' }}>
                <strong>Location:</strong> {inspector.current_location.lat.toFixed(4)}, {inspector.current_location.lng.toFixed(4)}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Inspectors
