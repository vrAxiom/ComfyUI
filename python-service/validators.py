import re
import math
from typing import Dict, Any, List

from jsonschema import validate as jsonschema_validate, Draft7Validator

SCHEMA_JSON = {
    "type": "object",
    "properties": {
        "job_title": {"type": ["string", "null"]},
        "employer": {"type": ["string", "null"]},
        "applicant_name": {"type": ["string", "null"]},
        "current_designation": {"type": ["string", "null"]},
        "current_company": {"type": ["string", "null"]},
        "experience_years": {"type": ["integer", "null"], "minimum": 0, "maximum": 50},
        "experience_months": {"type": ["integer", "null"], "minimum": 0, "maximum": 11},
        "current_ctc_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 1000},
        "expected_ctc_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 1000},
        "location_current": {"type": ["string", "null"]},
        "location_preferred": {"type": ["array", "null"], "items": {"type": "string"}},
        "past_company": {"type": ["string", "null"]},
        "notice_period_months": {"type": ["integer", "null"], "minimum": 0, "maximum": 6},
        "education": {"type": ["string", "null"]},
        "university": {"type": ["string", "null"]},
        "key_skills": {"type": ["array", "null"], "items": {"type": "string"}},
        "date_of_birth": {"type": ["string", "null"]},
        "mobile": {"type": ["string", "null"]},
        "email": {"type": ["string", "null"]},
        "offer_in_hand_lpa": {"type": ["number", "null"], "minimum": 0, "maximum": 1000},
        "ingested_at": {"type": ["string", "null"]},
        "email_subject": {"type": ["string", "null"]},
        "from_email": {"type": ["string", "null"]},
        "ai_provider": {"type": ["string", "null"]},
        "ai_model": {"type": ["string", "null"]},
        "confidence_score": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "response_link": {"type": ["string", "null"]},
        "contact_details_link": {"type": ["string", "null"]},
        "job_applicants_count": {"type": ["integer", "null"], "minimum": 0},
        "job_posted_days": {"type": ["integer", "null"], "minimum": 0}
    }
}

_phone_re = re.compile(r"(?:\+?91[\s-]?)?(\d{10})")
_email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize_phone(mobile: str | None) -> str | None:
    if not mobile:
        return None
    digits_match = _phone_re.search(mobile)
    if not digits_match:
        return None
    return "+91" + digits_match.group(1)


def _normalize_email(email: str | None) -> str | None:
    if not email:
        return None
    email = email.strip().lower()
    return email if _email_re.match(email) else None


def _normalize_ctc_lpa(text_val: Any) -> float | None:
    if text_val is None:
        return None
    if isinstance(text_val, (int, float)):
        return float(text_val) if float(text_val) > 0 else None
    s = str(text_val).strip().lower()
    if s in ("", "na", "n/a", "none", "0", "0.0"):
        return None
    # Extract number
    num_match = re.search(r"([0-9]+(?:\.[0-9]+)?)", s)
    if not num_match:
        return None
    val = float(num_match.group(1))
    # If indicates annual in rupees (₹850000), convert to lpa
    if any(u in s for u in ["per annum", "/year", "/annum"]) or "₹" in s or "," in s:
        if val > 1000:
            return round(val / 100000.0, 1)  # 100000 INR per lakh
    # If has lpa/lac/lakh/lacs keywords, assume already LPA
    return round(val, 1) if val > 0 else None


def normalize_and_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    # Coerce arrays
    if data.get("key_skills") is None:
        data["key_skills"] = []
    if data.get("location_preferred") is None:
        data["location_preferred"] = []

    # Numbers
    data["experience_years"] = int(data["experience_years"]) if data.get("experience_years") is not None else None
    data["experience_months"] = int(data["experience_months"]) if data.get("experience_months") is not None else None
    data["current_ctc_lpa"] = _normalize_ctc_lpa(data.get("current_ctc_lpa"))
    data["expected_ctc_lpa"] = _normalize_ctc_lpa(data.get("expected_ctc_lpa"))
    data["offer_in_hand_lpa"] = _normalize_ctc_lpa(data.get("offer_in_hand_lpa"))

    # Contacts
    data["mobile"] = _normalize_phone(data.get("mobile"))
    data["email"] = _normalize_email(data.get("email"))

    # Notice period textual to months
    np = data.get("notice_period_months")
    if isinstance(np, str):
        m = re.search(r"(\d+)", np)
        data["notice_period_months"] = int(m.group(1)) if m else None

    # Validate JSON schema (non-strict requireds here)
    Draft7Validator(SCHEMA_JSON).validate(data)
    return data
