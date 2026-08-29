# Deployment & Infrastructure Guide

This guide details local execution and Cloud Run deployment readiness for VERDICT.

> **Status Notice**: VERDICT is fully containerized and Cloud Run deployment-ready. Live production deployment on Google Cloud Run has not been executed yet.

---

## Environment Configuration

Copy `.env.example` to `.env` in the root or `backend/` directory:

```bash
# Gemini API Key
GEMINI_API_KEY=your-gemini-api-key-here

# Google Cloud Project Configuration
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_REGION=us-central1
FIRESTORE_DATABASE_ID=(default)

# CORS / Network Configuration
CORS_ORIGINS=http://localhost:3000

# Frontend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Local Container Execution (Docker)

### Backend Container
```bash
cd backend
docker build -t verdict-backend .
docker run -p 8000:8000 --env-file ../.env verdict-backend
```

### Frontend Container
```bash
cd frontend
docker build -t verdict-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 verdict-frontend
```

---

## Cloud Run Deployment Readiness

To deploy the backend service to Google Cloud Run:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Submit build to Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/verdict-backend ./backend

# Deploy to Cloud Run
gcloud run deploy verdict-backend \
  --image gcr.io/YOUR_PROJECT_ID/verdict-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY,GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
```
