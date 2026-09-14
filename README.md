# CivicGrid AI

> **Turning citizen needs into smarter infrastructure investment decisions.**

CivicGrid AI is a multilingual AI-powered decision-support platform that transforms citizen infrastructure requests into evidence-based priorities for public investment.

It is **not a chatbot or complaint-management system**. CivicGrid AI helps policymakers understand **where infrastructure demand is highest, who is affected, and which interventions should be prioritized.**

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
AI Project Recommendation
Gemini extracts:
- Category
- Location
- Language
- Severity
- Population impact
- Infrastructure gap
- Vulnerability
- Summary
The backend enriches requests with district-level demographic context, calculates an explainable priority score, identifies demand hotspots, and generates infrastructure project recommendations.
📊 Current Features
- 🤖 Gemini-powered request extraction
- 📍 Location normalization & district mapping
- 🏘️ District demographic context
- 📈 Context-aware priority scoring
- 🔎 Explainable priority scoring
- 🗺️ Demand hotspot aggregation
- 💡 AI-generated infrastructure project recommendations
- 🔌 Django REST APIs
- 🧪 Automated tests
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
CivicGrid AI aims to build a scalable decision-support layer between citizen needs and public infrastructure investment.
🚧 Status
Active Development
Currently focused on building the AI-powered backend and decision-support foundation.
👨‍💻 Contributors
Prince Biswal
- Jagatjeet Swain
- Abhishek Mishra
- Shreyash Mishra