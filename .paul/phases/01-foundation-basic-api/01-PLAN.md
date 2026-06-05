---
phase: 01-foundation-basic-api
plan: 01
type: execute
autonomous: true
---

<objective>
## Goal
Establish a minimal Flask API with API key authentication and basic endpoint routing.
</objective>

<context>
@.paul/PROJECT.md
</context>

<acceptance_criteria>
## AC-1: API Key Authentication
Given a Flask API with a required `X-API-Key` header
When a request is made with a valid API key
Then the API returns a 200 OK response
When a request is made with an invalid or missing API key
Then the API returns a 401 Unauthorized response
</acceptance_criteria>

<tasks>
<task type="auto">
  <name>Setup Flask Skeleton and Auth</name>
  <files>app.py, .env, requirements.txt</files>
  <action>
    1. Create requirements.txt with `flask`.
    2. Create .env with a dummy `API_KEY=test-secret-key`.
    3. Create app.py:
       - Initialize Flask.
       - Implement an `api_key_required` decorator that validates the `X-API-Key` header against the env var.
       - Add a `/health` endpoint to verify connectivity.
       - Add stub endpoints for `/models`, `/models/register`, `/models/query`, and `/models/refresh` (returning 200 "stub" responses).
  </action>
  <verify>
    - `curl -H "X-API-Key: test-secret-key" http://localhost:5000/health` -> 200 OK
    - `curl http://localhost:5000/health` -> 401 Unauthorized
  </verify>
  <done>AC-1 satisfied: API key authentication is functional and routing stubs are present.</done>
</task>
</tasks>

<output>
After completion, create compressed SUMMARY.md
</output>
