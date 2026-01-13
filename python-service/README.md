# Python Service (Local Bridge)

## Quick Start

1) Configure environment
- Copy `.env.example` to `.env`
- Set `AI_PROVIDER`, `AI_MODEL`, `EXCEL_PATH`, `MATCH_FROM`, `MATCH_SUBJECT_KEYWORDS`

2) Setup dependencies (venv recommended)
```powershell
cd .\python-service
./dev_setup.ps1
```

3) Start services
```powershell
./dev_up.ps1      # Starts Flask app
./dev_watcher.ps1 # Starts Outlook watcher (Windows only, optional)
```

4) Health check
```powershell
curl http://127.0.0.1:5000/health
```

5) Run sample
```powershell
python run_sample.py
```

## Notes
- Offer in hand is captured as `offer_in_hand_lpa` (float LPA); text like "32 Lacs" -> 32.0
- Arrays (`key_skills`, `location_preferred`) return as arrays in JSON; Excel stores CSV strings.
- OneDrive path is recommended for `EXCEL_PATH` to enable AppSheet sync.
