# Dog API App - DeployHub

A Flask web application that integrates with TheDogAPI and Supabase PostgreSQL to display and save dog images. Built as part of the IS2209 DevOps and CI/CD group project.

Live URL: https://flaskproject7-production.up.railway.app

---

## Team

- Isabel Sullivan (isabelxosullivan)
- Roisin (roisinxhealy)
- Cary Curran (caryscurran)

---

## Tech Stack

- Backend: Python 3.11, Flask
- Database: PostgreSQL via Supabase
- External API: TheDogAPI
- CI/CD: GitHub Actions
- Deployment: Railway
- Containerisation: Docker + Gunicorn

---

## Setup and Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/isabelxosullivan/FlaskProject7.git
cd FlaskProject7
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

```
DB_HOST=your_supabase_host
DB_PORT=5432
DB_NAME=postgres
DB_USER=your_supabase_user
DB_PASSWORD=your_supabase_password
DB_SSLMODE=require
DOG_API_KEY=your_thedogapi_key
```

### 5. Run the app
```bash
python app.py
```

App runs at http://127.0.0.1:5001

---

## Running with Docker
```bash
docker build -t dog-app .
docker run -p 8080:8080 --env-file .env dog-app
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/dog/view` | GET | View random dog from TheDogAPI and saved dogs |
| `/dog/save` | POST | Save a dog image URL to the database |
| `/dogs` | GET | View all saved dogs |
| `/health` | GET | Health check - checks DB connectivity |
| `/status` | GET | Status page with live diagnostics |

---

## Running Tests
```bash
python -m pytest test_app.py -v
```

Tests cover:
- Health endpoint reports dependencies
- Graceful degradation when external API is down
- Consolidated results from two sources
- Save dog success and failure cases
- Status and home endpoints

---

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and PR to main:

1. Lint - flake8 checks app.py
2. Test - pytest runs all tests
3. Build - Docker image is built

Secrets are stored in GitHub Actions secrets and never in code.

---

## Deployment

The app is deployed on Railway and automatically redeploys on every push to main.

Live URL: https://flaskproject7-production.up.railway.app

---

## Environment Variables

See `.env.example` for all required variables. For CI/CD, these are stored as GitHub Actions secrets.

---

## Project Structure

```
FlaskProject7/
├── app.py              # Main Flask application
├── test_app.py         # pytest tests
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions CI pipeline
└── templates/
    ├── index.html      # Home page
    ├── dog.html        # Dog viewer page
    ├── saved_dogs.html # Saved dogs grid
    ├── health.html     # Health check page
    └── status.html     # Status page
```
