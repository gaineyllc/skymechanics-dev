import React, { useState } from 'react'
import { styled } from 'baseui'
import { createMechanic, updateMechanicProfile, Mechanic } from '../services/api'

const ModalOverlay = styled('div', {
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
})

const ModalContent = styled('div', {
  backgroundColor: '#fff',
  borderRadius: '8px',
  width: '500px',
  maxHeight: '90vh',
  overflow: 'auto',
  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  display: 'flex',
  flexDirection: 'column',
})

const ModalHeader = styled('div', {
  padding: '16px 20px',
  borderBottom: '1px solid #e0e0e0',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
})

const ModalTitle = styled('h3', {
  margin: 0,
  fontSize: '18px',
  fontWeight: '600',
})

const ModalBody = styled('div', {
  padding: '20px',
  display: 'flex',
  flexDirection: 'column',
  gap: '16px',
})

const ModalFooter = styled('div', {
  padding: '16px 20px',
  borderTop: '1px solid #e0e0e0',
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '12px',
})

const FormField = styled('div', {
  display: 'flex',
  flexDirection: 'column',
  gap: '8px',
})

const Label = styled('label', {
  fontWeight: '600',
  fontSize: '14px',
  color: '#333',
})

const Input = styled('input', {
  width: '100%',
  padding: '8px 12px',
  border: '1px solid #ccc',
  borderRadius: '4px',
  fontSize: '14px',
  ':focus': {
    outline: 'none',
    border: '2px solid #007AFF',
  },
})

const TextArea = styled('textarea', {
  width: '100%',
  padding: '8px 12px',
  border: '1px solid #ccc',
  borderRadius: '4px',
  fontSize: '14px',
  minHeight: '60px',
  resize: 'vertical',
  ':focus': {
    outline: 'none',
    border: '2px solid #007AFF',
  },
})

const HelpText = styled('div', {
  fontSize: '12px',
  color: '#666',
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

interface CreateMechanicModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (mechanic: Mechanic) => void
}

export function CreateMechanicModal({ isOpen, onClose, onSuccess }: CreateMechanicModalProps) {
  const [step, setStep] = useState(1)
  const [basicData, setBasicData] = useState({
    name: '',
    email: '',
    phone: '',
  })
  const [profileData, setProfileData] = useState({
    licenseNumber: '',
    certifications: '',
    availability: '',
    currentLocation: '',
  })
  const [loading, setLoading] = useState(false)

  const handleCreate = async () => {
    setLoading(true)
    try {
      // Create the mechanic with basic info first
      const specialtiesArray = profileData.certifications
        .split(',')
        .map(s => s.trim())
        .filter(Boolean)

      const created = await createMechanic({
        ...basicData,
        specialties: specialtiesArray,
      })

      // If profile data was provided, update the mechanic profile
      if (
        profileData.licenseNumber ||
        profileData.certifications ||
        profileData.availability ||
        profileData.currentLocation
      ) {
        const profilePayload: Record<string, any> = {}
        if (profileData.licenseNumber) profilePayload.license_number = profileData.licenseNumber
        if (profileData.certifications) {
          profilePayload.certifications = specialtiesArray
        }
        if (profileData.availability) {
          try {
            profilePayload.availability = JSON.parse(profileData.availability)
          } catch {
            profilePayload.availability = { schedule: profileData.availability }
          }
        }
        if (profileData.currentLocation) {
          try {
            profilePayload.current_location = JSON.parse(profileData.currentLocation)
          } catch {
            profilePayload.current_location = { lat: 0, lng: 0 }
          }
        }

        await updateMechanicProfile(created.node_id, profilePayload)
      }

      onSuccess(created)
      onClose()
    } catch (err) {
      console.error('Failed to create mechanic:', err)
      alert('Failed to create mechanic. Please check the console for details.')
    } finally {
      setLoading(false)
    }
  }

  const updateBasicField = (field: keyof typeof basicData, value: string) => {
    setBasicData((prev) => ({ ...prev, [field]: value }))
  }

  const updateProfileField = (field: keyof typeof profileData, value: string) => {
    setProfileData((prev) => ({ ...prev, [field]: value }))
  }

  if (!isOpen) return null

  return (
    <ModalOverlay>
      <ModalContent>
        <ModalHeader>
          <ModalTitle>{step === 1 ? 'Create New Mechanic' : 'Mechanic Profile'}</ModalTitle>
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
        </ModalHeader>

        <ModalBody>
          {step === 1 ? (
            <>
              <FormField>
                <Label htmlFor="name">Name *</Label>
                <Input
                  id="name"
                  type="text"
                  value={basicData.name}
                  onChange={(e) => updateBasicField('name', e.target.value)}
                  placeholder="e.g., Alice Williams"
                  required
                />
              </FormField>

              <FormField>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={basicData.email}
                  onChange={(e) => updateBasicField('email', e.target.value)}
                  placeholder="alice@example.com"
                  required
                />
              </FormField>

              <FormField>
                <Label htmlFor="phone">Phone</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={basicData.phone}
                  onChange={(e) => updateBasicField('phone', e.target.value)}
                  placeholder="(555) 111-2222"
                />
              </FormField>
            </>
          ) : (
            <>
              <FormField>
                <Label htmlFor="licenseNumber">License Number</Label>
                <Input
                  id="licenseNumber"
                  type="text"
                  value={profileData.licenseNumber}
                  onChange={(e) => updateProfileField('licenseNumber', e.target.value)}
                  placeholder="e.g., FAA-2345678"
                />
              </FormField>

              <FormField>
                <Label htmlFor="certifications">Certifications / Specialties</Label>
                <Input
                  id="certifications"
                  type="text"
                  value={profileData.certifications}
                  onChange={(e) => updateProfileField('certifications', e.target.value)}
                  placeholder="e.g., IA, A&P, Powerplant"
                />
                <HelpText>Separate multiple certifications with commas</HelpText>
              </FormField>

              <FormField>
                <Label htmlFor="availability">Availability</Label>
                <TextArea
                  id="availability"
                  value={profileData.availability}
                  onChange={(e) => updateProfileField('availability', e.target.value)}
                  placeholder={`e.g.,\n{\n  "monday": "08:00-17:00",\n  "tuesday": "08:00-17:00",\n  "wednesday": "08:00-17:00",\n  "thursday": "08:00-17:00",\n  "friday": "08:00-17:00"\n}`}
                />
              </FormField>

              <FormField>
                <Label htmlFor="currentLocation">Current Location (GPS)</Label>
                <TextArea
                  id="currentLocation"
                  value={profileData.currentLocation}
                  onChange={(e) => updateProfileField('currentLocation', e.target.value)}
                  placeholder={`e.g.,\n{\n  "lat": 40.7128,\n  "lng": -74.0060\n}`}
                />
              </FormField>
            </>
          )}
        </ModalBody>

        <ModalFooter>
          {step === 2 && (
            <Button kind="secondary" onClick={() => setStep(1)}>
              Back
            </Button>
          )}
          <Button kind="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button
            kind="primary"
            onClick={step === 1 ? () => setStep(2) : handleCreate}
            disabled={loading || (step === 1 && (!basicData.name || !basicData.email))}
          >
            {loading ? 'Creating...' : step === 1 ? 'Next' : 'Create Mechanic'}
          </Button>
        </ModalFooter>
      </ModalContent>
    </ModalOverlay>
  )
}
