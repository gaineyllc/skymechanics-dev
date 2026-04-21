import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { styled } from '../utils/styled'
import { fetchCustomers, createCustomer, Customer } from '../services/api'
import { CreateCustomerModal } from '../components/CreateCustomerModal'

const CustomersContainer = styled('div', {
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const CustomersHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '24px',
})

const CustomersTitle = styled('h2', {
  margin: 0,
  fontSize: '20px',
  fontWeight: '600',
  color: '#1a1a1a',
})

const CustomerCard = styled('div', {
  backgroundColor: '#f8f9fa',
  padding: '16px',
  borderRadius: '8px',
  marginBottom: '12px',
  border: '1px solid #e0e0e0',
})

const CustomerName = styled('div', {
  fontWeight: '600',
  fontSize: '16px',
  marginBottom: '8px',
})

const CustomerContact = styled('div', {
  fontSize: '14px',
  color: '#333333',
})

const CustomerAddress = styled('div', {
  fontSize: '12px',
  color: '#666666',
  marginTop: '8px',
})

const Button = ({ kind = 'primary', onClick, children, disabled = false }: any) => {
  const baseStyles = {
    padding: '8px 16px',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontWeight: '500',
    fontSize: '14px',
    transition: 'all 0.2s',
  }

  const kinds = {
    primary: {
      backgroundColor: '#007AFF',
      color: '#ffffff',
      '&:hover': { backgroundColor: '#005ecb' },
    },
    secondary: {
      backgroundColor: '#f0f0f0',
      color: '#333333',
      '&:hover': { backgroundColor: '#e0e0e0' },
    },
    tertiary: {
      backgroundColor: 'transparent',
      color: '#666666',
      '&:hover': { backgroundColor: '#f0f0f0' },
    },
    negative: {
      backgroundColor: '#ff4d4d',
      color: '#ffffff',
      '&:hover': { backgroundColor: '#cc0000' },
    },
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        ...baseStyles,
        ...kinds[kind as keyof typeof kinds],
        ...(disabled ? { opacity: 0.5, cursor: 'not-allowed' } : {}),
      }}
    >
      {children}
    </button>
  )
}

const KIND = {
  primary: 'primary',
  secondary: 'secondary',
  tertiary: 'tertiary',
  negative: 'negative',
}

const Notification = ({ onClose, kind, title, subtitle, autoHide, autoHideDuration }: any) => {
  if (autoHide) {
    useEffect(() => {
      const timer = setTimeout(() => {
        onClose && onClose()
      }, autoHideDuration || 3000)
      return () => clearTimeout(timer)
    }, [])
  }

  const kinds = {
    negative: { backgroundColor: '#ffe5e5', color: '#d00' },
    warning: { backgroundColor: '#fff3e0', color: '#f57c00' },
    positive: { backgroundColor: '#e8f5e9', color: '#2e7d32' },
    info: { backgroundColor: '#e3f2fd', color: '#1565c0' },
  }

  return (
    <div
      style={{
        padding: '16px',
        borderRadius: '8px',
        marginBottom: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        ...kinds[kind as keyof typeof kinds],
      }}
    >
      <div>
        <div style={{ fontWeight: '600' }}>{title}</div>
        {subtitle && <div style={{ fontSize: '14px' }}>{subtitle}</div>}
      </div>
      <button
        onClick={onClose}
        style={{
          background: 'none',
          border: 'none',
          fontSize: '20px',
          cursor: 'pointer',
          color: 'inherit',
        }}
      >
        ×
      </button>
    </div>
  )
}

export function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        const data = await fetchCustomers()
        setCustomers(Array.isArray(data) ? data : [data])
      } catch (err) {
        setError('Failed to load customers')
      } finally {
        setLoading(false)
      }
    }
    loadCustomers()
  }, [])

  const handleCreateCustomer = async () => {
    setIsModalOpen(true)
  }

  if (loading) {
    return (
      <CustomersContainer>
        <CustomersHeader>
          <CustomersTitle>Customers</CustomersTitle>
          <Button kind={KIND.primary} onClick={handleCreateCustomer}>
            New Customer
          </Button>
        </CustomersHeader>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ fontSize: '48px', marginBottom: '16px' }}>⏳</div>
          <p>Loading customers...</p>
        </div>
      </CustomersContainer>
    )
  }

  return (
    <CustomersContainer>
      <CustomersHeader>
        <CustomersTitle>Customers ({customers.length})</CustomersTitle>
        <Button kind={KIND.primary} onClick={handleCreateCustomer}>
          New Customer
        </Button>
      </CustomersHeader>

      {error && (
        <Notification
          onClose={() => setError(null)}
          kind="negative"
          title="Error"
          subtitle={error}
          autoHide
          autoHideDuration={3000}
        />
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {customers.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>
            No customers yet. Create one to get started.
          </p>
        ) : (
          customers.map((customer) => (
            <div key={customer.node_id}>
              <CustomerCard>
                <CustomerName>{customer.properties.name}</CustomerName>
                <CustomerContact>
                  {customer.properties.email && <div>{customer.properties.email}</div>}
                  {customer.properties.phone && <div>{customer.properties.phone}</div>}
                </CustomerContact>
                {customer.properties.address && (
                  <CustomerAddress>{customer.properties.address}</CustomerAddress>
                )}
              </CustomerCard>
            </div>
          ))
        )}
      </div>

      <CreateCustomerModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={(customer) => setCustomers((prev) => [...prev, customer])}
      />
    </CustomersContainer>
  )
}
