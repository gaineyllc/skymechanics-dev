import React from 'react'
import { useLocation, Link } from 'react-router-dom'
import { styled } from 'baseui'
import { ChevronDown, ChevronUp } from 'baseui/icon'

const SidebarContainer = styled('div', {
  backgroundColor: '#1a1a1a',
  height: '100vh',
  padding: '20px',
  position: 'fixed',
  left: 0,
  top: 0,
  width: '250px',
  overflowY: 'auto',
}, ({ $layoutTestId }) => ($layoutTestId ? { 'data-testid': $layoutTestId } : {}))

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

const Header = styled('div', {
  marginBottom: '24px',
})

const NavGroup = styled('div', {
  marginBottom: '16px',
})

const NavLabel = styled('div', {
  fontSize: '14px',
  fontWeight: 'bold',
  color: '#999999',
  marginBottom: '8px',
})

const DisclosureContainer = styled('div', {
  marginTop: 'auto',
})

const DisclosureHeader = styled('div', {
  marginBottom: '8px',
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

  const additionalItems = [
    { path: '/settings', label: 'Settings' },
    { path: '/legal', label: 'Legal & Compliance' },
    { path: '/payroll', label: 'Payroll (TriNet)' },
    { path: '/reporting', label: 'Federal Reporting' },
  ]

  return (
    <div>
      <SidebarContainer>
        <Header>
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }} data-testid="brand-link">
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ffffff' }}>
              SkyMechanics
            </div>
            <div style={{ fontSize: '12px', color: '#999999' }}>
              Aircraft Maintenance
            </div>
          </Link>
        </Header>

        <NavGroup data-testid="main-nav">
          <NavLabel>MAIN NAVIGATION</NavLabel>
          {navItems.map((item) => (
            <MenuItem
              key={item.path}
              item={item}
              isActive={location.pathname === item.path}
            />
          ))}
        </NavGroup>

        <NavGroup data-testid="admin-nav">
          <NavLabel>ADMINISTRATION</NavLabel>
          {adminItems.map((item) => (
            <MenuItem
              key={item.path}
              item={item}
              isActive={location.pathname === item.path}
            />
          ))}
        </NavGroup>

        <DisclosureContainer>
          <DisclosureHeader>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              style={{
                width: '100%',
                padding: '8px 12px',
                background: 'transparent',
                border: '1px solid #555',
                borderRadius: '4px',
                color: '#fff',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
              }}
            >
              More Options
              {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            </button>
          </DisclosureHeader>
          {isExpanded && (
            <div style={{ paddingLeft: '16px', marginTop: '8px' }}>
              {additionalItems.map((item) => (
                <SidebarItem key={item.path} to={item.path}>
                  {item.label}
                </SidebarItem>
              ))}
            </div>
          )}
        </DisclosureContainer>
      </SidebarContainer>
      <ContentContainer>{children}</ContentContainer>
    </div>
  )
}

function MenuItem({ item, isActive }: { item: { path: string; label: string }; isActive: boolean }) {
  return isActive ? (
    <ActiveItem key={item.path} to={item.path}>
      {item.label}
    </ActiveItem>
  ) : (
    <SidebarItem key={item.path} to={item.path}>
      {item.label}
    </SidebarItem>
  )
}
