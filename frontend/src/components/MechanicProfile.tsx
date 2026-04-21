import React from 'react'
import { styled } from '../utils/styled'

const MechanicProfileCard = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const MechanicProfileHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'flex-start',
  marginBottom: '24px',
  paddingBottom: '24px',
  borderBottom: '1px solid #e0e0e0',
})

const MechanicProfileInfo = styled('div', {
  flex: 1,
})

const MechanicProfileName = styled('h2', {
  margin: '0 0 8px 0',
  fontSize: '24px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const MechanicProfileEmail = styled('div', {
  fontSize: '14px',
  color: '#666666',
  marginBottom: '4px',
})

const MechanicProfilePhone = styled('div', {
  fontSize: '14px',
  color: '#666666',
})

const MechanicProfileActions = styled('div', {
  display: 'flex',
  gap: '8px',
})

const MechanicProfileSection = styled('div', {
  marginBottom: '24px',
})

const MechanicSectionTitle = styled('h3', {
  margin: '0 0 16px 0',
  fontSize: '16px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const MechanicProfileGrid = styled('div', {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  gap: '16px',
})

const MechanicProfileField = styled('div', {
  display: 'flex',
  flexDirection: 'column',
})

const MechanicProfileLabel = styled('span', {
  fontSize: '12px',
  color: '#999999',
  marginBottom: '4px',
})

const MechanicProfileValue = styled('div', {
  fontSize: '14px',
  fontWeight: '500',
  color: '#1a1a1a',
})

// Export component
export function MechanicProfileCard({ 
  mechanic,
  onEdit,
  onAssign,
}: {
  mechanic: {
    node_id: number
    properties: {
      name: string
      email: string
      phone?: string
      specialties?: string[]
    }
    profile?: {
      license_number?: string
      certifications?: string[]
      availability?: Record<string, any>
      current_location?: { lat: number; lng: number }
      created_at?: string
      updated_at?: string
    }
    reputation?: {
      total_score: number
      component_scores: {
        certification_status: number
        experience_depth: number
        performance: number
        recent_activity: number
        compliance: number
      }
      review_count: number
      avg_rating?: number
    }
  }
  onEdit?: () => void
  onAssign?: () => void
}) {
  const { properties, profile, reputation } = mechanic

  return (
    <MechanicProfileCard>
      <MechanicProfileHeader>
        <MechanicProfileInfo>
          <MechanicProfileName>{properties.name}</MechanicProfileName>
          {properties.email && <MechanicProfileEmail>{properties.email}</MechanicProfileEmail>}
          {properties.phone && <MechanicProfilePhone>{properties.phone}</MechanicProfilePhone>}
        </MechanicProfileInfo>
        
        <MechanicProfileActions>
          {onEdit && (
            <button 
              onClick={onEdit}
              style={{
                padding: '8px 16px',
                backgroundColor: '#f0f0f0',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              Edit
            </button>
          )}
          {onAssign && (
            <button 
              onClick={onAssign}
              style={{
                padding: '8px 16px',
                backgroundColor: '#007AFF',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '14px',
                color: '#ffffff',
              }}
            >
              Assign Job
            </button>
          )}
        </MechanicProfileActions>
      </MechanicProfileHeader>

      {reputation && (
        <MechanicProfileSection>
          <MechanicSectionTitle>Reputation</MechanicSectionTitle>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
            <div style={{
              padding: '16px',
              backgroundColor: reputation.total_score >= 70 ? '#e8f5e9' : '#fff3e0',
              borderRadius: '12px',
              textAlign: 'center',
              minWidth: '100px',
            }}>
              <div style={{
                fontSize: '32px',
                fontWeight: 'bold',
                color: reputation.total_score >= 70 ? '#2e7d32' : '#f57c00',
              }}>
                {reputation.total_score}
              </div>
              <div style={{ fontSize: '12px', color: '#666666' }}>
                Reputation Score
              </div>
            </div>
            
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: '14px', color: '#1a1a1a', fontWeight: '600', marginBottom: '4px' }}>
                {reputation.avg_rating ? `${reputation.avg_rating.toFixed(1)}/5.0` : 'No ratings yet'}
              </div>
              <div style={{ fontSize: '12px', color: '#666666' }}>
                {reputation.review_count} reviews
              </div>
            </div>
          </div>
        </MechanicProfileSection>
      )}

      <MechanicProfileSection>
        <MechanicSectionTitle>Profile Information</MechanicSectionTitle>
        <MechanicProfileGrid>
          {profile?.license_number && (
            <MechanicProfileField>
              <MechanicProfileLabel>License Number</MechanicProfileLabel>
              <MechanicProfileValue>{profile.license_number}</MechanicProfileValue>
            </MechanicProfileField>
          )}
          
          {profile?.certifications && profile.certifications.length > 0 && (
            <MechanicProfileField>
              <MechanicProfileLabel>Certifications</MechanicProfileLabel>
              <MechanicProfileValue>{profile.certifications.join(', ')}</MechanicProfileValue>
            </MechanicProfileField>
          )}
          
          {properties.specialties && properties.specialties.length > 0 && (
            <MechanicProfileField>
              <MechanicProfileLabel>Specialties</MechanicProfileLabel>
              <MechanicProfileValue>{properties.specialties.join(', ')}</MechanicProfileValue>
            </MechanicProfileField>
          )}
          
          {profile?.current_location && (
            <MechanicProfileField>
              <MechanicProfileLabel>Current Location</MechanicProfileLabel>
              <MechanicProfileValue>
                {profile.current_location.lat.toFixed(4)}, {profile.current_location.lng.toFixed(4)}
              </MechanicProfileValue>
            </MechanicProfileField>
          )}
          
          {profile?.created_at && (
            <MechanicProfileField>
              <MechanicProfileLabel>Joined</MechanicProfileLabel>
              <MechanicProfileValue>{new Date(profile.created_at).toLocaleDateString()}</MechanicProfileValue>
            </MechanicProfileField>
          )}
        </MechanicProfileGrid>
      </MechanicProfileSection>

      {profile?.availability && (
        <MechanicProfileSection>
          <MechanicSectionTitle>Availability</MechanicSectionTitle>
          <MechanicProfileGrid>
            {profile.availability.days && (
              <MechanicProfileField>
                <MechanicProfileLabel>Available Days</MechanicProfileLabel>
                <MechanicProfileValue>{profile.availability.days.join(', ')}</MechanicProfileValue>
              </MechanicProfileField>
            )}
            
            {profile.availability.hours && (
              <MechanicProfileField>
                <MechanicProfileLabel>Working Hours</MechanicProfileLabel>
                <MechanicProfileValue>{profile.availability.hours}</MechanicProfileValue>
              </MechanicProfileField>
            )}
          </MechanicProfileGrid>
        </MechanicProfileSection>
      )}
    </MechanicProfileCard>
  )
}
