import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { Card, Button, KIND, SIZE, Spinner, Notification, TYPE } from 'baseui'
import { fetchMechanics, createMechanic, Mechanic } from '../services/api'
import { CreateMechanicModal } from '../components/CreateMechanicModal'

const MechanicsContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const MechanicsHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '24px',
})

const MechanicsTitle = styled('h2', {
  margin: 0,
  fontSize: '20px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const MechanicCard = styled('div', {
  backgroundColor: '#f8f9fa',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
})

const MechanicHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '12px',
})

const MechanicName = styled('div', {
  fontWeight: '600',
  fontSize: '16px',
})

const MechanicActions = styled('div', {
  display: 'flex',
  gap: '8px',
})

export function Mechanics() {
  const [mechanics, setMechanics] = useState<Mechanic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    const loadMechanics = async () => {
      try {
        const data = await fetchMechanics()
        setMechanics(Array.isArray(data) ? data : [data])
      } catch (err) {
        setError('Failed to load mechanics')
      } finally {
        setLoading(false)
      }
    }
    loadMechanics()
  }, [])

  const handleCreateMechanic = async () => {
    setIsModalOpen(true)
  }

  if (loading) {
    return (
      <MechanicsContainer>
        <MechanicsHeader>
          <MechanicsTitle>Mechanics</MechanicsTitle>
          <Button kind={KIND.primary} size={SIZE.compact} onClick={handleCreateMechanic}>
            Add Mechanic
          </Button>
        </MechanicsHeader>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spinner size={48} />
          <p>Loading mechanics...</p>
        </div>
      </MechanicsContainer>
    )
  }

  return (
    <MechanicsContainer>
      <MechanicsHeader>
        <MechanicsTitle>Mechanics ({mechanics.length})</MechanicsTitle>
        <Button kind={KIND.primary} size={SIZE.compact} onClick={handleCreateMechanic}>
          Add Mechanic
        </Button>
      </MechanicsHeader>

      {error && (
        <Notification
          onClose={() => setError(null)}
          kind={TYPE.negative}
          title="Error"
          subtitle={error}
          autoHide
          autoHideDuration={3000}
        />
      )}

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {mechanics.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>No mechanics yet. Add one to get started.</p>
        ) : (
          mechanics.map((mechanic) => (
            <MechanicCard key={mechanic.node_id}>
              <MechanicHeader>
                <MechanicName>{mechanic.properties.name}</MechanicName>
                <MechanicActions>
                  <Button kind="secondary" size={SIZE.compact}>View</Button>
                  <Button kind="secondary" size={SIZE.compact}>Edit</Button>
                </MechanicActions>
              </MechanicHeader>
              <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                {mechanic.properties.email}
              </div>
              <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                {mechanic.properties.phone}
              </div>
              <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#999999' }}>
                <span>Certifications: {mechanic.properties.specialties.join(', ')}</span>
              </div>
            </MechanicCard>
          ))
        )}
      </div>

      <CreateMechanicModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={(mechanic) => setMechanics((prev) => [...prev, mechanic])}
      />
    </MechanicsContainer>
  )
}
