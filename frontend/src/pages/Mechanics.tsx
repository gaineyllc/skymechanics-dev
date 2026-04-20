import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { fetchMechanics, createMechanic, Mechanic, getMechanic } from '../services/api'
import { CreateMechanicModal } from '../components/CreateMechanicModal'
import { MechanicsDetailModal } from '../components/MechanicsDetailModal'

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

const Button = ({ kind = 'primary', onClick, children, disabled = false, size = 'default' }: any) => {
  const sizes = {
    compact: { padding: '6px 12px', fontSize: '12px' },
    default: { padding: '8px 16px', fontSize: '14px' },
    large: { padding: '12px 24px', fontSize: '16px' },
  }

  const baseStyles = {
    ...sizes[size as keyof typeof sizes],
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontWeight: '500',
    transition: 'all 0.2s',
  }

  const kinds = {
    primary: {
      backgroundColor: '#007AFF',
      color: '#ffffff',
      '&:hover': { backgroundColor: '#005ecb' },
    },
    secondary: {
      backgroundColor: '#f0f0f0',
      color: '#333333',
      '&:hover': { backgroundColor: '#e0e0e0' },
    },
    tertiary: {
      backgroundColor: 'transparent',
      color: '#666666',
      '&:hover': { backgroundColor: '#f0f0e0' },
    },
    negative: {
      backgroundColor: '#ff4d4d',
      color: '#ffffff',
      '&:hover': { backgroundColor: '#cc0000' },
    },
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...baseStyles,
        ...kinds[kind as keyof typeof kinds],
        ...(disabled ? { opacity: 0.5, cursor: 'not-allowed' } : {}),
      }}
    >
      {children}
    </button>
  )
}

const KIND = {
  primary: 'primary',
  secondary: 'secondary',
  tertiary: 'tertiary',
  negative: 'negative',
}

const SIZE = {
  compact: 'compact',
  default: 'default',
  large: 'large',
}

const Notification = ({ onClose, kind, title, subtitle, autoHide, autoHideDuration }: any) => {
  if (autoHide) {
    useEffect(() => {
      const timer = setTimeout(() => {
        onClose && onClose()
      }, autoHideDuration || 3000)
      return () => clearTimeout(timer)
    }, [])
  }

  const kinds = {
    negative: { backgroundColor: '#ffe5e5', color: '#d00' },
    warning: { backgroundColor: '#fff3e0', color: '#f57c00' },
    positive: { backgroundColor: '#e8f5e9', color: '#2e7d32' },
    info: { backgroundColor: '#e3f2fd', color: '#1565c0' },
  }

  return (
    <div
      style={{
        padding: '16px',
        borderRadius: '8px',
        marginBottom: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        ...kinds[kind as keyof typeof kinds],
      }}
    >
      <div>
        <div style={{ fontWeight: '600' }}>{title}</div>
        {subtitle && <div style={{ fontSize: '14px' }}>{subtitle}</div>}
      </div>
      <button
        onClick={onClose}
        style={{
          background: 'none',
          border: 'none',
          fontSize: '20px',
          cursor: 'pointer',
          color: 'inherit',
        }}
      >
        ×
      </button>
    </div>
  )
}

export function Mechanics() {
  const [mechanics, setMechanics] = useState<Mechanic[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [selectedMechanic, setSelectedMechanic] = useState<Mechanic | null>(null)
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false)

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
    setIsCreateModalOpen(true)
  }

  const handleViewMechanic = async (mechanic: Mechanic) => {
    try {
      const detailed = await getMechanic(mechanic.node_id)
      setSelectedMechanic(detailed)
      setIsDetailModalOpen(true)
    } catch (err) {
      setError(`Failed to load mechanic details: ${err}`)
    }
  }

  const handleCreateSuccess = (mechanic: Mechanic) => {
    setMechanics((prev) => [...prev, mechanic])
  }

  if (loading) {
    return (
      <MechanicsContainer>
        <MechanicsHeader>
          <MechanicsTitle>Mechanics</MechanicsTitle>
          <Button kind={KIND.primary} onClick={handleCreateMechanic}>
            Add Mechanic
          </Button>
        </MechanicsHeader>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading mechanics...</p>
        </div>
      </MechanicsContainer>
    )
  }

  return (
    <MechanicsContainer>
      <MechanicsHeader>
        <MechanicsTitle>Mechanics ({mechanics.length})</MechanicsTitle>
        <Button kind={KIND.primary} onClick={handleCreateMechanic}>
          Add Mechanic
        </Button>
      </MechanicsHeader>

      {error && (
        <Notification
          onClose={() => setError(null)}
          kind="negative"
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
            <div key={mechanic.node_id}>
              <MechanicCard>
                <MechanicHeader>
                  <MechanicName>{mechanic.properties.name}</MechanicName>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <Button kind="secondary" size="compact" onClick={() => handleViewMechanic(mechanic)}>
                      View Details
                    </Button>
                    <Button kind="secondary" size="compact" onClick={() => {}}>
                      Edit
                    </Button>
                  </div>
                </MechanicHeader>
                <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                  {mechanic.properties.email}
                </div>
                <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                  {mechanic.properties.phone}
                </div>
                <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#999999' }}>
                  <span>Certifications: {mechanic.properties.specialties.join(', ') || 'None'}</span>
                </div>
              </MechanicCard>
            </div>
          ))
        )}
      </div>

      <CreateMechanicModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={handleCreateSuccess}
      />

      {selectedMechanic && (
        <MechanicsDetailModal
          isOpen={isDetailModalOpen}
          onClose={() => setIsDetailModalOpen(false)}
          mechanic={selectedMechanic}
        />
      )}
    </MechanicsContainer>
  )
}
