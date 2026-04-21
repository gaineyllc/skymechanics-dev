import React, { useState, useEffect } from 'react'
import { styled } from '../utils/styled'
import { WorkflowBuilder } from '../components/WorkflowBuilder'
import { ProcedureBuilder } from '../components/ProcedureBuilder'
import { ToolConfiguration } from '../components/ToolConfiguration'
import { PartsCatalog } from '../components/PartsCatalog'
import { 
    fetchProcedures, 
    createProcedure, 
    fetchTools, 
    fetchParts,
    ProcedureTemplate,
    Tool,
    Part
} from '../services/api'

export function Procedures() {
    const [activeTab, setActiveTab] = useState<'list' | 'builder' | 'tools' | 'parts'>('list')
    const [procedures, setProcedures] = useState<ProcedureTemplate[]>([])
    const [tools, setTools] = useState<Tool[]>([])
    const [parts, setParts] = useState<Part[]>([])
    const [selectedProcedure, setSelectedProcedure] = useState<ProcedureTemplate | null>(null)
    const [isCreating, setIsCreating] = useState(false)

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        try {
            const [proceduresData, toolsData, partsData] = await Promise.all([
                fetchProcedures(),
                fetchTools(),
                fetchParts()
            ])
            setProcedures(proceduresData)
            setTools(toolsData)
            setParts(partsData)
        } catch (error) {
            console.error('Failed to load data:', error)
        }
    }

    const handleProcedureCreate = async (name: string, category: string, authority: string) => {
        try {
            const newProcedure = await createProcedure({
                name,
                category,
                authority,
                estimated_duration_hours: 1,
                required_specialty: 'general',
                is_active: true
            })
            setProcedures([...procedures, newProcedure])
            setIsCreating(false)
        } catch (error) {
            console.error('Failed to create procedure:', error)
        }
    }

    return (
        <Container>
            <Header>
                <h2>Maintenance Procedures</h2>
                <div style={{ display: 'flex', gap: '8px' }}>
                    {activeTab === 'list' && !isCreating && (
                        <button onClick={() => setIsCreating(true)}>
                            + Create Procedure
                        </button>
                    )}
                    {isCreating && (
                        <button onClick={() => setIsCreating(false)}>
                            Cancel
                        </button>
                    )}
                </div>
            </Header>

            {/* Navigation Tabs */}
            <Tabs>
                <TabButton active={activeTab === 'list'} onClick={() => setActiveTab('list')}>
                    Procedures
                </TabButton>
                <TabButton active={activeTab === 'builder'} onClick={() => setActiveTab('builder')}>
                    Workflow Builder
                </TabButton>
                <TabButton active={activeTab === 'tools'} onClick={() => setActiveTab('tools')}>
                    Tools
                </TabButton>
                <TabButton active={activeTab === 'parts'} onClick={() => setActiveTab('parts')}>
                    Parts
                </TabButton>
            </Tabs>

            {/* Content */}
            <Content>
                {activeTab === 'list' && (
                    <ProcedureList
                        procedures={procedures}
                        isCreating={isCreating}
                        onProcedureCreate={handleProcedureCreate}
                        onSelectProcedure={(proc) => {
                            setSelectedProcedure(proc)
                            setActiveTab('builder')
                        }}
                    />
                )}
                
                {activeTab === 'builder' && (
                    <WorkflowBuilderSection>
                        {selectedProcedure ? (
                            <ProcedureBuilder
                                initialTasks={selectedProcedure.tasks.map((t, idx) => ({
                                    task_id: t.task_id || idx,
                                    name: t.name || 'Task',
                                    sequence: idx + 1,
                                    category: (t.category as any) || 'visual',
                                    estimated_duration_minutes: t.estimated_duration_minutes || 30,
                                    required_tools: t.required_tools || [],
                                    required_parts: t.required_parts || [],
                                    checklist_items: t.checklist_items || []
                                }))}
                                tools={tools}
                                parts={parts}
                            />
                        ) : (
                            <EmptyState>Select a procedure to edit, or create a new one.</EmptyState>
                        )}
                    </WorkflowBuilderSection>
                )}

                {activeTab === 'tools' && (
                    <ToolConfiguration tools={tools} />
                )}

                {activeTab === 'parts' && (
                    <PartsCatalog parts={parts} />
                )}
            </Content>

            {/* Create Procedure Modal */}
            {isCreating && (
                <Modal>
                    <ModalContent>
                        <h3>Create New Procedure</h3>
                        <FormRow>
                            <FormLabel>Procedure Name</FormLabel>
                            <input
                                type="text"
                                id="procName"
                                style={inputStyle}
                            />
                        </FormRow>
                        <FormRow>
                            <FormLabel>Category</FormLabel>
                            <select id="procCategory" style={inputStyle}>
                                <option value="annual">Annual Inspection</option>
                                <option value="100hr">100-Hour Inspection</option>
                                <option value="condition">Condition Inspection</option>
                                <option value="repair">Repair</option>
                            </select>
                        </FormRow>
                        <FormRow>
                            <FormLabel>Authority</FormLabel>
                            <input
                                type="text"
                                id="procAuthority"
                                placeholder="e.g., FAA AC 20-106"
                                style={inputStyle}
                            />
                        </FormRow>
                        <ModalButtons>
                            <button onClick={() => setIsCreating(false)}>Cancel</button>
                            <button
                                onClick={() => {
                                    const name = (document.getElementById('procName') as HTMLInputElement).value
                                    const category = (document.getElementById('procCategory') as HTMLSelectElement).value
                                    const authority = (document.getElementById('procAuthority') as HTMLInputElement).value
                                    if (name) {
                                        handleProcedureCreate(name, category, authority)
                                    }
                                }}
                                style={{ backgroundColor: '#007AFF', color: '#fff' }}
                            >
                                Create
                            </button>
                        </ModalButtons>
                    </ModalContent>
                </Modal>
            )}
        </Container>
    )
}

// ========== Procedure List Component ==========

interface ProcedureListProps {
    procedures: ProcedureTemplate[]
    isCreating: boolean
    onProcedureCreate: (name: string, category: string, authority: string) => void
    onSelectProcedure: (procedure: ProcedureTemplate) => void
}

function ProcedureList({ procedures, isCreating, onProcedureCreate, onSelectProcedure }: ProcedureListProps) {
    const [name, setName] = useState('')
    const [category, setCategory] = useState('annual')
    const [authority, setAuthority] = useState('')

    const handleCreate = () => {
        if (name) {
            onProcedureCreate(name, category, authority || 'FAA AC 20-106')
            setName('')
            setCategory('annual')
            setAuthority('')
        }
    }

    return (
        <ListContainer>
            {/* Create Procedure Form */}
            {isCreating && (
                <CreateForm>
                    <h4>Create New Procedure</h4>
                    <FormRow>
                        <FormLabel>Name</FormLabel>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Procedure name..."
                            style={inputStyle}
                        />
                    </FormRow>
                    <FormRow>
                        <FormLabel>Category</FormLabel>
                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            style={inputStyle}
                        >
                            <option value="annual">Annual Inspection</option>
                            <option value="100hr">100-Hour Inspection</option>
                            <option value="condition">Condition Inspection</option>
                            <option value="repair">Repair</option>
                        </select>
                    </FormRow>
                    <FormRow>
                        <FormLabel>Authority</FormLabel>
                        <input
                            type="text"
                            value={authority}
                            onChange={(e) => setAuthority(e.target.value)}
                            placeholder="e.g., FAA AC 20-106"
                            style={inputStyle}
                        />
                    </FormRow>
                    <FormButtons>
                        <button onClick={() => onProcedureCreate(name, category, authority || 'FAA AC 20-106')} style={{ backgroundColor: '#007AFF', color: '#fff' }}>
                            Create Procedure
                        </button>
                    </FormButtons>
                </CreateForm>
            )}

            {/* Procedures List */}
            <ProceduresGrid>
                {procedures.map(proc => (
                    <ProcedureCard key={proc.procedure_id} onClick={() => onSelectProcedure(proc)}>
                        <ProcedureHeader>
                            <ProcedureName>{proc.name}</ProcedureName>
                            <ProcedureBadge>{proc.category}</ProcedureBadge>
                        </ProcedureHeader>
                        <ProcedureMeta>
                            <span>{proc.authority}</span>
                            <span>{proc.estimated_duration_hours}h estimated</span>
                            <span>{proc.tasks.length} tasks</span>
                        </ProcedureMeta>
                        <ProcedureActions>
                            <button>View</button>
                            <button>Edit</button>
                        </ProcedureActions>
                    </ProcedureCard>
                ))}
                {procedures.length === 0 && !isCreating && (
                    <EmptyState>No procedures configured yet. Create one to get started.</EmptyState>
                )}
            </ProceduresGrid>
        </ListContainer>
    )
}

// ========== Workflow Builder Section ==========

function WorkflowBuilderSection({ children }: { children: React.ReactNode }) {
    return (
        <WorkflowBuilderContainer>
            {children}
        </WorkflowBuilderContainer>
    )
}

// ========== Styled Components ==========

const Container = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    padding: '20px',
})

const Header = styled('div', {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
})

const Tabs = styled('div', {
    display: 'flex',
    gap: '4px',
    borderBottom: '2px solid #e0e0e0',
    paddingBottom: '4px',
})

const TabButton = styled('button', ({ active }: { active: boolean }) => ({
    padding: '10px 20px',
    border: 'none',
    borderBottom: active ? '2px solid #007AFF' : 'none',
    backgroundColor: active ? '#f0f7ff' : 'transparent',
    color: active ? '#007AFF' : '#666',
    fontWeight: active ? '500' : 'normal',
    cursor: 'pointer',
    transition: 'all 0.2s',
}))

const Content = styled('div', {
    flex: 1,
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    padding: '20px',
    minHeight: '500px',
})

const ListContainer = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
})

const CreateForm = styled('div', {
    backgroundColor: '#fff',
    padding: '16px',
    borderRadius: '8px',
    border: '1px solid #e0e0e0',
})

const ProceduresGrid = styled('div', {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '12px',
})

const ProcedureCard = styled('div', {
    backgroundColor: '#fff',
    padding: '16px',
    borderRadius: '8px',
    border: '1px solid #e0e0e0',
    cursor: 'pointer',
    transition: 'all 0.2s',
    '&:hover': {
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        borderColor: '#007AFF',
    },
})

const ProcedureHeader = styled('div', {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '8px',
})

const ProcedureName = styled('h4', {
    margin: 0,
    fontSize: '14px',
    fontWeight: '500',
    color: '#333',
})

const ProcedureBadge = styled('span', {
    fontSize: '10px',
    padding: '2px 8px',
    backgroundColor: '#e3f2fd',
    borderRadius: '12px',
    color: '#007AFF',
})

const ProcedureMeta = styled('div', {
    display: 'flex',
    gap: '12px',
    fontSize: '11px',
    color: '#666',
    marginBottom: '8px',
})

const ProcedureActions = styled('div', {
    display: 'flex',
    gap: '8px',
})

const Modal = styled('div', {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
})

const ModalContent = styled('div', {
    backgroundColor: '#fff',
    padding: '24px',
    borderRadius: '12px',
    width: '100%',
    maxWidth: '400px',
})

const WorkflowBuilderContainer = styled('div', {
    minHeight: '600px',
})

const FormRow = styled('div', {
    display: 'flex',
    gap: '8px',
    alignItems: 'center',
    marginBottom: '12px',
})

const FormLabel = styled('span', {
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
    minWidth: '100px',
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
    marginTop: '12px',
})

const ModalButtons = styled('div', {
    display: 'flex',
    gap: '8px',
    justifyContent: 'flex-end',
    marginTop: '16px',
})

const EmptyState = styled('div', {
    color: '#999',
    padding: '40px',
    textAlign: 'center',
    fontStyle: 'italic',
})
