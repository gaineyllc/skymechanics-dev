import React, { useState } from 'react'
import { styled } from '../../utils/styled'

export interface ToolConfig {
    tool_id: number
    name: string
    category: string
    part_number?: string
    calibration_required: boolean
    calibration_interval_months?: number
    description?: string
    created_at: string
    updated_at: string
}

interface ToolConfigurationProps {
    tools?: ToolConfig[]
    onToolSelect?: (tool: ToolConfig) => void
    readOnly?: boolean
}

export function ToolConfiguration({ tools = [], onToolSelect, readOnly = false }: ToolConfigurationProps) {
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [selectedTool, setSelectedTool] = useState<ToolConfig | null>(null)
    const [isFormOpen, setIsFormOpen] = useState(false)

    const categories = ['all', 'torque', 'socket', 'wrench', 'specialty', 'measuring', 'cutting']

    const filteredTools = selectedCategory === 'all' 
        ? tools 
        : tools.filter(t => t.category === selectedCategory)

    const handleToolSelect = (tool: ToolConfig) => {
        setSelectedTool(tool)
        if (onToolSelect) {
            onToolSelect(tool)
        }
    }

    return (
        <Container>
            <Header>
                <h3>Tool Configuration</h3>
                <span style={{ fontSize: '12px', color: '#666' }}>
                    {tools.length} tools configured
                </span>
            </Header>

            {/* Category Filter */}
            <CategoryFilter>
                {categories.map(cat => (
                    <CategoryButton
                        key={cat}
                        active={selectedCategory === cat}
                        onClick={() => setSelectedCategory(cat)}
                    >
                        {cat.charAt(0).toUpperCase() + cat.slice(1)}
                    </CategoryButton>
                ))}
            </CategoryFilter>

            {/* Tool List */}
            <ToolList>
                {filteredTools.map(tool => (
                    <ToolItem
                        key={tool.tool_id}
                        tool={tool}
                        isSelected={selectedTool?.tool_id === tool.tool_id}
                        onClick={() => handleToolSelect(tool)}
                        readOnly={readOnly}
                    />
                ))}
                {filteredTools.length === 0 && (
                    <EmptyState>No tools found</EmptyState>
                )}
            </ToolList>

            {/* Tool Details Panel */}
            {selectedTool && (
                <ToolDetailsPanel>
                    <DetailsHeader>
                        <h4>Tool Details</h4>
                        {!readOnly && (
                            <button onClick={() => setIsFormOpen(!isFormOpen)}>
                                {isFormOpen ? 'Close' : 'Edit'}
                            </button>
                        )}
                    </DetailsHeader>

                    {!isFormOpen ? (
                        <DetailsContent>
                            <DetailRow>
                                <DetailLabel>Name</DetailLabel>
                                <DetailValue>{selectedTool.name}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Category</DetailLabel>
                                <DetailValue>{selectedTool.category}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Part Number</DetailLabel>
                                <DetailValue>{selectedTool.part_number || 'N/A'}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Calibration</DetailLabel>
                                <DetailValue>
                                    {selectedTool.calibration_required ? (
                                        <span style={{ color: '#f44336', fontWeight: '500' }}>
                                            Required ({selectedTool.calibration_interval_months} months)
                                        </span>
                                    ) : (
                                        <span style={{ color: '#4CAF50' }}>Not required</span>
                                    )}
                                </DetailValue>
                            </DetailRow>
                            {selectedTool.description && (
                                <DetailRow>
                                    <DetailLabel>Description</DetailLabel>
                                    <DetailValue>{selectedTool.description}</DetailValue>
                                </DetailRow>
                            )}
                        </DetailsContent>
                    ) : (
                        <EditForm>
                            <FormRow>
                                <FormLabel>Name</FormLabel>
                                <input
                                    type="text"
                                    value={selectedTool.name}
                                    onChange={(e) => setSelectedTool({ ...selectedTool, name: e.target.value })}
                                    style={inputStyle}
                                />
                            </FormRow>
                            <FormRow>
                                <FormLabel>Category</FormLabel>
                                <select
                                    value={selectedTool.category}
                                    onChange={(e) => setSelectedTool({ ...selectedTool, category: e.target.value })}
                                    style={inputStyle}
                                >
                                    <option value="torque">Torque</option>
                                    <option value="socket">Socket</option>
                                    <option value="wrench">Wrench</option>
                                    <option value="specialty">Specialty</option>
                                    <option value="measuring">Measuring</option>
                                    <option value="cutting">Cutting</option>
                                </select>
                            </FormRow>
                            <FormRow>
                                <FormLabel>Part Number</FormLabel>
                                <input
                                    type="text"
                                    value={selectedTool.part_number || ''}
                                    onChange={(e) => setSelectedTool({ ...selectedTool, part_number: e.target.value })}
                                    style={inputStyle}
                                />
                            </FormRow>
                            <FormRow>
                                <FormLabel>Calibration Required</FormLabel>
                                <input
                                    type="checkbox"
                                    checked={selectedTool.calibration_required}
                                    onChange={(e) => setSelectedTool({ ...selectedTool, calibration_required: e.target.checked })}
                                />
                            </FormRow>
                            {selectedTool.calibration_required && (
                                <FormRow>
                                    <FormLabel>Calibration Interval (months)</FormLabel>
                                    <input
                                        type="number"
                                        value={selectedTool.calibration_interval_months || 6}
                                        onChange={(e) => setSelectedTool({ ...selectedTool, calibration_interval_months: parseInt(e.target.value) || 6 })}
                                        style={inputStyle}
                                    />
                                </FormRow>
                            )}
                            <FormRow>
                                <FormLabel>Description</FormLabel>
                                <textarea
                                    value={selectedTool.description || ''}
                                    onChange={(e) => setSelectedTool({ ...selectedTool, description: e.target.value })}
                                    style={{ ...inputStyle, minHeight: '60px' }}
                                />
                            </FormRow>
                        </EditForm>
                    )}
                </ToolDetailsPanel>
            )}

            {/* Add Tool Form */}
            {!isFormOpen && !readOnly && (
                <AddToolSection>
                    <button onClick={() => setIsFormOpen(true)}>+ Add New Tool</button>
                </AddToolSection>
            )}

            {isFormOpen && !readOnly && (
                <AddToolForm>
                    <h4>Add New Tool</h4>
                    <FormRow>
                        <FormLabel>Name</FormLabel>
                        <input type="text" style={inputStyle} />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Category</FormLabel>
                        <select style={inputStyle}>
                            <option value="torque">Torque</option>
                            <option value="socket">Socket</option>
                            <option value="wrench">Wrench</option>
                            <option value="specialty">Specialty</option>
                            <option value="measuring">Measuring</option>
                            <option value="cutting">Cutting</option>
                        </select>
                    </FormRow>
                    <FormRow>
                        <FormLabel>Part Number</FormLabel>
                        <input type="text" style={inputStyle} />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Calibration Required</FormLabel>
                        <input type="checkbox" />
                    </FormRow>
                    <FormButtons>
                        <button onClick={() => setIsFormOpen(false)}>Cancel</button>
                        <button style={{ backgroundColor: '#007AFF', color: '#fff' }}>Save Tool</button>
                    </FormButtons>
                </AddToolForm>
            )}
        </Container>
    )
}

// ========== Components ==========

function ToolItem({ tool, isSelected, onClick, readOnly }: { tool: ToolConfig, isSelected: boolean, onClick: () => void, readOnly?: boolean }) {
    return (
        <ToolItemWrapper
            isSelected={isSelected}
            onClick={onClick}
            style={{ cursor: readOnly ? 'default' : 'pointer' }}
        >
            <ToolInfo>
                <ToolName>{tool.name}</ToolName>
                <ToolMeta>
                    <span>{tool.category}</span>
                    {tool.calibration_required && (
                        <span style={{ color: '#f44336', fontSize: '10px' }}>
                            Calib: {tool.calibration_interval_months}mo
                        </span>
                    )}
                </ToolMeta>
            </ToolInfo>
            <ToolActions>
                {tool.part_number && (
                    <span style={{ fontSize: '10px', color: '#999' }}>
                        {tool.part_number}
                    </span>
                )}
            </ToolActions>
        </ToolItemWrapper>
    )
}

// ========== Styled Components ==========

const Container = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '20px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
})

const Header = styled('div', {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottom: '1px solid #eee',
    paddingBottom: '12px',
})

const CategoryFilter = styled('div', {
    display: 'flex',
    gap: '4px',
    flexWrap: 'wrap',
})

const CategoryButton = styled('button', ({ active }: { active: boolean }) => ({
    padding: '6px 12px',
    borderRadius: '20px',
    border: active ? '1px solid #007AFF' : '1px solid #e0e0e0',
    backgroundColor: active ? '#007AFF' : '#fff',
    color: active ? '#fff' : '#333',
    fontSize: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    '&:hover': {
        opacity: 0.9,
    },
}))

const ToolList = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    maxHeight: '300px',
    overflowY: 'auto',
})

const ToolItemWrapper = styled('div', ({ isSelected }: { isSelected: boolean }) => ({
    padding: '12px',
    backgroundColor: isSelected ? '#e3f2fd' : '#f8f9fa',
    borderRadius: '8px',
    border: isSelected ? '1px solid #007AFF' : '1px solid #e0e0e0',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
}))

const ToolInfo = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
})

const ToolName = styled('span', {
    fontWeight: '500',
    fontSize: '13px',
})

const ToolMeta = styled('span', {
    fontSize: '11px',
    color: '#666',
    display: 'flex',
    gap: '8px',
})

const ToolActions = styled('div', {
    display: 'flex',
    gap: '8px',
})

const ToolDetailsPanel = styled('div', {
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    padding: '16px',
    border: '1px solid #e0e0e0',
})

const DetailsHeader = styled('div', {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
})

const DetailsContent = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
})

const DetailRow = styled('div', {
    display: 'flex',
    gap: '8px',
    padding: '8px',
    backgroundColor: '#fff',
    borderRadius: '6px',
})

const DetailLabel = styled('span', {
    fontWeight: '500',
    fontSize: '12px',
    color: '#666',
    minWidth: '100px',
})

const DetailValue = styled('span', {
    fontSize: '13px',
    color: '#333',
})

const EditForm = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
})

const AddToolSection = styled('div', {
    display: 'flex',
    justifyContent: 'center',
    padding: '12px',
})

const AddToolForm = styled('div', {
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    padding: '16px',
    border: '1px solid #e0e0e0',
})

const FormRow = styled('div', {
    display: 'flex',
    gap: '8px',
    alignItems: 'center',
})

const FormLabel = styled('span', {
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
    minWidth: '120px',
})

const inputStyle = {
    padding: '8px 12px',
    borderRadius: '4px',
    border: '1px solid #e0e0e0',
    fontSize: '13px',
    flex: 1,
}

const FormButtons = styled('div', {
    display: 'flex',
    gap: '8px',
    justifyContent: 'flex-end',
    marginTop: '8px',
})

const EmptyState = styled('div', {
    color: '#999',
    padding: '20px',
    textAlign: 'center',
    fontStyle: 'italic',
})
