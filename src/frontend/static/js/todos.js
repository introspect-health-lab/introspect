// Todos page functionality

let allTodos = [];
let currentFilter = 'all';

// Protect the page
requireAuth();

// Initialize the page
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserData();
    await loadTodos();
    setupEventListeners();
});

/**
 * Load and display user data
 */
async function loadUserData() {
    try {
        const userData = getUserData();
        if (userData) {
            document.getElementById('user-name').textContent = `${userData.first_name} ${userData.last_name}`;
        } else {
            await fetchUserData();
            const userData = getUserData();
            document.getElementById('user-name').textContent = `${userData.first_name} ${userData.last_name}`;
        }
    } catch (error) {
        console.error('Failed to load user data:', error);
    }
}

/**
 * Load todos from API
 */
async function loadTodos() {
    try {
        allTodos = await fetchTodos();
        renderTodos();
    } catch (error) {
        showToast('Failed to load todos', 'error');
        console.error(error);
    }
}

/**
 * Render todos based on current filter
 */
function renderTodos() {
    const container = document.getElementById('todos-container');
    const emptyState = document.getElementById('empty-state');
    
    let filteredTodos = allTodos;
    
    if (currentFilter === 'active') {
        filteredTodos = allTodos.filter(todo => !todo.is_completed);
    } else if (currentFilter === 'completed') {
        filteredTodos = allTodos.filter(todo => todo.is_completed);
    }
    
    if (filteredTodos.length === 0) {
        container.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
    }
    
    emptyState.classList.add('hidden');
    
    // Sort by priority (highest first) and then by due date
    filteredTodos.sort((a, b) => {
        if (a.is_completed !== b.is_completed) {
            return a.is_completed ? 1 : -1;
        }
        if (b.priority !== a.priority) {
            return b.priority - a.priority;
        }
        if (a.due_date && b.due_date) {
            return new Date(a.due_date) - new Date(b.due_date);
        }
        return 0;
    });
    
    container.innerHTML = filteredTodos.map(todo => createTodoCard(todo)).join('');
}

/**
 * Create HTML for a todo card
 */
function createTodoCard(todo) {
    const priorityColor = getPriorityColor(todo.priority);
    const priorityName = getPriorityName(todo.priority);
    const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.is_completed;
    
    return `
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition duration-150 p-6 ${todo.is_completed ? 'opacity-75' : ''} animate-fade-in">
            <div class="flex items-start justify-between">
                <div class="flex items-start space-x-4 flex-1">
                    <!-- Checkbox -->
                    <button 
                        onclick="toggleComplete('${todo.id}')" 
                        class="mt-1 flex-shrink-0 h-6 w-6 rounded-lg border-2 ${todo.is_completed ? 'bg-green-500 border-green-500' : 'border-gray-300 hover:border-blue-500'} flex items-center justify-center transition duration-150"
                    >
                        ${todo.is_completed ? '<svg class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>' : ''}
                    </button>
                    
                    <!-- Content -->
                    <div class="flex-1 min-w-0">
                        <p class="text-gray-900 font-medium ${todo.is_completed ? 'line-through text-gray-500' : ''} break-words">
                            ${escapeHtml(todo.description)}
                        </p>
                        
                        <!-- Meta Info -->
                        <div class="mt-2 flex flex-wrap items-center gap-3 text-sm">
                            <!-- Priority Badge -->
                            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${priorityColor}">
                                ${priorityName}
                            </span>
                            
                            <!-- Due Date -->
                            ${todo.due_date ? `
                                <span class="inline-flex items-center text-xs ${isOverdue ? 'text-red-600 font-medium' : 'text-gray-500'}">
                                    <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                    </svg>
                                    ${formatDate(todo.due_date)}
                                    ${isOverdue ? '(Overdue)' : ''}
                                </span>
                            ` : ''}
                            
                            <!-- Completed At -->
                            ${todo.completed_at ? `
                                <span class="inline-flex items-center text-xs text-green-600">
                                    <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                    </svg>
                                    Completed ${formatDate(todo.completed_at)}
                                </span>
                            ` : ''}
                        </div>
                    </div>
                </div>
                
                <!-- Actions -->
                <div class="flex items-center space-x-2 ml-4">
                    ${!todo.is_completed ? `
                        <button 
                            onclick="openEditModal('${todo.id}')" 
                            class="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-blue-50 transition duration-150"
                            title="Edit"
                        >
                            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                            </svg>
                        </button>
                    ` : ''}
                    <button 
                        onclick="deleteTodoItem('${todo.id}')" 
                        class="p-2 text-gray-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition duration-150"
                        title="Delete"
                    >
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Add todo form
    document.getElementById('add-todo-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleAddTodo(e);
    });
    
    // Edit todo form
    document.getElementById('edit-todo-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleEditTodo(e);
    });
}

/**
 * Handle add todo form submission
 */
async function handleAddTodo(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    const todoData = {
        description: document.getElementById('description').value,
        priority: parseInt(document.getElementById('priority').value),
        due_date: document.getElementById('due_date').value || null
    };
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="spinner mx-auto"></div>';
    
    try {
        const newTodo = await createTodo(todoData);
        allTodos.unshift(newTodo);
        renderTodos();
        form.reset();
        showToast('Todo created successfully!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
    }
}

/**
 * Toggle todo completion
 */
async function toggleComplete(todoId) {
    try {
        const updatedTodo = await completeTodo(todoId);
        const index = allTodos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            allTodos[index] = updatedTodo;
            renderTodos();
            showToast('Todo updated!', 'success');
        }
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Open edit modal
 */
function openEditModal(todoId) {
    const todo = allTodos.find(t => t.id === todoId);
    if (!todo) return;
    
    document.getElementById('edit-todo-id').value = todo.id;
    document.getElementById('edit-description').value = todo.description;
    document.getElementById('edit-priority').value = todo.priority;
    document.getElementById('edit-due-date').value = todo.due_date ? formatDateForInput(todo.due_date) : '';
    
    document.getElementById('edit-modal').classList.remove('hidden');
}

/**
 * Close edit modal
 */
function closeEditModal() {
    document.getElementById('edit-modal').classList.add('hidden');
}

/**
 * Handle edit todo form submission
 */
async function handleEditTodo(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    const todoId = document.getElementById('edit-todo-id').value;
    const todoData = {
        description: document.getElementById('edit-description').value,
        priority: parseInt(document.getElementById('edit-priority').value),
        due_date: document.getElementById('edit-due-date').value || null
    };
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="spinner mx-auto"></div>';
    
    try {
        const updatedTodo = await updateTodo(todoId, todoData);
        const index = allTodos.findIndex(t => t.id === todoId);
        if (index !== -1) {
            allTodos[index] = updatedTodo;
            renderTodos();
            closeEditModal();
            showToast('Todo updated successfully!', 'success');
        }
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
    }
}

/**
 * Delete a todo
 */
async function deleteTodoItem(todoId) {
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        await deleteTodo(todoId);
        allTodos = allTodos.filter(t => t.id !== todoId);
        renderTodos();
        showToast('Todo deleted successfully!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/**
 * Filter todos
 */
function filterTodos(filter) {
    currentFilter = filter;
    
    // Update button styles
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-blue-100', 'text-blue-700');
        btn.classList.add('text-gray-700', 'hover:bg-gray-100');
    });
    
    event.target.classList.remove('text-gray-700', 'hover:bg-gray-100');
    event.target.classList.add('bg-blue-100', 'text-blue-700');
    
    renderTodos();
}

