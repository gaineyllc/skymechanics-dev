import axios from 'axios'

const API_BASE_URL = 'http://localhost:8200'

export const authApi = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Owner Registration
export interface OwnerRegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  org_name: string
}

export interface OwnerRegisterResponse {
  message: string
  user_id: number
  org_name: string
  email: string
}

export const registerOwner = async (data: OwnerRegisterRequest): Promise<OwnerRegisterResponse> => {
  const response = await authApi.post('/api/v1/owner/register', data)
  return response.data
}

// Mechanic Registration
export interface MechanicRegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  license: string
  specialties: string[]
}

export interface MechanicRegisterResponse {
  message: string
  email: string
  name: string
}

export const registerMechanic = async (data: MechanicRegisterRequest): Promise<MechanicRegisterResponse> => {
  const response = await authApi.post('/api/v1/mechanic/register', data)
  return response.data
}

// Login
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await authApi.post('/login', data)
  return response.data
}

// Onboarding Status
export interface OnboardingStatus {
  is_complete: boolean
  user_id: number
  org_name?: string
}

export const getOnboardingStatus = async (): Promise<OnboardingStatus> => {
  const response = await authApi.get('/onboarding/status')
  return response.data
}
