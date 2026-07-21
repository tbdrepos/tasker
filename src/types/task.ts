export type TaskStatus = 'todo' | 'doing' | 'done'
export type TaskPriorities = 'important' | 'normal' | 'trivial'
export const priorityStyle = {
  important: '#FA6868',
  normal: '#FACE68',
  trivial: '#5A9CB5',
}

export interface Task {
  id: string
  user_id: string
  title: string
  description: string
  priority: TaskPriorities
  status: TaskStatus
  created_at: string
}
