# nViteXtracter - Complete Setup Summary

## What's Been Built

### ✅ Design Documents (Approved-Ready)
- **PRD.md** - Product requirements with OneDrive-first storage, pluggable AI providers (Ollama/LM Studio/OpenAI/Gemini), auto-trigger flow
- **ARCHITECTURE.md** - System design with provider abstraction, Windows mail watcher, OneDrive Excel storage
- **DATA_SCHEMA.md** - 26 core fields + 4 optional job/link fields; arrays for skills/locations; monetary `offer_in_hand_lpa`
- **IMPLEMENTATION_ROADMAP.md** - 6-week plan with provider setup, auto-trigger in Week 4
- **README.md** - Quick start guide

### ✅ Python Service (Flask Bridge)
**Location:** `python-service/`

**Core Files:**
- `app.py` - Flask REST API with `/health` and `/extract` endpoints
- `ai_providers.py` - Provider abstraction (Ollama, LM Studio ready; OpenAI/Gemini stubs)
- `prompt_templates.py` - JSON extraction prompt with schema + normalization rules
- `validators.py` - JSON Schema validation + field normalization (phone, CTC/LPA, arrays→CSV)
- `excel_writer.py` - OneDrive Excel append with formatting, column widths, freeze panes
- `watcher.py` - Windows Outlook COM event listener for auto-trigger (pywin32)
- `run_sample.py` - CLI test harness to POST sample email
- `requirements.txt` - All dependencies (Flask, pandas, openpyxl, pywin32, etc.)

**Dev Scripts:**
- `dev_setup.ps1` - Creates venv and installs dependencies
- `dev_up.ps1` - Starts Flask app
- `dev_watcher.ps1` - Starts mail watcher
- `README.md` - Service-specific quick start

### ✅ Test Assets
- `tests/sample_emails/nvite_sample_1.txt` - Real nVite email sample
- `tests/expected_json/nvite_sample_1.json` - Expected extraction output

### ✅ Configuration Template
- `python-service/.env.example` - All config keys with defaults

---

## Key Design Decisions

### 1. Offer In Hand → Monetary (LPA)
- **Old:** `offers_in_hand` (boolean)
- **New:** `offer_in_hand_lpa` (float|null)
- **Normalization:** "32 Lacs" → 32.0, "32.5 LPA" → 32.5, "0" → null

### 2. Arrays for Skills & Locations
- **JSON:** `key_skills` and `location_preferred` are arrays
- **Excel:** Converted to CSV strings (e.g., "Python,React,AWS")
- **Prompt:** Returns arrays; validator handles conversion

### 3. OneDrive-First Storage
- **Primary:** Excel in OneDrive (required for AppSheet)
- **Dev:** Local path allowed for testing
- **Config:** `EXCEL_PATH` in `.env`

### 4. AI Provider Abstraction
- **Supported:** Ollama (default), LM Studio, OpenAI, Gemini
- **Selection:** `AI_PROVIDER` in `.env`
- **Local-first:** Privacy by default; cloud optional

### 5. Windows Auto-Trigger
- **Method:** Outlook COM events via pywin32
- **Rules:** `MATCH_FROM` (email/domain) + `MATCH_SUBJECT_KEYWORDS`
- **Fallback:** Manual button extraction on Mac/Web

---

## Quick Start Commands

### 1. Setup (One-time)
```powershell
cd c:\Users\pankaj.AP-WIN11-DT\projects\nViteXtracter\python-service

# Option A: Use setup script
./dev_setup.ps1

# Option B: Manual venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure
```powershell
# Copy template and edit
cp .env.example .env
notepad .env
```

**Essential .env settings:**
```ini
AI_PROVIDER=ollama
AI_MODEL=mistral
EXCEL_PATH=C:\Users\pankaj.AP-WIN11-DT\OneDrive\Documents\nViteXtracter\applications.xlsx
MATCH_FROM=@naukri.com,@linkedin.com
MATCH_SUBJECT_KEYWORDS=application,applied,candidate
```

### 3. Start Services
```powershell
# Terminal 1: Flask API
cd python-service
.\.venv\Scripts\Activate.ps1
python app.py

# Terminal 2: Health check
Invoke-RestMethod http://127.0.0.1:5000/health

# Terminal 3 (optional): Watcher
cd python-service
.\.venv\Scripts\Activate.ps1
python watcher.py
```

### 4. Test Extraction
```powershell
# With Flask running
cd python-service
.\.venv\Scripts\Activate.ps1
python run_sample.py
```

---

## Data Schema Highlights

### Core 26 Fields
1-5: Job (title, employer) + Candidate (name, designation, company)  
6-9: Experience (years, months) + CTC (current, expected)  
10-13: Location (current, preferred) + Past company + Notice period  
14-16: Education + University + Key skills  
17-19: DOB + Mobile + Email  
20: **Offer in hand (LPA)** ← NEW monetary field  
21-25: Metadata (ingested_at, email_subject, from_email, ai_provider, ai_model)  
26: Confidence score (future)

### Optional 4 Fields
27-28: Links (response_link, contact_details_link)  
29-30: Job header (job_applicants_count, job_posted_days)

---

## Next Steps (After Approval)

### Immediate (Week 1-2)
1. ✅ Design approved → **START HERE**
2. Confirm AI provider choice (Ollama recommended for local)
3. Install Ollama: `winget install Ollama.Ollama`
4. Pull model: `ollama pull mistral`
5. Run Flask service and test with sample email

### Phase 1 (Week 1)
- Build Outlook Add-in UI (Office.js)
- Create manifest.xml
- Sideload add-in

### Phase 2 (Week 2)
- Integrate add-in with Flask `/extract`
- Test end-to-end flow

### Phase 3 (Week 3-4)
- Enable watcher for auto-trigger
- Configure From/Subject rules
- Test with real nVite emails

### Phase 4 (Week 5-6)
- AppSheet configuration
- User training
- Production launch

---

## Troubleshooting

### Flask won't start
- Check venv activated: `.\.venv\Scripts\Activate.ps1`
- Check port 5000 not in use: `netstat -ano | findstr :5000`
- Check Python version: `python --version` (need 3.10+)

### Can't connect to Ollama
- Start Ollama service
- Test: `curl http://localhost:11434/api/tags`
- Check firewall

### Excel write fails
- Close Excel if file is open
- Check OneDrive path exists
- Check file permissions

### Watcher not triggering
- Outlook must be running (desktop, not web)
- Check `.env` rules match incoming emails
- Check watcher logs for errors

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTLOOK EMAIL (nVite)                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │
            ┌─────────────┴──────────────┐
            │                            │
            ▼                            ▼
   ┌────────────────┐         ┌──────────────────┐
   │  Manual Button │         │  Auto-Watcher    │
   │  (Office.js)   │         │  (pywin32 COM)   │
   └────────┬───────┘         └────────┬─────────┘
            │                          │
            └────────────┬─────────────┘
                         ▼
            ┌──────────────────────────┐
            │   Flask /extract         │
            │   (localhost:5000)       │
            └──────────┬───────────────┘
                       │
                       ▼
            ┌──────────────────────────┐
            │  AI Provider Layer       │
            │  - Ollama (default)      │
            │  - LM Studio             │
            │  - OpenAI/Gemini (opt)   │
            └──────────┬───────────────┘
                       │
                       ▼
            ┌──────────────────────────┐
            │  Validator + Normalizer  │
            │  - Arrays → CSV          │
            │  - LPA conversion        │
            │  - Phone/email format    │
            └──────────┬───────────────┘
                       │
                       ▼
            ┌──────────────────────────┐
            │  Excel Writer            │
            │  (OneDrive path)         │
            └──────────┬───────────────┘
                       │
                       ▼
            ┌──────────────────────────┐
            │  AppSheet Sync           │
            │  (No-code UI)            │
            └──────────────────────────┘
```

---

## File Structure

```
nViteXtracter/
├── PRD.md
├── ARCHITECTURE.md
├── DATA_SCHEMA.md
├── IMPLEMENTATION_ROADMAP.md
├── README.md
├── SETUP_SUMMARY.md              ← You are here
├── python-service/
│   ├── .env.example
│   ├── requirements.txt
│   ├── app.py
│   ├── ai_providers.py
│   ├── prompt_templates.py
│   ├── validators.py
│   ├── excel_writer.py
│   ├── watcher.py
│   ├── run_sample.py
│   ├── dev_setup.ps1
│   ├── dev_up.ps1
│   ├── dev_watcher.ps1
│   └── README.md
└── tests/
    ├── sample_emails/
    │   └── nvite_sample_1.txt
    └── expected_json/
        └── nvite_sample_1.json
```

---

## Status: ✅ Design Complete, Ready for Implementation

**Last Updated:** January 10, 2026  
**Version:** 1.0 (Python service scaffolded, venv verified)

---

**Next Action:** Install Ollama, configure `.env`, and test `/extract` with the sample email.
