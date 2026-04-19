import React, { useState } from 'react'
import { Modal, ModalHeader, ModalBody, ModalFooter, Button, KIND, SIZE, TextInput } from 'baseui'
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
    <Modal isOpen={isOpen} onClose={onClose} closeable>
      <ModalHeader>Create New Customer</ModalHeader>
      <ModalBody>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Name
            </label>
            <TextInput
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              placeholder="e.g., John Smith"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Email
            </label>
            <TextInput
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              placeholder="john@example.com"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Phone
            </label>
            <TextInput
              value={formData.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="(555) 123-4567"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Address
            </label>
            <TextInput
              value={formData.address}
              onChange={(e) => handleChange('address', e.target.value)}
              placeholder="123 Aviation Way, Hangar 7"
              size="compact"
              multiline
              minRows={2}
            />
          </div>
        </div>
      </ModalBody>
      <ModalFooter>
        <Button kind={KIND.tertiary} onClick={onClose}>
          Cancel
        </Button>
        <Button kind={KIND.primary} onClick={handleSubmit}>
          Create Customer
        </Button>
      </ModalFooter>
    </Modal>
  )
}
