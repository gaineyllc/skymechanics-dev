import React, { useState } from 'react'
import { createMechanic, Mechanic } from '../services/api'

interface CreateMechanicModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (mechanic: Mechanic) => void
}

export function CreateMechanicModal({ isOpen, onClose, onSuccess }: CreateMechanicModalProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    specialties: '',
  })

  const handleSubmit = async () => {
    try {
      const specialtiesArray = formData.specialties.split(',').map(s => s.trim()).filter(Boolean)
      const created = await createMechanic({
        ...formData,
        specialties: specialtiesArray,
      })
      onSuccess(created)
      onClose()
    } catch (err) {
      console.error('Failed to create mechanic:', err)
    }
  }

  const handleChange = (field: keyof Mechanic['properties'], value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      visibility: isOpen ? 'visible' : 'hidden',
      opacity: isOpen ? 1 : 0,
      transition: 'opacity 0.2s ease',
    }}>
      <div style={{
        backgroundColor: '#fff',
        borderRadius: '8px',
        width: '400px',
        maxHeight: '90vh',
        overflow: 'auto',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        display: 'flex',
        flexDirection: 'column',
      }}>
        <div style={{
          padding: '16px 20px',
          borderBottom: '1px solid #e0e0e0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '600' }}>
            Create New Mechanic
          </h3>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '20px',
              cursor: 'pointer',
              color: '#666',
              padding: '4px 8px',
            }}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Name
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., Alice Williams"
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '14px',
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Email
            </label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              placeholder="alice@example.com"
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '14px',
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Phone
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="(555) 111-2222"
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '14px',
              }}
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Certifications / Specialties
            </label>
            <input
              type="text"
              value={formData.specialties}
              onChange={(e) => handleChange('specialties', e.target.value)}
              placeholder="e.g., IA, A&P, Powerplant"
              style={{
                width: '100%',
                padding: '8px 12px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '14px',
              }}
            />
            <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
              Separate multiple certifications with commas
            </div>
          </div>
        </div>

        <div style={{
          padding: '16px 20px',
          borderTop: '1px solid #e0e0e0',
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '12px',
        }}>
          <button
            onClick={onClose}
            style={{
              padding: '8px 16px',
              backgroundColor: '#f0f0f0',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '14px',
              cursor: 'pointer',
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            style={{
              padding: '8px 16px',
              backgroundColor: '#0066cc',
              border: 'none',
              borderRadius: '4px',
              fontSize: '14px',
              cursor: 'pointer',
              color: '#fff',
            }}
          >
            Create Mechanic
          </button>
        </div>
      </div>
    </div>
  )
}
