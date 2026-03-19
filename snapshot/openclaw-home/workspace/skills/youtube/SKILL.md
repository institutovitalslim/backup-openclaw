# youtube skill

Simple skill scaffold to call YouTube Data API using a Service Account. Place the service-account JSON in /root/.openclaw/youtube-sa.json (already saved from 1Password as "Youtube API Acesso Service").

Usage:
- python3 test_youtube_sa.py

Note: Some YouTube Data API endpoints require OAuth delegated to a user (service accounts may not have access to user-owned channels). This skill attempts read-only search operations that work with a service account when permitted by API.
