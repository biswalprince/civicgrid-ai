# CivicGrid AI

> **Turning citizen needs into smarter infrastructure investment decisions.**

CivicGrid AI is a multilingual AI-powered decision-support platform that transforms citizen infrastructure requests into evidence-based priorities for public investment.

It is **not a chatbot or complaint-management system**.

CivicGrid AI helps policymakers understand:

- Where infrastructure demand is concentrated
- Who is affected
- How severe the need is
- What infrastructure gaps exist
- Which interventions should receive higher priority

---

## 🚀 How It Works

```text
Citizen Request
      ↓
Gemini AI
      ↓
Structured Request Data
      ↓
Location + District Context
      ↓
Infrastructure + Demographic Evidence
      ↓
Context-Aware Priority Scoring
      ↓
Demand Hotspots
      ↓
AI Project Recommendation
      ↓
Policymaker Dashboard


Gemini extracts structured information from citizen requests, including:
- Category
- Location
- Language
- Severity
- Population impact
- Infrastructure gap
- Vulnerability
- Summary
The backend then enriches the request with district-level context, calculates an explainable priority score, aggregates demand hotspots, and generates infrastructure project recommendations.
🤖 AI Pipeline
CivicGrid AI uses Google Gemini to convert unstructured citizen messages into structured infrastructure intelligence.
Citizen Text / Voice / Message
             ↓
       Gemini Processing
             ↓
    Structured Extraction
             ↓
      Request Database
             ↓
  Context & Evidence Layer
             ↓
       Priority Engine
             ↓
    Recommendation Engine

The AI layer is designed to support multilingual citizen input while keeping the final decision process explainable through structured scoring and supporting evidence.
📊 Decision-Support Features
🤖 Gemini-powered request extraction
Converts unstructured citizen requests into structured data.
📍 Location normalization
Maps citizen-provided locations to supported districts where possible.
🏘️ District demographic context
Adds district-level demographic information to provide additional context for prioritization.
📈 Context-aware priority scoring
Combines request-level factors with district context to calculate a priority score.
🔎 Explainable scoring
Priority results expose the contribution of:
- Severity
- Affected population
- Infrastructure gap
- Vulnerability
- Context multiplier
🗺️ Demand hotspots
Aggregates citizen requests by location to identify areas with concentrated infrastructure demand.
🏗️ Infrastructure indicators
Provides infrastructure coverage indicators that can contribute to identifying infrastructure gaps.
💡 AI project recommendations
Gemini generates potential infrastructure interventions based on the request, priority context, and available evidence.
📊 Policymaker dashboard
Provides an overview of:
- Total citizen requests
- High-priority requests
- Demand hotspots
- Infrastructure indicators
- Priority distribution
- District-level impact
- Infrastructure recommendations
🧠 Priority Model
CivicGrid AI uses a weighted scoring model based on four core factors:
Severity
Affected Population
Infrastructure Gap
Vulnerability

The weighting can vary by infrastructure category.
For example, the prototype currently supports category-aware weighting for:
Water
Roads
Sanitation

The resulting score is combined with contextual information such as district-level demographic characteristics.
Priority levels are currently interpreted as:
< 30       LOW
30 – 59    MEDIUM
60+        HIGH

The scoring system is designed to be transparent and explainable, rather than producing an opaque AI-only decision.
🏗️ Architecture
                    ┌──────────────────────┐
                    │   Citizen Requests   │
                    │   Text / Voice /     │
                    │      Messages        │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │      Gemini AI       │
                    │ Extraction /         │
                    │ Structuring          │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Django + DRF      │
                    │   Decision Engine    │
                    └──────────┬───────────┘
                               ↓
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
       Citizen Data      District Context   Infrastructure
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Priority Scoring    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Demand Hotspots +    │
                    │ AI Recommendations   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Policymaker Dashboard│
                    └──────────────────────┘

🛠️ Tech Stack
Backend
- Python
- Django
- Django REST Framework
- SQLite
AI
- Google Gemini
- google-genai
Frontend
- React
- Vite
- JavaScript / JSX
Visualization & UI
- Lucide React
- Tailwind CSS
Deployment
- Docker
- Gunicorn
- Google Cloud Run-ready container architecture
Development
- Git
- GitHub
- PowerShell
📁 Project Structure
civicgrid-ai/
│
├── civicgrid/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services/
│       ├── gemini_services.py
│       └── priority_service.py
│
├── civicgrid-frontend/
│   └── src/
│       ├── api/
│       ├── components/
│       └── pages/
│
├── Dockerfile
├── .dockerignore
├── manage.py
├── requirements.txt
└── README.md

⚙️ Run Locally
1. Clone the repository
git clone https://github.com/biswalprince/civicgrid-ai.git
cd civicgrid-ai

2. Create a virtual environment
Windows:
py -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Copy-Item .env.example .env

Add your Gemini API key to .env.
Never commit .env or expose your API key.
5. Run migrations
py manage.py migrate

6. Start the backend
py manage.py runserver

Backend:
http://127.0.0.1:8000/

Health check:
http://127.0.0.1:8000/api/health/

🐳 Run with Docker
Build the backend image:
docker build -t civicgrid-backend .

Run the container:
docker run --rm -p 8080:8080 --env-file .env civicgrid-backend

Health check:
http://127.0.0.1:8080/api/health/

The Docker image uses Gunicorn to serve Django and is structured for deployment to a serverless container platform such as Google Cloud Run.
🔌 API Endpoints
Health
GET /api/health/

Citizen Requests
GET /api/requests/

Request Details
GET /api/requests/<id>/

Priority Calculation
POST /api/requests/<id>/calculate-priority/

AI Recommendation
POST /api/requests/<id>/recommend/

Infrastructure Indicators
GET /api/infrastructure-indicators/

Dashboard Summary
GET /api/dashboard/summary/

☁️ Deployment Architecture
The backend is containerized and ready for serverless deployment.
Planned production architecture:
React Frontend
      ↓
Cloud Run
      ↓
Django REST API
      ↓
Gemini API
      ↓
Cloud SQL / PostgreSQL

The current hackathon prototype is locally runnable and Dockerized.
Google Cloud Run deployment is planned as the next deployment stage and is not currently claimed as a live deployment.
📊 Prototype Data
The current prototype uses development/demo data to demonstrate the decision-support pipeline.
Some infrastructure indicators are synthetic prototype values created for demonstrating the system and should not be interpreted as current government statistics.
District demographic context is based on the available prototype dataset and should not be interpreted as real-time demographic information.
A production version would integrate authoritative and regularly updated government datasets.
🌍 Vision
Citizen Needs
      +
Public Data
      +
AI
      ↓
Infrastructure Intelligence
      ↓
Better Investment Decisions

CivicGrid AI aims to provide a scalable decision-support layer between citizen needs and public infrastructure investment.
The initial prototype focuses on water infrastructure, with the architecture designed to extend to:
- Roads
- Schools
- Hospitals
- Sanitation
- Electricity
- Public transport
The longer-term vision is to support infrastructure planning across regions and, eventually, different countries and public-sector contexts.
🚧 Status
Active Hackathon Development
Current prototype includes:
- Gemini-powered request extraction
- Django REST backend
- Context-aware priority scoring
- District-level context
- Infrastructure indicators
- Demand hotspot aggregation
- AI project recommendations
- Policymaker dashboard
- Automated tests
- Dockerized backend
👨‍💻 Contributors
- Prince Biswal
- Jagatjeet Swain
- Abhishek Mishra
- Shreyash Mishra