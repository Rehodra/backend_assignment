import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiPrivate } from '../api/axios';
import { LogOut, Plus, Trash2, Edit2, CheckCircle2, Circle, Clock, Loader2 } from 'lucide-react';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(null);
  
  // Form State
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState('todo');
  const [priority, setPriority] = useState('medium');

  const fetchTasks = async () => {
    try {
      const res = await apiPrivate.get('/tasks?page=1&limit=50');
      setTasks(res.data.tasks);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setStatus('todo');
    setPriority('medium');
    setIsEditing(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await apiPrivate.put(`/tasks/${isEditing}`, { title, description, status, priority });
      } else {
        await apiPrivate.post('/tasks', { title, description, status, priority });
      }
      resetForm();
      fetchTasks();
    } catch (err) {
      console.error('Failed to save task', err);
    }
  };

  const handleEdit = (task) => {
    setIsEditing(task.id);
    setTitle(task.title);
    setDescription(task.description || '');
    setStatus(task.status);
    setPriority(task.priority);
  };

  const handleDelete = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      await apiPrivate.delete(`/tasks/${taskId}`);
      fetchTasks();
    } catch (err) {
      console.error('Failed to delete task', err);
    }
  };

  const toggleStatus = async (task) => {
    const newStatus = task.status === 'done' ? 'todo' : 'done';
    try {
      await apiPrivate.put(`/tasks/${task.id}`, { status: newStatus });
      fetchTasks();
    } catch (err) {
      console.error('Failed to toggle status', err);
    }
  };

  const priorityColors = {
    high: 'text-red-700 bg-red-50 border-red-200',
    medium: 'text-yellow-700 bg-yellow-50 border-yellow-200',
    low: 'text-blue-700 bg-blue-50 border-blue-200'
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl font-bold tracking-tight text-gray-900">TaskFlow</h1>
            <div className="flex items-center gap-4">
              <div className="text-sm font-medium text-gray-700 bg-gray-100 px-3 py-1 rounded-full">
                {user?.username} ({user?.role})
              </div>
              <button
                onClick={logout}
                className="flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors"
                title="Log out"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Form Section */}
        <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            {isEditing ? <Edit2 className="h-5 w-5 text-blue-500" /> : <Plus className="h-5 w-5 text-blue-500" />}
            {isEditing ? 'Edit Task' : 'Create New Task'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-4">
                 <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                  <input
                    required
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none transition-colors"
                    placeholder="E.g., Review PR #44"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description (Optional)</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none transition-colors resize-none"
                    placeholder="Add more details..."
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                   <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                  >
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div className="flex gap-3 pt-2">
              <button
                type="submit"
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500 transition-colors"
              >
                {isEditing ? 'Save Changes' : 'Create Task'}
              </button>
              {isEditing && (
                <button
                  type="button"
                  onClick={resetForm}
                  className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-gray-700 border border-gray-300 hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
              )}
            </div>
          </form>
        </section>

        {/* Task List Section */}
        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Tasks</h2>
          {loading ? (
             <div className="flex justify-center py-12">
               <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
             </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-xl border border-gray-100 border-dashed">
              <p className="text-gray-500 text-sm">No tasks found. Create one above to get started.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tasks.map(task => (
                <div key={task.id} className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow group flex flex-col h-full">
                  <div className="flex items-start justify-between mb-3">
                    <button 
                      onClick={() => toggleStatus(task)}
                      className="mt-0.5 flex-shrink-0 text-gray-400 hover:text-blue-500 transition-colors"
                    >
                      {task.status === 'done' ? (
                        <CheckCircle2 className="h-6 w-6 text-green-500" />
                      ) : task.status === 'in_progress' ? (
                         <Clock className="h-6 w-6 text-yellow-500" />
                      ) : (
                        <Circle className="h-6 w-6" />
                      )}
                    </button>
                    <div className="ml-3 flex-grow">
                      <h3 className={`font-medium text-gray-900 line-clamp-2 ${task.status === 'done' ? 'line-through text-gray-400' : ''}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className={`mt-1 text-sm text-gray-500 line-clamp-3 ${task.status === 'done' ? 'line-through opacity-70' : ''}`}>
                          {task.description}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <div className="mt-auto pt-4 flex items-center justify-between border-t border-gray-50">
                    <span className={`px-2 py-1 rounded-md text-xs font-medium border uppercase tracking-wider ${priorityColors[task.priority]}`}>
                      {task.priority}
                    </span>
                    
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => handleEdit(task)}
                        className="p-1.5 text-gray-400 hover:text-blue-600 rounded bg-gray-50 hover:bg-blue-50 transition-colors"
                        title="Edit"
                      >
                        <Edit2 className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => handleDelete(task.id)}
                        className="p-1.5 text-gray-400 hover:text-red-600 rounded bg-gray-50 hover:bg-red-50 transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

      </main>
    </div>
  );
}
