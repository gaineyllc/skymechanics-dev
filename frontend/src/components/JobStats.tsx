import { useEffect, useState } from 'react'
import { Card, styled as baseStyled } from 'baseui'

const JobStats = baseStyled('div', {
  display: 'flex',
  gap: '16px',
  marginBottom: '24px',
})

const StatCard = baseStyled('div', {
  flex: 1,
  padding: '20px',
  backgroundColor: '#f8f9fa',
  borderRadius: '8px',
})

const StatLabel = baseStyled('div', {
  fontSize: '14px',
  color: '#666666',
  marginBottom: '8px',
})

const StatValue = baseStyled('div', {
  fontSize: '28px',
  fontWeight: 'bold',
  color: '#1a1a1a',
})

const ChartContainer = baseStyled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '8px',
  padding: '20px',
  marginBottom: '24px',
})

const ChartTitle = baseStyled('h3', {
  margin: 0,
  fontSize: '16px',
  fontWeight: '600',
  marginBottom: '16px',
})

export function JobStats() {
  const [stats, setStats] = useState({
    totalJobs: 0,
    completed: 0,
    pending: 0,
    revenue: 0,
  })

  useEffect(() => {
    // Fetch stats from API
    setStats({
      totalJobs: 12,
      completed: 8,
      pending: 4,
      revenue: 12500,
    })
  }, [])

  return (
    <div>
      <JobStats>
        <StatCard>
          <StatLabel>Total Jobs</StatLabel>
          <StatValue>{stats.totalJobs}</StatValue>
        </StatCard>
        <StatCard>
          <StatLabel>Completed</StatLabel>
          <StatValue>{stats.completed}</StatValue>
        </StatCard>
        <StatCard>
          <StatLabel>Pending</StatLabel>
          <StatValue>{stats.pending}</StatValue>
        </StatCard>
        <StatCard>
          <StatLabel>Revenue</StatLabel>
          <StatValue>${stats.revenue.toLocaleString()}</StatValue>
        </StatCard>
      </JobStats>

      <ChartContainer>
        <ChartTitle>Job Status Distribution</ChartTitle>
        <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#999999' }}>
          Chart placeholder
        </div>
      </ChartContainer>
    </div>
  )
}
