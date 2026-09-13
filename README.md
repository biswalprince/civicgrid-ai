
CivicGrid AI is a multilingual AI-powered decision-support platform that transforms citizen infrastructure requests into evidence-based priorities for public investment.

It is **not a chatbot or complaint-management system**. The goal is to help policymakers understand **where infrastructure demand is highest, who is affected, and where limited resources should be invested first.**

---

## 🚀 How It Works

```text
Citizen Request
      ↓
Gemini AI
      ↓
Structured Data
      ↓
Location + District Context
      ↓
Priority Scoring
      ↓
Demand Hotspots
      ↓
Future: Project Recommendations

Gemini extracts:
- Category
- Location
- Language
- Severity
- Population impact
- Infrastructure gap
- Vulnerability
- Summary
The backend then enriches the request with district-level demographic context and calculates a priority score.
📊 Current Features
- 🤖 Gemini-powered request extraction
- 📍 Location normalization & district mapping
- 🏘️ District demographic context
- 📈 Context-aware priority scoring
- 🗺️ Demand hotspot aggregation
- 🔌 Django REST APIs
- 🧪 Django test framework
Priority Model
Severity              × 4
Affected Population   × 3
Infrastructure Gap    × 2
Vulnerability         × 1
Priority levels:
< 30       LOW
30 – 59    MEDIUM
60+        HIGH
🛠️ Tech Stack
Backend: Python · Django · Django REST Framework · SQLite
AI: Google Gemini · google-genai
Development: Git · GitHub · PowerShell
Planned: Google Cloud Run · BigQuery · Firebase · Maps
⚙️ Run Locally
git clone https://github.com/biswalprince/civicgrid-ai.git
cd civicgrid-ai

py -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env
Add your Gemini API key to .env, then:
py manage.py migrate
py manage.py runserver
API:
http://127.0.0.1:8000/
Health check:
http://127.0.0.1:8000/api/health/
Run tests:
py manage.py test
🗺️ Roadmap
- Gemini request extraction
- Priority scoring
- District demographic context
- Demand hotspots
- Explainable scoring
- Infrastructure datasets
- AI project recommendations
- Policymaker dashboard
- Multilingual & voice input
- Cloud deployment
- Expansion to more regions and infrastructure domains
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
      ↓
Better Public Services
CivicGrid AI aims to build a scalable decision-support layer between citizen needs and public infrastructure investment.
🚧 Status
Active Development
Currently focused on the Django backend and AI-powered decision-support foundation.
👨‍💻 Author
Prince Biswal
