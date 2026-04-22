import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registerMechanic } from '../../services/authApi'
import { Card, Form, Button, Alert, Container, Row, Col, FormCheck } from 'react-bootstrap'

export default function MechanicRegister() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    license: '',
    specialties: [] as string[],
  })
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const specialtyOptions = [
    'Engine',
    'Airframe',
    'Powerplant',
    'Avionics',
    'Structures',
    'Hydraulics',
    'Electrical',
    'Mechanical',
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    
    if (name === 'specialties') {
      const selected = Array.from(value.split(',').map(s => s.trim()).filter(s => s))
      setFormData({ ...formData, specialties: selected })
    } else {
      setFormData({ ...formData, [name]: value })
    }
    setError(null)
  }

  const toggleSpecialty = (specialty: string) => {
    const current = formData.specialties
    const exists = current.includes(specialty)
    setFormData({
      ...formData,
      specialties: exists 
        ? current.filter(s => s !== specialty)
        : [...current, specialty]
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Validate minimum password length
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }

    // Validate license
    if (!formData.license.trim()) {
      setError('FAA license number is required')
      return
    }

    // Validate at least one specialty
    if (formData.specialties.length === 0) {
      setError('Select at least one specialty')
      return
    }

    try {
      setLoading(true)
      const response = await registerMechanic({
        email: formData.email,
        password: formData.password,
        first_name: formData.firstName,
        last_name: formData.lastName,
        license: formData.license,
        specialties: formData.specialties,
      })

      console.log('Mechanic registered:', response)
      navigate('/onboarding-success', { 
        state: { 
          message: 'Mechanic account created successfully',
          email: formData.email,
          license: formData.license
        }
      })
    } catch (err: any) {
      console.error('Registration error:', err)
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Container className="mt-5">
      <Row className="justify-content-center">
        <Col md={7}>
          <Card>
            <Card.Body>
              <h2 className="text-center mb-4">Register Mechanic Account</h2>
              <p className="text-center text-muted mb-4">
                Create your mechanic profile with FAA license and specialties
              </p>

              {error && <Alert variant="danger">{error}</Alert>}

              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Email Address</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Create a password (min 8 characters)"
                    minLength={8}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Confirm Password</Form.Label>
                  <Form.Control
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Confirm your password"
                    required
                  />
                </Form.Group>

                <Row className="mb-3">
                  <Col>
                    <Form.Group>
                      <Form.Label>First Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="firstName"
                        value={formData.firstName}
                        onChange={handleChange}
                        placeholder="First name"
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col>
                    <Form.Group>
                      <Form.Label>Last Name</Form.Label>
                      <Form.Control
                        type="text"
                        name="lastName"
                        value={formData.lastName}
                        onChange={handleChange}
                        placeholder="Last name"
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <Form.Group className="mb-3">
                  <Form.Label>FAA License Number</Form.Label>
                  <Form.Control
                    type="text"
                    name="license"
                    value={formData.license}
                    onChange={handleChange}
                    placeholder="e.g., FA-12345"
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>Specialties</Form.Label>
                  <div className="d-flex flex-wrap gap-2">
                    {specialtyOptions.map((specialty) => (
                      <FormCheck
                        key={specialty}
                        label={specialty}
                        type="checkbox"
                        id={`specialty-${specialty}`}
                        checked={formData.specialties.includes(specialty)}
                        onChange={() => toggleSpecialty(specialty)}
                      />
                    ))}
                  </div>
                  <Form.Text className="text-muted">
                    Select all specialties that apply to your qualifications
                  </Form.Text>
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100" disabled={loading}>
                  {loading ? 'Creating Account...' : 'Create Mechanic Account'}
                </Button>
              </Form>

              <div className="text-center mt-3">
                <p className="mb-0">
                  Already have an account?{' '}
                  <a href="/login">Log In</a>
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}
