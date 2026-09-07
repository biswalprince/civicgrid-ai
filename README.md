# CivicGrid AI Backend

CivicGrid AI is a multilingual decision-support platform for turning citizen development requests into evidence-based infrastructure investment priorities. The first planned use case is water infrastructure, with an architecture intended to grow into other public-service domains.

## Current development status

The project currently contains only the backend foundation: Django, Django REST Framework, environment-based configuration, and a health-check endpoint. AI, maps, dashboards, authentication, and business logic are intentionally not implemented yet.

## Local setup

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create your local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Replace `DJANGO_SECRET_KEY` in `.env` with a secure random value before using the project outside local development.

5. Apply database migrations:

   ```powershell
   py manage.py migrate
   ```

## Run the server

```powershell
py manage.py runserver
```

The health endpoint is available at <http://127.0.0.1:8000/api/health/>.

## Run tests

```powershell
py manage.py test
```
