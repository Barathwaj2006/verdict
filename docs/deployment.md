# VERDICT Deployment Guide

This guide explains how to deploy VERDICT to Google Cloud Run and Firestore. The deployment architecture relies entirely on native Google Cloud services using Application Default Credentials, completely avoiding committed secrets.

## Prerequisites

1. [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install) installed and authenticated.
2. A Google Cloud Project with billing enabled.

## 1. Google Cloud Setup

Ensure your active project is selected:
```bash
gcloud config set project YOUR_PROJECT_ID
```

Enable required APIs:
```bash
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable aiplatform.googleapis.com # If using Vertex AI / Gemini
```

### Firestore
Ensure Firestore is running in **Native Mode**.
```bash
gcloud firestore databases create --location=nam5
```

## 2. Deploying the Backend (FastAPI)

The backend exposes the core Investigation Controller and SSE streams.

```bash
cd backend
gcloud run deploy verdict-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID,CORS_ORIGINS=*" \
  --set-secrets="GEMINI_API_KEY=projects/YOUR_PROJECT_ID/secrets/GEMINI_API_KEY:latest"
```
*Note: Replace `CORS_ORIGINS=*` with your specific frontend domain in production.*

## 3. Deploying the Frontend (Next.js)

The frontend is a standalone Next.js 14 application. It must be provided the backend URL via the `NEXT_PUBLIC_API_BASE_URL` environment variable.

```bash
cd frontend
gcloud run deploy verdict-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_BASE_URL=https://verdict-backend-XXXXX.a.run.app"
```

## 4. Local Testing with Emulators

VERDICT supports Google Cloud Emulators natively.
1. Start the Firestore emulator.
2. Run backend:
   ```bash
   cd backend
   export FIRESTORE_EMULATOR_HOST="127.0.0.1:8080"
   export GEMINI_API_KEY="your-api-key"
   uvicorn main:app --port 8000
   ```
3. Run frontend:
   ```bash
   cd frontend
   export NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000"
   npm run dev
   ```

## Security Best Practices
- The `.dockerignore` and `.gitignore` files strictly prevent `.env` secrets from entering the Docker image or the git repository.
- Always use Google Secret Manager for `GEMINI_API_KEY`.
- Google Cloud Run automatically assigns a service account; ensure this service account has the `Cloud Datastore User` role to access Firestore.
