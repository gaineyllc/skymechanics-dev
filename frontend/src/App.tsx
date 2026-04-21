import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { BaseProvider, LightTheme } from 'baseui'
import { Provider as StyletronProvider } from 'styletron-react'
import { Client as Styletron } from 'styletron-engine-atomic'

import { AuthProvider, useAuth } from './context/AuthContext'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Jobs } from './pages/Jobs'
import { JobDetail } from './pages/JobDetail'
import { WorkflowBuilder } from './components/WorkflowBuilder'
import { Customers } from './pages/Customers'
import { Mechanics } from './pages/Mechanics'
import Onboarding from './pages/Onboarding'
import OnboardingSuccess from './pages/OnboardingSuccess'
import QuickStartWizard from './components/QuickStartWizard'
import { Admin } from './pages/Admin'
import Login from './pages/Login'

const engine = new Styletron()

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return <div>Loading...</div>
  }
  
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <AuthProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Onboarding />} />
                <Route path="/onboarding-success" element={<OnboardingSuccess />} />
                <Route path="/quick-start" element={<QuickStartWizard />} />
                <Route
                  path="/dashboard"
                  element={
                    <PrivateRoute>
                      <Dashboard />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/jobs"
                  element={
                    <PrivateRoute>
                      <Jobs />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/jobs/:id"
                  element={
                    <PrivateRoute>
                      <JobDetail />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/workflow"
                  element={
                    <PrivateRoute>
                      <WorkflowBuilder readOnly={true} />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/workflow/edit"
                  element={
                    <PrivateRoute>
                      <WorkflowBuilder readOnly={false} />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/customers"
                  element={
                    <PrivateRoute>
                      <Customers />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/mechanics"
                  element={
                    <PrivateRoute>
                      <Mechanics />
                    </PrivateRoute>
                  }
                />
                <Route
                  path="/admin"
                  element={
                    <PrivateRoute>
                      <Admin />
                    </PrivateRoute>
                  }
                />
              </Routes>
            </Layout>
          </Router>
        </AuthProvider>
      </BaseProvider>
    </StyletronProvider>
  )
}
