import React, { useState, useEffect, useCallback } from 'react'
import { styled } from 'baseui'

// Job workflow states
const JOB_WORKFLOW = {
    pending: { label: 'Pending', description: 'Job created, awaiting assignment' },
    open: { label: 'Open', description: 'Job accepted, work ready' },
    in_progress: { label: 'In Progress', description: 'Work in progress' },
    completed: { label: 'Completed', description: 'Work finished, awaiting sign-off' },
    cancelled: { label: 'Cancelled', description: 'Job cancelled' }
}

// Workflow transitions
const TRANSITIONS = {
    pending: ['open', 'cancelled'],
    open: ['in_progress', 'completed', 'cancelled'],
    in_progress: ['completed', 'pending'],
    completed: [],
    cancelled: []
}

// Graph visualization nodes
interface Node {
    id: string
    type: 'job' | 'customer' | 'mechanic' | 'aircraft'
    label: string
    status?: string
    priority?: string
}

// Graph edges
interface Edge {
    from: string
    to: string
    label: string
}

interface WorkflowBuilderProps {
    initialNodes?: Node[]
    initialEdges?: Edge[]
    readOnly?: boolean
}

export function WorkflowBuilder({ initialNodes = [], initialEdges = [], readOnly = false }: WorkflowBuilderProps) {
    const [nodes, setNodes] = useState<Node[]>(initialNodes)
    const [edges, setEdges] = useState<Edge[]>(initialEdges)
    const [selectedNode, setSelectedNode] = useState<string | null>(null)
    const [hoveredNode, setHoveredNode] = useState<string | null>(null)

    // Add a new node
    const addNode = useCallback((type: Node['type'], label: string, status?: string) => {
        const id = `${type}_${Date.now()}`
        setNodes(prev => [...prev, { id, type, label, status }])
    }, [])

    // Remove a node
    const removeNode = useCallback((id: string) => {
        setNodes(prev => prev.filter(n => n.id !== id))
        setEdges(prev => prev.filter(e => e.from !== id && e.to !== id))
        if (selectedNode === id) setSelectedNode(null)
    }, [selectedNode])

    // Update node status
    const updateNodeStatus = useCallback((id: string, status: string) => {
        setNodes(prev => prev.map(n => n.id === id ? { ...n, status } : n))
    }, [])

    // Add edge between nodes
    const addEdge = useCallback((from: string, to: string, label: string) => {
        setEdges(prev => [...prev, { from, to, label }])
    }, [])

    // Get valid transitions for a node
    const getValidTransitions = (currentStatus: string): string[] => {
        return TRANSITIONS[currentStatus] || []
    }

    return (
        <Container>
            <Header>
                <h3>Job Workflow Builder</h3>
                <span style={{ fontSize: '12px', color: '#666' }}>
                    {nodes.length} nodes, {edges.length} relationships
                </span>
            </Header>

            <Workspace>
                {/* Nodes panel */}
                <NodesPanel>
                    <h4>Add Objects</h4>
                    {!readOnly && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            <NodeButton onClick={() => addNode('job', 'New Job', 'pending')}>
                                [+] Job
                            </NodeButton>
                            <NodeButton onClick={() => addNode('customer', 'New Customer')}>
                                [+] Customer
                            </NodeButton>
                            <NodeButton onClick={() => addNode('mechanic', 'New Mechanic')}>
                                [+] Mechanic
                            </NodeButton>
                            <NodeButton onClick={() => addNode('aircraft', 'New Aircraft')}>
                                [+] Aircraft
                            </NodeButton>
                        </div>
                    )}
                </NodesPanel>

                {/* Canvas */}
                <Canvas onMouseLeave={() => setHoveredNode(null)}>
                    {nodes.map(node => (
                        <NodeView
                            key={node.id}
                            node={node}
                            isSelected={selectedNode === node.id}
                            isHovered={hoveredNode === node.id}
                            onClick={() => setSelectedNode(node.id)}
                            onMouseEnter={() => setHoveredNode(node.id)}
                            onDelete={() => removeNode(node.id)}
                            onUpdateStatus={readOnly ? undefined : updateNodeStatus}
                            getValidTransitions={getValidTransitions}
                        />
                    ))}
                    {/* Simple SVG edges */}
                    <svg style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        pointerEvents: 'none',
                        zIndex: 0
                    }}>
                        {edges.map((edge, index) => (
                            <path
                                key={index}
                                d={`M 0 0 L 100 100`}
                                stroke="#999"
                                strokeWidth="2"
                                fill="none"
                            />
                        ))}
                    </svg>
                </Canvas>

                {/* Properties panel */}
                {selectedNode && (
                    <PropertiesPanel>
                        <h4>Properties</h4>
                        {(() => {
                            const node = nodes.find(n => n.id === selectedNode)
                            if (!node) return null
                            return (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                    <PropertyField label="Type" value={node.type} />
                                    <PropertyField label="Label" value={node.label} />
                                    {node.status && (
                                        <div>
                                            <label>Status</label>
                                            <StatusSelect
                                                value={node.status}
                                                onChange={(e) => !readOnly && updateNodeStatus(selectedNode, e.target.value)}
                                                disabled={readOnly}
                                            >
                                                {Object.keys(JOB_WORKFLOW).map(status => (
                                                    <option key={status} value={status}>
                                                        {JOB_WORKFLOW[status as keyof typeof JOB_WORKFLOW].label}
                                                    </option>
                                                ))}
                                            </StatusSelect>
                                        </div>
                                    )}
                                    {!readOnly && (
                                        <button onClick={() => removeNode(selectedNode)} style={{ marginTop: '8px', color: '#ff4d4d' }}>
                                            Remove Node
                                        </button>
                                    )}
                                </div>
                            )
                        })()}
                    </PropertiesPanel>
                )}
            </Workspace>

            {/* Workflow legend */}
            <Legend>
                <h5>Workflow Legend</h5>
                <LegendItem>
                    <StatusDot status="pending" />
                    <span>Pending</span>
                    <small>Job created, awaiting assignment</small>
                </LegendItem>
                <LegendItem>
                    <StatusDot status="open" />
                    <span>Open</span>
                    <small>Job accepted, work ready</small>
                </LegendItem>
                <LegendItem>
                    <StatusDot status="in_progress" />
                    <span>In Progress</span>
                    <small>Work in progress</small>
                </LegendItem>
                <LegendItem>
                    <StatusDot status="completed" />
                    <span>Completed</span>
                    <small>Work finished</small>
                </LegendItem>
                <LegendItem>
                    <StatusDot status="cancelled" />
                    <span>Cancelled</span>
                    <small>Job cancelled</small>
                </LegendItem>
            </Legend>
        </Container>
    )
}

// Node view component
function NodeView({ node, isSelected, isHovered, onClick, onMouseEnter, onDelete, onUpdateStatus, getValidTransitions }: any) {
    const workflow = JOB_WORKFLOW[node.status as keyof typeof JOB_WORKFLOW] || JOB_WORKFLOW.pending

    return (
        <NodeWrapper
            onClick={onClick}
            onMouseEnter={onMouseEnter}
            style={{
                borderColor: isSelected ? '#007AFF' : isHovered ? '#005ecb' : '#e0e0e0',
                backgroundColor: isSelected ? '#f0f7ff' : '#fff',
            }}
        >
            <NodeContent>
                <NodeIcon status={node.status} />
                <NodeInfo>
                    <NodeLabel>{node.label}</NodeLabel>
                    <NodeType>{node.type}</NodeType>
                </NodeInfo>
            </NodeContent>

            <NodeActions>
                {node.status && onUpdateStatus && (
                    <StatusDropdown
                        value={node.status}
                        onChange={(e) => onUpdateStatus(e.target.value)}
                    >
                        {getValidTransitions(node.status).map(status => (
                            <option key={status} value={status}>
                                {JOB_WORKFLOW[status as keyof typeof JOB_WORKFLOW].label}
                            </option>
                        ))}
                    </StatusDropdown>
                )}
                <button onClick={(e) => { e.stopPropagation(); onDelete() }}>×</button>
            </NodeActions>
        </NodeWrapper>
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

const Workspace = styled('div', {
    display: 'flex',
    gap: '16px',
    minHeight: '400px',
})

const NodesPanel = styled('div', {
    width: '160px',
    padding: '12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    flexShrink: 0,
})

const NodeButton = styled('button', {
    width: '100%',
    padding: '10px',
    border: 'none',
    borderRadius: '6px',
    backgroundColor: '#fff',
    color: '#333',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    fontSize: '13px',
    transition: 'all 0.2s',
    '&:hover': {
        backgroundColor: '#007AFF',
        color: '#fff',
    },
})

const Canvas = styled('div', {
    flex: 1,
    position: 'relative',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    overflow: 'hidden',
})

const PropertiesPanel = styled('div', {
    width: '200px',
    padding: '12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    flexShrink: 0,
})

const Legend = styled('div', {
    backgroundColor: '#f8f9fa',
    padding: '12px',
    borderRadius: '8px',
})

const LegendItem = styled('div', {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '8px',
    '& small': {
        fontSize: '11px',
        color: '#666',
    },
})

const Dot = styled('div', {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
})

// ========== Helper Components ==========

function NodeWrapper({ children, style, onClick, onMouseEnter }: any) {
    return (
        <div
            style={{
                position: 'absolute',
                width: '160px',
                padding: '12px',
                backgroundColor: '#fff',
                border: '1px solid #e0e0e0',
                borderRadius: '8px',
                cursor: 'pointer',
                ...style,
            }}
            onClick={onClick}
            onMouseEnter={onMouseEnter}
        >
            {children}
        </div>
    )
}

function NodeContent({ children }: any) {
    return <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>{children}</div>
}

function NodeIcon({ status }: { status?: string }) {
    const colors = {
        pending: '#F57C00',
        open: '#007AFF',
        in_progress: '#FF9800',
        completed: '#4CAF50',
        cancelled: '#f44336'
    }
    return (
        <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            backgroundColor: status === 'completed' ? '#e8f5e9' : status === 'cancelled' ? '#ffebee' : '#f0f0f0',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: status === 'completed' ? '#4CAF50' : status === 'cancelled' ? '#f44336' : '#666',
            fontWeight: 'bold',
            fontSize: '14px',
        }}>
            {status ? status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ') : 'N/A'}
        </div>
    )
}

function NodeInfo({ children }: any) {
    return <div style={{ flex: 1 }}>{children}</div>
}

function NodeLabel({ children }: any) {
    return <strong style={{ fontSize: '13px' }}>{children}</strong>
}

function NodeType({ children }: any) {
    return <span style={{ fontSize: '11px', color: '#666', textTransform: 'capitalize' }}>{children}</span>
}

function NodeActions({ children }: any) {
    return <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>{children}</div>
}

function PropertyField({ label, value }: { label: string, value: string }) {
    return (
        <div>
            <label style={{ fontSize: '12px', color: '#666', display: 'block', marginBottom: '4px' }}>{label}</label>
            <div style={{ fontSize: '14px', fontWeight: '500', padding: '8px', backgroundColor: '#fff', borderRadius: '4px' }}>
                {value}
            </div>
        </div>
    )
}

function StatusSelect({ value, onChange, disabled }: any) {
    return (
        <select
            value={value}
            onChange={onChange}
            disabled={disabled}
            style={{
                width: '100%',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #e0e0e0',
                fontSize: '13px',
            }}
        />
    )
}

function StatusDropdown({ value, onChange }: any) {
    return (
        <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            style={{
                padding: '4px 8px',
                borderRadius: '4px',
                border: '1px solid #e0e0e0',
                fontSize: '12px',
            }}
        />
    )
}
