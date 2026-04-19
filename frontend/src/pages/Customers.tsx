import React, { useState, useEffect } from 'react'
import { styled } from 'baseui'
import { Card, Button, KIND, SIZE, Spinner, Notification, TYPE } from 'baseui'
import { Link } from 'react-router-dom'
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
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
})

const CustomerHeader = styled('div', {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '12px',
})

const CustomerName = styled('div', {
  fontWeight: '600',
  fontSize: '16px',
})

const CustomerActions = styled('div', {
  display: 'flex',
  gap: '8px',
})

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
          <Button kind={KIND.primary} size={SIZE.compact} onClick={handleCreateCustomer}>
            Add Customer
          </Button>
        </CustomersHeader>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spinner size={48} />
          <p>Loading customers...</p>
        </div>
      </CustomersContainer>
    )
  }

  return (
    <CustomersContainer>
      <CustomersHeader>
        <CustomersTitle>Customers ({customers.length})</CustomersTitle>
        <Button kind={KIND.primary} size={SIZE.compact} onClick={handleCreateCustomer}>
          Add Customer
        </Button>
      </CustomersHeader>

      {error && (
        <Notification
          onClose={() => setError(null)}
          kind={TYPE.negative}
          title="Error"
          subtitle={error}
          autoHide
          autoHideDuration={3000}
        />
      )}

      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {customers.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666' }}>No customers yet. Add one to get started.</p>
        ) : (
          customers.map((customer) => (
            <CustomerCard key={customer.node_id}>
              <CustomerHeader>
                <CustomerName>{customer.properties.name}</CustomerName>
                <CustomerActions>
                  <Button kind="secondary" size={SIZE.compact}>View</Button>
                  <Button kind="secondary" size={SIZE.compact}>Edit</Button>
                </CustomerActions>
              </CustomerHeader>
              <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                {customer.properties.email}
              </div>
              <div style={{ fontSize: '14px', color: '#666666', marginBottom: '8px' }}>
                {customer.properties.phone}
              </div>
              <div style={{ fontSize: '14px', color: '#666666' }}>
                Address: {customer.properties.address}
              </div>
            </CustomerCard>
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
