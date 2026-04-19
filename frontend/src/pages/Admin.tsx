import React from 'react'
import { styled } from 'baseui'
import { Card, styled as baseStyled, Button, KIND, SIZE, Tab, TabList, TabPanel, Tabs } from 'baseui'

const AdminContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const AdminHeader = styled('h2', {
  margin: 0,
  fontSize: '20px',
  fontWeight: '600',
  color: '#1a1a1a',
  marginBottom: '24px',
})

export function Admin() {
  return (
    <AdminContainer>
      <AdminHeader>Settings</AdminHeader>

      <Tabs>
        <TabList>
          <Tab>General</Tab>
          <Tab>Users</Tab>
          <Tab>Legal & Compliance</Tab>
          <Tab>Payroll (TriNet)</Tab>
          <Tab>Federal Reporting</Tab>
          <Tab>API Configuration</Tab>
        </TabList>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>General Settings</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Company Name
              </label>
              <input
                type="text"
                defaultValue="SkyMechanics"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Address
              </label>
              <input
                type="text"
                defaultValue="123 Aviation Way, Hangar 7, CA 90001"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                FAA Repair Station Certificate #
              </label>
              <input
                type="text"
                defaultValue="R-12345"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <Button kind={KIND.primary}>Save Changes</Button>
          </Card>
        </TabPanel>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>User Management</h3>
            <Button kind={KIND.primary} size={SIZE.compact} style={{ marginBottom: '16px' }}>
              Add User
            </Button>
            <div style={{ fontSize: '12px', color: '#999999' }}>
              User management interface will be implemented here
            </div>
          </Card>
        </TabPanel>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>Legal & Compliance</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Privacy Policy URL
              </label>
              <input
                type="text"
                defaultValue="https://skymechanics.com/privacy"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Terms of Service URL
              </label>
              <input
                type="text"
                defaultValue="https://skymechanics.com/terms"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                FAA Part 145 Compliance Documentation
              </label>
              <textarea
                rows={4}
                defaultValue="Upload your FAA Part 145 certification and compliance documents here."
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <Button kind={KIND.primary}>Save Compliance Info</Button>
          </Card>
        </TabPanel>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>Payroll Integration (TriNet)</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                TriNet API Key
              </label>
              <input
                type="password"
                defaultValue="sk_test_"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                  fontFamily: 'monospace',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Company ID
              </label>
              <input
                type="text"
                defaultValue="TRI-12345"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px', padding: '16px', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
              <h4 style={{ margin: '0 0 8px 0' }}>Sync Options</h4>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <input type="checkbox" defaultChecked />
                Sync employee data
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <input type="checkbox" defaultChecked />
                Sync payroll data
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" />
                Sync benefits data
              </label>
            </div>
            <Button kind={KIND.primary}>Save & Test Connection</Button>
          </Card>
        </TabPanel>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>Federal Reporting</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                FAA Form 8310-3 Auto-Fill
              </label>
              <p style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                Enable automatic generation of FAA Form 8310-3 for new repair station applications
              </p>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" defaultChecked />
                Enable auto-generation
              </label>
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                FAA Form 8130-3 (Authorized Release Certificate)
              </label>
              <p style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                Configure automatic generation of release certificates for completed work
              </p>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input type="checkbox" defaultChecked />
                Enable auto-generation
              </label>
            </div>
            <Button kind={KIND.primary}>Save Federal Reporting Settings</Button>
          </Card>
        </TabPanel>

        <TabPanel>
          <Card>
            <h3 style={{ marginBottom: '16px' }}>API Configuration</h3>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                API Base URL
              </label>
              <input
                type="text"
                defaultValue="http://localhost:8080"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Stripe API Key (Test)
              </label>
              <input
                type="password"
                defaultValue="sk_test_"
                style={{
                  width: '100%',
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  fontSize: '14px',
                  fontFamily: 'monospace',
                }}
              />
            </div>
            <Button kind={KIND.primary}>Test API Connection</Button>
          </Card>
        </TabPanel>
      </Tabs>
    </AdminContainer>
  )
}
