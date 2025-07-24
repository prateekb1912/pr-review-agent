# PR Review Agent

An intelligent AI-powered pull request review system that automatically analyzes GitHub pull requests and provides detailed code reviews using CrewAI and OpenAI.

## Architecture

The system consists of four main components:

1. **FastAPI Application** (`app/main.py`): REST API endpoints for submitting PR reviews and checking status
2. **Celery Worker** (`app/celery_app`): Background task processing
3. **CrewAI Agent** (`agent/`): AI-based agent to perform PR review
4. **Redis**: Message broker and storage for Celery task queue

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pr-review-agent
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This will start:

- FastAPI server on `http://localhost:8000`
- Celery worker for background processing
- Redis instance on port 6379

### 4. Submit a PR for Review

```bash
curl -X POST "http://localhost:8000/analyze-pr" \
     -H "Content-Type: application/json" \
     -d '{"pr_url": "https://github.com/:username/:repo/pull/:pr_number"}'
```

### 5. Check Review Status

```bash
# Get task status
curl "http://localhost:8000/status/{task_id}"

# Get review results
curl "http://localhost:8000/results/{task_id}"
```

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Redis

```bash
redis-server
```

### Run the Application

```bash
# Terminal 1: Start FastAPI server
uvicorn app.main:app --reload

# Terminal 2: Start Celery worker
celery -A app.celery_app worker --loglevel=info
```

## Configuration

The system uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `REDIS_URL`: Redis connection URL (defaults to `redis://localhost:6379/0`)

## How It Works

1. **PR Submission**: When a PR URL is submitted, the system creates a Celery task
2. **Code Analysis**: The CrewAI agent fetches the PR diff and analyzes the changes
3. **Review Generation**: Using GPT-4, the agent generates a comprehensive review covering:
   - Bug fixes needed
   - Logic errors
   - Style issues
   - Best practices
   - Security concerns
4. **Result Storage**: The review is stored in Redis and can be retrieved via the API

## Review Categories

The AI agent reviews pull requests across several categories:

- **Bug Fixes**: Identifies potential bugs and runtime errors
- **Logic Errors**: Finds logical flaws in the code
- **Style Issues**: Suggests code formatting and style improvements
- **Best Practices**: Recommends following language-specific best practices
- **Security Issues**: Identifies potential security vulnerabilities
- **Verdict**: Provides an overall recommendation (Approve/Needs Changes/Needs More Review)
