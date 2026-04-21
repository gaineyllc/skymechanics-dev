import React, { useState } from 'react'
import { styled } from '../../utils/styled'

export interface PartConfig {
    part_id: number
    part_number: string
    name: string
    category: string
    aircraft_compatible: string[]
    oem_source?: string
    description?: string
    created_at: string
    updated_at: string
}

interface PartsCatalogProps {
    parts?: PartConfig[]
    onPartSelect?: (part: PartConfig) => void
    readOnly?: boolean
}

export function PartsCatalog({ parts = [], onPartSelect, readOnly = false }: PartsCatalogProps) {
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [selectedPart, setSelectedPart] = useState<PartConfig | null>(null)
    const [isFormOpen, setIsFormOpen] = useState(false)

    const categories = ['all', 'structural', 'engine', 'avionics', 'tools', 'consumables']

    const filteredParts = selectedCategory === 'all'
        ? parts
        : parts.filter(p => p.category === selectedCategory)

    const handlePartSelect = (part: PartConfig) => {
        setSelectedPart(part)
        if (onPartSelect) {
            onPartSelect(part)
        }
    }

    return (
        <Container>
            <Header>
                <h3>Parts Catalog</h3>
                <span style={{ fontSize: '12px', color: '#666' }}>
                    {parts.length} parts available
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

            {/* Search */}
            <SearchBar>
                <input
                    type="text"
                    placeholder="Search parts by name or part number..."
                    style={{
                        width: '100%',
                        padding: '10px 12px',
                        borderRadius: '6px',
                        border: '1px solid #e0e0e0',
                        fontSize: '13px'
                    }}
                />
            </SearchBar>

            {/* Parts List */}
            <PartList>
                {filteredParts.map(part => (
                    <PartItem
                        key={part.part_id}
                        part={part}
                        isSelected={selectedPart?.part_id === part.part_id}
                        onClick={() => handlePartSelect(part)}
                        readOnly={readOnly}
                    />
                ))}
                {filteredParts.length === 0 && (
                    <EmptyState>No parts found</EmptyState>
                )}
            </PartList>

            {/* Part Details Panel */}
            {selectedPart && (
                <PartDetailsPanel>
                    <DetailsHeader>
                        <h4>Part Details</h4>
                        {!readOnly && (
                            <button onClick={() => setIsFormOpen(!isFormOpen)}>
                                {isFormOpen ? 'Close' : 'Edit'}
                            </button>
                        )}
                    </DetailsHeader>

                    {!isFormOpen ? (
                        <DetailsContent>
                            <DetailRow>
                                <DetailLabel>Part Number</DetailLabel>
                                <DetailValue>{selectedPart.part_number}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Name</DetailLabel>
                                <DetailValue>{selectedPart.name}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Category</DetailLabel>
                                <DetailValue>{selectedPart.category}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>OEM Source</DetailLabel>
                                <DetailValue>{selectedPart.oem_source || 'N/A'}</DetailValue>
                            </DetailRow>
                            <DetailRow>
                                <DetailLabel>Compatible Aircraft</DetailLabel>
                                <DetailValue>
                                    {selectedPart.aircraft_compatible.length > 0 ? (
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                                            {selectedPart.aircraft_compatible.map((aircraftId, idx) => (
                                                <span key={idx} style={{
                                                    padding: '2px 8px',
                                                    backgroundColor: '#e8f5e9',
                                                    borderRadius: '4px',
                                                    fontSize: '11px'
                                                }}>
                                                    {aircraftId}
                                                </span>
                                            ))}
                                        </div>
                                    ) : (
                                        <span style={{ color: '#999' }}>All</span>
                                    )}
                                </DetailValue>
                            </DetailRow>
                            {selectedPart.description && (
                                <DetailRow>
                                    <DetailLabel>Description</DetailLabel>
                                    <DetailValue>{selectedPart.description}</DetailValue>
                                </DetailRow>
                            )}
                        </DetailsContent>
                    ) : (
                        <EditForm>
                            <FormRow>
                                <FormLabel>Part Number</FormLabel>
                                <input
                                    type="text"
                                    value={selectedPart.part_number}
                                    onChange={(e) => setSelectedPart({ ...selectedPart, part_number: e.target.value })}
                                    style={inputStyle}
                                />
                            </FormRow>
                            <FormRow>
                                <FormLabel>Name</FormLabel>
                                <input
                                    type="text"
                                    value={selectedPart.name}
                                    onChange={(e) => setSelectedPart({ ...selectedPart, name: e.target.value })}
                                    style={inputStyle}
                                />
                            </FormRow>
                            <FormRow>
                                <FormLabel>Category</FormLabel>
                                <select
                                    value={selectedPart.category}
                                    onChange={(e) => setSelectedPart({ ...selectedPart, category: e.target.value })}
                                    style={inputStyle}
                                >
                                    <option value="structural">Structural</option>
                                    <option value="engine">Engine</option>
                                    <option value="avionics">Avionics</option>
                                    <option value="tools">Tools</option>
                                    <option value="consumables">Consumables</option>
                                </select>
                            </FormRow>
                            <FormRow>
                                <FormLabel>OEM Source</FormLabel>
                                <input
                                    type="text"
                                    value={selectedPart.oem_source || ''}
                                    onChange={(e) => setSelectedPart({ ...selectedPart, oem_source: e.target.value })}
                                    style={inputStyle}
                                />
                            </FormRow>
                            <FormRow>
                                <FormLabel>Description</FormLabel>
                                <textarea
                                    value={selectedPart.description || ''}
                                    onChange={(e) => setSelectedPart({ ...selectedPart, description: e.target.value })}
                                    style={{ ...inputStyle, minHeight: '60px' }}
                                />
                            </FormRow>
                        </EditForm>
                    )}
                </PartDetailsPanel>
            )}

            {/* Add Part Form */}
            {!isFormOpen && !readOnly && (
                <AddPartSection>
                    <button onClick={() => setIsFormOpen(true)}>+ Add New Part</button>
                </AddPartSection>
            )}

            {isFormOpen && !readOnly && (
                <AddPartForm>
                    <h4>Add New Part</h4>
                    <FormRow>
                        <FormLabel>Part Number</FormLabel>
                        <input type="text" style={inputStyle} />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Name</FormLabel>
                        <input type="text" style={inputStyle} />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Category</FormLabel>
                        <select style={inputStyle}>
                            <option value="structural">Structural</option>
                            <option value="engine">Engine</option>
                            <option value="avionics">Avionics</option>
                            <option value="tools">Tools</option>
                            <option value="consumables">Consumables</option>
                        </select>
                    </FormRow>
                    <FormRow>
                        <FormLabel>OEM Source</FormLabel>
                        <input type="text" style={inputStyle} />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Description</FormLabel>
                        <textarea style={{ ...inputStyle, minHeight: '60px' }} />
                    </FormRow>
                    <FormButtons>
                        <button onClick={() => setIsFormOpen(false)}>Cancel</button>
                        <button style={{ backgroundColor: '#007AFF', color: '#fff' }}>Save Part</button>
                    </FormButtons>
                </AddPartForm>
            )}
        </Container>
    )
}

// ========== Components ==========

function PartItem({ part, isSelected, onClick, readOnly }: { part: PartConfig, isSelected: boolean, onClick: () => void, readOnly?: boolean }) {
    return (
        <PartItemWrapper
            isSelected={isSelected}
            onClick={onClick}
            style={{ cursor: readOnly ? 'default' : 'pointer' }}
        >
            <PartInfo>
                <PartName>{part.name}</PartName>
                <PartMeta>
                    <span>{part.part_number}</span>
                    <span>{part.category}</span>
                    {part.oem_source && (
                        <span style={{ fontSize: '10px', color: '#999' }}>
                            {part.oem_source}
                        </span>
                    )}
                </PartMeta>
            </PartInfo>
        </PartItemWrapper>
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

const SearchBar = styled('div', {
    padding: '8px 0',
})

const PartList = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
    maxHeight: '300px',
    overflowY: 'auto',
})

const PartItemWrapper = styled('div', ({ isSelected }: { isSelected: boolean }) => ({
    padding: '12px',
    backgroundColor: isSelected ? '#e3f2fd' : '#f8f9fa',
    borderRadius: '8px',
    border: isSelected ? '1px solid #007AFF' : '1px solid #e0e0e0',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
}))

const PartInfo = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
})

const PartName = styled('span', {
    fontWeight: '500',
    fontSize: '13px',
})

const PartMeta = styled('span', {
    fontSize: '11px',
    color: '#666',
    display: 'flex',
    gap: '8px',
})

const PartDetailsPanel = styled('div', {
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
    minWidth: '120px',
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

const AddPartSection = styled('div', {
    display: 'flex',
    justifyContent: 'center',
    padding: '12px',
})

const AddPartForm = styled('div', {
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
