# autocoding-ml

## What This Is

A Python Flask API that provides queryable models for Hungarian statistical classification systems (FEOR, ISCO, TEAOR, COICOP, KEOR). The API allows users to create and refresh separate models for each classification type, query classifications by providing descriptive text, and runs in a containerized environment.

## Core Value

Users can automatically classify text into Hungarian statistical codes (FEOR, ISCO, TEAOR, COICOP, KEOR) with 90%+ accuracy through a simple REST API.

## Current State

| Attribute | Value |
|-----------|-------|
| Type | Application |
| Version | 0.0.0 |
| Status | Initializing |
| Last Updated | 2026-06-05 |

## Requirements

### Core Features

- Upload/register a new classification model (FEOR, ISCO, TEAOR, etc.)
- Query classification by sending descriptive text
- Refresh/retrain an existing model
- List available classification types

### Validated (Shipped)

- [x] Basic API Skeleton with API Key Auth — Phase 1

### Active (In Progress)
None yet.

### Planned (Next)
To be defined during `/paul:plan`

### Out of Scope
To be defined during planning.

## Target Users

**Primary:** Developers and data analysts working with Hungarian statistical classification systems
- Need automated classification of text data
- Require REST API integration for classification tasks
- Work with multiple Hungarian statistical code systems

## Context

**Business Context:**
Machine learning API for Hungarian statistical classification codes - enables automated categorization of text into standardized statistical taxonomies.

**Technical Context:**
Python-based REST API with ML classification capabilities, designed for containerized deployment from development through production.

## Constraints

### Technical Constraints

- Must support multiple classification models (FEOR, ISCO, TEAOR, COICOP, KEOR)
- Flask framework for REST API
- Docker containerization required
- Kubernetes deployment for production
- API key authentication

### Business Constraints

- Classification accuracy must exceed 90%
- Must support model refresh without complete redeployment

## Key Decisions

| Decision | Rationale | Date | Status |
|----------|-----------|------|--------|
| Flask for REST API | User preference - lightweight Python web framework | 2026-06-05 | Active |
| Docker + Kubernetes | Local dev in Docker, production K8s deployment | 2026-06-05 | Active |
| API key authentication | Simple auth mechanism appropriate for API service | 2026-06-05 | Active |
| Use python-dotenv | Simple and standard way to handle environment variables | 2026-06-05 | Active |
| Auth via Decorator | Clean and reusable way to protect endpoints | 2026-06-05 | Active |

## Success Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Classification accuracy | >90% | - | Not started |
| API availability | - | - | Not started |
| Model refresh capability | Working | - | Not started |

## Tech Stack / Tools

| Layer | Technology | Notes |
|-------|------------|-------|
| API Framework | Flask | REST API server |
| ML/Classification | TBD | scikit-learn, transformers, or spaCy candidates |
| Containerization | Docker | Development environment |
| Orchestration | Kubernetes | Production deployment |
| Authentication | API Keys | Simple token-based auth |

---
*Created: 2026-06-05*
