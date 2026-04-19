import React, { useState } from 'react'
import { Modal, ModalHeader, ModalBody, ModalFooter, Button, KIND, SIZE, TextInput } from 'baseui'
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
    <Modal isOpen={isOpen} onClose={onClose} closeable>
      <ModalHeader>Create New Mechanic</ModalHeader>
      <ModalBody>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Name
            </label>
            <TextInput
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., Alice Williams"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Email
            </label>
            <TextInput
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              placeholder="alice@example.com"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Phone
            </label>
            <TextInput
              value={formData.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="(555) 111-2222"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Certifications / Specialties
            </label>
            <TextInput
              value={formData.specialties}
              onChange={(e) => handleChange('specialties', e.target.value)}
              placeholder="e.g., IA, A&P, Powerplant"
              size="compact"
            />
            <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
              Separate multiple certifications with commas
            </div>
          </div>
        </div>
      </ModalBody>
      <ModalFooter>
        <Button kind={KIND.tertiary} onClick={onClose}>
          Cancel
        </Button>
        <Button kind={KIND.primary} onClick={handleSubmit}>
          Create Mechanic
        </Button>
      </ModalFooter>
    </Modal>
  )
}
