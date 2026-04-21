import React, { useState, useCallback } from 'react'
import { styled } from '../../utils/styled'

// Task category types
export type TaskCategory = 'visual' | 'disassembly' | 'inspection' | 'reassembly' | 'testing' | 'cleaning'

// Task interface
export interface ProcedureTask {
    task_id: number
    name: string
    sequence: number
    category: TaskCategory
    estimated_duration_minutes: number
    required_tools: string[]
    required_parts: string[]
    checklist_items: Array<{ item: string; checked: boolean }>
    instructions?: string
}

// Tool interface
export interface ProcedureTool {
    tool_id: number
    name: string
    category: string
}

// Part interface
export interface ProcedurePart {
    part_id: number
    name: string
    part_number: string
}

interface ProcedureBuilderProps {
    initialTasks?: ProcedureTask[]
    tools?: ProcedureTool[]
    parts?: ProcedurePart[]
    readOnly?: boolean
    onTaskChange?: (tasks: ProcedureTask[]) => void
}

export function ProcedureBuilder({ 
    initialTasks = [], 
    tools = [], 
    parts = [],
    readOnly = false, 
    onTaskChange 
}: ProcedureBuilderProps) {
    const [tasks, setTasks] = useState<ProcedureTask[]>(initialTasks)

    React.useEffect(() => {
        setTasks(initialTasks)
    }, [initialTasks])

    React.useEffect(() => {
        if (onTaskChange) {
            onTaskChange(tasks)
        }
    }, [tasks, onTaskChange])

    // Add a new task
    const addTask = useCallback(() => {
        const newTask: ProcedureTask = {
            task_id: Date.now(),
            name: 'New Task',
            sequence: tasks.length + 1,
            category: 'visual',
            estimated_duration_minutes: 30,
            required_tools: [],
            required_parts: [],
            checklist_items: []
        }
        setTasks(prev => [...prev, newTask])
    }, [tasks.length])

    // Remove a task
    const removeTask = useCallback((taskId: number) => {
        setTasks(prev => prev.filter(t => t.task_id !== taskId).map((t, idx) => ({ ...t, sequence: idx + 1 })))
    }, [])

    // Update a task
    const updateTask = useCallback((taskId: number, updates: Partial<ProcedureTask>) => {
        setTasks(prev => prev.map(t => t.task_id === taskId ? { ...t, ...updates } : t))
    }, [])

    // Reorder tasks
    const moveTask = useCallback((fromIndex: number, toIndex: number) => {
        setTasks(prev => {
            const newTasks = [...prev]
            const [moved] = newTasks.splice(fromIndex, 1)
            newTasks.splice(toIndex, 0, moved)
            return newTasks.map((t, idx) => ({ ...t, sequence: idx + 1 }))
        })
    }, [])

    // Add checklist item
    const addChecklistItem = useCallback((taskId: number, itemText: string) => {
        setTasks(prev => prev.map(t => {
            if (t.task_id === taskId) {
                return {
                    ...t,
                    checklist_items: [...t.checklist_items, { item: itemText, checked: false }]
                }
            }
            return t
        }))
    }, [])

    // Toggle checklist item
    const toggleChecklistItem = useCallback((taskId: number, itemIndex: number) => {
        setTasks(prev => prev.map(t => {
            if (t.task_id === taskId) {
                const newChecklist = [...t.checklist_items]
                newChecklist[itemIndex] = { ...newChecklist[itemIndex], checked: !newChecklist[itemIndex].checked }
                return { ...t, checklist_items: newChecklist }
            }
            return t
        }))
    }, [])

    return (
        <Container>
            <Header>
                <h3>Procedure Builder</h3>
                <span style={{ fontSize: '12px', color: '#666' }}>
                    {tasks.length} tasks | Total time: {tasks.reduce((sum, t) => sum + t.estimated_duration_minutes, 0)} min
                </span>
            </Header>

            {!readOnly && (
                <Toolbar>
                    <button onClick={addTask}>
                        + Add Task
                    </button>
                </Toolbar>
            )}

            <TaskList>
                {tasks.map((task, index) => (
                    <TaskCard 
                        key={task.task_id}
                        task={task}
                        index={index}
                        totalTasks={tasks.length}
                        tools={tools}
                        parts={parts}
                        readOnly={readOnly}
                        onRemove={removeTask}
                        onUpdate={updateTask}
                        onMove={moveTask}
                        onAddChecklistItem={addChecklistItem}
                        onToggleChecklistItem={toggleChecklistItem}
                    />
                ))}
            </TaskList>
        </Container>
    )
}

// Task Card Component
interface TaskCardProps {
    task: ProcedureTask
    index: number
    totalTasks: number
    tools: ProcedureTool[]
    parts: ProcedurePart[]
    readOnly: boolean
    onRemove: (taskId: number) => void
    onUpdate: (taskId: number, updates: Partial<ProcedureTask>) => void
    onMove: (fromIndex: number, toIndex: number) => void
    onAddChecklistItem: (taskId: number, itemText: string) => void
    onToggleChecklistItem: (taskId: number, itemIndex: number) => void
}

function TaskCard({ 
    task, 
    index, 
    totalTasks,
    tools, 
    parts, 
    readOnly, 
    onRemove, 
    onUpdate,
    onMove,
    onAddChecklistItem,
    onToggleChecklistItem
}: TaskCardProps) {
    const [showChecklistInput, setShowChecklistInput] = useState(false)
    const [newChecklistItem, setNewChecklistItem] = useState('')

    return (
        <TaskCardWrapper>
            <TaskHeader>
                <TaskSequence>{task.sequence}.</TaskSequence>
                <TaskTitle>
                    <input
                        type="text"
                        value={task.name}
                        onChange={(e) => onUpdate(task.task_id, { name: e.target.value })}
                        readOnly={readOnly}
                        placeholder="Task name"
                        style={{ 
                            width: '100%', 
                            border: 'none', 
                            background: 'transparent',
                            fontSize: '14px',
                            fontWeight: '500',
                            padding: '4px 8px'
                        }}
                    />
                </TaskTitle>
                <TaskActions>
                    <button 
                        onClick={() => onMove(index, Math.max(0, index - 1))}
                        disabled={readOnly || index === 0}
                        style={{ opacity: (index === 0 || readOnly) ? 0.5 : 1 }}
                    >
                        ↑
                    </button>
                    <button 
                        onClick={() => onMove(index, Math.min(totalTasks - 1, index + 1))}
                        disabled={readOnly || index === totalTasks - 1}
                        style={{ opacity: (index === totalTasks - 1 || readOnly) ? 0.5 : 1 }}
                    >
                        ↓
                    </button>
                    {!readOnly && (
                        <button onClick={() => onRemove(task.task_id)} style={{ color: '#ff4d4d' }}>
                            ×
                        </button>
                    )}
                </TaskActions>
            </TaskHeader>

            <TaskContent>
                {/* Basic Info */}
                <InfoRow>
                    <InfoLabel>Category:</InfoLabel>
                    <select
                        value={task.category}
                        onChange={(e) => onUpdate(task.task_id, { category: e.target.value as TaskCategory })}
                        disabled={readOnly}
                        style={{ padding: '4px 8px', borderRadius: '4px', border: '1px solid #e0e0e0' }}
                    >
                        <option value="visual">Visual Inspection</option>
                        <option value="disassembly">Disassembly</option>
                        <option value="inspection">Detailed Inspection</option>
                        <option value="reassembly">Reassembly</option>
                        <option value="testing">Testing</option>
                        <option value="cleaning">Cleaning</option>
                    </select>

                    <InfoLabel style={{ marginLeft: '16px' }}>Time:</InfoLabel>
                    <input
                        type="number"
                        value={task.estimated_duration_minutes}
                        onChange={(e) => onUpdate(task.task_id, { estimated_duration_minutes: parseInt(e.target.value) || 0 })}
                        disabled={readOnly}
                        style={{ width: '60px', padding: '4px 8px', borderRadius: '4px', border: '1px solid #e0e0e0' }}
                    />
                    <span>min</span>
                </InfoRow>

                {/* Required Tools */}
                <ResourcesRow>
                    <ResourcesLabel>Tools:</ResourcesLabel>
                    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                        {task.required_tools.map((toolId, idx) => {
                            const tool = tools.find(t => t.tool_id === toolId)
                            return (
                                <span key={idx} style={{
                                    padding: '2px 8px',
                                    backgroundColor: '#e3f2fd',
                                    borderRadius: '4px',
                                    fontSize: '12px'
                                }}>
                                    {tool?.name || `Tool #${toolId}`}
                                    {!readOnly && (
                                        <button
                                            onClick={() => onUpdate(task.task_id, { required_tools: task.required_tools.filter((_, i) => i !== idx) })}
                                            style={{ marginLeft: '4px', border: 'none', background: 'none', cursor: 'pointer' }}
                                        >
                                            ×
                                        </button>
                                    )}
                                </span>
                            )
                        })}
                        {!readOnly && (
                            <button onClick={() => {
                                // In a real app, this would open a tool selector
                                // For now, add a placeholder tool
                                const newToolId = Date.now()
                                onUpdate(task.task_id, { required_tools: [...task.required_tools, newToolId] })
                            }}>
                                + Add
                            </button>
                        )}
                    </div>
                </ResourcesRow>

                {/* Required Parts */}
                <ResourcesRow>
                    <ResourcesLabel>Parts:</ResourcesLabel>
                    <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                        {task.required_parts.map((partId, idx) => {
                            const part = parts.find(p => p.part_id === partId)
                            return (
                                <span key={idx} style={{
                                    padding: '2px 8px',
                                    backgroundColor: '#e8f5e9',
                                    borderRadius: '4px',
                                    fontSize: '12px'
                                }}>
                                    {part?.name || `Part #${partId}`}
                                    {!readOnly && (
                                        <button
                                            onClick={() => onUpdate(task.task_id, { required_parts: task.required_parts.filter((_, i) => i !== idx) })}
                                            style={{ marginLeft: '4px', border: 'none', background: 'none', cursor: 'pointer' }}
                                        >
                                            ×
                                        </button>
                                    )}
                                </span>
                            )
                        })}
                        {!readOnly && (
                            <button onClick={() => {
                                // In a real app, this would open a part selector
                                const newPartId = Date.now()
                                onUpdate(task.task_id, { required_parts: [...task.required_parts, newPartId] })
                            }}>
                                + Add
                            </button>
                        )}
                    </div>
                </ResourcesRow>

                {/* Checklist */}
                <ChecklistSection>
                    <ChecklistHeader>
                        <span>Checklist</span>
                        {!readOnly && (
                            <button onClick={() => setShowChecklistInput(!showChecklistInput)}>
                                {showChecklistInput ? 'Close' : '+ Add Item'}
                            </button>
                        )}
                    </ChecklistHeader>
                    
                    {showChecklistInput && !readOnly && (
                        <ChecklistInputRow>
                            <input
                                type="text"
                                value={newChecklistItem}
                                onChange={(e) => setNewChecklistItem(e.target.value)}
                                placeholder="Checklist item..."
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter' && newChecklistItem.trim()) {
                                        onAddChecklistItem(task.task_id, newChecklistItem.trim())
                                        setNewChecklistItem('')
                                        setShowChecklistInput(false)
                                    }
                                }}
                                style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #e0e0e0' }}
                            />
                            <button 
                                onClick={() => {
                                    if (newChecklistItem.trim()) {
                                        onAddChecklistItem(task.task_id, newChecklistItem.trim())
                                        setNewChecklistItem('')
                                        setShowChecklistInput(false)
                                    }
                                }}
                                style={{ padding: '8px 16px', backgroundColor: '#007AFF', color: '#fff', border: 'none', borderRadius: '4px' }}
                            >
                                Add
                            </button>
                        </ChecklistInputRow>
                    )}

                    <ChecklistItems>
                        {task.checklist_items.map((item, idx) => (
                            <ChecklistItem key={idx}>
                                <input
                                    type="checkbox"
                                    checked={item.checked}
                                    onChange={() => onToggleChecklistItem(task.task_id, idx)}
                                    disabled={readOnly}
                                />
                                <span style={{ 
                                    textDecoration: item.checked ? 'line-through' : 'none',
                                    color: item.checked ? '#888' : '#333'
                                }}>
                                    {item.item}
                                </span>
                            </ChecklistItem>
                        ))}
                        {task.checklist_items.length === 0 && (
                            <div style={{ color: '#999', fontSize: '12px', fontStyle: 'italic' }}>
                                No checklist items yet
                            </div>
                        )}
                    </ChecklistItems>
                </ChecklistSection>

                {/* Instructions */}
                <InstructionsSection>
                    <InstructionsLabel>Instructions</InstructionsLabel>
                    <textarea
                        value={task.instructions || ''}
                        onChange={(e) => onUpdate(task.task_id, { instructions: e.target.value })}
                        disabled={readOnly}
                        placeholder="Detailed instructions for this task..."
                        style={{
                            width: '100%',
                            minHeight: '60px',
                            padding: '8px',
                            borderRadius: '4px',
                            border: '1px solid #e0e0e0',
                            resize: 'vertical',
                            fontSize: '13px'
                        }}
                    />
                </InstructionsSection>
            </TaskContent>
        </TaskCardWrapper>
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

const Toolbar = styled('div', {
    display: 'flex',
    justifyContent: 'flex-end',
    padding: '8px 0',
})

const TaskList = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
})

const TaskCardWrapper = styled('div', {
    padding: '16px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    border: '1px solid #e0e0e0',
})

const TaskHeader = styled('div', {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '12px',
})

const TaskSequence = styled('span', {
    fontWeight: 'bold',
    color: '#007AFF',
    minWidth: '24px',
})

const TaskTitle = styled('div', {
    flex: 1,
})

const TaskActions = styled('div', {
    display: 'flex',
    gap: '4px',
})

const TaskContent = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
})

const InfoRow = styled('div', {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    flexWrap: 'wrap',
})

const InfoLabel = styled('span', {
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
})

const ResourcesRow = styled('div', {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    flexWrap: 'wrap',
})

const ResourcesLabel = styled('span', {
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
})

const ChecklistSection = styled('div', {
    backgroundColor: '#fff',
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid #e0e0e0',
})

const ChecklistHeader = styled('div', {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
})

const ChecklistInputRow = styled('div', {
    display: 'flex',
    gap: '8px',
    marginBottom: '8px',
})

const ChecklistItems = styled('div', {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
})

const ChecklistItem = styled('div', {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '4px 0',
})

const InstructionsSection = styled('div', {
    backgroundColor: '#fff',
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid #e0e0e0',
})

const InstructionsLabel = styled('span', {
    display: 'block',
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
    marginBottom: '4px',
})
