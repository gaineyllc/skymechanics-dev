import React, { useState } from 'react'
import { Button } from 'baseui/button'
import { Modal } from 'baseui/modal'
import { Input } from 'baseui/input'
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
      <h3 style={{ margin: 0, fontSize: '20px' }}>Create New Job</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '16px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Job Title
          </label>
          <Input
            value={formData.title}
            onChange={(e) => handleChange('title', (e.target as HTMLInputElement).value)}
            placeholder="e.g., Engine Repair"
            size="compact"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '600' }}>
            Description
          </label>
          <Input
            value={formData.description}
            onChange={(e) => handleChange('description', (e.target as HTMLInputElement).value)}
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
              onChange={(e) => handleChange('status', (e.target as HTMLInputElement).value)}
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
              onChange={(e) => handleChange('priority', (e.target as HTMLInputElement).value)}
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
          <Input
            type="number"
            value={formData.customer_id}
            onChange={(e) => handleChange('customer_id', Number((e.target as HTMLInputElement).value))}
            placeholder="Enter customer node ID"
            size="compact"
          />
        </div>
      </div>
      <div>
        <Button kind="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button kind="primary" onClick={handleSubmit} style={{ marginLeft: '8px' }}>
          Create Job
        </Button>
      </div>
    </Modal>
  )
}
