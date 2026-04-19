import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { fetchJobById, updateJob, deleteJob, Job } from '../services/api'

const JobDetailContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const JobHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '24px',
  paddingBottom: '24px',
  borderBottom: '1px solid #e0e0e0',
})

const JobTitle = styled('h1', {
  margin: 0,
  fontSize: '24px',
  color: '#1a1a1a',
})

const JobId = styled('span', {
  fontSize: '14px',
  color: '#999999',
})

const JobInfo = styled('div', {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
  gap: '16px',
  marginBottom: '24px',
})

const InfoCard = styled('div', {
  backgroundColor: '#f8f9fa',
  padding: '16px',
  borderRadius: '8px',
})

const InfoLabel = styled('div', {
  fontSize: '12px',
  color: '#666666',
  marginBottom: '4px',
})

const InfoValue = styled('div', {
  fontSize: '16px',
  fontWeight: '500',
  color: '#1a1a1a',
})

const Description = styled('div', {
  marginBottom: '24px',
})

const DescriptionLabel = styled('div', {
  fontSize: '14px',
  fontWeight: '600',
  marginBottom: '8px',
  color: '#1a1a1a',
})

const DescriptionText = styled('div', {
  fontSize: '14px',
  color: '#333333',
  lineHeight: '1.6',
})

const StatusBadge = styled('div', {
  padding: '4px 12px',
  borderRadius: '16px',
  fontSize: '12px',
  fontWeight: '600',
})

const StatusOpen = styled(StatusBadge, {
  backgroundColor: '#E8F5E9',
  color: '#2E7D32',
})

const StatusPending = styled(StatusBadge, {
  backgroundColor: '#FFF3E0',
  color: '#F57C00',
})

const StatusCompleted = styled(StatusBadge, {
  backgroundColor: '#E3F2FD',
  color: '#1565C0',
})

const Buttons = styled('div', {
  display: 'flex',
  gap: '8px',
  marginTop: '24px',
})

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
      '&:hover': { backgroundColor: '#f0f0f0' },
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

export function JobDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadJob = async () => {
      if (!id) return
      try {
        const data = await fetchJobById(id)
        setJob(data)
      } catch (err) {
        setError('Failed to load job')
      } finally {
        setLoading(false)
      }
    }
    loadJob()
  }, [id])

  const handleUpdate = async (status: string) => {
    if (!job) return
    try {
      const updated = await updateJob(job.node_id, { ...job.properties, status })
      setJob(updated)
    } catch (err) {
      setError('Failed to update job')
    }
  }

  const handleDelete = async () => {
    if (!job) return
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await deleteJob(job.node_id)
        navigate('/jobs')
      } catch (err) {
        setError('Failed to delete job')
      }
    }
  }

  if (loading) {
    return (
      <JobDetailContainer>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading job...</p>
        </div>
      </JobDetailContainer>
    )
  }

  if (error) {
    return (
      <JobDetailContainer>
        <Notification
          onClose={() => setError(null)}
          kind="negative"
          title="Error"
          subtitle={error}
          autoHide
          autoHideDuration={3000}
        />
        <Button kind={KIND.secondary} onClick={() => navigate('/jobs')}>
          Back to Jobs
        </Button>
      </JobDetailContainer>
    )
  }

  if (!job) {
    return (
      <JobDetailContainer>
        <p style={{ textAlign: 'center', color: '#666' }}>Job not found</p>
        <Button kind={KIND.secondary} onClick={() => navigate('/jobs')}>
          Back to Jobs
        </Button>
      </JobDetailContainer>
    )
  }

  return (
    <JobDetailContainer>
      <JobHeader>
        <div>
          <JobId>Job #{job.node_id}</JobId>
          <JobTitle>{job.properties.title}</JobTitle>
        </div>
        <div>
          {job.properties.status === 'open' && <StatusOpen>Open</StatusOpen>}
          {job.properties.status === 'pending' && <StatusPending>Pending</StatusPending>}
          {job.properties.status === 'completed' && <StatusCompleted>Completed</StatusCompleted>}
        </div>
      </JobHeader>

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

      <JobInfo>
        <InfoCard>
          <InfoLabel>Status</InfoLabel>
          <InfoValue>{job.properties.status}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Priority</InfoLabel>
          <InfoValue>{job.properties.priority}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Customer</InfoLabel>
          <InfoValue>{job.properties.customer_id}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Aircraft</InfoLabel>
          <InfoValue>{job.properties.aircraft_id}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Mechanic</InfoLabel>
          <InfoValue>{job.properties.mechanic_id}</InfoValue>
        </InfoCard>
      </JobInfo>

      <Description>
        <DescriptionLabel>Description</DescriptionLabel>
        <DescriptionText>{job.properties.description}</DescriptionText>
      </Description>

      <Buttons>
        {job.properties.status !== 'completed' && (
          <Button kind={KIND.primary} onClick={() => handleUpdate('completed')}>
            Mark Complete
          </Button>
        )}
        {job.properties.status !== 'open' && job.properties.status !== 'completed' && (
          <Button kind={KIND.secondary} onClick={() => handleUpdate('open')}>
            Set Open
          </Button>
        )}
        <Button kind={KIND.tertiary} onClick={() => navigate('/jobs')}>
          Cancel
        </Button>
        <Button kind={KIND.negative} onClick={handleDelete}>
          Delete
        </Button>
      </Buttons>
    </JobDetailContainer>
  )
}
