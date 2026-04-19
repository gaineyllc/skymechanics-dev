import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { Link } from 'react-router-dom'
import { fetchJobs, createJob, Job } from '../services/api'
import { CreateJobModal } from '../components/CreateJobModal'

const JobsContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const JobsHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '24px',
})

const JobsTitle = styled('h2', {
  margin: 0,
  fontSize: '20px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const Button = ({ kind = 'primary', onClick, children, disabled = false }: any) => {
  const baseStyles = {
    padding: '8px 16px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontWeight: '500',
    fontSize: '14px',
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

const StatusBadge = styled('div', {
  padding: '4px 12px',
  borderRadius: '16px',
  fontSize: '12px',
  fontWeight: '600',
})

const JobCard = styled(Link, {
  display: 'block',
  textDecoration: 'none',
  color: 'inherit',
})

const JobHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '12px',
})

const JobId = styled('span', {
  fontSize: '12px',
  color: '#999999',
})

const JobCustomer = styled('div', {
  fontWeight: '600',
  fontSize: '16px',
  marginBottom: '8px',
})

const JobDescription = styled('div', {
  fontSize: '14px',
  color: '#333333',
  marginBottom: '12px',
})

const JobMeta = styled('div', {
  display: 'flex',
  gap: '16px',
  fontSize: '12px',
  color: '#666666',
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

export function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    const loadJobs = async () => {
      try {
        const data = await fetchJobs()
        setJobs(Array.isArray(data) ? data : [data])
      } catch (err) {
        setError('Failed to load jobs')
      } finally {
        setLoading(false)
      }
    }
    loadJobs()
  }, [])

  const handleCreateJob = async () => {
    setIsModalOpen(true)
  }

  if (loading) {
    return (
      <JobsContainer>
        <JobsHeader>
          <JobsTitle>Jobs</JobsTitle>
          <Button kind={KIND.primary} onClick={handleCreateJob}>
            New Job
          </Button>
        </JobsHeader>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading jobs...</p>
        </div>
      </JobsContainer>
    )
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

  return (
    <JobsContainer>
      <JobsHeader>
        <JobsTitle>Jobs ({jobs.length})</JobsTitle>
        <Button kind={KIND.primary} onClick={handleCreateJob}>
          New Job
        </Button>
      </JobsHeader>

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

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {jobs.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>No jobs yet. Create one to get started.</p>
        ) : (
          jobs.map((job) => (
            <JobCard key={job.node_id} to={`/jobs/${job.node_id}`}>
              <div
                style={{
                  backgroundColor: '#fff',
                  border: '1px solid #e0e0e0',
                  borderRadius: '8px',
                  padding: '16px',
                  marginBottom: '8px',
                }}
              >
                <JobHeader>
                  <JobId>{job.node_id}</JobId>
                  {job.properties.status === 'open' && <StatusOpen>Open</StatusOpen>}
                  {job.properties.status === 'pending' && <StatusPending>Pending</StatusPending>}
                  {job.properties.status === 'completed' && <StatusCompleted>Completed</StatusCompleted>}
                </JobHeader>
                
                <JobCustomer>{job.properties.title}</JobCustomer>
                <JobDescription>{job.properties.description}</JobDescription>
                
                <JobMeta>
                  <span>ID: {job.node_id}</span>
                  <span>Priority: {job.properties.priority}</span>
                </JobMeta>
              </div>
            </JobCard>
          ))
        )}
      </div>

      <CreateJobModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={(job) => setJobs((prev) => [...prev, job])}
      />
    </JobsContainer>
  )
}
