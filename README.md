# CivicGrid AI

> **Turning citizen needs into smarter infrastructure investment decisions.**

CivicGrid AI is an AI-powered decision-support platform that transforms citizen infrastructure requests into evidence-based priorities for public investment.

It is **not a chatbot or complaint-management system**.

CivicGrid AI helps policymakers understand:

- Where infrastructure demand is concentrated
- Who is affected
- How severe the need is
- What infrastructure gaps exist
- Which requests should receive higher priority

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
AI Project Recommendations
      ↓
Policymaker Dashboard

Citizens submit infrastructure problems through the web interface.
Gemini analyzes the request and extracts structured information such as:
- Category
- Location
- Language
- Severity
- Affected population
- Infrastructure gap
- Vulnerability
- Summary
The backend then enriches the request with district context, calculates an explainable priority score, identifies demand hotspots, and generates potential infrastructure recommendations.
🤖 AI Pipeline
Citizen Text Request
        ↓
   Gemini Processing
        ↓
 Structured Extraction
        ↓
    Request Database
        ↓
 Context & Evidence
        ↓
   Priority Engine
        ↓
Recommendations

Google Gemini is used to convert unstructured citizen requests into structured infrastructure intelligence.
The AI layer is designed to support multilingual citizen input while keeping prioritization explainable through structured scoring and supporting evidence.
📊 Key Features
🤖 Gemini-Powered Request Extraction
Converts natural-language citizen requests into structured infrastructure data.
📝 Citizen Request Submission
Citizens can submit infrastructure problems directly through the web interface. Requests are analyzed by Gemini and automatically added to the policymaker request system.
📍 Location & District Context
Normalizes supported locations and enriches requests with district-level demographic context.
📈 Context-Aware Priority Scoring
Combines request-level factors with district context to calculate a priority score.
🔎 Explainable Scoring
Priority results expose the contribution of:
- Severity
- Affected population
- Infrastructure gap
- Vulnerability
- Context multiplier
🗺️ Demand Hotspots
Aggregates requests by location to identify areas with concentrated infrastructure demand.
🏗️ Infrastructure Indicators
Provides infrastructure indicators that can contribute to identifying infrastructure gaps.
💡 AI Project Recommendations
Gemini generates potential infrastructure interventions based on request details and available context.
📊 Policymaker Dashboard
Provides an overview of:
- Total citizen requests
- High-priority requests
- Demand hotspots
- Infrastructure indicators
- Priority distribution
- District-level impact
- AI recommendations
🧠 Priority Model
CivicGrid AI uses a weighted scoring model based on four core factors:
Severity
    +
Affected Population
    +
Infrastructure Gap
    +
Vulnerability
    ↓
Base Priority Score
    ↓
District Context
    ↓
Final Priority Score

The prototype currently interprets scores as:
Score	Priority
< 30	LOW
30 – 59	MEDIUM
60+	HIGH


The scoring system is designed to make prioritization transparent and explainable rather than relying on an opaque AI-only decision.
🏗️ Architecture
┌──────────────────────┐
│   Citizen Request    │
│        Text          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      Gemini AI       │
│ Extraction /         │
│ Structuring          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     Django + DRF     │
│   Decision Engine    │
└──────────┬───────────┘
           ↓
    ┌──────┼───────┐
    ↓      ↓       ↓
 Citizen  District  Infrastructure
  Data    Context    Indicators
    └──────┼───────┘
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
- Tailwind CSS
- Lucide React
Deployment
- Docker
- Gunicorn
- Render
Development
- Git
- GitHub
- Linux / PowerShell
🌐 Live Demo
Frontend
https://civicgrid-ai-frontend.onrender.com
Backend API
https://civicgrid-ai.onrender.com
Health Check
https://civicgrid-ai.onrender.com/api/health/
Source Code
https://github.com/biswalprince/civicgrid-ai
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
Never commit your .env file or expose your API key.
5. Run migrations
py manage.py migrate

6. Start the backend
py manage.py runserver

Backend:
http://127.0.0.1:8000/

Health check:
http://127.0.0.1:8000/api/health/

7. Start the frontend
cd civicgrid-frontend
npm install
npm run dev

🐳 Docker
Build the backend image:
docker build -t civicgrid-backend .

Run:
docker run --rm -p 8080:8080 --env-file .env civicgrid-backend

Health check:
http://127.0.0.1:8080/api/health/

The backend container uses Gunicorn and is deployed on Render.
🔌 API
Endpoint	Method	Purpose
/api/health/	GET	Backend health check
/api/requests/	GET / POST	List or submit citizen requests
/api/requests/<id>/	GET	Request details
/api/requests/<id>/recommend/	POST	Generate AI recommendation
/api/infrastructure-indicators/	GET	Infrastructure indicators
/api/dashboard/summary/	GET	Dashboard data


📊 Prototype Data
The current prototype uses development and demonstration data.
Some infrastructure indicators are synthetic prototype values intended to demonstrate the decision-support pipeline and should not be interpreted as current government statistics.
District demographic context uses a prototype dataset based on available Census 2011 baseline information and should not be interpreted as real-time demographic data.
A production implementation would integrate authoritative, regularly updated government datasets.
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

CivicGrid AI aims to provide a decision-support layer between citizen needs and public infrastructure investment.
The initial prototype focuses on infrastructure requests such as water-related needs, while the architecture can be extended to areas including:
- Roads
- Schools
- Healthcare
- Sanitation
- Electricity
- Public transport
The long-term goal is to support evidence-based infrastructure planning across regions and public-sector contexts.
🚧 Project Status
Active Hackathon Prototype
Current implementation includes:
- Gemini-powered request extraction
- Citizen request submission
- Django REST backend
- Context-aware priority scoring
- Explainable priority breakdown
- District-level context
- Infrastructure indicators
- Demand hotspot aggregation
- AI project recommendations
- Policymaker dashboard
- Dockerized backend
- Live frontend and backend deployment
👨‍💻 Contributors
- Prince Kumar Biswal
- Jagatjeet Swain
- Abhishek Mishra
- Shreyash Mishra