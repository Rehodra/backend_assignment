# 🚀 Backend Assignment – FastAPI + React Full-Stack

A production-ready full-stack application featuring a FastAPI backend with JWT authentication, role-based access control, and a React/Vite frontend.

---

## 📁 Project Structure

```
backend_assignment/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py             # App entry point, CORS, Rate Limiting
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic settings (reads .env)
│   │   │   ├── security.py     # Password hashing, JWT utils
│   │   │   └── dependencies.py # FastAPI DI: auth, RBAC
│   │   ├── db/
│   │   │   ├── database.py     # Motor async MongoDB connection
│   │   │   └── indexes.py      # MongoDB index creation on startup
│   │   ├── models/
│   │   │   ├── user.py         # User document model
│   │   │   └── task.py         # Task document model
│   │   ├── schemas/
│   │   │   ├── user.py         # User request/response schemas
│   │   │   └── task.py         # Task request/response schemas
│   │   ├── routes/
│   │   │   ├── __init__.py     # Versioned API router (/api/v1)
│   │   │   ├── auth.py         # Auth endpoints (Register, Login)
│   │   │   ├── oauth.py        # Google OAuth Login
│   │   │   └── tasks.py        # Task CRUD endpoints
│   │   └── services/
│   │       ├── auth_service.py # Auth business logic
│   │       └── task_service.py # Task business logic
│   ├── gunicorn_conf.py        # Production Gunicorn config
│   ├── pyproject.toml          # UV project configuration
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                    # Local dev (gitignored)
│
└── frontend/                   # React/Vite application
    ├── src/
    │   ├── api/                # Axios instances & interceptors
    │   ├── context/            # AuthContext (JWT management)
    │   ├── pages/              # Login, Register, Dashboard
    │   ├── App.jsx             # Main routing
    │   └── main.jsx            # GoogleOAuthProvider setup
    ├── tailwind.config.js
    └── package.json
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.11+) |
| Database | MongoDB (Motor async driver) |
| Auth | JWT + Google OAuth (google-auth) |
| Security | BCrypt + Rate Limiting (SlowAPI) |
| Validation | Pydantic v2 (Strict Complexity) |
| Frontend | React + Vite + Tailwind CSS |
| Docs | Swagger UI (`/docs`), ReDoc (`/redoc`) |
| Process Mgmt | Gunicorn + Uvicorn Workers |

---
<table>
  <tr>
    <td colspan="2">
      <h3>Landing Page</h3>
     <img width="1466" height="659" alt="image" src="https://github.com/user-attachments/assets/1a194fd7-90bd-4f61-a106-8d4f92610064" />
      <p align="center"><em>Dashboard with admin and user features</em></p>
    </td>
  <tr>
    <td colspan="2">
     <img width="730" height="753" alt="image" src="https://github.com/user-attachments/assets/c89485b8-3cd5-4d69-afa4-70568169b39c" />
      <p align="center"><em>Login/Signin page with Google OAuth</em></p>
    </td>
  </tr>
</table>


## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- MongoDB running locally (`mongodb://localhost:27017`)
- Node.js 18+ (for frontend)

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
copy .env.example .env
# Edit .env with your MongoDB URI and a strong JWT_SECRET_KEY

# 5. Run the development server (Hot Reload)
uvicorn app.main:app --reload --port 8000

# 6. Run for Production (Scalable - Multiple Workers)
gunicorn -c gunicorn_conf.py app.main:app
```


The API will be available at:
- **API Base**: `http://localhost:8000/api/v1`
- **Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

---

## 🔐 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | ❌ | Register new user |
| POST | `/login` | ❌ | Login, get JWT tokens |
| POST | `/google` | ❌ | Google OAuth login |
| POST | `/refresh` | ❌ | Refresh access token |
| POST | `/logout` | ❌ | Revoke refresh token |
| GET | `/me` | ✅ User | Get current user profile |
| GET | `/users` | 🔒 Admin | List all users |
| PATCH | `/users/{id}/role` | 🔒 Admin | Change user role |


### Tasks (`/api/v1/tasks`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/tasks` | ✅ User | Create a task |
| GET | `/tasks` | ✅ User | List own tasks (admin: all tasks) |
| GET | `/tasks/{id}` | ✅ User | Get single task |
| PUT | `/tasks/{id}` | ✅ User | Update task |
| DELETE | `/tasks/{id}` | ✅ User | Delete task |

---



## 🏗 Architecture & Scalability

See [SCALABILITY.md](./SCALABILITY.md) for a detailed note on microservices, caching, and load balancing strategies.

### Key Design Decisions
- **Clean architecture**: Routes → Services → DB (each layer single-responsibility)
- **Async everything**: Motor async driver + FastAPI async handlers for max throughput
- **Token blacklist**: MongoDB TTL index auto-purges expired revoked tokens
- **RBAC via dependency injection**: `require_admin` guard composable on any route
- **API versioning**: All routes under `/api/v1`, ready to add `/api/v2`

---

## 📖 API Documentation

Interactive Swagger UI is auto-generated by FastAPI at `/docs`. Import `openapi.json` from `/openapi.json` into Postman for a full collection.

## Assignment by
 Mounasuvra  Banerjee
