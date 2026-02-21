# Monagent 🚀

> **Lead generation + business logic integrated in one FastAPI monorepo**

Monagent is a modern, scalable API service built for the Monynha ecosystem, designed to handle lead generation, business integrations, and future AI capabilities. Built with FastAPI and Supabase for high performance and reliability.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
- [Running the Application](#-running-the-application)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## ✨ Features

- **Lead Management**: Capture and manage leads with rich metadata
- **UTM Tracking**: Full support for marketing campaign tracking (source, medium, campaign, content, term)
- **IP & User Agent Logging**: Automatic capture of client information
- **Supabase Integration**: Secure database operations with Row Level Security (RLS)
- **RESTful API**: Clean, well-documented endpoints
- **Health Monitoring**: Built-in health check endpoint
- **Type Safety**: Full Pydantic validation for data integrity
- **Email Validation**: Built-in email validation with Pydantic
- **Modular Architecture**: Easy to extend with new modules

---

## 🛠 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) 0.129.x
- **Database**: [Supabase](https://supabase.com/) 2.28.x (PostgreSQL)
- **Python**: 3.13+
- **Validation**: Pydantic 2.12.x with email support
- **Server**: Uvicorn 0.41.x
- **HTTP Client**: HTTPX 0.28.x
- **Development Tools**:
  - pytest 9.x (testing)
  - pytest-asyncio (async testing)
  - ruff (linting)
  - mypy (type checking)

---

## 📁 Project Structure

```
monagent/
├── src/
│   └── monagent/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── app.py              # FastAPI application
│       ├── core/
│       │   ├── __init__.py
│       │   ├── settings.py         # Application settings
│       │   └── supabase_client.py  # Supabase client factory
│       └── modules/
│           └── leads/
│               ├── __init__.py
│               ├── router.py       # Lead endpoints
│               └── service.py      # Lead business logic
├── scripts/
│   └── lead.sql                    # Database schema
├── tests/                          # Test directory
├── docs/                           # Documentation
├── pyproject.toml                  # Project configuration
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

**Option 1: Python (Development)**
- Python 3.13 or higher
- [Poetry](https://python-poetry.org/) (recommended) or pip
- A Supabase project ([create one here](https://supabase.com))

**Option 2: Docker (Production/Quick Start)**
- [Docker](https://www.docker.com/get-started) 20.10+ 
- [Docker Compose](https://docs.docker.com/compose/install/) 2.0+ (optional but recommended)
- A Supabase project ([create one here](https://supabase.com))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/marcelo-m7/Monagent.git
cd Monagent
```

2. **Install dependencies**

Using Poetry (recommended):
```bash
poetry install
```

Or using pip:
```bash
pip install -e .
```

3. **Install development dependencies** (optional)

```bash
poetry install --with dev
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Environment
ENV=dev

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_SCHEMA=monagent
```

> ⚠️ **Security Note**: Never commit your `.env` file or expose your service role key publicly.

### Database Setup

1. **Create the schema and table** in your Supabase project:

Run the SQL script from [scripts/lead.sql](scripts/lead.sql) in your Supabase SQL editor:

```sql
-- Creates monagent schema
-- Creates leads table with all necessary fields
-- Sets up unique email constraint
-- Adds performance indexes
-- Enables Row Level Security (RLS)
```

The script creates:
- `monagent` schema
- `leads` table with fields: id, email, name, company, pain, source, campaign, medium, content, term, ip, user_agent, status, notes
- Unique constraint on email (case-insensitive)
- Indexes for performance optimization
- Row Level Security enabled

---

## 🏃 Running the Application

### Development Mode

```bash
# Using Poetry
poetry run uvicorn monagent.api.app:app --reload

# Or using Python directly
python -m uvicorn monagent.api.app:app --reload
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn monagent.api.app:app --host 0.0.0.0 --port 8000
```

### Docker Deployment (Recommended for Production)

**Build and run with Docker:**

```bash
# Build the image
docker build -t monagent:latest .

# Run the container
docker run -d \
  --name monagent-api \
  -p 8000:8000 \
  --env-file .env \
  monagent:latest
```

**Or use Docker Compose:**

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Production considerations:**
- The Docker image uses multi-stage builds for smaller size
- Runs with 4 Uvicorn workers for better performance
- Includes health checks for container orchestration
- Runs as non-root user for security
- Uses Python 3.13 slim image

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "data": "Hi World! :D s2",
  "status": "ok"
}
```

---

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `POST /leads`

Create a new lead.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "company": "Acme Inc",
  "pain": "Need better lead management",
  "source": "monynha.com",
  "campaign": "summer_campaign",
  "medium": "email",
  "content": "newsletter",
  "term": "lead management"
}
```

**Response:**
```json
{
  "created": true,
  "lead_id": "uuid-here"
}
```

**Auto-captured fields:**
- `ip`: Client IP address
- `user_agent`: Browser/client user agent
- `created_at`: Timestamp (server-side)
- `status`: Default "new"

---

## � Deployment

### Docker (Recommended)

The project includes production-ready Docker configuration files.

**Quick Start:**

```bash
# Build the image
docker build -t monagent:latest .

# Run with environment variables
docker run -d \
  --name monagent-api \
  -p 8000:8000 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_ANON_KEY=your-key \
  -e SUPABASE_SERVICE_ROLE_KEY=your-service-key \
  -e SUPABASE_SCHEMA=monagent \
  monagent:latest
```

**Using Docker Compose (Easier):**

```bash
# Ensure .env file is configured first
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f monagent

# Stop
docker-compose down
```

**Docker Features:**
- ✅ Multi-stage build for optimized image size
- ✅ Runs with 4 Uvicorn workers for production load
- ✅ Built-in health checks for container orchestration
- ✅ Non-root user for enhanced security
- ✅ Python 3.13 slim base image
- ✅ Automatic restart on failure

### Cloud Platforms

**Deploy to Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Deploy to Fly.io:**
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Launch and deploy
fly launch
fly deploy
```

**Deploy to Render:**
1. Connect your GitHub repository
2. Select "Docker" as environment
3. Add environment variables
4. Deploy

### Environment Variables for Production

Ensure these are properly set in your deployment:

```env
ENV=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_SCHEMA=monagent
```

---

## �💻 Development

### Code Quality

Run linting:
```bash
poetry run ruff check .
```

Run type checking:
```bash
poetry run mypy src/
```

Auto-fix linting issues:
```bash
poetry run ruff check --fix .
```

### Project Configuration

The project uses `pyproject.toml` for all configuration, following modern Python best practices with Poetry as the build backend.

---

## 🧪 Testing

Run tests with pytest:

```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=monagent
```

Run async tests:
```bash
poetry run pytest -v
```

---

## 🗺️ Roadmap

- [x] Lead management API
- [x] Supabase integration
- [x] UTM tracking support
- [ ] Admin panel for lead management
- [ ] Email notifications
- [ ] CRM integrations (HubSpot, Salesforce)
- [ ] AI-powered lead scoring
- [ ] Webhook support
- [ ] Analytics dashboard
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is part of the Monynha ecosystem.

---

## 👏 Credits

**Developed by:**  
**Marcelo Santos**

- GitHub: [@marcelo-m7](https://github.com/marcelo-m7)
- Email: [marcelo@monynha.com](mailto:marcelo@monynha.com)

---

## 📞 Support

For support and questions:
- Email: marcelo@monynha.com
- Open an issue on GitHub

---

Made with ❤️ by [Marcelo Santos](https://github.com/marcelo-m7) for the Monynha ecosystem.
