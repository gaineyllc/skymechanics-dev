import React, { useState } from 'react'
import { Modal, ModalHeader, ModalBody, ModalFooter, Button, KIND, SIZE, TextInput } from 'baseui'
import { createJob, Job } from '../services/api'

interface CreateJobModalProps {
  isOpen: boolean
  onClose: () => void
  onSuccess: (job: Job) => void
}

export function CreateJobModal({ isOpen, onClose, onSuccess }: CreateJobModalProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pending',
    priority: 'medium',
    customer_id: 0,
  })

  const handleSubmit = async () => {
    try {
      const created = await createJob(formData)
      onSuccess(created)
      onClose()
    } catch (err) {
      console.error('Failed to create job:', err)
    }
  }

  const handleChange = (field: keyof Job['properties'], value: string | number) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} closeable>
      <ModalHeader>Create New Job</ModalHeader>
      <ModalBody>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Job Title
            </label>
            <TextInput
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="e.g., Engine Repair"
              size="compact"
            />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Description
            </label>
            <TextInput
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Enter job details"
              size="compact"
              multiline
              minRows={3}
            />
          </div>

          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px',
                  borderRadius: '4px',
                  border: '1px solid #e0e0e0',
                }}
              >
                <option value="pending">Pending</option>
                <option value="open">Open</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
                Priority
              </label>
              <select
                value={formData.priority}
                onChange={(e) => handleChange('priority', e.target.value)}
                style={{
                  width: '100%',
                  padding: '8px',
                  borderRadius: '4px',
                  border: '1px solid #e0e0e0',
                }}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
              Customer ID
            </label>
            <TextInput
              type="number"
              value={formData.customer_id}
              onChange={(e) => handleChange('customer_id', Number(e.target.value))}
              placeholder="Enter customer node ID"
              size="compact"
            />
          </div>
        </div>
      </ModalBody>
      <ModalFooter>
        <Button kind={KIND.tertiary} onClick={onClose}>
          Cancel
        </Button>
        <Button kind={KIND.primary} onClick={handleSubmit}>
          Create Job
        </Button>
      </ModalFooter>
    </Modal>
  )
}
