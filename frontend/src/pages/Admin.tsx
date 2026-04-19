import React, { useState } from 'react'

const AdminContainer = {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
}

const AdminHeader = {
  margin: 0,
  fontSize: '20px',
  fontWeight: '600',
  color: '#1a1a1a',
  marginBottom: '24px',
}

const SectionCard = {
  backgroundColor: '#f8f9fa',
  padding: '16px',
  borderRadius: '8px',
  marginBottom: '16px',
}

const SectionTitle = {
  fontSize: '18px',
  fontWeight: '600',
  marginBottom: '16px',
}

const FormLabel = {
  display: 'block',
  marginBottom: '8px',
  fontWeight: '600',
}

const InputField = {
  width: '100%',
  padding: '12px',
  borderRadius: '8px',
  border: '1px solid #e0e0e0',
  fontSize: '14px',
}

const PrimaryButton = {
  padding: '12px 24px',
  backgroundColor: '#0066cc',
  border: 'none',
  borderRadius: '8px',
  fontSize: '14px',
  cursor: 'pointer',
  color: '#fff',
}

const SecondaryButton = {
  padding: '12px 24px',
  backgroundColor: '#f0f0f0',
  border: '1px solid #ccc',
  borderRadius: '8px',
  fontSize: '14px',
  cursor: 'pointer',
}

const TabsContainer = {
  display: 'flex',
  flexDirection: 'column',
}

const TabListContainer = {
  display: 'flex',
  borderBottom: '1px solid #e0e0e0',
  marginBottom: '16px',
}

const TabItem = ({
  label,
  active,
  onClick,
}: {
  label: string
  active: boolean
  onClick: () => void
}) => (
  <button
    onClick={onClick}
    style={{
      padding: '12px 20px',
      border: 'none',
      borderBottom: active ? '2px solid #0066cc' : '2px solid transparent',
      backgroundColor: 'transparent',
      fontSize: '14px',
      fontWeight: active ? '600' : '400',
      color: active ? '#0066cc' : '#666',
      cursor: 'pointer',
      marginRight: '8px',
    }}
  >
    {label}
  </button>
)

const TabContent = {
  padding: '16px',
}

export function Admin() {
  const [activeTab, setActiveTab] = useState('General')

  return (
    <div style={AdminContainer}>
      <h2 style={AdminHeader}>Settings</h2>

      <TabsContainer>
        <TabListContainer>
          <TabItem label="General" active={activeTab === 'General'} onClick={() => setActiveTab('General')} />
          <TabItem label="Users" active={activeTab === 'Users'} onClick={() => setActiveTab('Users')} />
          <TabItem label="Legal & Compliance" active={activeTab === 'Legal'} onClick={() => setActiveTab('Legal')} />
          <TabItem label="Payroll (TriNet)" active={activeTab === 'Payroll'} onClick={() => setActiveTab('Payroll')} />
          <TabItem label="Federal Reporting" active={activeTab === 'Federal'} onClick={() => setActiveTab('Federal')} />
          <TabItem label="API Configuration" active={activeTab === 'API'} onClick={() => setActiveTab('API')} />
        </TabListContainer>

        <div style={TabContent}>
          {activeTab === 'General' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>General Settings</h3>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Company Name</label>
                <input type="text" defaultValue="SkyMechanics" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Address</label>
                <input type="text" defaultValue="123 Aviation Way, Hangar 7, CA 90001" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>FAA Repair Station Certificate #</label>
                <input type="text" defaultValue="R-12345" style={InputField} />
              </div>
              <button style={PrimaryButton}>Save Changes</button>
            </div>
          )}

          {activeTab === 'Users' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>User Management</h3>
              <button style={{ ...PrimaryButton, marginBottom: '16px' }}>
                Add User
              </button>
              <p style={{ fontSize: '12px', color: '#999999' }}>
                User management interface will be implemented here
              </p>
            </div>
          )}

          {activeTab === 'Legal' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>Legal & Compliance</h3>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Privacy Policy URL</label>
                <input type="text" defaultValue="https://skymechanics.com/privacy" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Terms of Service URL</label>
                <input type="text" defaultValue="https://skymechanics.com/terms" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>FAA Part 145 Compliance Documentation</label>
                <textarea rows={4} defaultValue="Upload your FAA Part 145 certification and compliance documents here." style={{ ...InputField, fontFamily: 'inherit' }} />
              </div>
              <button style={PrimaryButton}>Save Compliance Info</button>
            </div>
          )}

          {activeTab === 'Payroll' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>Payroll Integration (TriNet)</h3>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>TriNet API Key</label>
                <input type="password" defaultValue="sk_test_" style={{ ...InputField, fontFamily: 'monospace' }} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Company ID</label>
                <input type="text" defaultValue="TRI-12345" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px', padding: '16px', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
                <h4 style={{ margin: '0 0 8px 0' }}>Sync Options</h4>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                  <input type="checkbox" defaultChecked /> Sync employee data
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                  <input type="checkbox" defaultChecked /> Sync payroll data
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <input type="checkbox" /> Sync benefits data
                </label>
              </div>
              <button style={PrimaryButton}>Save & Test Connection</button>
            </div>
          )}

          {activeTab === 'Federal' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>Federal Reporting</h3>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>FAA Form 8310-3 Auto-Fill</label>
                <p style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                  Enable automatic generation of FAA Form 8310-3 for new repair station applications
                </p>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <input type="checkbox" defaultChecked /> Enable auto-generation
                </label>
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>FAA Form 8130-3 (Authorized Release Certificate)</label>
                <p style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                  Configure automatic generation of release certificates for completed work
                </p>
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <input type="checkbox" defaultChecked /> Enable auto-generation
                </label>
              </div>
              <button style={PrimaryButton}>Save Federal Reporting Settings</button>
            </div>
          )}

          {activeTab === 'API' && (
            <div style={SectionCard}>
              <h3 style={SectionTitle}>API Configuration</h3>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>API Base URL</label>
                <input type="text" defaultValue="http://localhost:8080" style={InputField} />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={FormLabel}>Stripe API Key (Test)</label>
                <input type="password" defaultValue="sk_test_" style={{ ...InputField, fontFamily: 'monospace' }} />
              </div>
              <button style={PrimaryButton}>Test API Connection</button>
            </div>
          )}
        </div>
      </TabsContainer>
    </div>
  )
}
