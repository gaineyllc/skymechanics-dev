import React from 'react'
import { styled } from '../utils/styled'

// ========== Rep Score Badge ==========
const RepScoreBadge = styled('div', {
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  padding: '8px 16px',
  borderRadius: '20px',
  fontWeight: '600',
  fontSize: '14px',
})

const RepScoreColors = {
  excellent: { backgroundColor: '#e8f5e9', color: '#2e7d32' },
  good: { backgroundColor: '#e3f2fd', color: '#1565c0' },
  average: { backgroundColor: '#fff3e0', color: '#f57c00' },
  needs_improvement: { backgroundColor: '#ffebee', color: '#c62828' },
}

// ========== Rep Breakdown Card ==========
const RepBreakdownCard = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '20px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const RepBreakdownHeader = styled('div', {
  marginBottom: '16px',
})

const RepBreakdownTitle = styled('h4', {
  margin: 0,
  fontSize: '16px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const RepBreakdownItem = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '12px',
  padding: '8px 0',
})

const RepBreakdownLabel = styled('span', {
  fontSize: '14px',
  color: '#666666',
})

const RepBreakdownValue = styled('span', {
  fontSize: '14px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const RepBreakdownBar = styled('div', {
  width: '100%',
  height: '4px',
  backgroundColor: '#f0f0f0',
  borderRadius: '2px',
  overflow: 'hidden',
  marginTop: '8px',
})

const RepBreakdownFill = styled('div', {
  height: '100%',
  backgroundColor: '#007AFF',
  borderRadius: '2px',
})

// ========== Certifications List ==========
const CertificationsList = styled('div', {
  display: 'flex',
  flexWrap: 'wrap',
  gap: '8px',
})

const CertificationBadge = styled('div', {
  display: 'flex',
  alignItems: 'center',
  gap: '6px',
  padding: '6px 12px',
  backgroundColor: '#f0f0f0',
  borderRadius: '16px',
  fontSize: '12px',
  fontWeight: '500',
})

// ========== Experience Timeline ==========
const ExperienceTimeline = styled('div', {
  display: 'flex',
  flexDirection: 'column',
  gap: '16px',
})

const ExperienceItem = styled('div', {
  display: 'flex',
  gap: '16px',
})

const ExperienceDate = styled('div', {
  minWidth: '100px',
  fontSize: '12px',
  color: '#999999',
})

const ExperienceDetails = styled('div', {
  flex: 1,
})

const ExperienceTitle = styled('div', {
  fontSize: '14px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const ExperienceDescription = styled('div', {
  fontSize: '13px',
  color: '#666666',
})

// ========== Reputation Metrics ==========
const ReputationMetrics = styled('div', {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
  gap: '12px',
  marginBottom: '20px',
})

const MetricCard = styled('div', {
  backgroundColor: '#f5f5f5',
  padding: '16px',
  borderRadius: '8px',
  textAlign: 'center',
})

const MetricValue = styled('div', {
  fontSize: '24px',
  fontWeight: 'bold',
  color: '#007AFF',
})

const MetricLabel = styled('div', {
  fontSize: '12px',
  color: '#666666',
  marginTop: '4px',
})

// Export components
export function RepScoreBadge({ score }: { score: number }) {
  let colorKey: keyof typeof RepScoreColors
  
  if (score >= 90) {
    colorKey = 'excellent'
  } else if (score >= 70) {
    colorKey = 'good'
  } else if (score >= 50) {
    colorKey = 'average'
  } else {
    colorKey = 'needs_improvement'
  }

  return (
    <RepScoreBadge style={RepScoreColors[colorKey]}>
      <span>★ {score}/100</span>
    </RepScoreBadge>
  )
}

export function RepBreakdownCard({ 
  totalScore,
  certificationStatus,
  experienceDepth,
  performance,
  recentActivity,
  compliance,
  componentScores,
}: {
  totalScore: number
  certificationStatus: number
  experienceDepth: number
  performance: number
  recentActivity: number
  compliance: number
  componentScores?: {
    certification_status?: number
    experience_depth?: number
    performance?: number
    recent_activity?: number
    compliance?: number
  }
}) {
  // Use componentScores if provided, otherwise use individual props
  const scores = componentScores || {
    certification_status: certificationStatus,
    experience_depth: experienceDepth,
    performance: performance,
    recent_activity: recentActivity,
    compliance: compliance,
  }

  const breakdowns = [
    { label: 'Certification Status', value: scores.certification_status || 0, color: '#007AFF', weight: '25%' },
    { label: 'Experience Depth', value: scores.experience_depth || 0, color: '#34C759', weight: '20%' },
    { label: 'Performance', value: scores.performance || 0, color: '#FF9500', weight: '30%' },
    { label: 'Recent Activity', value: scores.recent_activity || 0, color: '#AF52DE', weight: '15%' },
    { label: 'Compliance', value: scores.compliance || 0, color: '#FF3B30', weight: '10%' },
  ]

  return (
    <RepBreakdownCard>
      <RepBreakdownHeader>
        <RepBreakdownTitle>Reputation Breakdown</RepBreakdownTitle>
      </RepBreakdownHeader>

      <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <RepScoreBadge score={totalScore} />
        </div>
        <div style={{ fontSize: '12px', color: '#999999' }}>
          Weighted average across 5 components
        </div>
      </div>

      {breakdowns.map((item) => (
        <div key={item.label}>
          <RepBreakdownItem>
            <RepBreakdownLabel>{item.label} ({item.weight})</RepBreakdownLabel>
            <RepBreakdownValue>{item.value}/100</RepBreakdownValue>
          </RepBreakdownItem>
          <RepBreakdownBar>
            <RepBreakdownFill 
              style={{ 
                width: `${(item.value / 100) * 100}%`, 
                backgroundColor: item.color 
              }} 
            />
          </RepBreakdownBar>
        </div>
      ))}
    </RepBreakdownCard>
  )
}

export function CertificationsList({ certifications }: { certifications: string[] }) {
  return (
    <CertificationsList>
      {certifications.map((cert, index) => (
        <CertificationBadge key={index}>
          <span>✓</span>
          <span>{cert}</span>
        </CertificationBadge>
      ))}
    </CertificationsList>
  )
}

export function ExperienceTimeline({ experiences }: { experiences: { date: string; title: string; description: string }[] }) {
  return (
    <ExperienceTimeline>
      {experiences.map((exp, index) => (
        <ExperienceItem key={index}>
          <ExperienceDate>{exp.date}</ExperienceDate>
          <ExperienceDetails>
            <ExperienceTitle>{exp.title}</ExperienceTitle>
            <ExperienceDescription>{exp.description}</ExperienceDescription>
          </ExperienceDetails>
        </ExperienceItem>
      ))}
    </ExperienceTimeline>
  )
}

export function ReputationMetricsCard({ 
  reviewCount,
  avgRating,
  totalScore,
  componentScores,
}: {
  reviewCount: number
  avgRating?: number
  totalScore: number
  componentScores: {
    certification_status: number
    experience_depth: number
    performance: number
    recent_activity: number
    compliance: number
  }
}) {
  return (
    <div>
      <ReputationMetrics>
        <MetricCard>
          <MetricValue>{reviewCount}</MetricValue>
          <MetricLabel>Reviews</MetricLabel>
        </MetricCard>
        
        <MetricCard>
          <MetricValue>{avgRating?.toFixed(1) || '0.0'}</MetricValue>
          <MetricLabel>Avg Rating</MetricLabel>
        </MetricCard>
        
        <MetricCard>
          <MetricValue>{totalScore}</MetricValue>
          <MetricLabel>Score</MetricLabel>
        </MetricCard>
      </ReputationMetrics>
      
      <RepBreakdownCard
        totalScore={totalScore}
        componentScores={componentScores}
      />
    </div>
  )
}
