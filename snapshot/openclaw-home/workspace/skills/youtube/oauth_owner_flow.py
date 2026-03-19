#!/usr/bin/env python3
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS = '/root/.openclaw/client_secret_gog_desktop.json'
SCOPES = ['https://www.googleapis.com/auth/youtube','https://www.googleapis.com/auth/youtube.readonly','https://www.googleapis.com/auth/userinfo.email']

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
print(auth_url)
print('\nAfter visiting the URL and consenting, you will be redirected to a URL. Paste that full redirect URL here; I will exchange the code and save the credentials.')
