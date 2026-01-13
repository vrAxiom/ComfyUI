import os
import sys
import json
import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SAMPLE = os.path.join(ROOT, 'tests', 'sample_emails', 'nvite_sample_1.txt')

API = os.environ.get('API_URL', 'http://127.0.0.1:5000/extract')


def main():
    email_path = SAMPLE
    if len(sys.argv) > 1:
        email_path = sys.argv[1]
    with open(email_path, 'r', encoding='utf-8') as f:
        body = f.read()

    payload = {
        'email': body,
        'subject': 'nVite: New applicant response - Innovation Manager',
        'from_email': 'notifications@naukri.com'
    }
    r = requests.post(API, json=payload, timeout=60)
    print('Status:', r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)


if __name__ == '__main__':
    main()
