import React from 'react'
import { styled } from 'baseui'
import { Mechanic } from '../services/api'

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
  width: '600px',
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

const CloseButton = styled('button', {
  background: 'none',
  border: 'none',
  fontSize: '20px',
  cursor: 'pointer',
  color: '#666',
  padding: '4px 8px',
})

const ModalBody = styled('div', {
  padding: '20px',
})

const DetailSection = styled('div', {
  marginBottom: '24px',
})

const DetailSectionTitle = styled('h4', {
  margin: '0 0 12px 0',
  fontSize: '14px',
  fontWeight: '600',
  color: '#333',
  textTransform: 'uppercase',
  letterSpacing: '0.5px',
})

const DetailGrid = styled('div', {
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  gap: '16px',
})

const DetailItem = styled('div', {
  display: 'flex',
  flexDirection: 'column',
  gap: '4px',
})

const DetailLabel = styled('span', {
  fontSize: '12px',
  color: '#666',
  fontWeight: '500',
})

const DetailValue = styled('span', {
  fontSize: '14px',
  color: '#333',
  wordBreak: 'break-word',
})

const CertificationsList = styled('div', {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '8px',
  marginTop: '8px',
})

const CertificationBadge = styled('span', {
  backgroundColor: '#e3f2fd',
  color: '#1565c0',
  padding: '4px 12px',
  borderRadius: '16px',
  fontSize: '12px',
  fontWeight: '500',
})

const LocationCard = styled('div', {
  backgroundColor: '#f5f5f5',
  borderRadius: '8px',
  padding: '16px',
})

const LocationLabel = styled('span', {
  fontSize: '12px',
  color: '#666',
  fontWeight: '500',
})

const LocationValue = styled('div', {
  fontSize: '14px',
  color: '#333',
  fontFamily: 'monospace',
  marginTop: '4px',
})

const ModalFooter = styled('div', {
  padding: '16px 20px',
  borderTop: '1px solid #e0e0e0',
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '12px',
})

interface MechanicsDetailModalProps {
  isOpen: boolean
  onClose: () => void
  mechanic: Mechanic
}

export function MechanicsDetailModal({ isOpen, onClose, mechanic }: MechanicsDetailModalProps) {
  if (!isOpen) return null

  const { properties, profile } = mechanic

  return (
    <ModalOverlay>
      <ModalContent>
        <ModalHeader>
          <ModalTitle>Mechanic Details</ModalTitle>
          <CloseButton onClick={onClose} aria-label="Close">
            ×
          </CloseButton>
        </ModalHeader>

        <ModalBody>
          <DetailSection>
            <DetailSectionTitle>Basic Information</DetailSectionTitle>
            <DetailGrid>
              <DetailItem>
                <DetailLabel>Name</DetailLabel>
                <DetailValue>{properties.name}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Email</DetailLabel>
                <DetailValue>{properties.email}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Phone</DetailLabel>
                <DetailValue>{properties.phone || 'Not provided'}</DetailValue>
              </DetailItem>
            </DetailGrid>
          </DetailSection>

          <DetailSection>
            <DetailSectionTitle>Certifications</DetailSectionTitle>
            {properties.specialties.length > 0 ? (
              <CertificationsList>
                {properties.specialties.map((cert, index) => (
                  <CertificationBadge key={index}>{cert}</CertificationBadge>
                ))}
              </CertificationsList>
            ) : (
              <DetailValue style={{ color: '#999' }}>None listed</DetailValue>
            )}
          </DetailSection>

          {profile && (
            <DetailSection>
              <DetailSectionTitle>Profile Details</DetailSectionTitle>
              
              <DetailGrid>
                <DetailItem>
                  <DetailLabel>License Number</DetailLabel>
                  <DetailValue>{profile.license_number || 'Not provided'}</DetailValue>
                </DetailItem>
                <DetailItem>
                  <DetailLabel>Updated</DetailLabel>
                  <DetailValue>
                    {profile.updated_at
                      ? new Date(profile.updated_at).toLocaleDateString()
                      : 'N/A'}
                  </DetailValue>
                </DetailItem>
              </DetailGrid>

              {profile.availability && (
                <DetailItem style={{ marginTop: '12px' }}>
                  <DetailLabel>Availability</DetailLabel>
                  <DetailValue>
                    <pre style={{ margin: 0, fontFamily: 'inherit', fontSize: '12px' }}>
                      {JSON.stringify(profile.availability, null, 2)}
                    </pre>
                  </DetailValue>
                </DetailItem>
              )}

              {profile.current_location && (
                <DetailItem style={{ marginTop: '12px' }}>
                  <DetailLabel>Current Location</DetailLabel>
                  <LocationCard>
                    <LocationLabel>GPS Coordinates</LocationLabel>
                    <LocationValue>
                      {profile.current_location.lat.toFixed(6)}, {profile.current_location.lng.toFixed(6)}
                    </LocationValue>
                  </LocationCard>
                </DetailItem>
              )}
            </DetailSection>
          )}

          <DetailSection>
            <DetailSectionTitle>System Information</DetailSectionTitle>
            <DetailGrid>
              <DetailItem>
                <DetailLabel>Node ID</DetailLabel>
                <DetailValue>{mechanic.node_id}</DetailValue>
              </DetailItem>
              <DetailItem>
                <DetailLabel>Label</DetailLabel>
                <DetailValue>{mechanic.label}</DetailValue>
              </DetailItem>
            </DetailGrid>
          </DetailSection>
        </ModalBody>

        <ModalFooter>
          <Button kind="secondary" onClick={onClose}>
            Close
          </Button>
        </ModalFooter>
      </ModalContent>
    </ModalOverlay>
  )
}
