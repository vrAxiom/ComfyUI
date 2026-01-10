# nViteXtracter - System Architecture

## Visual System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                         USER'S OUTLOOK CLIENT                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Email: "Application for Senior Developer - nVite"              │  │
│  │  From: rajesh.kumar@example.com                                 │  │
│  │  Body: Full candidate details in natural language              │  │
│  │                                                                  │  │
│  │  ┌────────────────────────────────────┐                        │  │
│  │  │  [Extract Candidate Data] Button   │  ← Outlook Add-in      │  │
│  │  └────────────────────────────────────┘                        │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────────────┘
                     │ Office.js API Call
                     │ Office.context.mailbox.item.body.getAsync()
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    OUTLOOK ADD-IN (Browser Context)                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  File: taskpane.js                                               │  │
│  │  Function: extractCandidate()                                    │  │
│  │  - Reads email body as plain text                               │  │
│  │  - Reads email subject                                           │  │
│  │  - Shows loading spinner                                         │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────────────┘
                     │ HTTP POST localhost:5000/extract
                     │ Body: { "email": "...", "subject": "..." }
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│              LOCAL PYTHON SERVICE (Flask - Port 5000)                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  File: app.py                                                    │  │
│  │  Endpoint: POST /extract                                         │  │
│  │                                                                  │  │
│  │  Step 1: Receive email text                                     │  │
│  │  Step 2: Construct AI prompt with JSON schema                   │  │
│  │  Step 3: Call AI Provider (local/cloud) ────┐                   │  │
│  │  Step 4: Validate JSON response   │                             │  │
│  │  Step 5: Normalize data            │                             │  │
│  │  Step 6: Write to Excel ───────────┼────────┐                   │  │
│  │  Step 7: Return success/failure    │        │                   │  │
│  └────────────────────────────────────┼────────┼───────────────────┘  │
└────────────────────────────────────────┼────────┼───────────────────────┘
                                         │        │
                     ┌───────────────────┘        │
                     │ HTTP POST                  │
                     │ (Local)  localhost:11434/api/generate  [Ollama]
                     │ (Local)  localhost:1234/v1/...         [LM Studio]
                     │ (Cloud)  api.openai.com/v1/...         [OpenAI]
                     │ (Cloud)  generativelanguage.googleapis.com/... [Gemini]
                     ▼                            │
┌────────────────────────────────────────────────┐│
│         AI PROVIDER LAYER (Configurable)       ││
│  ┌──────────────────────────────────────────┐  ││
│  │  Local: Ollama (mistral:7b, llama3, phi) │  ││
│  │  Local: LM Studio (OpenAI-compatible)    │  ││
│  │  Cloud: OpenAI GPT-4.x, Gemini 1.5       │  ││
│  │  Input: Structured prompt + email text   │  ││
│  │  Output: JSON with extracted fields      │  ││
│  │                                           │  ││
│  │  {                                        │  ││
│  │    "applicant_name": "Rajesh Kumar",     │  ││
│  │    "experience_years": 5,                │  ││
│  │    "current_ctc_lpa": 8.5,               │  ││
│  │    "key_skills": ["Python", "React"],    │  ││
│  │    ...                                    │  ││
│  │  }                                        │  ││
│  └──────────────────────────────────────────┘  ││
└────────────────────────────────────────────────┘│
                                                  │
                                                  │ pandas.DataFrame.to_excel()
                                                  │ mode='a', if_sheet_exists='overlay'
                                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     EXCEL FILE (applications.xlsx)                     │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Sheet: Applications                                             │  │
│  │  ┌──────────┬────────────┬───────────┬──────────┬─────────────┐ │  │
│  │  │   Name   │  Company   │   CTC     │  Skills  │  Ingested   │ │  │
│  │  ├──────────┼────────────┼───────────┼──────────┼─────────────┤ │  │
│  │  │ Rajesh K │    TCS     │   8.5     │ Py,React │ 2026-01-10  │ │  │
│  │  │ Priya S  │  Infosys   │   12      │ Java,AWS │ 2026-01-10  │ │  │
│  │  │ ...      │   ...      │   ...     │  ...     │    ...      │ │  │
│  │  └──────────┴────────────┴───────────┴──────────┴─────────────┘ │  │
│  │                                                                  │  │
│  │  Location: OneDrive (primary) or SharePoint                     │  │
│  │  Dev-only: C:\Users\...\applications.xlsx (local)               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────────────────┘
                     │ Auto-Sync (OneDrive connector)
                     │ Frequency: Real-time or every 5 minutes
                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        APPSHEET APPLICATION                            │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Data Source: applications.xlsx (OneDrive)                       │  │
│  │                                                                  │  │
│  │  Views:                                                          │  │
│  │  - Candidate Dashboard (cards)                                  │  │
│  │  - Pipeline View (by status)                                    │  │
│  │  - Search & Filter (by skills, location)                        │  │
│  │                                                                  │  │
│  │  Actions:                                                        │  │
│  │  - Schedule Interview                                            │  │
│  │  - Update Status (Shortlisted/Rejected)                         │  │
│  │  - Send Email Template                                           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Component Interaction Sequence

### User Initiates Extraction

```
User                 Outlook Add-in      Python Service      Ollama          Excel
  │                        │                   │               │              │
  │ Click "Extract"        │                   │               │              │
  ├───────────────────────>│                   │               │              │
  │                        │                   │               │              │
  │                        │ Read email body   │               │              │
  │                        │ (Office.js API)   │               │              │
  │                        │────┐              │               │              │
  │                        │<───┘              │               │              │
  │                        │                   │               │              │
  │                        │ POST /extract     │               │              │
  │                        │ {email, subject}  │               │              │
  │                        ├──────────────────>│               │              │
  │                        │                   │               │              │
  │                        │                   │ Construct     │              │
  │                        │                   │ AI prompt     │              │
  │                        │                   │────┐          │              │
  │                        │                   │<───┘          │              │
  │                        │                   │               │              │
  │                        │                   │ POST /generate│              │
  │                        │                   ├──────────────>│              │
  │                        │                   │               │              │
  │                        │                   │               │ Process      │
  │                        │                   │               │ (5-10s)      │
  │                        │                   │               │────┐         │
  │                        │                   │               │<───┘         │
  │                        │                   │               │              │
  │                        │                   │ JSON response │              │
  │                        │                   │<──────────────┤              │
  │                        │                   │               │              │
  │                        │                   │ Validate JSON │              │
  │                        │                   │────┐          │              │
  │                        │                   │<───┘          │              │
  │                        │                   │               │              │
  │                        │                   │ Write row     │              │
  │                        │                   ├──────────────────────────────>│
  │                        │                   │               │              │
  │                        │                   │               │      Success │
  │                        │                   │<──────────────────────────────┤
  │                        │                   │               │              │
  │                        │ {status: "ok"}    │               │              │
  │                        │<──────────────────┤               │              │
  │                        │                   │               │              │
  │ Show success message   │                   │               │              │
  │<───────────────────────┤                   │               │              │
  │ "Candidate extracted!" │                   │               │              │
  │                        │                   │               │              │
```

### Auto-Trigger on Arrival (Windows Mail Watcher)

```
Outlook (Windows)     Mail Watcher (pywin32)     Python Service      AI Provider     Excel
    │                        │                        │                 │             │
    │ New email arrives      │                        │                 │             │
    ├───────────────────────>│                        │                 │             │
    │                        │ Evaluate rules:        │                 │             │
    │                        │ From domain + Subject  │                 │             │
    │                        │ contains keywords      │                 │             │
    │                        │────┐                   │                 │             │
    │                        │<───┘ (match)           │                 │             │
    │                        │ Read body/subject      │                 │             │
    │                        │ POST /extract          │                 │             │
    │                        ├───────────────────────>│                 │             │
    │                        │                        │ Call provider   │             │
    │                        │                        ├───────────────> │             │
    │                        │                        │                 │ JSON        │
    │                        │                        │<───────────────┤             │
    │                        │                        │ Write to Excel  │             │
    │                        │                        ├──────────────────────────────>│
    │                        │                        │                 │             │
    │                        │ Success callback/log   │                 │             │
    │                        │<───────────────────────┤                 │             │
```

---

## Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S MACHINE (localhost)               │
│                                                             │
│  ┌──────────────────┐          ┌──────────────────┐        │
│  │  Browser Process │          │  Python Process  │        │
│  │  (Outlook Add-in)│◄────────►│  (Flask Service) │        │
│  │  Port: N/A       │  HTTP    │  Port: 5000      │        │
│  └──────────────────┘          └────────┬─────────┘        │
│                                          │                  │
│                                          │ HTTP             │
│                                          ▼                  │
│                                 ┌──────────────────┐        │
│                                 │ Ollama Process   │        │
│                                 │ Port: 11434      │        │
│                                 └──────────────────┘        │
│                                          ▲                  │
│                                          │                  │
│                                 ┌──────────────────┐        │
│                                 │ LM Studio        │        │
│                                 │ Port: 1234       │        │
│                                 └──────────────────┘        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  File System                                         │  │
│  │  - OneDrive/applications.xlsx (primary)             │  │
│  │  - SharePoint/apps/applications.xlsx (optional)     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ OneDrive Sync (if configured)
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   MICROSOFT CLOUD (OneDrive)                │
│  applications.xlsx (synced copy)                            │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ AppSheet Connector
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   GOOGLE CLOUD (AppSheet)                   │
│  Real-time app reading from Excel                           │
└─────────────────────────────────────────────────────────────┘
```

**Key Security Points:**
- ✅ Local-first AI; cloud providers optional via config
- ✅ Python service only accepts localhost connections
- ✅ No public IP exposure
- ✅ Excel stored in OneDrive (user tenant control)

---

## Data Flow Architecture

### Extraction Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Email Capture                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Email opened in Outlook                                    │
│ Process: Office.js reads email.body + email.subject                │
│ Output:  Raw text string (HTML stripped)                           │
│ Error:   If fails → "Cannot read email" alert                      │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Prompt Engineering                                        │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Raw email text                                             │
│ Process: Construct prompt with:                                    │
│          - JSON schema definition                                  │
│          - Extraction rules (null if missing)                      │
│          - Example format                                          │
│          - Email text                                              │
│ Output:  Structured prompt (string)                                │
│ Error:   Never fails (pure string manipulation)                    │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3: AI Inference                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Prompt + Model name (mistral:7b)                           │
│ Process: Ollama performs:                                          │
│          - Tokenization                                            │
│          - Transformer inference (5-10 seconds)                    │
│          - Text generation (JSON format)                           │
│ Output:  Raw JSON string                                           │
│ Error:   If Ollama down → "AI service unavailable"                 │
│          If malformed → Retry with stricter prompt                 │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4: JSON Validation                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Raw JSON string                                            │
│ Process: - Parse JSON                                              │
│          - Check all required keys exist                           │
│          - Validate data types                                     │
│          - Convert arrays to comma-separated strings               │
│ Output:  Validated dictionary                                      │
│ Error:   If invalid → Log error + use partial data with nulls      │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 5: Data Enrichment                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Validated dictionary                                       │
│ Process: - Add timestamp (ingested_at)                             │
│          - Add email subject                                       │
│          - Calculate confidence score (future)                     │
│          - Format phone number (+91 prefix)                        │
│ Output:  Complete record (dict)                                    │
│ Error:   Never fails (adds metadata only)                          │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 6: Excel Write                                               │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Complete record (dict)                                     │
│ Process: - Convert to pandas DataFrame                             │
│          - Open Excel file (create if missing)                     │
│          - Append row to "Applications" sheet                      │
│          - Save and close                                          │
│ Output:  File path confirmation                                    │
│ Error:   If file locked → Retry 3 times with 1s delay              │
│          If disk full → Alert user                                 │
└─────────────────────────────────────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 7: User Feedback                                             │
├─────────────────────────────────────────────────────────────────────┤
│ Input:  Success/failure status from Python                         │
│ Process: - Show alert() in Outlook Add-in                          │
│          - Update UI button state                                  │
│ Output:  "Candidate extracted successfully" OR error message       │
│ Error:   N/A (final stage)                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Details

### Frontend (Outlook Add-in)

```
┌─────────────────────────────────────────────────┐
│ Outlook Add-in Technology Stack                │
├─────────────────────────────────────────────────┤
│                                                 │
│ HTML5 (taskpane.html)                          │
│   └─> Semantic HTML, minimal styling          │
│                                                 │
│ CSS3 (inline styles)                           │
│   └─> Simple button, loading spinner          │
│                                                 │
│ JavaScript ES6+ (taskpane.js)                  │
│   ├─> Office.js (Microsoft library)           │
│   ├─> Fetch API (HTTP calls)                  │
│   └─> Async/await (modern promises)           │
│                                                 │
│ Office.js v1.1 (minimum requirement)           │
│   ├─> Office.context.mailbox.item             │
│   ├─> body.getAsync()                          │
│   └─> subject (read-only property)            │
│                                                 │
│ NO dependencies (zero npm packages)            │
│   ├─> No React                                 │
│   ├─> No jQuery                                │
│   └─> No lodash                                │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Backend (Python Service)

```
┌─────────────────────────────────────────────────┐
│ Python Service Technology Stack                │
├─────────────────────────────────────────────────┤
│                                                 │
│ Python 3.10+                                   │
│   └─> Type hints, f-strings, match/case       │
│                                                 │
│ Flask 3.0.0 (HTTP server)                      │
│   ├─> @app.route decorators                   │
│   ├─> request.json                             │
│   ├─> jsonify()                                │
│   └─> flask_cors (CORS handling)              │
│                                                 │
│ requests 2.31.0 (HTTP client)                  │
│   └─> AI provider API calls                    │
│                                                 │
│ pandas 2.1.4 (Excel manipulation)              │
│   ├─> DataFrame creation                       │
│   └─> to_excel() method                        │
│                                                 │
│ openpyxl 3.1.2 (Excel engine)                  │
│   └─> Backend for pandas                       │
│                                                 │
│ json (stdlib) - JSON parsing                   │
│ datetime (stdlib) - Timestamps                 │
│ python-dotenv - Config via .env                │
│ pywin32 (Windows) - Outlook COM watcher        │
│                                                 │
└─────────────────────────────────────────────────┘
```

### AI Layer (Provider Abstraction)

```
┌─────────────────────────────────────────────────┐
│ AI Provider Technology Stack                   │
├─────────────────────────────────────────────────┤
│                                                 │
│ Local Providers:                               │
│   ├─> Ollama Runtime 0.1.20+ (REST 11434)      │
│   └─> LM Studio (OpenAI-compatible 1234/v1)    │
│                                                 │
│ Cloud Providers (optional):                    │
│   ├─> OpenAI (chat/completions)                │
│   └─> Google Gemini (generateContent)          │
│                                                 │
│ Models:                                        │
│   ├─> Mistral 7B, LLaMA 3, Phi-3 (local)       │
│   ├─> GPT-4.x (OpenAI), Gemini 1.5 (Google)    │
│                                                 │
│ Endpoints:                                     │
│   ├─> http://localhost:11434/api/generate      │
│   ├─> http://localhost:1234/v1/chat/completions│
│   ├─> https://api.openai.com/v1/chat/completions│
│   └─> https://generativelanguage.googleapis.com │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## File Structure

```
nViteXtracter/
│
├── PRD.md                          ← Product Requirements Document
├── ARCHITECTURE.md                 ← This file (system design)
├── README.md                       ← User-facing setup guide
│
├── outlook-addin/                  ← Outlook Add-in source code
│   ├── manifest.xml                ← Add-in configuration
│   ├── taskpane.html               ← UI (button, status)
│   ├── taskpane.js                 ← Business logic
│   ├── taskpane.css                ← Minimal styling
│   └── assets/                     ← Icons and images
│       ├── icon-16.png
│       ├── icon-32.png
│       ├── icon-64.png
│       └── icon-128.png
│
├── python-service/                 ← Local AI bridge service
│   ├── app.py                      ← Main Flask application
│   ├── requirements.txt            ← Python dependencies
│   ├── config.py                   ← Configuration (file paths, ports)
│   ├── prompt_templates.py         ← AI prompt engineering
│   ├── validators.py               ← JSON schema validation
│   └── excel_writer.py             ← Excel operations
│
├── tests/                          ← Automated tests
│   ├── test_extraction.py          ← Unit tests for AI extraction
│   ├── test_excel.py               ← Unit tests for Excel writes
│   ├── sample_emails/              ← Test email samples
│   │   ├── email_1.txt
│   │   ├── email_2.txt
│   │   └── email_3.txt
│   └── expected_outputs/           ← Expected JSON outputs
│       ├── email_1.json
│       ├── email_2.json
│       └── email_3.json
│
├── scripts/                        ← Automation scripts
│   ├── setup_ollama.bat            ← Windows: Install & start Ollama
│   ├── start_service.bat           ← Windows: Start Python service
│   └── install_addin.ps1           ← PowerShell: Sideload add-in
│
├── docs/                           ← Additional documentation
│   ├── USER_GUIDE.md               ← End-user manual
│   ├── TROUBLESHOOTING.md          ← Common issues & solutions
│   └── DEPLOYMENT.md               ← IT deployment guide
│
└── data/                           ← Generated data (gitignored)
    ├── applications.xlsx           ← Output Excel file
    └── logs/                       ← Application logs
        └── extraction.log
```

---

## Error Handling Architecture

### Error Categories & Responses

```
┌──────────────────────────────────────────────────────────────┐
│ ERROR TYPE               │ RESPONSE                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. Ollama Not Running    │                                   │
│    └─> Check: curl localhost:11434                          │
│        Response: "AI service unavailable"                    │
│        Action: Show link to start Ollama                     │
│                                                              │
│ 2. Python Service Down   │                                   │
│    └─> Check: fetch('http://localhost:5000/health')         │
│        Response: "Cannot connect to extraction service"      │
│        Action: Show command to start service                 │
│                                                              │
│ 3. Excel File Locked     │                                   │
│    └─> Check: try/except on df.to_excel()                   │
│        Response: "Excel file is open, please close it"       │
│        Action: Retry 3 times with 1s delay                   │
│                                                              │
│ 4. Malformed JSON        │                                   │
│    └─> Check: json.loads() exception                        │
│        Response: "AI returned invalid format"                │
│        Action: Retry with stricter prompt once               │
│                                                              │
│ 5. Email Read Failed     │                                   │
│    └─> Check: Office.AsyncResultStatus                      │
│        Response: "Cannot read email content"                 │
│        Action: Refresh Outlook, try again                    │
│                                                              │
│ 6. Disk Space Full       │                                   │
│    └─> Check: OSError on file write                         │
│        Response: "Insufficient disk space"                   │
│        Action: Alert user to free space                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Health Check Endpoints

```python
# Python service health checks

@app.route("/health", methods=["GET"])
def health_check():
    """Check if service is alive"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/health/ollama", methods=["GET"])
def ollama_health():
    """Check if Ollama is reachable"""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return jsonify({"ollama": "ok", "models": r.json()})
    except:
        return jsonify({"ollama": "unreachable"}), 503

@app.route("/health/excel", methods=["GET"])
def excel_health():
    """Check if Excel file is writable"""
    try:
        test_df = pd.DataFrame([{"test": "value"}])
        test_df.to_excel("test_write.xlsx", index=False)
        os.remove("test_write.xlsx")
        return jsonify({"excel": "writable"})
    except:
        return jsonify({"excel": "locked"}), 503
```

---

## Performance Characteristics

### Expected Latencies

```
┌─────────────────────────────────────────────────────────┐
│ Operation                    │ Expected Time            │
├─────────────────────────────────────────────────────────┤
│ Button click → Email read    │ < 1 second               │
│ HTTP call (add-in → Python)  │ < 100 ms                 │
│ Prompt construction          │ < 50 ms                  │
│ Ollama inference (Mistral)   │ 5-10 seconds             │
│ JSON validation              │ < 100 ms                 │
│ Excel write                  │ < 500 ms                 │
│ Response back to add-in      │ < 100 ms                 │
├─────────────────────────────────────────────────────────┤
│ TOTAL (end-to-end)           │ 7-12 seconds             │
└─────────────────────────────────────────────────────────┘
```

### Resource Requirements

```
┌──────────────────────────────────────────────────────┐
│ Component         │ CPU      │ RAM      │ Disk      │
├──────────────────────────────────────────────────────┤
│ Outlook Add-in    │ < 1%     │ 50 MB    │ 2 MB      │
│ Python Service    │ < 5%     │ 200 MB   │ 10 MB     │
│ Ollama (idle)     │ < 1%     │ 500 MB   │ 5 GB      │
│ Ollama (active)   │ 50-80%   │ 4-6 GB   │ 5 GB      │
├──────────────────────────────────────────────────────┤
│ TOTAL             │ 55-85%   │ 5-7 GB   │ 5.02 GB   │
└──────────────────────────────────────────────────────┘
```

**Recommendation:** 8GB RAM minimum, 16GB preferred

---

## Security Model

### Threat Surface Analysis

```
┌────────────────────────────────────────────────────────────┐
│ Attack Vector              │ Mitigation                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ 1. Email Injection         │                               │
│    Malicious code in email │ → Treated as plain text only  │
│    body to exploit AI      │ → No code execution           │
│                            │ → Schema validation           │
│                                                            │
│ 2. CORS Bypass             │                               │
│    Unauthorized domain     │ → Flask CORS whitelist        │
│    calling Python service  │ → localhost:* only            │
│                                                            │
│ 3. Path Traversal          │                               │
│    Write Excel outside     │ → Fixed file path             │
│    intended directory      │ → No user-supplied paths      │
│                                                            │
│ 4. JSON Injection          │                               │
│    Malicious JSON from AI  │ → Schema validation           │
│                            │ → Type checking               │
│                            │ → No eval() or exec()         │
│                                                            │
│ 5. Resource Exhaustion     │                               │
│    Spam extraction requests│ → Rate limiting (optional)    │
│                            │ → Single request at a time    │
│                                                            │
│ 6. Data Exfiltration       │                               │
│    Stealing candidate data │ → All processing local        │
│                            │ → No external API calls       │
│                            │ → User controls Excel location│
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Privacy Guarantees

✅ **No data leaves user's machine** (except optional OneDrive sync)  
✅ **No AI telemetry** (Ollama is fully offline)  
✅ **No third-party tracking**  
✅ **User owns all data** (Excel file = single source of truth)

---

## Scalability Considerations

### Current Limitations

- **Sequential Processing:** One email at a time
- **Single Machine:** Cannot distribute across multiple PCs
- **Memory Bound:** Ollama needs 4-6 GB RAM per instance

### Future Scale (If Needed)

```
Scenario 1: Single User, High Volume
├─> Problem: 500 emails/day to process
├─> Solution: Batch processing mode
│   └─> Select multiple emails → Process queue
│   └─> Show progress bar (1 of 500)
│   └─> Estimated time: 500 × 10s = 83 minutes
│   └─> Run overnight or during lunch

Scenario 2: Multi-User Team
├─> Problem: 10 recruiters need this
├─> Solution: Each runs own instance
│   └─> No conflicts (isolated environments)
│   └─> Shared Excel in OneDrive/SharePoint
│   └─> Excel has built-in concurrent write handling

Scenario 3: Enterprise Scale
├─> Problem: 100+ users, 10,000 emails/day
├─> Solution: Centralized server architecture
│   └─> Replace localhost service with hosted API
│   └─> Use GPU-accelerated Ollama (NVIDIA A100)
│   └─> PostgreSQL instead of Excel
│   └─> Load balancer for multiple workers
│   └─> Cost: ~$500/month (DigitalOcean)
```

**Current Design Choice:** Optimized for 1-10 users, < 500 emails/day

---

## Deployment Architecture

### Development Environment

```
Developer Laptop
├─> Windows 11 or macOS
├─> Visual Studio Code (recommended IDE)
├─> Git (version control)
├─> Node.js (for Office.js validation)
└─> Python 3.10+ + Ollama
```

### User Environment (Production)

```
End User Laptop/Desktop
├─> Windows 10/11 (primary target)
│   ├─> Outlook 2019 or Microsoft 365
│   ├─> Python 3.10+ installed
│   ├─> Ollama installed (mistral model pulled)
│   └─> OneDrive (optional, for AppSheet)
│
└─> macOS 12+ (secondary target)
    ├─> Outlook for Mac
    ├─> Python 3.10+ (Homebrew)
    ├─> Ollama (native Mac version)
    └─> OneDrive (optional)
```

**Linux:** Not supported (Outlook Add-ins require Windows/Mac)

---

## Monitoring & Observability

### Logging Strategy

```python
# Python service logging
import logging

logging.basicConfig(
    filename='data/logs/extraction.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Log every extraction
logging.info(f"Extraction started: {email_subject}")
logging.info(f"Ollama response time: {elapsed}s")
logging.info(f"Fields extracted: {len([v for v in data.values() if v])}/20")
logging.error(f"Excel write failed: {error}")
```

### Metrics to Track

```
Daily Metrics:
├─> Total extractions attempted
├─> Success rate (%)
├─> Average processing time
├─> Most common errors
└─> Field accuracy (spot checks)

Weekly Metrics:
├─> Total candidates in database
├─> Growth rate (new candidates/week)
└─> AI model performance trends

Monthly Metrics:
├─> Cost savings vs. manual entry
└─> User satisfaction survey
```

---

## Appendix: Alternative Architectures Considered

### Alternative 1: Power Automate + AI Builder
❌ Rejected: High licensing cost (₹40,000+/user/year)

### Alternative 2: Azure Functions + OpenAI API
❌ Rejected: Usage-based cost (₹5,000+/month)

### Alternative 3: Desktop App (Electron)
❌ Rejected: Requires separate installation, less integrated

### Alternative 4: Outlook VBA Macro
❌ Rejected: Limited AI capabilities, deprecated technology

### Alternative 5: Python-only (No Add-in)
❌ Rejected: Poor UX (manual email copy-paste)

**Winner: Current Architecture** ✅
- Zero recurring cost
- Privacy-first
- Native Outlook integration
- Production-grade accuracy

---

**Document Version:** 1.0  
**Last Updated:** January 10, 2026  
**Maintained By:** nViteXtracter Development Team
