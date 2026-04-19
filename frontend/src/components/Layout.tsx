import React from 'react'
import { useLocation, Link } from 'react-router-dom'
import { styled } from 'baseui'
import { 
  Grid, 
  GridItem, 
  Block, 
  Drawer, 
  Button, 
  KIND, 
  SIZE, 
  Disclosure, 
  ChevronDown, 
  ChevronUp 
} from 'baseui'

const SidebarContainer = styled('div', {
  backgroundColor: '#1a1a1a',
  height: '100vh',
  padding: '20px',
  position: 'fixed',
  left: 0,
  top: 0,
  width: '250px',
  overflowY: 'auto',
})

const SidebarItem = styled(Link, {
  display: 'flex',
  alignItems: 'center',
  padding: '12px 16px',
  textDecoration: 'none',
  color: '#ffffff',
  borderRadius: '8px',
  marginBottom: '8px',
  transition: 'background-color 0.2s',

  '&:hover': {
    backgroundColor: '#333333',
  },
})

const ActiveItem = styled(SidebarItem, {
  backgroundColor: '#007AFF',
})

const ContentContainer = styled('div', {
  marginLeft: '270px',
  padding: '20px',
  minHeight: '100vh',
})

export function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const [isExpanded, setIsExpanded] = React.useState(false)

  const navItems = [
    { path: '/', label: 'Dashboard' },
    { path: '/jobs', label: 'Jobs' },
    { path: '/customers', label: 'Customers' },
    { path: '/mechanics', label: 'Mechanics' },
  ]

  const adminItems = [
    { path: '/admin', label: 'Settings' },
  ]

  return (
    <Grid>
      <GridItem span={2}>
        <SidebarContainer>
          <Block marginBottom="24px">
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Block fontSize="24px" fontWeight="bold" color="#ffffff">
                SkyMechanics
              </Block>
              <Block fontSize="12px" color="#999999">
                Aircraft Maintenance
              </Block>
            </Link>
          </Block>

          <Block marginBottom="16px">
            <Block fontSize="14px" fontWeight="bold" color="#999999" marginBottom="8px">
              MAIN NAVIGATION
            </Block>
            {navItems.map((item) => {
              const isActive = location.pathname === item.path
              return isActive ? (
                <ActiveItem key={item.path} to={item.path}>
                  {item.label}
                </ActiveItem>
              ) : (
                <SidebarItem key={item.path} to={item.path}>
                  {item.label}
                </SidebarItem>
              )
            })}
          </Block>

          <Block>
            <Block fontSize="14px" fontWeight="bold" color="#999999" marginBottom="8px">
              ADMINISTRATION
            </Block>
            {adminItems.map((item) => {
              const isActive = location.pathname === item.path
              return isActive ? (
                <ActiveItem key={item.path} to={item.path}>
                  {item.label}
                </ActiveItem>
              ) : (
                <SidebarItem key={item.path} to={item.path}>
                  {item.label}
                </SidebarItem>
              )
            })}
          </Block>

          <Block marginTop="auto">
            <Button
              kind={KIND.secondary}
              size={SIZE.compact}
              onClick={() => setIsExpanded(!isExpanded)}
              endEnhancer={() => isExpanded ? <ChevronUp /> : <ChevronDown />}
              fullWidth
            >
              More Options
            </Button>
            {isExpanded && (
              <Disclosure
                isOpen={true}
                heading="Additional Options"
                overrides={{
                  Body: { style: { marginTop: '8px' } },
                }}
              >
                <Block paddingLeft="16px">
                  <SidebarItem to="/settings">Settings</SidebarItem>
                  <SidebarItem to="/legal">Legal & Compliance</SidebarItem>
                  <SidebarItem to="/payroll">Payroll (TriNet)</SidebarItem>
                  <SidebarItem to="/reporting">Federal Reporting</SidebarItem>
                </Block>
              </Disclosure>
            )}
          </Block>
        </SidebarContainer>
      </GridItem>
      <GridItem span={10}>
        <ContentContainer>{children}</ContentContainer>
      </GridItem>
    </Grid>
  )
}
