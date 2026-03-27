#!/usr/bin/env python3
import json,sys
from google.oauth2 import service_account
import google.auth.transport.requests
import requests

KEY_PATH='/root/.openclaw/youtube-sa.json'
SCOPES=['https://www.googleapis.com/auth/youtube.readonly']

try:
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    token = creds.token
    print('Access token obtained (truncated):', token[:40]+'...')
    # sample search for public videos (may work if API allows)
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {'part':'snippet','q':'institutovitalslim','maxResults':3,'type':'video'}
    headers={'Authorization': 'Bearer '+token}
    r = requests.get(url, params=params, headers=headers, timeout=20)
    print('HTTP', r.status_code)
    print(r.text[:1000])
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
