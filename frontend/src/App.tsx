import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { BaseProvider, LightTheme } from 'baseui'
import { Provider as StyletronProvider } from 'styletron-react'
import { Client as Styletron } from 'styletron-engine-monolithic'

import { AuthProvider } from './context/AuthContext'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Jobs } from './pages/Jobs'
import { JobDetail } from './pages/JobDetail'
import { Customers } from './pages/Customers'
import { Mechanics } from './pages/Mechanics'
import { Admin } from './pages/Admin'

const engine = new Styletron()

export default function App() {
  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <AuthProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/jobs/:id" element={<JobDetail />} />
                <Route path="/customers" element={<Customers />} />
                <Route path="/mechanics" element={<Mechanics />} />
                <Route path="/admin" element={<Admin />} />
              </Routes>
            </Layout>
          </Router>
        </AuthProvider>
      </BaseProvider>
    </StyletronProvider>
  )
}
