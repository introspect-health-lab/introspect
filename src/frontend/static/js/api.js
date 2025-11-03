// API functions for todo operations

/**
 * Fetch all todos for the current user
 * @returns {Promise<Array>} Array of todos
 */
async function fetchTodos() {
    const response = await authenticatedFetch('/todos/');
    
    if (!response.ok) {
        throw new Error('Failed to fetch todos');
    }
    
    return await response.json();
}

/**
 * Create a new todo
 * @param {object} todoData - Todo data
 * @returns {Promise<object>} Created todo
 */
async function createTodo(todoData) {
    const response = await authenticatedFetch('/todos/', {
        method: 'POST',
        body: JSON.stringify(todoData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create todo');
    }
    
    return await response.json();
}

/**
 * Update a todo
 * @param {string} todoId - Todo ID
 * @param {object} todoData - Updated todo data
 * @returns {Promise<object>} Updated todo
 */
async function updateTodo(todoId, todoData) {
    const response = await authenticatedFetch(`/todos/${todoId}`, {
        method: 'PUT',
        body: JSON.stringify(todoData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update todo');
    }
    
    return await response.json();
}

/**
 * Mark a todo as complete
 * @param {string} todoId - Todo ID
 * @returns {Promise<object>} Updated todo
 */
async function completeTodo(todoId) {
    const response = await authenticatedFetch(`/todos/${todoId}/complete`, {
        method: 'PUT'
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to complete todo');
    }
    
    return await response.json();
}

/**
 * Delete a todo
 * @param {string} todoId - Todo ID
 * @returns {Promise<void>}
 */
async function deleteTodo(todoId) {
    const response = await authenticatedFetch(`/todos/${todoId}`, {
        method: 'DELETE'
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to delete todo');
    }
}

