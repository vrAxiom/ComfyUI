import json

SCHEMA = {
  "job_title": None,
  "employer": None,
  "applicant_name": None,
  "current_designation": None,
  "current_company": None,
  "experience_years": None,
  "experience_months": None,
  "current_ctc_lpa": None,
  "expected_ctc_lpa": None,
  "location_current": None,
  "location_preferred": [],
  "past_company": None,
  "notice_period_months": None,
  "education": None,
  "university": None,
  "key_skills": [],
  "date_of_birth": None,
  "mobile": None,
  "email": None,
  "offer_in_hand_lpa": None,
  "ingested_at": None,
  "email_subject": None,
  "from_email": None,
  "ai_provider": None,
  "ai_model": None,
  "confidence_score": None,
  "response_link": None,
  "contact_details_link": None,
  "job_applicants_count": None,
  "job_posted_days": None
}

EXTRACTION_PROMPT = """
You are a precise data extraction engine for job application emails.
Your task is to extract candidate information and return ONLY valid JSON.

CRITICAL RULES:
1. Output ONLY JSON, no explanations or extra text
2. Use null for missing information, NEVER guess
3. Follow the exact schema provided
4. Normalize data according to rules
5. Do not invent data that is not in the email
6. If an "offer in hand" monetary value is present, return it as LPA in offer_in_hand_lpa; if absent or "0", return null

JSON SCHEMA (keys with example null values):
{schema}

NORMALIZATION RULES:
- Arrays (key_skills, location_preferred): return as arrays (will be converted to CSV later)
- Phone: Add +91 prefix if missing, remove spaces/hyphens
- Email: Lowercase, trim
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

def build_prompt(subject: str, body: str) -> str:
    return EXTRACTION_PROMPT.format(
        schema=json.dumps(SCHEMA, indent=2),
        email_subject=subject,
        email_body=body,
    )
