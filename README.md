# LinkedIn Profile Finder - Production-Grade Web App

An AI-powered platform for discovering qualified LinkedIn prospects through automated ICP (Ideal Customer Profile) and buyer persona generation.

## 🚀 Features

- **AI-Powered Website Analysis**: Automatically crawls and understands business websites
- **ICP Generation**: Creates detailed Ideal Customer Profiles using Claude AI
- **Persona Builder**: Interactive interface to create and edit buyer personas
- **LinkedIn Discovery**: Legal search-engine-based profile discovery
- **Smart Scoring**: AI-powered relevance scoring with full explainability
- **CRM Integration**: Export to HubSpot, Salesforce, or CSV
- **Async Processing**: Scales to handle 100+ concurrent jobs
- **Learning Loop**: Continuously improves from user feedback

## 🏗️ Architecture

### Monorepo Structure
```
linkedin-profile-founder/
├── apps/
│   ├── frontend/          # Next.js 14 + TypeScript + Tailwind
│   └── backend/           # FastAPI + PostgreSQL + Redis
├── packages/              # Shared packages (future)
└── docker-compose.yml     # Local development setup
```

### Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query (TanStack Query)
- Zustand (State Management)
- Recharts (Data Visualization)

**Backend:**
- FastAPI (Python)
- PostgreSQL (Database)
- Redis (Caching & Queues)
- Celery (Async Tasks)
- SQLAlchemy (ORM)
- Playwright (Web Scraping)
- Anthropic Claude (AI)

## 📋 Prerequisites

- Node.js 18+ and pnpm 8+
- Python 3.11+
- Docker and Docker Compose
- Anthropic API key
- Google Custom Search API key (for LinkedIn discovery)

## 🛠️ Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Install Node dependencies
pnpm install

# Install Python dependencies
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Start Infrastructure Services

```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3. Configure Environment Variables

**Backend (.env):**
```bash
cd apps/backend
cp .env.example .env

# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY
# - GOOGLE_API_KEY
# - GOOGLE_CSE_ID
# - SECRET_KEY (generate with: openssl rand -hex 32)
```

**Frontend (.env.local):**
```bash
cd apps/frontend
cp .env.example .env.local

# Default values should work for local development
```

### 4. Initialize Database

```bash
cd apps/backend

# Run migrations (creates all tables)
alembic upgrade head
```

### 5. Start Development Servers

**Terminal 1 - Backend API:**
```bash
cd apps/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
cd apps/backend
source venv/bin/activate
celery -A app.core.celery_app worker --loglevel=info
```

**Terminal 3 - Frontend:**
```bash
cd apps/frontend
pnpm dev
```

**Optional - Flower (Celery Monitor):**
```bash
cd apps/backend
celery -A app.core.celery_app flower --port=5555
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Flower Monitor**: http://localhost:5555

## 🎯 Usage

### Quick Start

1. **Register**: Create an account at http://localhost:3000
2. **Login**: Sign in to access the dashboard
3. **Create Job**: Enter a business website URL
4. **Review ICP**: Wait for AI to generate ICP and personas
5. **Edit Personas**: Customize personas as needed
6. **Run Discovery**: Trigger LinkedIn profile search
7. **Review Results**: Filter and score candidates
8. **Export**: Download as CSV or push to CRM

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user

#### Jobs
- `POST /api/jobs` - Create new discovery job
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{job_id}` - Get job details

#### ICPs & Personas
- `GET /api/icps/{icp_id}` - Get ICP
- `PATCH /api/icps/{icp_id}` - Update ICP
- `POST /api/personas` - Create persona
- `PATCH /api/personas/{id}` - Update persona
- `DELETE /api/personas/{id}` - Delete persona

#### Candidates
- `GET /api/candidates/job/{job_id}` - List candidates with filters
- `GET /api/candidates/{id}` - Get candidate details

#### Discovery
- `POST /api/discovery/{job_id}/run` - Run discovery process

#### Exports
- `POST /api/exports/csv/{job_id}` - Export to CSV
- `POST /api/exports/hubspot/{job_id}` - Export to HubSpot

## 🏭 Production Deployment

### Environment Variables

Set these in your production environment:

```bash
# Backend
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=<strong-secret-key>
ANTHROPIC_API_KEY=<your-key>
GOOGLE_API_KEY=<your-key>
SENTRY_DSN=<your-sentry-dsn>
ENVIRONMENT=production
DEBUG=False

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## 📚 Project Structure

### Backend Services

- **Crawler Service**: Web scraping with Playwright
- **NLP Service**: Text analysis with Claude AI
- **ICP Generator**: Automated ICP and persona creation
- **Discovery Service**: LinkedIn profile search
- **Scoring Service**: Candidate ranking with explainability
- **Export Service**: CRM integrations

### Database Schema

- `users` - User accounts
- `jobs` - Discovery jobs
- `icps` - Ideal Customer Profiles
- `personas` - Buyer personas
- `candidates` - Found LinkedIn profiles
- `feedbacks` - User feedback for learning loop

## 🔒 Security

- JWT token-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention (SQLAlchemy)
- XSS protection (React)
- Environment variable secrets

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres
```

### Celery Not Processing Tasks
```bash
# Check Redis connection
docker-compose logs redis

# Restart Celery worker
pkill -f celery
celery -A app.core.celery_app worker --loglevel=info
```

### Frontend Build Errors
```bash
# Clear Next.js cache
rm -rf apps/frontend/.next
pnpm build
```

---

Built with modern web technologies for production-grade performance