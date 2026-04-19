import React, { useState } from 'react'
import { Button } from 'baseui/button'
import { Modal } from 'baseui/modal'
import { Input } from 'baseui/input'
import { createCustomer, Customer } from '../services/api'

interface CreateCustomerModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (customer: Customer) => void
}

export function CreateCustomerModal({ isOpen, onClose, onSuccess }: CreateCustomerModalProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
  })

  const handleSubmit = async () => {
    try {
      const created = await createCustomer(formData)
      onSuccess(created)
      onClose()
    } catch (err) {
      console.error('Failed to create customer:', err)
    }
  }

  const handleChange = (field: keyof Customer['properties'], value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      closeable
      size="modalSizeSmall"
      overrides={{
        Body: {
          style: {
            padding: '24px',
          },
        },
        Header: {
          style: {
            padding: '16px 24px',
            borderBottom: '1px solid #eee',
          },
        },
        Footer: {
          style: {
            padding: '16px 24px',
            borderTop: '1px solid #eee',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '8px',
          },
        },
        Overlay: {
          style: {
            backgroundColor: 'rgba(0,0,0,0.5)',
          },
        },
      }}
    >
      <h3 style={{ margin: 0, fontSize: '20px' }}>Create New Customer</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Name
          </label>
          <Input
            value={formData.name}
            onChange={(e) => handleChange('name', (e.target as HTMLInputElement).value)}
            placeholder="e.g., John Smith"
            size="compact"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Email
          </label>
          <Input
            value={formData.email}
            onChange={(e) => handleChange('email', (e.target as HTMLInputElement).value)}
            placeholder="john@example.com"
            size="compact"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Phone
          </label>
          <Input
            value={formData.phone}
            onChange={(e) => handleChange('phone', (e.target as HTMLInputElement).value)}
            placeholder="(555) 123-4567"
            size="compact"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Address
          </label>
          <Input
            value={formData.address}
            onChange={(e) => handleChange('address', (e.target as HTMLInputElement).value)}
            placeholder="123 Aviation Way, Hangar 7"
            size="compact"
            multiline
            minRows={2}
          />
        </div>
      </div>
      <div>
        <Button kind="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button kind="primary" onClick={handleSubmit} style={{ marginLeft: '8px' }}>
          Create Customer
        </Button>
      </div>
    </Modal>
  )
}
