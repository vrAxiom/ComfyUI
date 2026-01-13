# Windows-only Outlook watcher using pywin32
# Listens for new mail and posts matching messages to the local extractor

import os
import time
import threading
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()

MATCH_FROM = [s.strip().lower() for s in os.getenv('MATCH_FROM', '').split(',') if s.strip()]
SUBJECT_KEYS = [s.strip().lower() for s in os.getenv('MATCH_SUBJECT_KEYWORDS', '').split(',') if s.strip()]
API_URL = os.getenv('API_URL', 'http://127.0.0.1:5000/extract')
WATCH_FOLDER = os.getenv('WATCH_FOLDER', 'Inbox')
POLL_INTERVAL = int(os.getenv('WATCH_POLL_INTERVAL', '5'))

try:
    import win32com.client
    import pythoncom
except Exception as e:
    print('pywin32 is required on Windows. Error:', e)
    raise


def _match_sender(sender_email: str) -> bool:
    s = (sender_email or '').lower()
    if not MATCH_FROM:
        return True
    for pat in MATCH_FROM:
        if pat in s:
            return True
    return False


def _match_subject(subject: str) -> bool:
    s = (subject or '').lower()
    if not SUBJECT_KEYS:
        return True
    for k in SUBJECT_KEYS:
        if k in s:
            return True
    return False


class InboxEvents:
    def __init__(self, items):
        self._items = items

    def OnItemAdd(self, item):
        try:
            subject = getattr(item, 'Subject', '')
            sender = getattr(getattr(item, 'Sender', None), 'Address', None) or getattr(item, 'SenderEmailAddress', '')
            if not (_match_sender(sender) and _match_subject(subject)):
                return
            body = getattr(item, 'Body', '')
            payload = {
                'email': body,
                'subject': subject,
                'from_email': sender,
            }
            try:
                requests.post(API_URL, json=payload, timeout=60)
                print('Auto-extracted:', subject)
            except Exception as e:
                print('POST failed:', e)
        except Exception as e:
            print('OnItemAdd error:', e)


def main():
    pythoncom.CoInitialize()
    outlook = win32com.client.gencache.EnsureDispatch('Outlook.Application')
    ns = outlook.GetNamespace('MAPI')
    inbox = ns.GetDefaultFolder(6)  # 6 = Inbox
    items = inbox.Items

    # Attach event sink
    import win32com.client
    handler = win32com.client.WithEvents(items, InboxEvents)

    print('Watcher running. Filtering by from:', MATCH_FROM, 'subject keys:', SUBJECT_KEYS)
    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
