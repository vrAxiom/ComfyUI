# nViteXtracter - Data Schema & Field Definitions

**Version:** 1.0  
**Last Updated:** January 10, 2026

---

## Complete Data Schema

### Master Field List (Core 26 + Optional Job/Links)

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
  "date_of_birth": "string|null",
  "mobile": "string|null",
  "email": "string|null",
  "offer_in_hand_lpa": "float|null",
  "ingested_at": "string (ISO8601)",
  "email_subject": "string",
  "from_email": "string",
  "ai_provider": "string",
  "ai_model": "string",
  "confidence_score": "float|null",

  "response_link": "string|null",
  "contact_details_link": "string|null",
  "job_applicants_count": "integer|null",
  "job_posted_days": "integer|null"
}
```

---

## Field Definitions (Detailed Specification)

### 1. job_title
- **Type:** `string | null`
- **Description:** Position applied for
- **Examples:** 
  - "Senior Software Engineer"
  - "Product Manager"
  - "Data Analyst"
- **Extraction Logic:** Look for phrases like:
  - "Applying for [TITLE]"
  - "Position: [TITLE]"
  - "Subject: Application for [TITLE]"
- **Validation:** Max 100 characters
- **Null Condition:** If not mentioned in email

---

### 2. employer
- **Type:** `string | null`
- **Description:** Company name from job posting
- **Examples:**
  - "nVite Technologies"
  - "TCS"
  - "Google India"
- **Extraction Logic:** Look for:
  - "Applying to [COMPANY]"
  - "Position at [COMPANY]"
  - Email recipient domain (if recruiting@nvite.com → "nVite")
- **Validation:** Max 100 characters
- **Null Condition:** If not mentioned

---

### 3. applicant_name
- **Type:** `string | null`
- **Description:** Full name of candidate
- **Examples:**
  - "Rajesh Kumar Sharma"
  - "Priya Nair"
  - "Amit Singh"
- **Extraction Logic:** Look for:
  - Email signature
  - "My name is [NAME]"
  - "This is [NAME]"
- **Validation:** 
  - Min 2 characters
  - Max 100 characters
  - Should contain letters only (spaces allowed)
- **Null Condition:** If not mentioned (critical field)

---

### 4. current_designation
- **Type:** `string | null`
- **Description:** Current job title
- **Examples:**
  - "Software Engineer"
  - "Team Lead"
  - "Associate Consultant"
- **Extraction Logic:** Look for:
  - "Currently working as [TITLE]"
  - "Current role: [TITLE]"
  - "Designation: [TITLE]"
- **Validation:** Max 100 characters
- **Null Condition:** If unemployed or not mentioned

---

### 5. current_company
- **Type:** `string | null`
- **Description:** Current employer name
- **Examples:**
  - "Tata Consultancy Services"
  - "Infosys"
  - "Freelance"
- **Extraction Logic:** Look for:
  - "Working at [COMPANY]"
  - "Currently employed with [COMPANY]"
  - "Company: [COMPANY]"
- **Validation:** Max 100 characters
- **Null Condition:** If unemployed or not mentioned

---

### 6. experience_years
- **Type:** `integer | null`
- **Description:** Total years of work experience
- **Examples:** `5`, `10`, `2`
- **Extraction Logic:** Parse from:
  - "5 years 3 months" → Extract `5`
  - "3.5 years experience" → Extract `3`
  - "6+ years" → Extract `6`
- **Validation:** Range 0-50
- **Null Condition:** If not mentioned or fresher

---

### 7. experience_months
- **Type:** `integer | null`
- **Description:** Additional months beyond full years
- **Examples:** `3`, `6`, `0`
- **Extraction Logic:** Parse from:
  - "5 years 3 months" → Extract `3`
  - "3.5 years" → Extract `6` (0.5 years = 6 months)
- **Validation:** Range 0-11
- **Null Condition:** If not mentioned

---

### 8. current_ctc_lpa
- **Type:** `float | null`
- **Description:** Current salary in Lakhs Per Annum (LPA)
- **Examples:** `8.5`, `12.0`, `25.5`
- **Extraction Logic:** Parse from:
  - "Current CTC: ₹8.5 LPA" → Extract `8.5`
  - "Earning 850000 per year" → Convert to `8.5`
  - "₹8,50,000 annual" → Convert to `8.5`
- **Validation:** Range 0-500 (LPA)
- **Null Condition:** If not mentioned

---

### 9. expected_ctc_lpa
- **Type:** `float | null`
- **Description:** Expected salary in Lakhs Per Annum (LPA)
- **Examples:** `12.0`, `15.5`, `30.0`
- **Extraction Logic:** Parse from:
  - "Expected CTC: ₹12 LPA" → Extract `12.0`
  - "Looking for 15-18 LPA" → Extract `15.0` (lower bound)
- **Validation:** Range 0-1000 (LPA)
- **Null Condition:** If not mentioned

---

### 10. location_current
- **Type:** `string | null`
- **Description:** Current city/location
- **Examples:**
  - "Bangalore"
  - "Mumbai"
  - "Hyderabad"
- **Extraction Logic:** Look for:
  - "Currently based in [LOCATION]"
  - "Location: [LOCATION]"
  - "Living in [LOCATION]"
- **Validation:** Max 100 characters
- **Null Condition:** If not mentioned

---

### 11. location_preferred
- **Type:** `array[string] | null`
- **Description:** Preferred work locations
- **Examples:**
  - ["Bangalore", "Pune"]
  - ["Mumbai"]
  - ["Open to relocation"]
- **Extraction Logic:** Parse from:
  - "Open to Bangalore, Pune, Hyderabad" → "Bangalore,Pune,Hyderabad"
  - "Prefer Mumbai" → "Mumbai"
- **Excel Representation:** Converted to CSV string for Excel
- **Validation:** Max 200 characters total
- **Null Condition:** If not mentioned

---

### 12. past_company
- **Type:** `string | null`
- **Description:** Previous employer (most recent)
- **Examples:**
  - "Cognizant"
  - "Wipro"
  - "Startup (stealth mode)"
- **Extraction Logic:** Look for:
  - "Previously worked at [COMPANY]"
  - "Former employer: [COMPANY]"
  - Resume work history
- **Validation:** Max 100 characters
- **Null Condition:** If fresher or not mentioned

---

### 13. notice_period_months
- **Type:** `integer | null`
- **Description:** Notice period in months
- **Examples:** `1`, `2`, `3`, `0`
- **Extraction Logic:** Parse from:
  - "Notice period: 2 months" → Extract `2`
  - "Can join immediately" → `0`
  - "60 days notice" → Convert to `2`
- **Validation:** Range 0-6
- **Null Condition:** If not mentioned

---

### 14. education
- **Type:** `string | null`
- **Description:** Highest degree obtained
- **Examples:**
  - "B.Tech Computer Science"
  - "MBA"
  - "MCA"
- **Extraction Logic:** Look for:
  - "Graduated with [DEGREE]"
  - "Education: [DEGREE]"
  - "B.Tech / B.E. / M.Tech / MBA / MCA"
- **Validation:** Max 150 characters
- **Null Condition:** If not mentioned

---

### 15. university
- **Type:** `string | null`
- **Description:** Educational institution name
- **Examples:**
  - "VIT University"
  - "IIT Bombay"
  - "Anna University"
- **Extraction Logic:** Look for:
  - "From [UNIVERSITY]"
  - "Graduated from [UNIVERSITY]"
  - "College: [UNIVERSITY]"
- **Validation:** Max 150 characters
- **Null Condition:** If not mentioned

---

### 16. key_skills
- **Type:** `array[string] | null`
- **Description:** Technical/professional skills
- **Examples:**
  - ["Python", "React", "AWS", "Docker"]
  - ["Java", "Spring Boot", "Microservices"]
  - ["Data Analysis", "SQL", "Tableau"]
- **Extraction Logic:** Parse from:
  - "Skills: Python, React, AWS" → "Python,React,AWS"
  - "Proficient in Java and SQL" → "Java,SQL"
- **Excel Representation:** Converted to CSV string for Excel

---

### 27. response_link (Optional)
- **Type:** `string | null`
- **Description:** URL to the portal page showing the candidate's full response
- **Examples:**
  - "https://naukri.com/employer/response/abcd1234"
- **Extraction Logic:** From "View response" hyperlink in email
- **Validation:** Max 500 characters; must be URL if present

---

### 28. contact_details_link (Optional)
- **Type:** `string | null`
- **Description:** URL to view contact details when gated by the portal
- **Examples:**
  - "https://naukri.com/employer/contact/efgh5678"
- **Extraction Logic:** From "View Contact Details" hyperlink in email
- **Validation:** Max 500 characters; must be URL if present

---

### 29. job_applicants_count (Optional)
- **Type:** `integer | null`
- **Description:** Number of applicants shown in the job summary header
- **Examples:** `4`, `17`
- **Extraction Logic:** From header like "Applicants 4"
- **Validation:** Range 0-100000

---

### 30. job_posted_days (Optional)
- **Type:** `integer | null`
- **Description:** Age of the job posting in days shown in the header
- **Examples:** `1`, `7`, `30`
- **Extraction Logic:** From header like "Posted 1 days ago"
- **Validation:** Range 0-3650
- **Validation:** Max 500 characters total
- **Null Condition:** If not mentioned

---

### 17. date_of_birth
- **Type:** `string (YYYY-MM-DD) | null`
- **Description:** Candidate's birth date
- **Examples:**
  - "1995-06-15"
  - "1992-12-01"
- **Extraction Logic:** Parse from:
  - "DOB: 15/06/1995" → Convert to "1995-06-15"
  - "Born on 1st Dec 1992" → Convert to "1992-12-01"
- **Validation:** ISO 8601 format, reasonable year (1950-2010)
- **Null Condition:** If not mentioned (often not provided)

---

### 18. mobile
- **Type:** `string | null`
- **Description:** Contact phone number
- **Examples:**
  - "+919876543210"
  - "+918123456789"
- **Extraction Logic:** Parse from:
  - "Mobile: 9876543210" → Normalize to "+919876543210"
  - "+91-98765-43210" → Normalize to "+919876543210"
  - "Call me at 9876543210" → "+919876543210"
- **Validation:** 
  - Indian format: +91 followed by 10 digits
  - Remove spaces, hyphens, parentheses
- **Null Condition:** If not mentioned (critical field)

---

### 19. email
- **Type:** `string | null`
- **Description:** Contact email address
- **Examples:**
  - "rajesh.kumar@example.com"
  - "priya.nair@gmail.com"
- **Extraction Logic:** Parse from:
  - Email body text
  - Email signature
  - "Contact: [EMAIL]"
- **Validation:** 
  - Valid email format (regex: `^[^@]+@[^@]+\.[^@]+$`)
  - Lowercase
  - Trim whitespace
- **Null Condition:** If not mentioned (critical field)

---

### 20. offer_in_hand_lpa
- **Type:** `float | null`
- **Description:** Monetary value of current offer in hand, in LPA
- **Examples:** `32.0`, `32.5`, `null`
- **Extraction Logic:** Parse from:
  - "Offer in hand: 32 LPA" → `32.0`
  - "Offer: 32.5 lacs" → `32.5`
  - "0" or "No offers" → `null`
- **Validation:** Range 0-1000 (LPA)
- **Null Condition:** If not specified numerically
- **Notes:** Replaces previous boolean `offers_in_hand` (deprecated)

---

### 21. ingested_at (Metadata)
- **Type:** `string (ISO8601)`
- **Description:** Timestamp when data was extracted
- **Examples:** 
  - "2026-01-10T14:35:22.123Z"
  - "2026-01-10T09:15:00.000Z"
- **Generation:** Automatic (Python: `datetime.now().isoformat()`)
- **Validation:** ISO 8601 format
- **Null Condition:** Never null (always generated)

---

### 22. email_subject (Metadata)
- **Type:** `string`
- **Description:** Original email subject line
- **Examples:**
  - "Application for Senior Developer - nVite"
  - "Interested in Product Manager role"
- **Extraction:** Direct read from Outlook API
- **Validation:** Max 500 characters
- **Null Condition:** Never null (emails always have subjects)

---

### 23. from_email (Metadata)
- **Type:** `string`
- **Description:** Sender's email address (for identification and dedup)
- **Examples:**
  - "naukri@notifications.naukri.com"
  - "jobs@linkedin.com"
- **Extraction:** Direct read from Outlook API (`item.from.emailAddress`)
- **Validation:** Valid email format
- **Null Condition:** Never null for received emails

---

### 24. ai_provider (Metadata)
- **Type:** `string`
- **Description:** AI provider used for extraction
- **Examples:** `"ollama"`, `"lmstudio"`, `"openai"`, `"gemini"`
- **Generation:** From service configuration
- **Null Condition:** Never null

---

### 25. ai_model (Metadata)
- **Type:** `string`
- **Description:** Model identifier used
- **Examples:** `"mistral:7b"`, `"gpt-4o-mini"`, `"gemini-1.5-pro"`
- **Generation:** From service configuration
- **Null Condition:** Never null

---

### 26. confidence_score (Future Enhancement)
- **Type:** `float | null`
- **Description:** AI extraction confidence (0.0 to 1.0)
- **Examples:** `0.95`, `0.72`, `null`
- **Calculation Logic (Phase 2):**
  ```python
  score = (
      (fields_extracted / total_fields) * 0.5 +  # Coverage
      (valid_formats / formatted_fields) * 0.3 +   # Format accuracy
      (high_confidence_count / total_fields) * 0.2 # AI certainty
  )
  ```
- **Validation:** Range 0.0-1.0
- **Null Condition:** Not implemented in MVP (always null)

---

## Data Type Mappings

### JSON → Excel Type Conversion

| JSON Type | Excel Type | Python Type | Pandas Dtype |
|-----------|------------|-------------|--------------|
| `string` | Text | `str` | `object` |
| `integer` | Number | `int` | `int64` |
| `float` | Number | `float` | `float64` |
| `boolean` | Boolean | `bool` | `bool` |
| `null` | Empty Cell | `None` | `NaN` |
| `array[string]` | Text (CSV) | `str` | `object` |
| `url` | Text (Hyperlink) | `str` | `object` |
| `lpa` (money) | Number | `float` | `float64` |

---

## Excel Column Configuration

### Column Headers (Exact Names)

```python
COLUMNS = [
    "Job Title",
    "Employer",
    "Applicant Name",
    "Current Designation",
    "Current Company",
    "Experience (Years)",
    "Experience (Months)",
    "Current CTC (LPA)",
    "Expected CTC (LPA)",
    "Current Location",
    "Preferred Locations",
    "Past Company",
    "Notice Period (Months)",
    "Education",
    "University",
    "Key Skills",
    "Date of Birth",
    "Mobile",
    "Email",
    "Offer In Hand (LPA)",
    "Ingested At",
    "Email Subject",
    "From Email",
    "AI Provider",
    "AI Model",
    "Confidence Score",
    "Response Link",
    "Contact Details Link",
    "Job Applicants Count",
    "Job Posted (Days)"
]
```

### Column Widths (Optimal for Display)

```python
COLUMN_WIDTHS = {
    "Job Title": 30,
    "Employer": 25,
    "Applicant Name": 25,
    "Current Designation": 30,
    "Current Company": 25,
    "Experience (Years)": 18,
    "Experience (Months)": 18,
    "Current CTC (LPA)": 18,
    "Expected CTC (LPA)": 18,
    "Current Location": 20,
    "Preferred Locations": 35,
    "Past Company": 25,
    "Notice Period (Months)": 22,
    "Education": 40,
    "University": 30,
    "Key Skills": 60,
    "Date of Birth": 15,
    "Mobile": 18,
    "Email": 30,
    "Offer In Hand (LPA)": 18,
    "Ingested At": 25,
    "Email Subject": 50,
    "From Email": 35,
    "AI Provider": 14,
    "AI Model": 22,
    "Confidence Score": 18,
    "Response Link": 40,
    "Contact Details Link": 40,
    "Job Applicants Count": 20,
    "Job Posted (Days)": 20
}
```

---

## Normalization Rules

### 1. Array to CSV String
```python
# Input (from Ollama):
{
  "key_skills": ["Python", "React", "AWS"],
  "location_preferred": ["Bangalore", "Pune"]
}

# Output (for Excel):
{
  "key_skills": "Python,React,AWS",
  "location_preferred": "Bangalore,Pune"
}
```

### 2. Phone Number Normalization
```python
# Input variations:
"9876543210"
"+91-98765-43210"
"(+91) 9876543210"
"+91 98765 43210"

# Output (normalized):
"+919876543210"
```

### 3. Email Normalization
```python
# Input variations:
"Rajesh.Kumar@Example.COM"
"  rajesh.kumar@example.com  "

# Output (normalized):
"rajesh.kumar@example.com"
```

### 4. CTC Conversion
```python
# Input variations:
"₹8.5 LPA"
"850000 per annum"
"₹8,50,000"
"8.5L"
"21 Lacs"

# Output (normalized):
8.5  # Always as float LPA
```

### 5. Date Normalization
```python
# Input variations:
"15/06/1995"
"15-Jun-1995"
"June 15, 1995"
"1995-06-15"

# Output (normalized):
"1995-06-15"  # Always ISO 8601
```

---

## Validation Schema (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "job_title": {"type": ["string", "null"], "maxLength": 100},
    "employer": {"type": ["string", "null"], "maxLength": 100},
    "applicant_name": {"type": ["string", "null"], "maxLength": 100, "pattern": "^[A-Za-z\\s]+$"},
    "current_designation": {"type": ["string", "null"], "maxLength": 100},
    "current_company": {"type": ["string", "null"], "maxLength": 100},
    "experience_years": {"type": ["integer", "null"], "minimum": 0, "maximum": 50},
    "experience_months": {"type": ["integer", "null"], "minimum": 0, "maximum": 11},
    "current_ctc_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 500},
    "expected_ctc_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 1000},
    "location_current": {"type": ["string", "null"], "maxLength": 100},
    "location_preferred": {"type": ["array", "null"], "items": {"type": "string"}},
    "past_company": {"type": ["string", "null"], "maxLength": 100},
    "notice_period_months": {"type": ["integer", "null"], "minimum": 0, "maximum": 6},
    "education": {"type": ["string", "null"], "maxLength": 150},
    "university": {"type": ["string", "null"], "maxLength": 150},
    "key_skills": {"type": ["array", "null"], "items": {"type": "string"}},
    "date_of_birth": {"type": ["string", "null"], "format": "date"},
    "mobile": {"type": ["string", "null"], "pattern": "^\\+91[0-9]{10}$"},
    "email": {"type": ["string", "null"], "format": "email"},
    "offer_in_hand_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 1000},
    "ingested_at": {"type": "string", "format": "date-time"},
    "email_subject": {"type": "string", "maxLength": 500},
    "from_email": {"type": "string", "format": "email"},
    "ai_provider": {"type": "string", "enum": ["ollama", "lmstudio", "openai", "gemini"]},
    "ai_model": {"type": "string", "maxLength": 100},
    "confidence_score": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
    "response_link": {"type": ["string", "null"], "maxLength": 500},
    "contact_details_link": {"type": ["string", "null"], "maxLength": 500},
    "job_applicants_count": {"type": ["integer", "null"], "minimum": 0, "maximum": 100000},
    "job_posted_days": {"type": ["integer", "null"], "minimum": 0, "maximum": 3650}
  },
  "required": ["ingested_at", "email_subject", "from_email", "ai_provider", "ai_model"]
}
```

---

## AI Prompt Template

### Ollama Prompt Structure

```python
EXTRACTION_PROMPT = """
You are a precise data extraction engine for job application emails.
Your task is to extract candidate information and return ONLY valid JSON.

CRITICAL RULES:
1. Output ONLY JSON, no explanations or extra text
2. Use null for missing information, NEVER guess
3. Follow the exact schema provided
4. Normalize data according to rules
5. Do not invent data that is not in the email
6. If an "offer in hand" monetary value is present, return it as LPA in `offer_in_hand_lpa`; if absent or "0", return null

JSON SCHEMA:
{schema}

NORMALIZATION RULES:
- Arrays (key_skills, location_preferred): Return as arrays, will be converted to CSV
- Phone: Add +91 prefix if missing, remove spaces/hyphens
- Email: Lowercase
- CTC: Convert to LPA float (₹850000 → 8.5)
  - Support units: LPA, Lacs, Lac, Lakh; e.g., "32 Lacs" → 32.0
- Date: Use YYYY-MM-DD format
- Experience: "5 years 3 months" → years=5, months=3

EMAIL CONTENT:
---
Subject: {email_subject}

{email_body}
---

OUTPUT (JSON only):
"""

# Usage:
prompt = EXTRACTION_PROMPT.format(
    schema=json.dumps(SCHEMA, indent=2),
    email_subject=subject,
    email_body=body
)
```

---

## Sample Data (Test Cases)

### Test Case 1: Complete Profile

**Input Email:**
```
Subject: Application for Senior Developer - nVite

Dear Hiring Manager,

I am Rajesh Kumar, applying for the Senior Developer position at nVite Technologies.

Current Role: Software Engineer at TCS
Experience: 5 years 3 months
Current CTC: 8.5 LPA
Expected CTC: 12 LPA
Location: Bangalore (open to Pune, Hyderabad)
Notice Period: 2 months

Education: B.Tech Computer Science, VIT University
Skills: Python, React, AWS, Docker
DOB: 15th June 1995
Mobile: +91-9876543210
Email: rajesh.kumar@example.com

I have an offer from Infosys but interested in nVite.

Regards,
Rajesh Kumar
```

**Expected JSON:**
```json
{
  "job_title": "Senior Developer",
  "employer": "nVite Technologies",
  "applicant_name": "Rajesh Kumar",
  "current_designation": "Software Engineer",
  "current_company": "TCS",
  "experience_years": 5,
  "experience_months": 3,
  "current_ctc_lpa": 8.5,
  "expected_ctc_lpa": 12.0,
  "location_current": "Bangalore",
  "location_preferred": ["Bangalore", "Pune", "Hyderabad"],
  "past_company": null,
  "notice_period_months": 2,
  "education": "B.Tech Computer Science",
  "university": "VIT University",
  "key_skills": ["Python", "React", "AWS", "Docker"],
  "date_of_birth": "1995-06-15",
  "mobile": "+919876543210",
  "email": "rajesh.kumar@example.com",
  "offer_in_hand_lpa": null,
  "ingested_at": "2026-01-10T14:30:00.000Z",
  "email_subject": "Application for Senior Developer - nVite",
  "from_email": "rajesh.kumar@example.com",
  "ai_provider": "ollama",
  "ai_model": "mistral:7b",
  "confidence_score": null
}
```

**Expected Excel Row (after normalization):**
| Job Title | Employer | Applicant Name | ... | Key Skills | Mobile | Offers in Hand |
|-----------|----------|----------------|-----|------------|--------|----------------|
| Senior Developer | nVite Technologies | Rajesh Kumar | ... | Python,React,AWS,Docker | +919876543210 | TRUE |

---

### Test Case 2: Minimal Profile (Many Nulls)

**Input Email:**
```
Subject: Interested in Data Analyst Role

Hi,

I am Priya Nair and I want to apply for the Data Analyst position.

I have 2 years experience in SQL and Tableau.

Contact: priya.nair@gmail.com

Thanks,
Priya
```

**Expected JSON:**
```json
{
  "job_title": "Data Analyst",
  "employer": null,
  "applicant_name": "Priya Nair",
  "current_designation": null,
  "current_company": null,
  "experience_years": 2,
  "experience_months": null,
  "current_ctc_lpa": null,
  "expected_ctc_lpa": null,
  "location_current": null,
  "location_preferred": null,
  "past_company": null,
  "notice_period_months": null,
  "education": null,
  "university": null,
  "key_skills": ["SQL", "Tableau"],
  "date_of_birth": null,
  "mobile": null,
  "email": "priya.nair@gmail.com",
  "offer_in_hand_lpa": null,
  "ingested_at": "2026-01-10T14:35:00.000Z",
  "email_subject": "Interested in Data Analyst Role",
  "from_email": "priya.nair@gmail.com",
  "ai_provider": "ollama",
  "ai_model": "mistral:7b",
  "confidence_score": null
}
```

---

### Test Case 3: nVite/Naukri Response (Provided Sample)

**Input Email (abridged):**
```
NVite

You have a new response

Job Title
Innovation Manager    Applicants
4

Pune

Posted 1 days ago

Pratyush

Senior Business Analyst at Michelin

7 Years & 0 Months

21 Lacs

View Contact Details

Location        Pune (preferred location is Bangalore/Bengaluru, Pune, Mumbai, Hyderabad/Secunderabad, Noida, Ahmedabad, Gurgaon/Gurugram, Kolkata, Chennai, Delhi / NCR)

Past Experience        Senior Business Analyst at HCLTech

Notice Period        1 Month

Education        MBA/PGDM at TA Pai Management Institute, Karnataka

Keyskills        Aiml,generative ai,Requirement Analysis,Impact Analysis,Business Analysis,Process Consulting,Business Consulting,Brd,Salesforce,Agile,UAT,Requirement Gathering,User Stories,Use Cases,Gap Analysis,JIRA,Visio,Requirements Management

View response

Check out candidate's response to your questions

Phone No/Email id/DOB

7709160411

current CTC /Expected CTC/Offer in Hand if any

0

What is your notice period?

1 Month
```

**Expected JSON:**
```json
{
  "job_title": "Innovation Manager",
  "employer": null,
  "applicant_name": "Pratyush",
  "current_designation": "Senior Business Analyst",
  "current_company": "Michelin",
  "experience_years": 7,
  "experience_months": 0,
  "current_ctc_lpa": 21.0,
  "expected_ctc_lpa": null,
  "location_current": "Pune",
  "location_preferred": [
    "Bangalore/Bengaluru",
    "Pune",
    "Mumbai",
    "Hyderabad/Secunderabad",
    "Noida",
    "Ahmedabad",
    "Gurgaon/Gurugram",
    "Kolkata",
    "Chennai",
    "Delhi / NCR"
  ],
  "past_company": "HCLTech",
  "notice_period_months": 1,
  "education": "MBA/PGDM",
  "university": "TA Pai Management Institute, Karnataka",
  "key_skills": [
    "Aiml",
    "generative ai",
    "Requirement Analysis",
    "Impact Analysis",
    "Business Analysis",
    "Process Consulting",
    "Business Consulting",
    "Brd",
    "Salesforce",
    "Agile",
    "UAT",
    "Requirement Gathering",
    "User Stories",
    "Use Cases",
    "Gap Analysis",
    "JIRA",
    "Visio",
    "Requirements Management"
  ],
  "date_of_birth": null,
  "mobile": "+917709160411",
  "email": null,
  "offer_in_hand_lpa": null,
  "ingested_at": "2026-01-10T14:45:00.000Z",
  "email_subject": "nVite: New applicant response - Innovation Manager",
  "from_email": "notifications@naukri.com",
  "ai_provider": "ollama",
  "ai_model": "mistral:7b",
  "confidence_score": null,
  "response_link": "https://example.naukri.com/view-response/abc",
  "contact_details_link": "https://example.naukri.com/view-contact/xyz",
  "job_applicants_count": 4,
  "job_posted_days": 1
}
```

Notes:
- CTC: "21 Lacs" normalized to 21.0 LPA
- Phone: Indian 10-digit normalized to "+91" format
- Preferred locations parsed into array; Excel will store CSV
- "0" under "current CTC /Expected CTC/Offer in Hand" is ambiguous → kept as nulls for expected/offer
- Links are placeholders if actual URLs are present in the HTML

---

## Field Extraction Accuracy Targets

| Field Category | Target Accuracy | Critical? |
|----------------|-----------------|-----------|
| **Candidate Identity** | | |
| ├─ applicant_name | 95%+ | ✅ Yes |
| ├─ mobile | 90%+ | ✅ Yes |
| └─ email | 95%+ | ✅ Yes |
| **Job Details** | | |
| ├─ job_title | 90%+ | Medium |
| └─ employer | 85%+ | Medium |
| **Experience** | | |
| ├─ experience_years | 85%+ | Medium |
| ├─ current_company | 80%+ | Medium |
| └─ current_designation | 80%+ | Medium |
| **Compensation** | | |
| ├─ current_ctc_lpa | 75%+ | Low |
| └─ expected_ctc_lpa | 80%+ | Medium |
| **Skills** | | |
| └─ key_skills | 70%+ | Medium |
| **Other** | | |
| └─ All other fields | 60%+ | Low |

**Overall Target:** 80%+ average accuracy across all fields

---

## Data Quality Checks

### Post-Extraction Validation

```python
def validate_extracted_data(data: dict) -> dict:
    """
    Perform data quality checks after Ollama extraction.
    Returns a dict with validation results.
    """
    issues = []
    
    # Critical field checks
    if not data.get("applicant_name"):
        issues.append("Missing applicant name (critical)")
    
    if not data.get("email") and not data.get("mobile"):
        issues.append("Missing both email and mobile (critical)")
    
    # Logical consistency checks
    if data.get("experience_years", 0) > 50:
        issues.append("Experience years suspiciously high")
    
    if data.get("expected_ctc_lpa", 0) < data.get("current_ctc_lpa", 0):
        issues.append("Expected CTC lower than current (unusual)")
    
    if data.get("experience_months", 0) > 11:
        issues.append("Experience months > 11 (should be years)")
    
    # Format checks
    if data.get("email") and "@" not in data.get("email"):
        issues.append("Invalid email format")
    
    if data.get("mobile") and not data.get("mobile").startswith("+91"):
        issues.append("Mobile missing country code")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "quality_score": 1.0 - (len(issues) * 0.1)  # Each issue reduces score by 10%
    }
```

---

## AppSheet Data Types

### Recommended AppSheet Column Types

| Field | AppSheet Type | Display Format |
|-------|---------------|----------------|
| job_title | Text | Plain |
| employer | Text | Plain |
| applicant_name | Text | Plain |
| current_designation | Text | Plain |
| current_company | Text | Plain |
| experience_years | Number | Integer |
| experience_months | Number | Integer |
| current_ctc_lpa | Number | Decimal (1 place) |
| expected_ctc_lpa | Number | Decimal (1 place) |
| location_current | Text | Plain |
| location_preferred | Text | Comma-separated |
| past_company | Text | Plain |
| notice_period_months | Number | Integer |
| education | Text | Plain |
| university | Text | Plain |
| key_skills | Text | Comma-separated |
| date_of_birth | Date | DD/MM/YYYY |
| mobile | Phone | +91 format |
| email | Email | Clickable link |
| offers_in_hand | Yes/No | Checkbox |
| ingested_at | DateTime | DD/MM/YYYY HH:MM |
| email_subject | Text | Plain |
| from_email | Email | Clickable link |
| ai_provider | Text | Enum (ollama/lmstudio/openai/gemini) |
| ai_model | Text | Plain |
| confidence_score | Number | Percentage (0-100%) |
| response_link | URL | Hyperlink |
| contact_details_link | URL | Hyperlink |
| job_applicants_count | Number | Integer |
| job_posted_days | Number | Integer |

---

## Future Enhancements (Field-Level)

### Phase 2: Additional Fields

```json
{
  "linkedin_url": "string|null",
  "github_url": "string|null",
  "portfolio_url": "string|null",
  "years_in_current_company": "integer|null",
  "total_companies_worked": "integer|null",
  "highest_qualification": "string|null",
  "graduation_year": "integer|null",
  "certifications": "array[string]",
  "languages_known": "array[string]",
  "willing_to_relocate": "boolean|null",
  "visa_status": "string|null",
  "marital_status": "string|null",
  "current_location_pincode": "string|null"
}
```

### Phase 3: Calculated Fields (Excel Formulas)

```excel
=IF(AND([Experience (Years)]>=3, [Current CTC (LPA)]>=8), "Senior", "Junior")  // Seniority
=DATEDIF([Date of Birth], TODAY(), "Y")  // Age (calculated)
=[Expected CTC (LPA)]-[Current CTC (LPA)]  // CTC Hike Expectation
=IF([Notice Period (Months)]<=1, "Immediate", "Delayed")  // Availability
```

---

**Document Version:** 1.0  
**Last Updated:** January 10, 2026  
**Maintained By:** nViteXtracter Development Team
