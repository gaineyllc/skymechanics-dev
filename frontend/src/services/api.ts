import axios from 'axios'

const API_BASE_URL = 'http://localhost:8200'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Customer {
  node_id: number
  label: string
  properties: {
    name: string
    email: string
    phone: string
    address: string
  }
}

export interface Job {
  node_id: number
  label: string
  properties: {
    title: string
    description: string
    status: string
    priority: string
    customer_id: number
  }
}

export interface Mechanic {
  node_id: number
  label: string
  properties: {
    name: string
    email: string
    phone: string
    specialties: string[]
  }
  profile?: {
    license_number: string
    certifications: string[]
    availability: Record<string, any>
    current_location: { lat: number; lng: number }
    created_at: string
    updated_at: string
  }
}

// Customers
export const fetchCustomers = async (): Promise<Customer[]> => {
  const response = await api.get('/customers')
  return response.data
}

export const createCustomer = async (data: Partial<Customer['properties']>): Promise<Customer> => {
  const response = await api.post('/customers', data)
  return response.data
}

// Jobs
export const fetchJobs = async (): Promise<Job[]> => {
  const response = await api.get('/jobs')
  return response.data
}

export const fetchJobById = async (id: number): Promise<Job> => {
  const response = await api.get(`/jobs/${id}`)
  return response.data
}

export const updateJob = async (id: number, data: Partial<Job['properties']>): Promise<Job> => {
  const response = await api.put(`/jobs/${id}`, data)
  return response.data
}

export const deleteJob = async (id: number): Promise<void> => {
  await api.delete(`/jobs/${id}`)
}

export const createJob = async (data: Partial<Job['properties']>): Promise<Job> => {
  const response = await api.post('/jobs', data)
  return response.data
}

export const updateJobStatus = async (id: number, status: string, newStatus: string, comment?: string): Promise<Job> => {
  const response = await api.post(`/jobs/${id}/status`, { status, new_status: newStatus, comment })
  return response.data
}

export const getJobWorkflow = async (id: number): Promise<any> => {
  const response = await api.get(`/jobs/${id}/workflow`)
  return response.data
}

export const getCompleteWorkflow = async (): Promise<any> => {
  const response = await api.get('/jobs/workflow/complete')
  return response.data
}

// Mechanics
export const fetchMechanics = async (): Promise<Mechanic[]> => {
  const response = await api.get('/mechanics')
  return response.data
}

export const createMechanic = async (data: Partial<Mechanic['properties']>): Promise<Mechanic> => {
  const response = await api.post('/mechanics', data)
  return response.data
}

export const getMechanic = async (id: number): Promise<Mechanic> => {
  const response = await api.get(`/mechanics/${id}`)
  return response.data
}

export const updateMechanicProfile = async (
  id: number,
  profileData: Partial<Mechanic['profile']>
): Promise<Mechanic> => {
  const response = await api.post(`/mechanics/${id}/profile`, profileData)
  return response.data
}

// Health check
export const fetchHealth = async () => {
  const response = await api.get('/health')
  return response.data
}
