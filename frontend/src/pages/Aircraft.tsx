import React, { useState, useEffect } from 'react'
import { styled } from '../utils/styled'
import { apiRequest } from '../context/AuthContext'

interface Aircraft {
  id: number
  name: string
  registration: string
  model: string
  manufacturer: string
  year: number
  engine_type: string
  total_hours: number
  last_inspection: string
  next_inspection_due: string
  status: 'active' | 'maintenance' | ' grounded'
  owner_id: number
  location: { lat: number; lng: number }
  specs: Record<string, any>
}

export function Aircraft() {
  const [aircrafts, setAircrafts] = useState<Aircraft[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    const loadAircrafts = async () => {
      try {
        const data: Aircraft[] = await apiRequest('GET', '/aircraft')
        setAircrafts(Array.isArray(data) ? data : [data])
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to load aircraft')
      } finally {
        setLoading(false)
      }
    }
    loadAircrafts()
  }, [])

  const handleCreateAircraft = async () => {
    setIsModalOpen(true)
  }

  const handleDeleteAircraft = async (id: number) => {
    if (confirm('Are you sure you want to delete this aircraft?')) {
      try {
        await apiRequest('DELETE', `/aircraft/${id}`)
        setAircrafts((prev) => prev.filter((aircraft) => aircraft.id !== id))
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to delete aircraft')
      }
    }
  }

  if (loading) {
    return (
      <div style={{ padding: '24px' }}>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading aircraft...</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '24px', fontWeight: '600' }}>Aircraft ({aircrafts.length})</h1>
        <button
          onClick={handleCreateAircraft}
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
          + New Aircraft
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
        {aircrafts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', gridColumn: '1 / -1', color: '#666' }}>
            No aircraft yet. Create one to get started.
          </div>
        ) : (
          aircrafts.map((aircraft) => (
            <div
              key={aircraft.id}
              style={{
                backgroundColor: '#fff',
                borderRadius: '12px',
                padding: '20px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>{aircraft.name}</h3>
                  <p style={{ margin: '4px 0 0 0', color: '#666', fontSize: '14px' }}>{aircraft.registration}</p>
                </div>
                <div
                  style={{
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    fontWeight: '600',
                    backgroundColor: aircraft.status === 'active' ? '#E8F5E9' : '#FFF3E0',
                    color: aircraft.status === 'active' ? '#2E7D32' : '#F57C00',
                  }}
                >
                  {aircraft.status.charAt(0).toUpperCase() + aircraft.status.slice(1)}
                </div>
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '8px' }}>
                <strong>Model:</strong> {aircraft.model} ({aircraft.manufacturer})
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '8px' }}>
                <strong>Year:</strong> {aircraft.year} | <strong>Engine:</strong> {aircraft.engine_type}
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '8px' }}>
                <strong>Hours:</strong> {aircraft.total_hours.toLocaleString()} hrs
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '8px' }}>
                <strong>Last Inspection:</strong> {aircraft.last_inspection}
              </div>

              <div style={{ fontSize: '14px', color: '#333', marginBottom: '16px' }}>
                <strong>Next Inspection Due:</strong> {aircraft.next_inspection_due}
              </div>

              <div style={{ fontSize: '14px', color: '#666', marginBottom: '16px' }}>
                <strong>Location:</strong> {aircraft.location.lat.toFixed(4)}, {aircraft.location.lng.toFixed(4)}
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={() => handleDeleteAircraft(aircraft.id)}
                  style={{
                    flex: 1,
                    padding: '10px',
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
                <button
                  style={{
                    flex: 1,
                    padding: '10px',
                    backgroundColor: '#f0f0f0',
                    color: '#333',
                    border: 'none',
                    borderRadius: '6px',
                    fontSize: '12px',
                    fontWeight: '500',
                    cursor: 'pointer',
                  }}
                >
                  Edit
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Aircraft
