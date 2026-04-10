# KanMind Backend

A Django REST Framework backend for the KanMind Kanban board application. Provides API endpoints for user authentication, board management, task tracking, and commenting.

## Tech Stack

- Python 3.13
- Django 6.0
- Django REST Framework 3.17
- Token Authentication
- SQLite (development)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd KanMind-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
```

**Windows:**
```bash
env\Scripts\activate
```

**macOS/Linux:**
```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Log in with email and password |
| POST | `/api/logout/` | Log out (delete auth token) |
| GET | `/api/email-check/?email=<email>` | Check if email exists |

### Boards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List boards (author or member) |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/<id>/` | Retrieve a board |
| PATCH | `/api/boards/<id>/` | Update a board (author only) |
| DELETE | `/api/boards/<id>/` | Delete a board (author only) |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List tasks on own boards |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/<id>/` | Retrieve a task |
| PATCH | `/api/tasks/<id>/` | Update a task (author only) |
| DELETE | `/api/tasks/<id>/` | Delete a task (author only) |
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to current user |
| GET | `/api/tasks/reviewing/` | List tasks where current user is reviewer |

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/<id>/comments/` | List comments on a task |
| POST | `/api/tasks/<id>/comments/` | Create a comment |
| DELETE | `/api/tasks/<id>/comments/<id>/` | Delete a comment (author only) |

## Testing

```bash
python manage.py test
```

## Project Structure

```
KanMind-backend/
├── core/                  # Project settings, main URL config
├── auth_app/              # User registration, login, logout
│   └── api/               # Serializers, views, URLs, permissions
├── kanban_app/            # Boards, tasks, comments
│   └── api/               # Serializers, views, URLs, permissions
├── manage.py
├── requirements.txt
└── README.md
```

## Notes

- Authentication uses Token-based auth. Include the token in the `Authorization` header: `Token <your-token>`.
- CORS is configured for development. Adjust `CORS_ALLOW_ALL_ORIGINS` in `core/settings.py` for production.
- The database file (`db.sqlite3`) is excluded from version control via `.gitignore`.
