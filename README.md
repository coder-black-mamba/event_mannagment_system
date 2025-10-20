# 🎉 Event Management System

## 📋 Project Description
A comprehensive Event Management System built with Django that allows users to create, manage, and participate in events. This system provides a platform for event organizers to host events and for participants to discover and register for events that interest them.

## ✨ Key Features

### 🎯 User Management
- User registration and authentication
- Role-based access control (Admin, Organizer, Participant)
- User profiles with customizable information
- Secure password management

### 📅 Event Management
- Create and manage events
- Event categorization and search
- Event registration and ticketing
- Event scheduling and calendar integration

### 👥 User Profiles
- Personal information management
- Profile picture upload
- Event participation history
- Saved/favorite events

### 🔒 Security
- Secure authentication system
- Role-based permissions
- CSRF protection
- Secure file uploads

## 🛠️ Technical Stack
- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (Development), PostgreSQL (Production)
- **Authentication**: Django Allauth
- **Static Files**: WhiteNoise
- **Deployment**: Docker, Nginx, Gunicorn

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/event-management-system.git
   cd event-management-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## 📂 Project Structure
```
event_management_system/
├── accounts/            # User authentication and profiles
├── events/              # Event management
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── manage.py            # Django management script
└── requirements.txt     # Project dependencies
```

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact
For any inquiries, please contact [your-email@example.com](mailto:your-email@example.com)

---
*Last Updated: October 20, 2025*