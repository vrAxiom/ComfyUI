# nViteXtracter - Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** January 10, 2026  
**Status:** Draft - Awaiting Approval  
**Project Type:** Outlook Add-in with Local AI Processing

---

## Executive Summary

**nViteXtracter** is a zero-cost, privacy-first Outlook Add-in that automatically extracts structured candidate data from job application emails using local AI (Ollama/LM Studio) or optional cloud AI (OpenAI/Gemini), writes to an Excel file in OneDrive, and syncs with AppSheet for recruitment workflow management.

### Key Value Propositions
- ✅ **Zero AI Runtime Costs** - Uses locally hosted Ollama (Mistral/LLaMA)
- ✅ **Privacy Compliant** - All AI processing happens locally
- ✅ **No Licensing Fees** - Open-source stack
- ✅ **AppSheet Ready** - Clean, structured data output
- ✅ **Production Grade** - Schema-enforced JSON validation
- ✅ **OneDrive-first** - Excel stored in OneDrive by default
- ✅ **Pluggable AI** - Local or cloud provider via config

---

## Problem Statement

Manual candidate data entry from job application emails is:
- Time-consuming (5-10 minutes per application)
- Error-prone (typos, missed fields)
- Not scalable (100+ applications = hours of work)
- Delays recruitment pipeline visibility

**Current Pain Points:**
- Copy-paste between email → spreadsheet → ATS
- Inconsistent data formats
- No centralized candidate database
- Difficult to track application status

---

## Solution Architecture

### High-Level System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      OUTLOOK EMAIL (User Reads)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              OUTLOOK ADD-IN (Office.js in Browser)              │
│  - Button: "Extract Candidate"                                  │
│  - Reads email body using Office.context.mailbox.item.body     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP POST
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│         LOCAL PYTHON SERVICE (Flask - localhost:5000)           │
│  - Receives email text                                          │
│  - Constructs AI prompt with schema                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP Request
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               AI PROVIDER LAYER (Configurable)                   │
│  - Local: Ollama (11434) or LM Studio (OpenAI-compatible)       │
│  - Cloud: OpenAI (gpt-4.x) or Gemini (1.5)                      │
│  - Returns strict JSON                                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ JSON Response
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              PYTHON SERVICE (Data Validation)                   │
│  - Validates JSON against schema                                │
│  - Normalizes arrays (skills, locations)                        │
│  - Adds metadata (timestamp, source)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Write
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│        EXCEL FILE (OneDrive primary; SharePoint optional)       │
│  - Sheet: "Applications"                                        │
│  - Append-only mode                                             │
│  - Structured columns matching schema                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ Auto-Sync
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   APPSHEET (No-Code Frontend)                   │
│  - Real-time dashboard                                          │
│  - Candidate pipeline views                                     │
│  - Status tracking workflows                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technical Architecture

### Component Breakdown

#### 1. **Outlook Add-in (Frontend)**
- **Technology:** Plain JavaScript + Office.js
- **Hosting:** Office Add-in Manifest (XML)
- **UI:** Minimal taskpane with single button
- **Permissions:** `ReadWriteItem` (email body access only)

**Key Files:**
- `manifest.xml` - Add-in configuration and permissions
- `taskpane.html` - Simple UI (button, status display)
- `taskpane.js` - Office.js integration logic
- `assets/` - Icons and branding

**Why Not React/Angular?**
- Unnecessary complexity for a single-button UI
- Faster load times
- Easier debugging
- Lower maintenance overhead

---

#### 2. **Local Python Bridge Service (Backend)**
- **Technology:** Flask (lightweight HTTP server)
- **Port:** 5000 (localhost only)
- **Purpose:** Bridge between browser-based add-in and local Ollama

**Key Responsibilities:**
1. Receive email text via POST `/extract`
2. Construct AI prompt with schema enforcement
3. Call AI provider via provider abstraction (Ollama/LM Studio/OpenAI/Gemini)
4. Validate and clean JSON response
5. Write to Excel with error handling
6. Return success/failure status

**Dependencies:**
```txt
flask==3.0.0
requests==2.31.0
pandas==2.1.4
openpyxl==3.1.2
flask-cors==4.0.0
python-dotenv==1.0.1
pywin32==306
```

---

#### 3. **AI Provider Layer (Local/Cloud)**
- **Model Options:**
   - Local: **Mistral 7B** (Ollama), **LLaMA 3**, **Phi-3**
   - Cloud: **OpenAI GPT-4.x**, **Google Gemini 1.5**
- **APIs:**
   - Ollama REST (localhost:11434)
   - LM Studio OpenAI-compatible (localhost:1234/v1)
   - OpenAI REST (/v1/chat/completions)
   - Gemini REST (/v1beta/models/...:generateContent)

**Why provider abstraction?**
- Single code path, switch via config/env
- Local-first, cloud fallback when allowed
- Easy benchmarking across models

---

#### 4. **Excel Storage Layer**
- **Format:** .xlsx (OpenXML)
- **Location Options:**
   - OneDrive (mandated primary for AppSheet sync)
   - SharePoint (enterprise alternative)
   - Local folder (development only)
- **Write Strategy:** Append-only (no overwrites)
- **Sheet Name:** `Applications`

---

#### 5. **AppSheet Integration**
- **Connection Type:** Excel connector (OneDrive/SharePoint)
- **Sync Frequency:** Real-time or scheduled
- **Views:** Pre-configured in AppSheet, not in scope for this project

---

## Data Schema

### Extraction Fields (20 Mandatory + Metadata)

```json
{
  "job_title": "string|null",
  "employer": "string|null",
  "applicant_name": "string|null",
  "current_designation": "string|null",
  "current_company": "string|null",
  "experience_years": "integer|null",
  "experience_months": "integer|null",
  "current_ctc_lpa": "float|null",
  "expected_ctc_lpa": "float|null",
  "location_current": "string|null",
   "location_preferred": "array[string]",
  "past_company": "string|null",
  "notice_period_months": "integer|null",
  "education": "string|null",
  "university": "string|null",
   "key_skills": "array[string]",
  "date_of_birth": "string (YYYY-MM-DD)|null",
  "mobile": "string|null",
  "email": "string|null",
   "offer_in_hand_lpa": "float|null",
  
  "ingested_at": "string (ISO8601)",
  "email_subject": "string",
   "from_email": "string",
   "ai_provider": "string",
   "ai_model": "string",
   "confidence_score": "float (0-1)",
    "response_link": "string|null",
    "contact_details_link": "string|null",
    "job_applicants_count": "integer|null",
    "job_posted_days": "integer|null"
}
```

### Field Normalization Rules

| Field | Rule |
|-------|------|
| `key_skills` | Convert array to comma-separated string |
| `location_preferred` | Convert array to comma-separated string |
| `mobile` | Remove spaces, keep only digits |
| `email` | Lowercase, trim whitespace |
| `experience_years` | Extract integer from "5 years 3 months" |
| `current_ctc_lpa` | Extract float from "₹8.5 LPA" or "850000" |

### Null Handling Philosophy
**Critical Rule:** If data is not explicitly found in email → Use `null`
- ❌ Never guess or infer
- ❌ Never use default values (0, "N/A", "Unknown")
- ✅ Always preserve data integrity

---

## Security & Privacy

### Threat Model

| Risk | Mitigation |
|------|------------|
| Email content exposure | All AI processing local-only by default |
| Data breach | No cloud AI services used (unless explicitly enabled) |
| Unauthorized access | Python service bound to localhost |
| PII leakage | Excel stored in user-controlled location |
| CORS attacks | Flask CORS limited to Office.js origin |
| Cloud API keys | Stored in `.env`, never logged; use least privilege |

### Compliance Considerations
- **GDPR:** Local processing = no data transfer to third parties
- **HIPAA:** Not applicable (recruitment data)
- **Corporate IT:** No external connections required

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
**Goal:** Working Outlook Add-in that reads email text

**Deliverables:**
- [ ] Manifest.xml with correct permissions
- [ ] Taskpane UI with "Extract" button
- [ ] Office.js integration to read email body
- [ ] Manual sideloading instructions
- [ ] Basic error handling

**Success Criteria:**
- Button appears in Outlook email view
- Console logs full email text on click
- No JavaScript errors

---

### Phase 2: AI Bridge + Provider Abstraction (Week 2)
**Goal:** Python service that calls local or cloud AI via a provider interface and returns JSON

**Deliverables:**
- [ ] Flask app with `/extract` endpoint
- [ ] Provider abstraction interface (`AIProvider`)
- [ ] Providers: Ollama (default), LM Studio (OpenAI-compatible)
- [ ] Optional providers: OpenAI, Gemini (env-gated)
- [ ] JSON validation logic
- [ ] Error handling for AI failures
- [ ] Testing with 10 sample emails

**Success Criteria:**
- Postman call returns valid JSON for test emails
- 80%+ field extraction accuracy
- Response time < 10 seconds (local); < 8 seconds (cloud)

---

### Phase 3: Excel Integration (Week 3)
**Goal:** Automatic writing to Excel with proper formatting

**Deliverables:**
- [ ] Pandas DataFrame construction
- [ ] Append-only Excel write logic
- [ ] Column header creation (first run)
- [ ] Data type enforcement
- [ ] Duplicate detection (optional)

**Success Criteria:**
- 100 emails → 100 Excel rows
- No data corruption
- Proper date/number formatting

---

### Phase 4: End-to-End + Auto-Trigger (Week 4)
**Goal:** Complete flow from Outlook button → Excel row, plus Windows auto-trigger on email arrival

**Deliverables:**
- [ ] Connect Outlook Add-in to Python service
- [ ] CORS configuration
- [ ] Loading states in UI
- [ ] Success/error notifications
- [ ] Windows Mail Watcher (Outlook COM via `pywin32`) to auto-process arrivals
- [ ] Identification rules: From email and Subject contains configured keywords
- [ ] User documentation

**Success Criteria:**
- User can extract candidate data in < 15 seconds
- Auto-trigger processes new matching emails within 10 seconds
- Clear error messages for failures
- Works on Windows 10/11 + Outlook 2019/365

---

### Phase 5: Polish & Scale (Week 5-6)
**Goal:** Production-ready system

**Deliverables:**
- [ ] Confidence scoring per field
- [ ] Batch processing (select multiple emails)
- [ ] Auto-trigger on new email arrival (optional)
- [ ] AppSheet template configuration
- [ ] Admin dashboard for monitoring

**Success Criteria:**
- Handles 500+ emails without issues
- < 5% error rate
- Self-service deployment guide

---

## Success Metrics (KPIs)

### Functional Metrics
- **Extraction Accuracy:** > 85% fields correctly extracted
- **Processing Time:** < 15 seconds per email
- **Uptime:** Python service 99%+ (local machine on)
- **Error Rate:** < 5% failed extractions

### Business Metrics
- **Time Saved:** 5 minutes/email → 15 seconds (95% reduction)
- **Data Quality:** 100% structured vs. manual copy-paste
- **Cost Savings:** ₹0 vs. ₹50,000+/year for AI APIs
- **Scalability:** 1000+ emails/day capacity

---

## Technical Decisions & Trade-offs

### Why This Stack?

| Choice | Rationale | Alternative Rejected |
|--------|-----------|----------------------|
| **Plain JS** | Simplest for single-button UI | React (overkill) |
| **Flask** | Lightweight, fast to develop | FastAPI (unnecessary async) |
| **Ollama** | Free, local, private | OpenAI ($$$), Azure AI (license) |
| **Excel** | AppSheet native, universally available | SQL DB (overengineered) |
| **Pandas** | Battle-tested Excel manipulation | Manual openpyxl (verbose) |

### Known Limitations

1. **Ollama Must Be Running (Local Mode)**
   - Solution: Auto-start script or user checklist
   
2. **Localhost Security**
   - Excel files accessible to any local process
   - Solution: Document security model

3. **Auto-Trigger is Windows-only**
   - Outlook COM watcher requires Windows desktop Outlook
   - Solution: Fallback to button-based extraction on Mac

4. **Model Accuracy Ceiling**
   - Mistral 7B is good but not GPT-4 level
   - Solution: Confidence scores + manual review workflow

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ollama crashes | Medium | High | Health check endpoint + auto-restart |
| Excel file locked | High | Medium | Retry logic with backoff |
| AI extraction errors | Medium | Medium | Confidence scoring + manual override |
| CORS blocks request | Low | High | Proper Flask CORS config |
| Manifest not approved | Low | High | Use sideloading (no admin approval) |

### Operational Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| User doesn't start Python service | High | High | Desktop shortcut + clear docs |
| Ollama model not downloaded | High | High | Setup script checks model |
| Excel not in OneDrive | Medium | Medium | Support local files in v1 |

---

## Dependencies & Prerequisites

### Software Requirements

#### Development Machine
- **OS:** Windows 10/11, macOS 12+, Linux
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 10GB free (for Ollama models)
- **Tools:**
  - Node.js 18+ (for Office.js development)
  - Python 3.10+
  - Ollama 0.1.20+
  - Visual Studio Code (recommended)

#### User Machine
- **OS:** Windows 10/11 (primary target)
- **Outlook:** 2019 or Microsoft 365
- **Excel:** 2019 or Microsoft 365
- **RAM:** 8GB+ (for Ollama)
- **OneDrive:** Required (primary Excel storage)
   - For auto-trigger watcher (Windows only): Outlook desktop client installed and running

### Installation Steps (User)
1. Install Ollama from ollama.ai
2. Pull model: `ollama pull mistral`
3. Install Python 3.10+
4. Install Python dependencies: `pip install -r requirements.txt`
5. Sign in to OneDrive and confirm target Excel path
6. Sideload Outlook Add-in (one-time)
7. Start Python service: `python app.py`
8. (Optional, Windows) Start Mail Watcher tray app for auto-trigger

**Estimated Setup Time:** 30-45 minutes (first time)

---

## Testing Strategy

### Unit Tests (Python Service)
- JSON schema validation
- Field normalization logic
- Excel write/append functions
- Error handling paths

**Tool:** pytest

### Integration Tests
- Outlook → Python → Excel flow
- Ollama API communication
 - Mail Watcher auto-trigger on arrival
- File locking scenarios

### User Acceptance Testing (UAT)
- **Test Emails:** 50 real job application emails
- **Acceptance Criteria:** 85% extraction accuracy
- **Testers:** 2-3 recruitment team members
- **Duration:** 1 week

### Performance Testing
- 100 emails in 30 minutes
- Memory usage < 2GB
- No memory leaks

---

## Future Enhancements (Post-MVP)

### Phase 2 Features (Next 3 Months)
1. **CV/Resume Parsing** - Extract from PDF attachments
2. **Duplicate Detection** - Match by email/mobile
3. **Confidence Scoring** - Per-field reliability indicator
4. **Auto-Trigger Mode** - Process emails automatically
5. **Batch Processing** - Select 10 emails, extract all

### Phase 3 Features (Next 6 Months)
1. **Multi-Language Support** - Hindi, Tamil, etc.
2. **Email Response Templates** - Auto-reply to candidates
3. **Interview Scheduling** - Calendar integration
4. **Recruiter Dashboard** - Analytics in AppSheet
5. **ATS-Lite** - Full recruitment workflow

### Never Planned (Out of Scope)
- ❌ Cloud-hosted AI (defeats privacy goal)
- ❌ Mobile app (Outlook Add-in is desktop-only)
- ❌ Video interview integration
- ❌ Background check services

---

## Cost Analysis

### Traditional Approach (AI APIs)
- **OpenAI GPT-4:** $0.03/1K tokens × 2K tokens/email × 1000 emails = **$60/month**
- **Azure AI:** Similar pricing + licensing
- **Power Automate AI Builder:** $500/user/year

### nViteXtracter (This Solution)
- **Ollama:** Free
- **Python/Flask:** Free (open-source)
- **Office.js:** Free (included with Office)
- **Electricity:** ~₹50/month (PC runtime)

**ROI:** 99% cost reduction

---

## Deployment Options

### Option 1: Sideloading (Recommended for v1)
- **Pros:** No admin approval, instant setup
- **Cons:** Per-user installation
- **Best For:** Small teams (1-10 users)

### Option 2: Centralized Deployment (Future)
- **Pros:** One-click install for all users
- **Cons:** Requires IT admin + Microsoft 365 tenant
- **Best For:** Enterprise rollout

### Option 3: AppSource (Far Future)
- **Pros:** Public availability
- **Cons:** Microsoft certification process
- **Best For:** Product commercialization

---

## Maintenance & Support

### Ongoing Tasks
- **Weekly:** Check Ollama model updates
- **Monthly:** Review extraction accuracy
- **Quarterly:** Update dependencies (security patches)

### Troubleshooting Playbook
| Issue | Solution |
|-------|----------|
| "Extraction failed" | Check if Ollama is running |
| "Cannot write to Excel" | Close Excel file |
| "Add-in button missing" | Re-sideload manifest.xml |
| Slow extraction (>30s) | Switch to smaller model (Phi-3) |

---

## Approval Checklist

### Technical Sign-Off
- [ ] Architecture reviewed by technical lead
- [ ] Security model approved
- [ ] Data schema validated
- [ ] Tech stack confirmed

### Business Sign-Off
- [ ] Budget approved (essentially zero)
- [ ] Timeline acceptable (6 weeks)
- [ ] Success metrics agreed upon
- [ ] AppSheet integration plan confirmed

### Legal/Compliance Sign-Off
- [ ] Privacy policy reviewed (if applicable)
- [ ] Data retention policy defined
- [ ] User consent mechanism (not needed for this use case)

---

## Next Steps After Approval

1. **Set Up Development Environment** (Day 1)
   - Install all dependencies
   - Create project repository
   - Initialize git

2. **Kickoff Meeting** (Day 2)
   - Confirm roles and responsibilities
   - Set up weekly progress reviews
   - Create Slack/Teams channel

3. **Phase 1 Sprint** (Week 1)
   - Build Outlook Add-in skeleton
   - First working prototype

4. **Weekly Demos** (Every Friday)
   - Show progress to stakeholders
   - Gather feedback
   - Adjust priorities

---

## Appendix

### A. Glossary
- **Office.js:** Microsoft's JavaScript library for Office Add-ins
- **Ollama:** Local LLM runtime (like Docker for AI models)
- **LLaMA/Mistral:** Open-source language models
- **AppSheet:** Google's no-code app builder
- **Sideloading:** Manual add-in installation (no store)

### B. References
- [Office Add-ins Documentation](https://learn.microsoft.com/en-us/office/dev/add-ins/)
- [Ollama Documentation](https://ollama.ai/docs)
- [AppSheet Excel Integration](https://help.appsheet.com/en/articles/961509-excel)

### C. Sample Email (Test Case)
```
Subject: Application for Senior Developer - nVite

Dear Hiring Manager,

I am applying for the Senior Developer position at nVite Technologies.

Name: Rajesh Kumar
Current Role: Software Engineer at TCS
Experience: 5 years 3 months
Current CTC: 8.5 LPA
Expected CTC: 12 LPA
Location: Bangalore (open to Pune, Hyderabad)
Notice Period: 2 months
Education: B.Tech Computer Science, VIT University
Skills: Python, React, AWS, Docker
Mobile: +91 9876543210
Email: rajesh.kumar@example.com

Looking forward to hearing from you.
```

---

**Document End**

**Prepared By:** AI Assistant (GitHub Copilot)  
**Review Required:** Technical Lead + Business Owner  
**Approval Date:** _____________  
**Signed By:** _____________
