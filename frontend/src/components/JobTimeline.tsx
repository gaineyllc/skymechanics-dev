import { useEffect, useState } from 'react'
import { styled } from 'baseui'

const JobStatusTimeline = styled('div', {
  display: 'flex',
  alignItems: 'center',
  gap: '16px',
  marginBottom: '24px',
})

const TimelineStep = styled('div', {
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
  position: 'relative',
  zIndex: 2,
})

const TimelineLine = styled('div', {
  flex: 1,
  height: '2px',
  backgroundColor: '#e0e0e0',
  position: 'relative',
  zIndex: 1,
})

const TimelineLabel = styled('div', {
  fontSize: '12px',
  fontWeight: '600',
})

const TimelineStepActive = styled(TimelineStep, {
  '& $TimelineCircle': {
    backgroundColor: '#007AFF',
    color: '#ffffff',
  },
  '& $TimelineLine': {
    backgroundColor: '#007AFF',
  },
  '& $TimelineLabel': {
    color: '#007AFF',
  },
})

interface JobTimelineProps {
  currentStep: number
  totalSteps: number
}

export function JobTimeline({ currentStep, totalSteps }: JobTimelineProps) {
  const steps = ['Requested', 'Assigned', 'In Progress', 'Completed', 'Approved', 'Paid']

  return (
    <JobStatusTimeline>
      {steps.map((step, index) => {
        const isCompleted = index < currentStep
        const isActive = index === currentStep

        return (
          <TimelineStep key={step} className={isCompleted || isActive ? 'active' : ''}>
            <TimelineCircle>
              {isCompleted ? '✓' : isActive ? '●' : index + 1}
            </TimelineCircle>
            <TimelineLabel className={isCompleted || isActive ? 'active' : ''}>
              {step}
            </TimelineLabel>
          </TimelineStep>
        )
      })}
    </JobStatusTimeline>
  )
}
