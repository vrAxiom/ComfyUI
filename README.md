# nViteXtracter - Quick Start Summary

## 📋 What We've Prepared

A comprehensive design package for your **Outlook Add-in with local or cloud AI** project:

### 📄 Documentation Created

1. **[PRD.md](PRD.md)** - Complete Product Requirements Document
   - Executive summary & problem statement
   - Technical architecture (5 components)
   - Data schema (26 core fields incl. provenance + optional job/link fields)
   - 6-week implementation roadmap
   - Risk assessment & mitigation
   - Cost analysis (99% savings vs. cloud AI)

2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System Architecture
   - Visual component diagrams
   - Data flow sequences
   - Network topology
   - Technology stack details
   - Error handling architecture
   - Performance characteristics
   - Security model

3. **[DATA_SCHEMA.md](DATA_SCHEMA.md)** - Field Definitions
   - 23 field specifications
   - Extraction rules per field
   - Validation schema
   - Normalization logic
   - Sample test cases
   - Excel column configuration
   - AI prompt templates

4. **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** - 6-Week Plan
   - Week 1: Foundation (Outlook Add-in UI)
   - Week 2: AI Bridge (Python + provider abstraction)
   - Week 3: Excel Integration
   - Week 4: End-to-End Flow
   - Week 5: Advanced Features
   - Week 6: Deployment & Training
   - Detailed tasks with acceptance criteria

5. **[README.md](README.md)** - This Quick Start Guide

---

## 🎯 Project Overview

**nViteXtracter** extracts structured candidate data from job application emails using:
- ✅ **Outlook Add-in** (button-click extraction; Windows auto-trigger supported)
- ✅ **AI Provider Layer**: Local (Ollama / LM Studio) or Cloud (OpenAI / Gemini)
- ✅ **Excel Storage in OneDrive** (AppSheet-ready, tenant-controlled)
- ✅ **Privacy-First** (local by default; cloud optional via config)

---

## 🏗️ System Architecture (High-Level)

```
Email → Outlook Add-in → Python Service → AI Provider (Local/Cloud) → Excel (OneDrive) → AppSheet
```

**Processing Time:** 7-12 seconds per email  
**Accuracy Target:** 85%+ field extraction  
**Cost:** ₹0 AI fees (vs. ₹60/month with OpenAI)

---

## 📊 What Gets Extracted (26 Fields)

### Critical Fields
- Applicant Name, Email, Mobile
- Current Company, Designation, Experience
- Current CTC, Expected CTC
- Key Skills, Education

### Optional Fields
- Location (current + preferred)
- Notice Period, Date of Birth
- Past Company, University
- Offer in Hand (LPA)

### Metadata
- Ingested Timestamp, Email Subject, From Email
- AI Provider, AI Model (provenance)
- Confidence Score (future)
 - Response/Contact links (if present), Applicants count, Job posted days

---

## 🛠️ Technology Stack

### Frontend
- Office.js (Outlook Add-in API)
- Plain JavaScript (no React - simplicity)
- HTML5/CSS3 (minimal UI)

### Backend
- Python 3.10+ (Flask)
- AI Provider Layer (configurable)
   - Local: Ollama (11434), LM Studio (OpenAI-compatible 1234/v1)
   - Cloud (optional): OpenAI, Gemini
   - Config via `.env` (see python-service/.env.example)

### Storage
- Excel (.xlsx via pandas/openpyxl)
- OneDrive (primary; SharePoint optional)
- AppSheet (no-code frontend)

---

## 📅 6-Week Timeline

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Foundation | Working Outlook Add-in button |
| 2 | AI Bridge + Provider | Python service with provider abstraction |
| 3 | Excel | Automated Excel writing |
| 4 | Integration + Auto-Trigger | Complete flow + Windows Mail Watcher |
| 5 | Polish | Batch processing, confidence scoring |
| 6 | Launch | Deployment, docs, training |

---

## 💰 Cost Analysis

### Traditional Approach
- OpenAI GPT-4: **₹60/month** (1000 emails)
- Power Automate: **₹40,000/user/year**

### nViteXtracter
- Development: **₹1,20,000** (one-time, 240 hours)
- Ongoing: **₹4,500/month** (10 users)
- AI Costs: **₹0** (local) or variable (cloud if enabled)

**ROI:** 78% cost reduction vs. manual entry

---

## ✅ Next Steps (Approval Required)

### Before Building, Confirm:

1. **Architecture Approved?**
   - [ ] Outlook Add-in approach accepted
   - [ ] AI Provider strategy: Local (Ollama/LM Studio) or Cloud (OpenAI/Gemini)
   - [ ] Excel in OneDrive as primary storage approved

2. **Scope Agreed?**
   - [ ] 23 fields sufficient (see DATA_SCHEMA.md)
   - [ ] 85% accuracy target acceptable
   - [ ] 6-week timeline realistic

3. **Resources Committed?**
   - [ ] 1-2 developers allocated
   - [ ] Hardware meets requirements (8GB+ RAM)
   - [ ] Outlook 2019/365 available

4. **Success Metrics Defined?**
   - [ ] KPIs agreed (time saved, accuracy, adoption)
   - [ ] Testing approach confirmed (50+ sample emails)
   - [ ] UAT participants identified

---

## 🚀 How to Start After Approval

### Day 1 Actions:
1. Clone/fork this repository
2. Set up development environment:
   ```powershell
   # Install dependencies
   winget install Python.Python.3.10
   pip install flask requests pandas openpyxl flask-cors python-dotenv

   # Choose an AI provider
   # A) Local - Ollama
   winget install Ollama.Ollama
   ollama pull mistral
   # B) Local - LM Studio
   # Download LM Studio and enable local server (OpenAI-compatible)
   # C) Cloud - OpenAI/Gemini
   # Obtain API keys and set in .env
   ```
3. Copy `python-service/.env.example` to `.env` and set:
   - `AI_PROVIDER`, `AI_MODEL`, `EXCEL_PATH` (OneDrive path)
   - `MATCH_FROM`, `MATCH_SUBJECT_KEYWORDS`
4. Review PRD.md with team
5. Create project board (use IMPLEMENTATION_ROADMAP.md tasks)

### Week 1 Sprint:
- Follow [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) Phase 1
- Goal: Working Outlook Add-in skeleton

---

## 📖 Document Index

| Document | Purpose | Read If... |
|----------|---------|-----------|
| **PRD.md** | Complete requirements | You're a stakeholder/PM |
| **ARCHITECTURE.md** | Technical design | You're building the system |
| **DATA_SCHEMA.md** | Field definitions | You're testing or refining AI prompts |
| **IMPLEMENTATION_ROADMAP.md** | Build plan | You're managing the project |
| **README.md** | Quick start | You need overview (this file) |

---

## ❓ Key Questions to Answer Now

1. **Who will maintain this after launch?**
   - Recommendation: 2 hours/week for monitoring + fixes

2. **Where will Excel file be stored?**
   - OneDrive (primary; required for AppSheet)
   - SharePoint (enterprise option)
   - Local folder (development only)

3. **Which Outlook version?**
   - Outlook 2019: Supported ✅
   - Outlook 365 (Desktop): Supported ✅
   - Outlook Web: Limited support ⚠️ (no auto-trigger)
   - Outlook Mobile: Not supported ❌

4. **How many users at launch?**
   - Impacts: Training strategy, Excel concurrent writes

5. **What's the approval process?**
   - Technical sign-off: _______________
   - Business sign-off: _______________
   - Security review needed? (if enterprise)

---

## 🎓 Learn More

### External Resources
- [Office Add-ins Documentation](https://learn.microsoft.com/en-us/office/dev/add-ins/)
- [Ollama Official Guide](https://ollama.ai/docs)
- [AppSheet + Excel Tutorial](https://help.appsheet.com/en/articles/961509-excel)

### Reference Implementations
- Office.js Samples: [GitHub](https://github.com/OfficeDev/Office-Add-in-samples)
- Flask + Ollama Example: [Community Projects](https://ollama.ai/blog)

---

## 🤝 Decision Log

### Decisions Made (in PRD):
✅ Local-first AI (Ollama/LM Studio) with optional cloud  
✅ Plain JavaScript over React for add-in  
✅ Excel (OneDrive) over SQL database  
✅ Sideloading over AppSource submission  
✅ Mistral 7B as default local model

### Decisions Pending (Your Input):
⏳ Cloud provider usage policy (if any)  
⏳ Batch processing priority (Phase 2 vs. MVP)  
⏳ AppSheet view design (to be defined)

---

## 📞 Support & Questions

### During Design Review:
- Ask questions in project Slack/Teams channel
- Schedule walkthrough session if needed
- Request architecture clarifications

### After Approval:
- Weekly progress reviews (30 minutes)
- Blocker resolution (daily standups)
- UAT feedback sessions (Week 5)

---

## ✍️ Approval Sign-Off

**I have reviewed and approve the design:**

- [ ] **Technical Lead** - Architecture approved  
  Name: _______________ Date: _______________

- [ ] **Product Owner** - Requirements approved  
  Name: _______________ Date: _______________

- [ ] **Security/IT** - Security model approved (if required)  
  Name: _______________ Date: _______________

**Comments/Concerns:**
_________________________________________________________________
_________________________________________________________________

---

## 🏁 Final Checklist Before Build

- [ ] All 4 design documents reviewed
- [ ] Architecture questions answered
- [ ] Timeline accepted (6 weeks)
- [ ] Budget approved (₹1.2L development)
- [ ] Resources allocated (1-2 developers)
- [ ] Test data ready (50+ sample emails)
- [ ] Success metrics defined
- [ ] Stakeholder sign-off obtained

**Status:** 🟡 Awaiting Approval (OneDrive-first, provider-agnostic, auto-trigger on Windows)

---

**Once approved, move to IMPLEMENTATION_ROADMAP.md Phase 1!**

---

_Generated: January 10, 2026 (updated for OneDrive + auto-trigger + provider abstraction)_  
_Project: nViteXtracter_  
_Version: 1.0 (Design Phase)_
