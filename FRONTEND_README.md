# Introspect Frontend Documentation

## Overview

The Introspect system includes a web-based frontend for demonstration purposes, built with:
- **Jinja2 Templates** for server-side rendering
- **Tailwind CSS** (via CDN) for modern, utility-first styling
- **Vanilla JavaScript** with Fetch API for API communication
- **No build tools required** - everything works out of the box!

**Note**: The primary frontend for Introspect is designed to be a **Flutter mobile/web application**. This web frontend serves as a reference implementation and admin interface.

## Features

### 🎨 Modern UI/UX
- Clean, polished interface with smooth animations
- Responsive design that works on all devices
- Bootstrap-inspired components with Tailwind CSS
- Gradient backgrounds and modern card designs
- Smooth transitions and hover effects

### 🔐 Authentication
- **Sign Up**: Create a new account with email validation
- **Sign In**: Secure login with JWT tokens
- **Sign Out**: Clear session and redirect to sign-in
- **Protected Routes**: Automatic redirect if not authenticated
- **Session Management**: Token stored in localStorage

### ✅ Todo Management
- **Create Todos**: Add new todos with description, priority, and due date
- **View Todos**: See all your todos in a beautiful card layout
- **Edit Todos**: Update todo details with a modal form
- **Complete Todos**: Mark todos as complete with a single click
- **Delete Todos**: Remove todos with confirmation
- **Filter Todos**: View all, active, or completed todos
- **Priority Levels**: Normal, Low, Medium, High, Top with color-coded badges
- **Due Dates**: Optional due dates with overdue indicators
- **Smart Sorting**: Automatically sorted by completion status, priority, and due date

## Project Structure

```
src/frontend/
├── __init__.py
├── controller.py              # FastAPI routes for serving templates
├── static/
│   ├── css/
│   │   └── custom.css        # Custom styles and animations
│   └── js/
│       ├── utils.js          # Utility functions (toast, formatting, etc.)
│       ├── auth.js           # Authentication management
│       ├── api.js            # API calls for todos
│       └── todos.js          # Todo page functionality
└── templates/
    ├── base.html             # Base template with Tailwind CSS
    ├── index.html            # Landing page
    ├── signin.html           # Sign in page
    ├── signup.html           # Sign up page
    └── todos.html            # Todo dashboard
```

## Routes

### Frontend Routes
- `/` - Landing page (redirects to /todos if authenticated)
- `/signin` - Sign in page
- `/signup` - Sign up page
- `/todos` - Todo dashboard (protected)

### API Routes (unchanged)
- `POST /auth/` - Register new user
- `POST /auth/token` - Login and get JWT token
- `GET /users/me` - Get current user info
- `GET /todos/` - Get all todos for current user
- `POST /todos/` - Create new todo
- `GET /todos/{id}` - Get specific todo
- `PUT /todos/{id}` - Update todo
- `PUT /todos/{id}/complete` - Mark todo as complete
- `DELETE /todos/{id}` - Delete todo

## Form Design

### Modern Form Features
All forms include:
- **Rounded corners** (rounded-xl) for a softer, modern look
- **Icon prefixes** for visual context
- **Smooth focus states** with ring effects
- **Gradient buttons** with hover animations
- **Proper spacing** and padding for comfort
- **Responsive design** that works on mobile
- **Loading states** with spinners during API calls
- **Error handling** with toast notifications

### Add Todo Form
- **Description**: Multi-line textarea with placeholder
- **Priority**: Dropdown with 5 levels (Normal, Low, Medium, High, Top)
- **Due Date**: DateTime picker for optional deadlines
- **Submit Button**: Gradient button with icon and hover effect

### Edit Todo Modal
- Same fields as Add Todo form
- Appears as a centered modal overlay
- Pre-filled with current todo data
- Cancel and Save buttons

## JavaScript Architecture

### utils.js
- `showToast()` - Display notifications
- `formatDate()` - Format dates for display
- `formatDateForInput()` - Format dates for input fields
- `getPriorityColor()` - Get Tailwind classes for priority badges
- `getPriorityName()` - Get priority display name
- `escapeHtml()` - Prevent XSS attacks

### auth.js
- `signIn()` - Authenticate user and store token
- `signUp()` - Register new user
- `signOut()` - Clear session and redirect
- `getAuthToken()` - Retrieve stored token
- `isAuthenticated()` - Check if user is logged in
- `authenticatedFetch()` - Make authenticated API requests
- `requireAuth()` - Protect pages from unauthenticated access

### api.js
- `fetchTodos()` - Get all todos
- `createTodo()` - Create new todo
- `updateTodo()` - Update existing todo
- `completeTodo()` - Mark todo as complete
- `deleteTodo()` - Delete todo

### todos.js
- Page initialization and event handling
- Todo rendering and filtering
- Modal management
- Form submission handling

## Styling Details

### Color Scheme
- **Primary**: Blue (500-600) to Indigo (600-700) gradients
- **Success**: Green (500)
- **Error**: Red (500)
- **Warning**: Orange/Yellow (for priorities)
- **Neutral**: Gray scale for text and backgrounds

### Typography
- **Headings**: Bold, extrabold weights
- **Body**: Regular weight, gray-900 for primary text
- **Secondary**: Gray-600 for less important text

### Spacing
- Consistent use of Tailwind spacing scale
- Generous padding in cards and forms
- Proper gap between elements

### Shadows
- `shadow-lg` for cards
- `shadow-xl` for hover states
- `shadow-2xl` for modals

### Animations
- Fade in for page loads
- Slide in for toasts and modals
- Smooth transitions on all interactive elements
- Transform effects on hover

## Usage

### Running the Application

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   uvicorn src.main:app --reload
   ```

3. **Open your browser**:
   Navigate to `http://localhost:8000`

### First Time Setup

1. Click "Get Started" or "Sign Up"
2. Fill in your details (first name, last name, email, password)
3. Click "Create account"
4. Sign in with your credentials
5. Start creating todos!

### Creating a Todo

1. In the left sidebar, fill in the "Add New Todo" form
2. Enter a description (required)
3. Select a priority (default: Medium)
4. Optionally set a due date
5. Click "Add Todo"

### Managing Todos

- **Complete**: Click the checkbox next to a todo
- **Edit**: Click the edit icon (only for active todos)
- **Delete**: Click the trash icon
- **Filter**: Use the All/Active/Completed tabs

## Browser Compatibility

The frontend works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **No build step**: Uses Tailwind CDN for instant development
- **Minimal JavaScript**: Only ~500 lines of vanilla JS
- **Fast rendering**: Client-side rendering with efficient DOM updates
- **Optimized assets**: Small CSS and JS files

## Security

- **XSS Protection**: All user input is escaped before rendering
- **CSRF Protection**: JWT tokens in Authorization headers
- **Secure Storage**: Tokens stored in localStorage (consider httpOnly cookies for production)
- **Input Validation**: Client-side and server-side validation

## Future Enhancements

Potential improvements:
- [ ] Add todo categories/tags
- [ ] Implement search functionality
- [ ] Add todo sharing between users
- [ ] Dark mode toggle
- [ ] Drag-and-drop reordering
- [ ] Recurring todos
- [ ] Todo attachments
- [ ] Export todos to CSV/JSON
- [ ] Progressive Web App (PWA) support
- [ ] Offline support with Service Workers

## Troubleshooting

### Styles not loading
- Check that `/static` route is properly mounted
- Verify Tailwind CDN is accessible
- Check browser console for errors

### API calls failing
- Ensure backend is running on port 8000
- Check that database is connected
- Verify JWT token is valid (check localStorage)

### Forms not submitting
- Check browser console for JavaScript errors
- Verify all required fields are filled
- Check network tab for API responses

## Contributing

When adding new features:
1. Follow the existing code structure
2. Use Tailwind utility classes for styling
3. Add proper error handling
4. Include loading states for async operations
5. Test on mobile devices
6. Update this documentation

## License

Same as the main project.

