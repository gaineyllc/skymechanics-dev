import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { Card, Button, KIND, SIZE, Heading, Spinner, Notification, TYPE } from 'baseui'
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

const JobTitle = styled(Heading, {
  margin: 0,
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

const InfoCard = styled(Card, {
  backgroundColor: '#f8f9fa',
})

const InfoLabel = styled('div', {
  fontSize: '12px',
  color: '#666666',
  marginBottom: '4px',
})

const InfoValue = styled('div', {
  fontSize: '16px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const Timeline = styled('div', {
  display: 'flex',
  alignItems: 'center',
  gap: '16px',
  marginBottom: '24px',
})

const TimelineItem = styled('div', {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  flex: 1,
})

const TimelineCircle = styled('div', {
  width: '40px',
  height: '40px',
  borderRadius: '50%',
  backgroundColor: '#e0e0e0',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  marginBottom: '8px',
})

const TimelineCircleActive = styled(TimelineCircle, {
  backgroundColor: '#007AFF',
  color: '#ffffff',
})

const TimelineLabel = styled('div', {
  fontSize: '14px',
  fontWeight: '600',
})

const TimelineLabelActive = styled(TimelineLabel, {
  color: '#007AFF',
})

const TabBar = styled('div', {
  display: 'flex',
  gap: '8px',
  marginBottom: '24px',
})

const TabButton = styled('button', {
  padding: '12px 24px',
  borderRadius: '8px',
  border: 'none',
  backgroundColor: '#f5f5f5',
  color: '#666666',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '600',
})

const TabButtonActive = styled(TabButton, {
  backgroundColor: '#007AFF',
  color: '#ffffff',
})

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
        const data = await fetchJobById(Number(id))
        setJob(data)
      } catch (err) {
        setError('Failed to load job')
      } finally {
        setLoading(false)
      }
    }
    loadJob()
  }, [id])

  const handleDelete = async () => {
    if (!job || !confirm('Are you sure you want to delete this job?')) return
    try {
      await deleteJob(job.node_id)
      navigate('/jobs')
    } catch (err) {
      setError('Failed to delete job')
    }
  }

  const handleUpdate = async (status: string) => {
    if (!job) return
    try {
      const updated = await updateJob(job.node_id, { ...job.properties, status })
      setJob(updated)
    } catch (err) {
      setError('Failed to update job')
    }
  }

  if (loading) {
    return (
      <JobDetailContainer>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spinner size={48} />
          <p>Loading job...</p>
        </div>
      </JobDetailContainer>
    )
  }

  if (error) {
    return (
      <JobDetailContainer>
        <Notification
          kind={TYPE.negative}
          title="Error"
          subtitle={error}
          autoHide
          autoHideDuration={5000}
        />
        <Link to="/jobs">
          <Button kind={KIND.secondary}>Back to Jobs</Button>
        </Link>
      </JobDetailContainer>
    )
  }

  if (!job) {
    return (
      <JobDetailContainer>
        <p>Job not found</p>
        <Link to="/jobs">
          <Button kind={KIND.secondary}>Back to Jobs</Button>
        </Link>
      </JobDetailContainer>
    )
  }

  const statusOptions = ['pending', 'open', 'completed']

  return (
    <JobDetailContainer>
      <JobHeader>
        <div>
          <JobTitle>Job #{job.node_id}</JobTitle>
          <JobId>Created: April 18, 2026</JobId>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button kind="secondary" size={SIZE.compact} onClick={() => navigate(-1)}>
            Back
          </Button>
          <Button kind={KIND.secondary} size={SIZE.compact} onClick={() => alert('Edit dialog not yet implemented')}>
            Edit
          </Button>
          <Button kind={KIND.primary} size={SIZE.compact} onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </JobHeader>

      <JobInfo>
        <InfoCard>
          <InfoLabel>Customer</InfoLabel>
          <InfoValue>Customer #{job.properties.customer_id}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Status</InfoLabel>
          <InfoValue>{job.properties.status}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Priority</InfoLabel>
          <InfoValue>{job.properties.priority}</InfoValue>
        </InfoCard>
        <InfoCard>
          <InfoLabel>Estimated Cost</InfoLabel>
          <InfoValue>${(Math.random() * 1000 + 100).toFixed(2)}</InfoValue>
        </InfoCard>
      </JobInfo>

      <Timeline>
        <TimelineItem>
          <TimelineCircleActive>
            <span>1</span>
          </TimelineCircleActive>
          <TimelineLabelActive>Requested</TimelineLabelActive>
        </TimelineItem>
        <div style={{ flex: 1, height: '2px', backgroundColor: '#e0e0e0' }} />
        <TimelineItem>
          <TimelineCircleActive>
            <span>2</span>
          </TimelineCircleActive>
          <TimelineLabelActive>Assigned</TimelineLabelActive>
        </TimelineItem>
        <div style={{ flex: 1, height: '2px', backgroundColor: '#e0e0e0' }} />
        <TimelineItem>
          <TimelineCircle>
            <span>3</span>
          </TimelineCircle>
          <TimelineLabel>Completed</TimelineLabel>
        </TimelineItem>
        <div style={{ flex: 1, height: '2px', backgroundColor: '#e0e0e0' }} />
        <TimelineItem>
          <TimelineCircle>
            <span>4</span>
          </TimelineCircle>
          <TimelineLabel>Approved</TimelineLabel>
        </TimelineItem>
        <div style={{ flex: 1, height: '2px', backgroundColor: '#e0e0e0' }} />
        <TimelineItem>
          <TimelineCircle>
            <span>5</span>
          </TimelineCircle>
          <TimelineLabel>PAID</TimelineLabel>
        </TimelineItem>
      </Timeline>

      <TabBar>
        <TabButtonActive>Overview</TabButtonActive>
        <TabButton>Timeline</TabButton>
        <TabButton>Documents</TabButton>
        <TabButton>Communication</TabButton>
        <TabButton>Invoice</TabButton>
      </TabBar>

      <Card>
        <Heading level="h3" marginBottom="16px">
          Job Details
        </Heading>
        <p style={{ color: '#333333', marginBottom: '16px' }}>
          <strong>Service Requested:</strong> {job.properties.title}
        </p>
        <p style={{ color: '#333333', marginBottom: '16px' }}>
          <strong>Description:</strong> {job.properties.description}
        </p>
        <p style={{ color: '#333333', marginBottom: '16px' }}>
          <strong>Parts Required:</strong>
        </p>
        <ul style={{ color: '#333333', marginBottom: '16px', paddingLeft: '24px' }}>
          <li>Piston Rings Set - $150.00</li>
          <li>Oil Filter - $25.00</li>
          <li>Spark Plugs (4-pack) - $40.00</li>
          <li>Engine Oil (5QT) - $35.00</li>
        </ul>
        <p style={{ color: '#333333' }}>
          <strong>Labor:</strong> 8 hours @ $75/hour = $600.00
        </p>
      </Card>

      <Card style={{ marginTop: '24px' }}>
        <Heading level="h3" marginBottom="16px">
          Change Status
        </Heading>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {statusOptions.map((status) => (
            <Button
              key={status}
              kind={job.properties.status === status ? KIND.primary : KIND.secondary}
              size={SIZE.compact}
              onClick={() => handleUpdate(status)}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </Button>
          ))}
        </div>
      </Card>
    </JobDetailContainer>
  )
}
