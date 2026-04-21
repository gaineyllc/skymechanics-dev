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

// ============== Procedure Configuration ==============

export interface ConfigSource {
  source_id: number
  name: string
  type: string
  version?: string
  url?: string
  description?: string
  is_active: boolean
  created_at: string
  last_updated: string
}

export interface ProcedureTemplate {
  procedure_id: number
  name: string
  category: string
  authority: string
  estimated_duration_hours: number
  required_specialty: string
  source_id?: number
  is_active: boolean
  created_at: string
  updated_at: string
  tasks: any[]
}

export interface TaskTemplate {
  task_id: number
  procedure_id: number
  name: string
  sequence: number
  category: string
  estimated_duration_minutes: number
  required_tools: string[]
  required_parts: string[]
  checklist_items: any[]
  instructions?: string
  created_at: string
  updated_at: string
}

export interface Tool {
  tool_id: number
  name: string
  category: string
  part_number?: string
  calibration_required: boolean
  calibration_interval_months?: number
  description?: string
  created_at: string
  updated_at: string
}

export interface Part {
  part_id: number
  part_number: string
  name: string
  category: string
  aircraft_compatible: string[]
  oem_source?: string
  description?: string
  created_at: string
  updated_at: string
}

export interface AircraftType {
  aircraft_type_id: number
  make: string
  model: string
  category: string
  certification: string
  amm_ref?: string
  mpd_ref?: string
  ipc_ref?: string
  created_at: string
  updated_at: string
}

// Configuration Sources
export const fetchConfigSources = async (): Promise<ConfigSource[]> => {
  const response = await api.get('/config/sources')
  return response.data
}

export const createConfigSource = async (data: Partial<ConfigSource>): Promise<ConfigSource> => {
  const response = await api.post('/config/sources', data)
  return response.data
}

export const getConfigSource = async (id: number): Promise<ConfigSource> => {
  const response = await api.get(`/config/sources/${id}`)
  return response.data
}

// Procedure Templates
export const fetchProcedures = async (category?: string, isActive?: boolean): Promise<ProcedureTemplate[]> => {
  const params = new URLSearchParams()
  if (category) params.append('category', category)
  if (isActive !== undefined) params.append('is_active', isActive.toString())
  const response = await api.get(`/config/procedures?${params.toString()}`)
  return response.data
}

export const createProcedure = async (data: Partial<ProcedureTemplate>): Promise<ProcedureTemplate> => {
  const response = await api.post('/config/procedures', data)
  return response.data
}

export const getProcedure = async (id: number): Promise<ProcedureTemplate> => {
  const response = await api.get(`/config/procedures/${id}`)
  return response.data
}

export const updateProcedure = async (id: number, data: Partial<ProcedureTemplate>): Promise<ProcedureTemplate> => {
  const response = await api.put(`/config/procedures/${id}`, data)
  return response.data
}

export const deleteProcedure = async (id: number): Promise<void> => {
  await api.delete(`/config/procedures/${id}`)
}

// Tasks
export const fetchTasks = async (procedureId?: number): Promise<TaskTemplate[]> => {
  const params = new URLSearchParams()
  if (procedureId) params.append('procedure_id', procedureId.toString())
  const response = await api.get(`/config/tasks?${params.toString()}`)
  return response.data
}

export const createTask = async (data: Partial<TaskTemplate>): Promise<TaskTemplate> => {
  const response = await api.post('/config/tasks', data)
  return response.data
}

export const getTask = async (id: number): Promise<TaskTemplate> => {
  const response = await api.get(`/config/tasks/${id}`)
  return response.data
}

export const updateTask = async (id: number, data: Partial<TaskTemplate>): Promise<TaskTemplate> => {
  const response = await api.put(`/config/tasks/${id}`, data)
  return response.data
}

export const deleteTask = async (id: number): Promise<void> => {
  await api.delete(`/config/tasks/${id}`)
}

// Tools
export const fetchTools = async (category?: string): Promise<Tool[]> => {
  const params = new URLSearchParams()
  if (category) params.append('category', category)
  const response = await api.get(`/config/tools?${params.toString()}`)
  return response.data
}

export const createTool = async (data: Partial<Tool>): Promise<Tool> => {
  const response = await api.post('/config/tools', data)
  return response.data
}

export const getTool = async (id: number): Promise<Tool> => {
  const response = await api.get(`/config/tools/${id}`)
  return response.data
}

export const updateTool = async (id: number, data: Partial<Tool>): Promise<Tool> => {
  const response = await api.put(`/config/tools/${id}`, data)
  return response.data
}

export const deleteTool = async (id: number): Promise<void> => {
  await api.delete(`/config/tools/${id}`)
}

// Parts
export const fetchParts = async (category?: string, aircraftId?: string): Promise<Part[]> => {
  const params = new URLSearchParams()
  if (category) params.append('category', category)
  if (aircraftId) params.append('aircraft_id', aircraftId)
  const response = await api.get(`/config/parts?${params.toString()}`)
  return response.data
}

export const createPart = async (data: Partial<Part>): Promise<Part> => {
  const response = await api.post('/config/parts', data)
  return response.data
}

export const getPart = async (id: number): Promise<Part> => {
  const response = await api.get(`/config/parts/${id}`)
  return response.data
}

export const updatePart = async (id: number, data: Partial<Part>): Promise<Part> => {
  const response = await api.put(`/config/parts/${id}`, data)
  return response.data
}

export const deletePart = async (id: number): Promise<void> => {
  await api.delete(`/config/parts/${id}`)
}

// Aircraft Types
export const fetchAircraftTypes = async (): Promise<AircraftType[]> => {
  const response = await api.get('/config/aircraft-types')
  return response.data
}

export const createAircraftType = async (data: Partial<AircraftType>): Promise<AircraftType> => {
  const response = await api.post('/config/aircraft-types', data)
  return response.data
}

export const getAircraftType = async (id: number): Promise<AircraftType> => {
  const response = await api.get(`/config/aircraft-types/${id}`)
  return response.data
}

export const updateAircraftType = async (id: number, data: Partial<AircraftType>): Promise<AircraftType> => {
  const response = await api.put(`/config/aircraft-types/${id}`, data)
  return response.data
}

export const deleteAircraftType = async (id: number): Promise<void> => {
  await api.delete(`/config/aircraft-types/${id}`)
}

// FAA Documentation Import
export const importAC4313 = async (): Promise<any> => {
  const response = await api.post('/config/import/faa/ac-43-13-1b')
  return response.data
}

export const importAC20106 = async (): Promise<any> => {
  const response = await api.post('/config/import/faa/ac-20-106')
  return response.data
}

// Execute Procedure
export const executeProcedure = async (procedureId: number): Promise<any> => {
  const response = await api.get(`/config/procedures/${procedureId}/execute`)
  return response.data
}

// Health check
export const fetchHealth = async () => {
  const response = await api.get('/health')
  return response.data
}
