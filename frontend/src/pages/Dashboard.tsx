import React, { useState, useEffect } from 'react'
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

interface JobStats {
  pending: number;
  open: number;
  inProgress: number;
  completed: number;
}

interface ActivityItem {
  type: string;
  description: string;
  time: string;
  jobTitle?: string;
  mechanicName?: string;
}

export function Dashboard() {
  const [stats, setStats] = useState({
    activeJobs: 0,
    pendingApproval: 0,
    customers: 0,
    mechanics: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [jobs, setJobs] = useState<JobStats>({ pending: 0, open: 0, inProgress: 0, completed: 0 });
  const [activities, setActivities] = useState<ActivityItem[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch jobs from API
        const jobsResponse = await fetch('/api/v1/jobs');
        if (jobsResponse.ok) {
          const jobsData = await jobsResponse.json();
          const jobCounts: JobStats = { pending: 0, open: 0, inProgress: 0, completed: 0 };
          
          jobsData.forEach((job: any) => {
            const status = job.properties?.status || 'pending';
            if (jobCounts[status as keyof JobStats] !== undefined) {
              jobCounts[status as keyof JobStats]++;
            }
          });
          
          setJobs(jobCounts);
          setStats({
            activeJobs: jobCounts.open + jobCounts.inProgress,
            pendingApproval: jobCounts.pending,
            customers: 24, // Will be replaced with real count from API
            mechanics: 8,  // Will be replaced with real count from API
          });
        }
        
        // Generate sample activities based on job data
        const sampleActivities: ActivityItem[] = [];
        if (jobCounts.open > 0) {
          sampleActivities.push({
            type: 'Job Started',
            description: 'Hydraulic System Check - Mountain Air Inc.',
            time: '2 hours ago',
            jobTitle: 'Hydraulic System Check',
            mechanicName: 'John Smith',
          });
        }
        if (jobCounts.completed > 0) {
          sampleActivities.push({
            type: 'Job Completed',
            description: 'Brake Replacement - Coastal Aviation',
            time: '4 hours ago',
            jobTitle: 'Brake Replacement',
            mechanicName: 'Jane Doe',
          });
        }
        sampleActivities.push({
          type: 'Payment Received',
          description: 'Invoice #1234 - Bob Johnson',
          time: '6 hours ago',
        });
        if (jobCounts.inProgress > 0) {
          sampleActivities.push({
            type: 'Mechanic Assigned',
            description: 'Alice Williams - Diagnostic Check',
            time: '1 day ago',
            jobTitle: 'Diagnostic Check',
            mechanicName: 'Alice Williams',
          });
        }
        
        setActivities(sampleActivities);

      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div>
        <h1 style={{ marginBottom: '24px' }}>Dashboard</h1>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h1 style={{ marginBottom: '24px' }}>Dashboard</h1>
        <div style={{ textAlign: 'center', padding: '40px', color: '#e53e3e' }}>
          <p>{error}</p>
          <button onClick={() => window.location.reload()} style={{ marginTop: '16px', padding: '8px 16px' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{ marginBottom: '24px' }}>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <CardContainer>
          <CardHeader>
            <CardTitle>Active Jobs</CardTitle>
          </CardHeader>
          <CardBody>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#007AFF' }}>
              {stats.activeJobs}
            </div>
            <div style={{ fontSize: '14px', color: '#666666', marginTop: '4px' }}>
              {jobs.open} open + {jobs.inProgress} in progress
            </div>
          </CardBody>
        </CardContainer>
        
        <CardContainer>
          <CardHeader>
            <CardTitle>Pending</CardTitle>
          </CardHeader>
          <CardBody>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#FF9500' }}>
              {stats.pendingApproval}
            </div>
            <div style={{ fontSize: '14px', color: '#666666', marginTop: '4px' }}>
              {jobs.pending} pending approval
            </div>
          </CardBody>
        </CardContainer>
        
        <CardContainer>
          <CardHeader>
            <CardTitle>Customers</CardTitle>
          </CardHeader>
          <CardBody>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#34C759' }}>
              {stats.customers}
            </div>
            <div style={{ fontSize: '14px', color: '#666666', marginTop: '4px' }}>
              +4 from last week
            </div>
          </CardBody>
        </CardContainer>
        
        <CardContainer>
          <CardHeader>
            <CardTitle>Mechanics</CardTitle>
          </CardHeader>
          <CardBody>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#AF52DE' }}>
              {stats.mechanics}
            </div>
            <div style={{ fontSize: '14px', color: '#666666', marginTop: '4px' }}>
              {jobs.completed} completed this week
            </div>
          </CardBody>
        </CardContainer>
      </div>

      <CardContainer>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>
        <CardBody>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {activities.length > 0 ? (
              activities.map((activity, index) => (
                <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
                  <div>
                    <div style={{ fontWeight: '600' }}>{activity.type}</div>
                    <div style={{ fontSize: '14px', color: '#666666' }}>{activity.description}</div>
                    {activity.mechanicName && (
                      <div style={{ fontSize: '12px', color: '#888888' }}>Mechanic: {activity.mechanicName}</div>
                    )}
                    {activity.jobTitle && (
                      <div style={{ fontSize: '12px', color: '#888888' }}>Job: {activity.jobTitle}</div>
                    )}
                  </div>
                  <div style={{ fontSize: '12px', color: '#999999' }}>{activity.time}</div>
                </div>
              ))
            ) : (
              <div style={{ padding: '20px', textAlign: 'center', color: '#666666' }}>
                No recent activity
              </div>
            )}
          </div>
        </CardBody>
      </CardContainer>
    </div>
  );
}
