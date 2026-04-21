import React from 'react'
import { styled } from '../utils/styled'

const CardContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const CardHeader = styled('div', {
  marginBottom: '16px',
})

const CardTitle = styled('h3', {
  margin: 0,
  fontSize: '18px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const CardBody = styled('div', {
  color: '#333333',
})

const CardFooter = styled('div', {
  marginTop: '16px',
  paddingTop: '16px',
  borderTop: '1px solid #e0e0e0',
})

export function Dashboard() {
  const stats = [
    { label: 'Active Jobs', value: '12', change: '+2', color: '#007AFF' },
    { label: 'Pending Approval', value: '5', change: '-1', color: '#FF9500' },
    { label: 'Customers', value: '24', change: '+4', color: '#34C759' },
    { label: 'Mechanics', value: '8', change: '0', color: '#AF52DE' },
  ]

  return (
    <div>
      <h1 style={{ marginBottom: '24px' }}>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        {stats.map((stat, index) => (
          <CardContainer key={index}>
            <CardHeader>
              <CardTitle>{stat.label}</CardTitle>
            </CardHeader>
            <CardBody>
              <div style={{ fontSize: '36px', fontWeight: 'bold', color: stat.color }}>
                {stat.value}
              </div>
              <div style={{ fontSize: '14px', color: '#666666', marginTop: '4px' }}>
                {stat.change} from last week
              </div>
            </CardBody>
          </CardContainer>
        ))}
      </div>

      <CardContainer>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardBody>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {[
              { type: 'Job Created', description: 'Engine Repair - John Smith', time: '2 hours ago' },
              { type: 'Job Completed', description: 'Brake Replacement - Jane Doe', time: '4 hours ago' },
              { type: 'Payment Received', description: 'Invoice #1234 - Bob Johnson', time: '6 hours ago' },
              { type: 'Mechanic Assigned', description: 'Alice Williams - Diagnostic Check', time: '1 day ago' },
            ].map((activity, index) => (
              <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                <div>
                  <div style={{ fontWeight: '600' }}>{activity.type}</div>
                  <div style={{ fontSize: '14px', color: '#666666' }}>{activity.description}</div>
                </div>
                <div style={{ fontSize: '12px', color: '#999999' }}>{activity.time}</div>
              </div>
            ))}
          </div>
        </CardBody>
      </CardContainer>
    </div>
  )
}
