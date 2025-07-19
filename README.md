# Contact Management System

A full-stack web application for managing contacts with a modern React frontend and Flask backend.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete contacts
- **Search & Filter**: Real-time search and category filtering
- **Responsive Design**: Works on desktop and mobile devices
- **Form Validation**: Client-side and server-side validation
- **Auto-categorization**: Automatically categorizes contacts based on email domain
- **Modern UI**: Clean, intuitive interface with smooth animations

## Technologies Used

### Backend
- **Python** - Core programming language
- **Flask** - Web framework for API development
- **SQLAlchemy** - ORM for database management
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React** - JavaScript library for building user interfaces
- **Vite** - Fast build tool and development server
- **CSS3** - Modern styling with responsive design

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scriptsctivate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   ```bash
   python main.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

The frontend will run on `http://localhost:3000`

## API Endpoints

- `GET /contacts` - Get all contacts (with optional search and category filters)
- `POST /create_contact` - Create a new contact
- `PATCH /update_contact/<id>` - Update an existing contact
- `DELETE /delete_contact/<id>` - Delete a contact

## Features in Detail

### Contact Management
- Add new contacts with validation
- Edit existing contact information
- Delete contacts with confirmation
- View contact details with timestamps

### Search & Filter
- Real-time search across name and email
- Filter by contact categories
- Clear search and filter options
- Responsive search interface

### Auto-categorization
- Personal emails (Gmail, Yahoo, Hotmail) → Personal category
- Other email domains → Work category
- Manual category selection available

### Form Validation
- Required field validation
- Email format validation
- Phone number format validation
- Real-time error feedback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

