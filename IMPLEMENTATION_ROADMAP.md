# nViteXtracter - Implementation Roadmap

**Version:** 1.0  
**Last Updated:** January 10, 2026  
**Total Duration:** 6 Weeks  
**Team:** 1-2 Developers

---

## Project Timeline Overview

```
Week 1                  Week 2                           Week 3                 Week 4                           Week 5            Week 6
[Foundation] →     [AI Bridge + Provider]        → [Excel (OneDrive)]  → [Integration + Auto-Trigger] → [Polish]        → [Launch]
  ↓                        ↓                               ↓                         ↓                          ↓                 ↓
Add-in UI           Flask API + .env                 Pandas Write            E2E + Watcher (Win)         Batch Mode        Deployment
Office.js           AI Provider Abstraction          Excel Format            CORS + Rules (From/Subject) Confidence       Documentation
Button              Local/Cloud Options              Validation              Error Handling               Logging          User Training
```

---

## Phase 1: Foundation (Week 1)

### Objective
Build a working Outlook Add-in that can read email content and display it.

### Deliverables

#### 1.1 Development Environment Setup (Day 1)
- [ ] Install Node.js 18+ (for Office.js validation)
- [ ] Install Python 3.10+
- [ ] Install Visual Studio Code
- [ ] Install Git for version control
- [ ] Create project folder structure
- [ ] Initialize git repository

**Acceptance Criteria:**
- All tools installed and verified with `--version` commands
- Project folder created at `C:\Users\...\projects\nViteXtracter`

---

#### 1.2 Outlook Add-in Manifest (Day 1-2)
- [ ] Create `manifest.xml` with correct schema
- [ ] Define add-in metadata (name, version, provider)
- [ ] Set permissions: `ReadWriteItem`
- [ ] Add button to ribbon/context menu
- [ ] Configure icon assets (16px, 32px, 64px, 128px)

**File:** `outlook-addin/manifest.xml`

**Key Configuration:**
```xml
<Id>12345678-1234-1234-1234-123456789abc</Id>
<Version>1.0.0</Version>
<ProviderName>nVite Technologies</ProviderName>
<DefaultLocale>en-US</DefaultLocale>
<DisplayName>nViteXtracter</DisplayName>
<Description>Extract candidate data from job application emails</Description>
<Permissions>ReadWriteItem</Permissions>
```

**Acceptance Criteria:**
- Manifest validates against Office Add-in schema
- No XML syntax errors

---

#### 1.3 Basic HTML UI (Day 2-3)
- [ ] Create `taskpane.html` with minimal UI
- [ ] Add "Extract Candidate" button
- [ ] Add loading spinner (hidden by default)
- [ ] Add status message area
- [ ] Apply basic CSS styling

**File:** `outlook-addin/taskpane.html`

**UI Elements:**
```html
<body>
  <div class="container">
    <h2>nViteXtracter</h2>
    <button id="extractBtn">Extract Candidate Data</button>
    <div id="spinner" class="hidden">Processing...</div>
    <div id="status"></div>
  </div>
</body>
```

**Acceptance Criteria:**
- HTML renders correctly in browser
- Button is clickable (no action yet)
- Spinner can be toggled via CSS class

---

#### 1.4 Office.js Integration (Day 3-4)
- [ ] Load Office.js library
- [ ] Implement `Office.onReady()` initialization
- [ ] Read email body using `Office.context.mailbox.item.body.getAsync()`
- [ ] Read email subject
- [ ] Log email content to console (for testing)

**File:** `outlook-addin/taskpane.js`

**Core Function:**
```javascript
function extractCandidate() {
  const item = Office.context.mailbox.item;
  
  item.body.getAsync(Office.CoercionType.Text, function(result) {
    if (result.status === Office.AsyncResultStatus.Succeeded) {
      const emailBody = result.value;
      const emailSubject = item.subject;
      console.log("Subject:", emailSubject);
      console.log("Body:", emailBody);
      // Next: Send to Python service
    } else {
      showError("Failed to read email content");
    }
  });
}
```

**Acceptance Criteria:**
- Office.js loads without errors
- Console logs full email text when button clicked
- Error handling works (try with non-email context)

---

#### 1.5 Sideload Add-in (Day 4-5)
- [ ] Export manifest to network share or OneDrive
- [ ] Sideload in Outlook (File → Manage Add-ins → My Add-ins)
- [ ] Verify button appears in email view
- [ ] Test on multiple emails

**Sideloading Steps:**
1. Save `manifest.xml` to `\\network\addins\` or OneDrive
2. Outlook → File → Manage Add-ins → My Add-ins
3. Custom Add-ins → Add from File
4. Select `manifest.xml`
5. Restart Outlook

**Acceptance Criteria:**
- Add-in button visible in Outlook ribbon
- No manifest errors in Outlook
- Button click triggers JavaScript function

---

#### 1.6 Basic Error Handling (Day 5)
- [ ] Implement try-catch blocks
- [ ] Show user-friendly error messages
- [ ] Log errors to console
- [ ] Disable button during processing

**Error Scenarios:**
- Email cannot be read
- Office.js not loaded
- Network share unavailable

**Acceptance Criteria:**
- User sees clear error messages (no technical jargon)
- App doesn't crash on errors

---

### Week 1 Milestone

**Demo:** Click button in Outlook → Console logs email text

**Definition of Done:**
✅ Add-in sideloaded successfully  
✅ Button appears in Outlook  
✅ Email content retrieved and logged  
✅ No JavaScript errors  
✅ Basic error handling works

---

## Phase 2: Local AI Bridge (Week 2)

### Objective
Build Python Flask service with a pluggable AI Provider (local/cloud) returning structured JSON.

### Deliverables

#### 2.1 AI Runtime Setup (Local or Cloud) (Day 6)
- [ ] Choose provider via `.env` (`AI_PROVIDER=ollama|lmstudio|openai|gemini`)
- [ ] Local (Ollama): Install from ollama.ai, `ollama pull mistral`, verify `http://localhost:11434`
- [ ] Local (LM Studio): Install LM Studio, enable server (OpenAI-compatible) at `http://localhost:1234/v1`
- [ ] Cloud (OpenAI/Gemini): Set API keys in `.env`, verify simple curl call

**Acceptance Criteria:**
- Selected provider reachable from the machine
- Model available and responds to a test prompt
- `.env` configured and loaded by Python service

---

#### 2.2 Flask Service Setup (Day 6-7)
- [ ] Create `python-service/app.py`
- [ ] Install dependencies: `pip install flask requests pandas openpyxl flask-cors python-dotenv`
- [ ] Load configuration from `.env` (provider, model, Excel path, rules)
- [ ] Create `/extract` endpoint (POST)
- [ ] Implement CORS (Outlook/Office origins + localhost)
- [ ] Add health check endpoint `/health`

**File:** `python-service/app.py` (skeleton)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/extract", methods=["POST"])
def extract():
    data = request.json
    email_text = data["email"]
    email_subject = data["subject"]
    
    # TODO: Call AI provider via abstraction
    # TODO: Validate JSON
    # TODO: Write to Excel
    
    return jsonify({"status": "ok", "message": "Not implemented yet"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
```

**Acceptance Criteria:**
- Flask starts without errors
- `/health` endpoint returns 200 OK
- `/extract` endpoint accepts POST requests
- CORS allows localhost connections

---

#### 2.3 AI Prompt Engineering (Day 7-8)
- [ ] Create `prompt_templates.py`
- [ ] Define JSON schema dictionary
- [ ] Write extraction prompt template
- [ ] Test prompt with `ollama run mistral` (manual)
- [ ] Iterate on prompt for better accuracy

**File:** `python-service/prompt_templates.py`

```python
SCHEMA = {
    "job_title": None,
    "employer": None,
    "applicant_name": None,
    # ... (all 23 fields)
}

EXTRACTION_PROMPT = """
You are a data extraction engine.
Output ONLY valid JSON. No explanations.
Use null for missing data. Never guess.

Schema:
{schema}

Email:
---
Subject: {subject}

{body}
---

JSON Output:
"""
```

**Testing Strategy:**
1. Use 5 sample emails (varied completeness)
2. Manually test each with chosen provider CLI/API
3. Measure extraction accuracy (target: 80%+)
4. Refine prompt based on failures

**Acceptance Criteria:**
- Ollama returns valid JSON (parseable)
- 80%+ fields extracted correctly (sample emails)
- No hallucinations (invented data)

---

#### 2.4 AI Provider Abstraction (Day 8-9)
- [ ] Define `AIProvider` interface (`generate_json(subject, body) -> dict`)
- [ ] Implement `OllamaProvider` (11434), `LMStudioProvider` (OpenAI-compatible)
- [ ] Implement optional `OpenAIProvider`, `GeminiProvider` (env-gated)
- [ ] Parse/validate JSON output; add retry with JSON guardrails
- [ ] Add timeout handling (15 seconds max)

**Code:**
```python
import requests, json

class AIProvider:
  def generate_json(self, subject: str, body: str) -> dict:
    raise NotImplementedError

class OllamaProvider(AIProvider):
  def __init__(self, base_url: str, model: str):
    self.url = f"{base_url}/api/generate"
    self.model = model
  def generate_json(self, subject: str, body: str) -> dict:
    prompt = build_prompt(subject, body)
    r = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False}, timeout=15)
    return json.loads(r.json()["response"])  # guarded by validator in 2.5
```

**Acceptance Criteria:**
- Provider selected via `.env` and used at runtime
- JSON parsing works 90%+ of the time
- Timeout errors handled gracefully

---

#### 2.5 JSON Validation (Day 9-10)
- [ ] Create `validators.py`
- [ ] Implement schema validation
- [ ] Check required fields
- [ ] Validate data types (int, float, string)
- [ ] Normalize arrays to CSV strings
- [ ] Add data quality checks

**File:** `python-service/validators.py`

```python
def validate_extraction(data: dict) -> dict:
    validated = {}
    
    # Type coercion
    validated["experience_years"] = int(data.get("experience_years") or 0) or None
    validated["current_ctc_lpa"] = float(data.get("current_ctc_lpa") or 0) or None
    
    # Array normalization
    skills = data.get("key_skills", [])
    validated["key_skills"] = ",".join(skills) if isinstance(skills, list) else skills
    
    # Phone normalization
    mobile = data.get("mobile", "")
    if mobile and not mobile.startswith("+91"):
        validated["mobile"] = f"+91{mobile.replace(' ', '').replace('-', '')}"
    
    return validated
```

**Acceptance Criteria:**
- Invalid JSON types corrected
- Arrays converted to CSV strings
- Phone numbers normalized
- No exceptions thrown

---

#### 2.6 Configuration & Rules (Day 10)
- [ ] Add `.env` support with keys:
  - `AI_PROVIDER`, `AI_MODEL`, `OLLAMA_URL`, `LMSTUDIO_BASE_URL`, `OPENAI_API_KEY`, `GEMINI_API_KEY`
  - `EXCEL_PATH` (OneDrive path), `MATCH_FROM`, `MATCH_SUBJECT_KEYWORDS`
- [ ] Provide `python-service/.env.example`
- [ ] Load and validate config at startup

**Acceptance Criteria:**
- `.env` drives provider selection and OneDrive Excel path
- From/Subject rule configuration persists and is testable

---

#### 2.6 End-to-End Testing (Day 10)
- [ ] Create `tests/sample_emails/` folder
- [ ] Add 10 test emails (varied quality)
- [ ] Run extraction on each
- [ ] Compare output to expected JSON
- [ ] Calculate accuracy metrics

**Test Cases:**
1. **Complete Profile** - All 20 fields present
2. **Minimal Profile** - Only name, email, skills
3. **Formatting Variations** - ₹ vs. INR, +91 vs. 9876...
4. **Ambiguous Text** - "5+ years" vs. "5 years"
5. **Noise** - Long email chains, signatures

**Success Metrics:**
- 80%+ overall accuracy
- 90%+ for critical fields (name, email, mobile)
- < 5% hallucination rate

**Acceptance Criteria:**
- All 10 test emails processed without crashes
- Accuracy report generated
- Failures documented for Phase 3 improvements

---

### Week 2 Milestone

**Demo:** Postman POST request → Flask → Ollama → JSON response

**Definition of Done:**
✅ Ollama running and responding  
✅ Flask `/extract` endpoint works  
✅ AI returns valid JSON  
✅ 80%+ extraction accuracy on test data  
✅ Validation and normalization working

---

## Phase 3: Excel Integration (Week 3)

### Objective
Write extracted data to an Excel file in OneDrive with proper formatting.

### Deliverables

#### 3.1 Excel Writer Module (Day 11-12)
- [ ] Create `excel_writer.py`
- [ ] Implement DataFrame creation
- [ ] Handle file creation (first run)
- [ ] Handle file append (subsequent runs)
- [ ] Set column widths and headers

**File:** `python-service/excel_writer.py`

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

EXCEL_FILE = os.getenv("EXCEL_PATH", os.path.expandvars(r"%UserProfile%\\OneDrive\\Documents\\nViteXtracter\\applications.xlsx"))
SHEET_NAME = "Applications"

def write_to_excel(data: dict):
    df = pd.DataFrame([data])
    
    # Check if file exists
    if not os.path.exists(EXCEL_FILE):
        # Create new file
        df.to_excel(EXCEL_FILE, sheet_name=SHEET_NAME, index=False)
        format_excel_sheet(EXCEL_FILE, SHEET_NAME)
    else:
        # Append to existing file
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name=SHEET_NAME, index=False, header=False, startrow=writer.sheets[SHEET_NAME].max_row)
```

**Acceptance Criteria:**
- First run creates file (in OneDrive path) with headers
- Subsequent runs append rows
- No data corruption
- Column order matches schema

---

#### 3.2 Column Formatting (Day 12-13)
- [ ] Set column widths (e.g., Name = 25, Skills = 60)
- [ ] Apply number formatting (CTC = 1 decimal place)
- [ ] Apply date formatting (ISO 8601)
- [ ] Freeze header row
- [ ] Add auto-filter

**Code:**
```python
from openpyxl.styles import Font

def format_excel_sheet(filename: str, sheet_name: str):
    wb = load_workbook(filename)
    ws = wb[sheet_name]
    
    # Column widths
    ws.column_dimensions['A'].width = 30  # Job Title
    ws.column_dimensions['C'].width = 25  # Applicant Name
    ws.column_dimensions['P'].width = 60  # Key Skills
    
    # Bold headers
    for cell in ws[1]:
        cell.font = Font(bold=True)
    
    # Freeze top row
    ws.freeze_panes = "A2"
    
    # Auto-filter
    ws.auto_filter.ref = ws.dimensions
    
    wb.save(filename)
```

**Acceptance Criteria:**
- Columns readable without horizontal scrolling
- Numbers formatted correctly (no scientific notation)
- Headers bold and frozen

---

#### 3.3 File Locking Handling (Day 13)
- [ ] Detect if Excel file is open
- [ ] Implement retry logic (3 attempts, 1s delay)
- [ ] Return error to user if file locked
- [ ] Log lock errors

**Code:**
```python
import time

def write_to_excel_with_retry(data: dict, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            write_to_excel(data)
            return {"success": True}
        except PermissionError:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return {"success": False, "error": "Excel file is open. Please close it and try again."}
```

**Acceptance Criteria:**
- Retry logic works (test by opening file during write)
- User gets clear error message after 3 failures
- No data loss

---

#### 3.4 Data Type Enforcement (Day 14)
- [ ] Ensure integers stored as numbers (not text)
- [ ] Ensure floats have correct precision
- [ ] Ensure dates in ISO 8601 format
- [ ] Ensure booleans as TRUE/FALSE

**Code:**
```python
def prepare_data_for_excel(data: dict) -> dict:
    # Ensure correct types
    if data.get("experience_years") is not None:
        data["experience_years"] = int(data["experience_years"])
    
    if data.get("current_ctc_lpa") is not None:
        data["current_ctc_lpa"] = round(float(data["current_ctc_lpa"]), 1)
    
    if data.get("offer_in_hand_lpa") is not None:
      try:
        val = float(data["offer_in_hand_lpa"]) if data["offer_in_hand_lpa"] != "" else None
      except (ValueError, TypeError):
        val = None
      data["offer_in_hand_lpa"] = round(val, 1) if (val is not None and val > 0) else None
    
    return data
```

**Acceptance Criteria:**
- Excel recognizes numbers as numbers (can SUM)
- Dates sortable
- Booleans show as checkboxes in Excel

---

#### 3.5 Metadata Addition (Day 14-15)
- [ ] Add `ingested_at` timestamp (ISO 8601)
- [ ] Add `email_subject` field
- [ ] Add `confidence_score` placeholder (null for now)
- [ ] Add extraction version number (future-proofing)

**Code:**
```python
from datetime import datetime

def add_metadata(data: dict, email_subject: str) -> dict:
    data["ingested_at"] = datetime.now().isoformat()
    data["email_subject"] = email_subject
    data["confidence_score"] = None  # Phase 2 feature
    return data
```

**Acceptance Criteria:**
- Timestamp accurate to the second
- Email subject preserved correctly

---

#### 3.6 Integration Testing (Day 15)
- [ ] End-to-end test: Email text → Excel row
- [ ] Test with 50 sample emails
- [ ] Verify all data types correct in Excel
- [ ] Check for data corruption
- [ ] Test concurrent writes (edge case)

**Test Scenarios:**
1. Fresh file creation (no existing Excel)
2. Appending to existing file (100 rows)
3. File locked scenario
4. Disk full scenario (simulate)
5. Invalid data types from AI

**Acceptance Criteria:**
- 100% of test emails result in Excel rows
- No data misalignment (columns match headers)
- Error handling works for all edge cases

---

### Week 3 Milestone

**Demo:** Python service → Excel file with 50 candidate records

**Definition of Done:**
✅ Excel file created and formatted  
✅ Data appended correctly  
✅ File locking handled  
✅ Data types enforced  
✅ 50+ test records in Excel

---

## Phase 4: End-to-End Integration + Auto-Trigger (Week 4)

### Objective
Connect Outlook Add-in to Python service and complete the full flow; add Windows auto-trigger based on From/Subject rules.

### Deliverables

#### 4.1 HTTP Client in Add-in (Day 16-17)
- [ ] Update `taskpane.js` to call Flask API
- [ ] Implement `fetch()` POST request
- [ ] Send email text + subject to `/extract`
- [ ] Handle HTTP errors (500, 503, timeout)
- [ ] Show loading spinner during processing

**Code:**
```javascript
async function extractCandidate() {
  const emailBody = await getEmailBody();
  const emailSubject = Office.context.mailbox.item.subject;
  
  showSpinner();
  
  try {
    const response = await fetch("http://localhost:5000/extract", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email: emailBody,
        subject: emailSubject
      })
    });
    
    const result = await response.json();
    
    if (response.ok) {
      showSuccess("Candidate extracted successfully!");
    } else {
      showError(result.error || "Extraction failed");
    }
  } catch (error) {
    showError("Cannot connect to extraction service. Is it running?");
  } finally {
    hideSpinner();
  }
}
```

**Acceptance Criteria:**
- Fetch call succeeds from add-in
- Loading spinner shows/hides correctly
- Error messages clear and actionable

---

#### 4.2 CORS Configuration (Day 17)
- [ ] Configure Flask CORS to allow Outlook origin
- [ ] Handle preflight OPTIONS requests
- [ ] Test from actual Outlook (not just browser dev tools)

**Code:**
```python
from flask_cors import CORS

app = Flask(__name__)

# Allow Outlook Add-in origin
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:*",
            "https://*.outlook.com",
            "https://*.office.com"
        ]
    }
})
```

**Acceptance Criteria:**
- No CORS errors in browser console
- Requests from Outlook succeed

---

#### 4.3 Status Feedback (Day 18)
- [ ] Show real-time status updates in UI
- [ ] Display extraction progress (e.g., "Calling AI...")
- [ ] Show success message with details (e.g., "Extracted: Rajesh Kumar")
- [ ] Show error message with troubleshooting tips

**UI States:**
1. **Idle**: Button enabled, no message
2. **Processing**: Spinner visible, "Extracting data..."
3. **Success**: Green checkmark, "Candidate: [Name] extracted"
4. **Error**: Red X, "Error: [Message]"

**Acceptance Criteria:**
- User always knows what's happening
- Success state shows candidate name
- Error state suggests next steps

---

#### 4.4 Error Handling & Retry (Day 18-19)
- [ ] Detect if Python service is down
- [ ] Detect if Ollama is not running
- [ ] Implement retry logic (1 automatic retry)
- [ ] Show actionable error messages

**Error Messages:**
```javascript
const ERROR_MESSAGES = {
  SERVICE_DOWN: "Extraction service not running. Please start python-service/app.py",
  OLLAMA_DOWN: "AI service unavailable. Please start Ollama.",
  TIMEOUT: "Extraction took too long. Try a shorter email.",
  EXCEL_LOCKED: "Excel file is open. Please close it and try again.",
  UNKNOWN: "Extraction failed. Check python-service logs for details."
};
```

**Acceptance Criteria:**
- Each error has a clear, actionable message
- Retry logic works (test by stopping/starting services)
- No silent failures

---

#### 4.5 Auto-Trigger: Windows Mail Watcher (Day 19-20)
- [ ] Implement Outlook COM-based watcher using `pywin32` (Windows only)
- [ ] Run as a tray/background script `python-service/watcher.py`
- [ ] Listen for new mail in configured Inbox/Folder
- [ ] Apply identification rules: `MATCH_FROM` and `MATCH_SUBJECT_KEYWORDS`
- [ ] On match, call local `/extract` with subject/body
- [ ] Log actions and errors

**Acceptance Criteria:**
- New matching emails auto-processed within 10 seconds
- Non-matching emails ignored
- Clear logs available for diagnostics

---

#### 4.6 User Experience Polish (Day 20-21)
- [ ] Add keyboard shortcuts (e.g., Ctrl+E for extract)
- [ ] Improve button styling (professional look)
- [ ] Add success sound (optional)
- [ ] Add "View Excel" link after extraction

**Enhancements:**
- Button: Blue with white text, hover effect
- Success: Green background, 3-second auto-dismiss
- Error: Red background, manual dismiss
- Link to Excel: Opens file in default app

**Acceptance Criteria:**
- UI looks professional (not default HTML)
- User can trigger extraction with keyboard
- "View Excel" link works

---

#### 4.7 End-to-End Testing (Day 21)
- [ ] Test complete flow: Outlook → Flask → Ollama → Excel → AppSheet
- [ ] Test with 20 real job application emails
- [ ] Measure end-to-end time (target: < 15 seconds)
- [ ] Test error scenarios (service down, file locked)
- [ ] Test on different Outlook versions (2019, 365)

**Test Matrix:**

| Email Type | Expected Outcome | Pass/Fail |
|------------|------------------|-----------|
| Complete profile (all fields) | All 20 fields extracted | |
| Minimal profile (name, email) | Name + email extracted, rest null | |
| Ambiguous text | Best-effort extraction, nulls where unclear | |
| Non-job email | Graceful failure or partial extraction | |
| HTML-heavy email | Plain text extracted correctly | |

**Acceptance Criteria:**
- 90%+ success rate on real emails
- Average extraction time < 15 seconds
- Error recovery works in all scenarios
- Auto-trigger success: 90%+ of matching arrivals processed automatically

---

### Week 4 Milestone

**Demo:** Live demo with real Outlook email → Click button → Excel row appears

**Definition of Done:**
✅ Full flow working (Outlook → Excel)  
✅ CORS configured correctly  
✅ Error handling comprehensive  
✅ UX polished  
✅ Tested with 20+ real emails  
✅ Performance acceptable (< 15s)

---

## Phase 5: Advanced Features & Polish (Week 5)

### Objective
Add production-ready features and optimize performance.

### Deliverables

#### 5.1 Batch Processing (Day 22-23)
- [ ] Add "Extract Multiple" button in add-in
- [ ] Allow user to select multiple emails (Outlook API)
- [ ] Process emails in sequence
- [ ] Show progress bar (1 of 10)
- [ ] Write all to Excel in batch

**Code:**
```javascript
async function extractMultiple() {
  const mailbox = Office.context.mailbox;
  const selectedItems = mailbox.selectedItems;  // Requires additional permissions
  
  for (let i = 0; i < selectedItems.length; i++) {
    updateProgress(i + 1, selectedItems.length);
    await extractSingleEmail(selectedItems[i]);
  }
  
  showSuccess(`Extracted ${selectedItems.length} candidates`);
}
```

**Acceptance Criteria:**
- User can select 10 emails → Click once → All extracted
- Progress bar updates in real-time
- No performance degradation

---

#### 5.2 Confidence Scoring (Day 23-24)
- [ ] Calculate per-field confidence
- [ ] Calculate overall confidence score
- [ ] Highlight low-confidence fields in Excel (future: conditional formatting)
- [ ] Add confidence threshold (e.g., reject if < 50%)

**Algorithm:**
```python
def calculate_confidence(data: dict, ai_metadata: dict) -> float:
    scores = []
    
    # Coverage score: How many fields were extracted?
    filled_fields = sum(1 for v in data.values() if v not in [None, "", []])
    coverage = filled_fields / len(data)
    scores.append(coverage * 0.5)  # 50% weight
    
    # Format score: Are formats valid? (email, phone, CTC)
    valid_formats = 0
    if data.get("email") and "@" in data["email"]:
        valid_formats += 1
    if data.get("mobile") and data["mobile"].startswith("+91"):
        valid_formats += 1
    format_score = valid_formats / 3  # Assuming 3 format-sensitive fields
    scores.append(format_score * 0.3)  # 30% weight
    
    # AI certainty (future: use logprobs from Ollama)
    ai_certainty = ai_metadata.get("certainty", 0.7)  # Default 70%
    scores.append(ai_certainty * 0.2)  # 20% weight
    
    return sum(scores)
```

**Acceptance Criteria:**
- Confidence score between 0-1
- Low confidence (< 0.5) triggers warning
- Scores stored in Excel

---

#### 5.3 Duplicate Detection (Day 24-25)
- [ ] Check if candidate already exists (by email or mobile)
- [ ] Warn user before adding duplicate
- [ ] Offer to skip or update existing record

**Code:**
```python
def check_duplicate(data: dict) -> dict | None:
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    
    # Check by email
    if data.get("email"):
        matches = df[df["Email"] == data["email"]]
        if not matches.empty:
            return {"type": "email", "row": matches.index[0], "name": matches.iloc[0]["Applicant Name"]}
    
    # Check by mobile
    if data.get("mobile"):
        matches = df[df["Mobile"] == data["mobile"]]
        if not matches.empty:
            return {"type": "mobile", "row": matches.index[0], "name": matches.iloc[0]["Applicant Name"]}
    
    return None
```

**Acceptance Criteria:**
- Duplicate detected before write
- User prompted to confirm
- No duplicate entries in Excel

---

#### 5.4 UI Settings Panel (Day 25-26)
- [ ] Add simple settings UI in taskpane to show current provider/model
- [ ] Display `.env` driven rules (read-only) and Excel path
- [ ] Link to open watcher logs

**Acceptance Criteria:**
- Users can view configuration context easily
- Quick access to logs for troubleshooting

---

#### 5.5 Logging & Monitoring (Day 26-27)
- [ ] Implement structured logging in Python
- [ ] Log every extraction attempt
- [ ] Log errors with stack traces
- [ ] Create daily log rotation
- [ ] Add metrics dashboard (simple HTML page)

**Logging:**
```python
import logging

logging.basicConfig(
    filename=f"logs/extraction_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info(f"Extraction started | Subject: {subject}")
logging.info(f"Ollama latency: {elapsed}s | Fields: {filled_count}/23")
logging.error(f"Extraction failed | Error: {error}")
```

**Metrics Dashboard:**
- Total extractions today
- Success rate
- Average latency
- Top errors

**Acceptance Criteria:**
- All extractions logged
- Logs rotated daily
- Dashboard accessible at `http://localhost:5000/metrics`

---

#### 5.6 Performance Optimization (Day 27-28)
- [ ] Profile Python service (identify bottlenecks)
- [ ] Optimize Ollama prompt (reduce tokens)
- [ ] Cache frequently used data
- [ ] Parallelize batch processing (if possible)

**Optimizations:**
1. **Reduce Prompt Size**: Remove verbose examples
2. **Faster Model**: Test Phi-3 (4s vs. 8s)
3. **Excel Buffering**: Write in batches of 10
4. **Connection Pooling**: Reuse HTTP connections

**Targets:**
- Single extraction: < 10 seconds (down from 15s)
- Batch of 10: < 60 seconds (6s per email)

**Acceptance Criteria:**
- 30%+ performance improvement
- No accuracy loss

---

### Week 5 Milestone

**Demo:** Extract 50 emails in one click with progress bar and confidence scores

**Definition of Done:**
✅ Batch processing works  
✅ Confidence scoring implemented  
✅ Duplicate detection active  
✅ Logging comprehensive  
✅ Performance optimized

---

## Phase 6: Deployment & Documentation (Week 6)

### Objective
Prepare for production deployment and user onboarding.

### Deliverables

#### 6.1 Deployment Scripts (Day 29)
- [ ] Create `setup_ollama.bat` (Windows)
- [ ] Create `start_service.bat` (Windows)
- [ ] Create `install_addin.ps1` (PowerShell)
- [ ] Test on fresh Windows 10/11 machine

**setup_ollama.bat:**
```batch
@echo off
echo Installing Ollama...
winget install Ollama.Ollama

echo Pulling Mistral model...
ollama pull mistral

echo Setup complete! Press any key to exit.
pause
```

**start_service.bat:**
```batch
@echo off
cd /d "%~dp0python-service"
python app.py
pause
```

**Acceptance Criteria:**
- Scripts work on clean machine
- Non-technical user can follow instructions

---

#### 6.2 User Documentation (Day 29-30)
- [ ] Create `USER_GUIDE.md`
- [ ] Add screenshots of each step
- [ ] Create video tutorial (optional)
- [ ] Write FAQ section

**USER_GUIDE.md Contents:**
1. System Requirements
2. Installation Steps (with screenshots)
3. First-Time Setup
4. Daily Usage
5. Troubleshooting
6. FAQ

**Acceptance Criteria:**
- Non-technical user can follow guide
- All steps have screenshots
- Common issues documented

---

#### 6.3 Technical Documentation (Day 30-31)
- [ ] Complete code comments
- [ ] Generate API documentation (Swagger for Flask)
- [ ] Document architecture decisions
- [ ] Create troubleshooting guide for developers

**TROUBLESHOOTING.md:**
- Ollama won't start
- Python dependencies fail
- Add-in doesn't appear in Outlook
- Extraction accuracy low
- Excel file corrupted

**Acceptance Criteria:**
- All code has docstrings
- API documentation generated
- Troubleshooting guide covers 20+ issues

---

#### 6.4 Testing & QA (Day 31-32)
- [ ] Full regression testing (all features)
- [ ] User acceptance testing with 3 recruiters
- [ ] Performance testing (100 emails)
- [ ] Security review (CORS, input validation)
- [ ] Browser compatibility (Edge, Chrome)

**Test Checklist:**
- [ ] Fresh installation works
- [ ] All features function correctly
- [ ] No data loss in edge cases
- [ ] Error messages clear
- [ ] Performance acceptable

**Acceptance Criteria:**
- 95%+ test pass rate
- All P0 bugs fixed
- UAT sign-off from stakeholders

---

#### 6.5 AppSheet Configuration (Day 32-33)
- [ ] Upload Excel to OneDrive/SharePoint
- [ ] Connect AppSheet to Excel
- [ ] Create basic views (table, card, dashboard)
- [ ] Add filters (by location, CTC, skills)
- [ ] Test real-time sync

**AppSheet Views:**
1. **Candidate List**: Table with all fields
2. **Pipeline View**: Cards grouped by status (to be added manually)
3. **Search**: Filter by skills, location, CTC
4. **Dashboard**: Metrics (total candidates, avg CTC, etc.)

**Acceptance Criteria:**
- AppSheet syncs within 5 minutes
- All fields visible and editable
- Views render correctly on mobile

---

#### 6.6 Launch Preparation (Day 33-35)
- [ ] Create deployment checklist
- [ ] Train 2-3 power users
- [ ] Set up support channel (email/Slack)
- [ ] Create backup of Excel template
- [ ] Schedule go-live date

**Launch Checklist:**
- [ ] All users have Outlook 2019/365
- [ ] Ollama installed on each machine
- [ ] Python dependencies installed
- [ ] Add-in sideloaded for all users
- [ ] Excel in OneDrive configured
- [ ] AppSheet app shared with team

**Training Session (60 minutes):**
1. Overview of system (10 min)
2. Live demo (15 min)
3. Hands-on practice (20 min)
4. Q&A (15 min)

**Acceptance Criteria:**
- All users trained
- Support channel active
- Deployment checklist 100% complete

---

### Week 6 Milestone

**Demo:** Full production deployment on 3 user machines

**Definition of Done:**
✅ Scripts tested on fresh machines  
✅ Documentation complete  
✅ UAT passed  
✅ AppSheet configured  
✅ Users trained  
✅ System live in production

---

## Post-Launch (Week 7+)

### Immediate Next Steps
1. **Monitor Usage** (Daily for first week)
   - Track extractions per day
   - Monitor error rates
   - Collect user feedback

2. **Quick Fixes** (Week 7)
   - Address bugs reported by users
   - Adjust AI prompt based on accuracy issues
   - Optimize slow operations

3. **Iteration** (Week 8-12)
   - Add requested features
   - Improve accuracy (target: 90%+)
   - Expand to CV/resume parsing

---

## Risk Management

### Critical Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ollama fails to install | Medium | High | Pre-test on target machines, provide manual install guide |
| Excel file corruption | Low | High | Daily backups to OneDrive, implement atomic writes |
| Low extraction accuracy | Medium | Medium | Extensive testing in Week 2, prompt iteration |
| User adoption resistance | Low | Medium | Strong training, show time savings |
| Outlook version incompatibility | Low | Medium | Test on 2019 and 365, document minimum version |

---

## Success Criteria (Final)

### Functional Criteria
✅ User can extract candidate from email in < 15 seconds  
✅ 85%+ extraction accuracy on real emails  
✅ Excel file grows to 100+ candidates without issues  
✅ AppSheet syncs and displays data correctly

### Non-Functional Criteria
✅ System runs on standard corporate hardware (8GB RAM)  
✅ Internet optional (local-first); cloud only if enabled  
✅ User-friendly (non-technical users can operate)  
✅ Maintainable (clear code, good documentation)

### Business Criteria
✅ 90% reduction in manual data entry time  
✅ Zero recurring costs  
✅ GDPR/privacy compliant  
✅ Scalable to 10+ users

---

## Budget & Resources

### Development Costs
- **Labor**: 1 developer × 6 weeks × 40 hours = 240 hours
- **Hardware**: None (use existing laptops)
- **Software**: $0 (all open-source)
- **Cloud**: $0 (local-first architecture)

**Total Cost**: Labor only (estimate: ₹1,20,000 at ₹500/hour)

### Ongoing Costs
- **Maintenance**: 2 hours/week (₹4,000/month)
- **Electricity**: ~₹50/month per user
- **Total**: ~₹4,500/month for 10 users

**ROI Calculation:**
- Manual entry: 5 min/email × 500 emails/month = 41.6 hours
- Cost of manual work: 41.6 hours × ₹500/hour = ₹20,800/month
- nViteXtracter cost: ₹4,500/month
- **Savings: ₹16,300/month (78% reduction)**

---

## Appendix: Sprint Board Template

### Sprint Structure (2-Week Sprints)

**Sprint 1 (Week 1-2): Foundation + AI**
- User Story 1: As a recruiter, I want to click a button in Outlook to extract candidate data
- User Story 2: As a system, I need to call a local AI to parse email text

**Sprint 2 (Week 3-4): Excel + Integration**
- User Story 3: As a recruiter, I want extracted data to appear in an Excel file
- User Story 4: As a recruiter, I want to see the extracted candidate name immediately

**Sprint 3 (Week 5-6): Polish + Launch**
- User Story 5: As a recruiter, I want to extract multiple emails at once
- User Story 6: As a team, we want to use AppSheet to manage candidates

---

**Document Version:** 1.0  
**Last Updated:** January 10, 2026  
**Maintained By:** nViteXtracter Development Team
