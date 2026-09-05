# ANVAY.

### AI Integration Analysis Platform

**Analyze. Map. Generate. Verify.**

Anvay is a developer tool for integrating independently built backend and AI services.

It analyzes their API contracts, detects mismatches, generates the adapter layer between them, runs the integrated system in Docker, verifies it with a real end-to-end request, and packages the result.

[Live Demo](https://anvay-sigma.vercel.app/) · [GitHub](https://github.com/Dibyasha2305/Anvay)

---

## The Problem

Two services can be logically compatible while having completely different interfaces.

For example:

**Backend**

```http
POST /predict
```

```json
{
  "input": "I love this movie"
}
```

**AI Service**

```http
POST /generate
```

```json
{
  "prompt": "I love this movie"
}
```

The services can work together, but someone still has to figure out the translation between them.

That usually means manually:

- inspecting both APIs
- identifying differences
- mapping fields
- writing adapter code
- testing the integration
- packaging the result

**Anvay automates that workflow.**

---

## How It Works

```text
        BACKEND                  AI SERVICE
           │                         │
           │                         │
           └──────────┬──────────────┘
                      │
                      ▼
              CONTRACT ANALYSIS
                      │
                      ▼
              MISMATCH DETECTION
                      │
                      ▼
                FIELD MAPPING
                      │
                      ▼
             ADAPTER GENERATION
                      │
                      ▼
               DOCKER BUILD
                      │
                      ▼
              END-TO-END TEST
                      │
                      ▼
              VERIFIED PROJECT
                      │
                      ▼
                  ZIP OUTPUT
```

---

## What Anvay Does

### 01 — Analyze

Extracts API contract information from both services.

### 02 — Detect

Identifies interface differences such as:

```text
/predict → /generate
```

### 03 — Map

Finds corresponding request and response fields:

```text
input       → prompt
prediction  → result
confidence  → score
```

### 04 — Generate

Creates an integration adapter that translates between the two service contracts.

### 05 — Verify

Builds and starts the generated Docker environment and sends a real request through the integrated system.

### 06 — Package

Produces a downloadable integrated project after successful verification.

---

# Example

### Backend Contract

```text
POST /predict

REQUEST
input: str

RESPONSE
prediction: str
confidence: float
```

### AI Contract

```text
POST /generate

REQUEST
prompt: str

RESPONSE
result: str
score: float
```

### Generated Mapping

```text
input       → prompt
prediction  → result
confidence  → score
```

### Generated Integration

```text
                 ANVAY
                  │
                  ▼
Backend ────── Adapter ────── AI Service
 /predict                     /generate
```

The backend keeps its original public contract while the generated adapter handles communication with the AI service internally.

---

# Verification

Anvay does not consider generated code successful just because it was produced.

The generated project is actually executed.

A real request is sent:

```json
{
  "input": "I love this movie"
}
```

The integrated system returns:

```json
{
  "prediction": "positive",
  "confidence": 0.95
}
```

The verification pipeline reports:

```text
DOCKER BUILD       PASS
BACKEND            PASS
AI SERVICE         PASS
E2E REQUEST        PASS
```

Only after the integration passes verification is the project packaged.

---

# Why This Matters

A code generator can produce something that looks correct without proving that it works.

Anvay is built around a different idea:

> **Generate the integration, then prove the integration.**

The workflow is therefore:

```text
ANALYZE
   ↓
GENERATE
   ↓
BUILD
   ↓
RUN
   ↓
VERIFY
   ↓
DELIVER
```

---

# Architecture

```text
┌───────────────────────────────────────────────┐
│                  React UI                     │
│                                               │
│ Upload • Progress • Results • Download        │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                FastAPI Server                 │
└───────────────────────┬───────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
    Backend         AI Service    Contract
    Analyzer         Analyzer       Matcher
          │             │             │
          └─────────────┼─────────────┘
                        ▼
               Integration Generator
                        │
                        ▼
                Project Integrator
                        │
                        ▼
                 Docker Verifier
                        │
                        ▼
                 Package Generator
```

---

# Project Structure

```text
Anvay/
│
├── src/
│   ├── analyzer/
│   │   ├── ai_analyzer.py
│   │   ├── backend_analyzer.py
│   │   ├── contract_matcher.py
│   │   ├── docker_e2e_verifier.py
│   │   ├── docker_verifier.py
│   │   ├── glue_generator.py
│   │   ├── package_project.py
│   │   ├── pipeline.py
│   │   ├── project_integrator.py
│   │   ├── report_generator.py
│   │   └── verifier.py
│   │
│   └── server/
│       └── main.py
│
├── examples/
│   └── sample_project/
│       ├── backend/
│       ├── ai_service/
│       └── frontend/
│
└── generated/
```

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Validation | Pydantic |
| Integration Engine | Python |
| API Communication | REST / HTTP |
| Containers | Docker |
| Multi-service Runtime | Docker Compose |
| Verification | End-to-End HTTP Testing |
| Packaging | ZIP |
| Frontend Deployment | Vercel |

---

# Run Locally

## Requirements

- Python 3.10+
- Node.js
- npm
- Docker Desktop

## 1. Clone

```bash
git clone https://github.com/Dibyasha2305/Anvay.git
cd Anvay
```

## 2. Start the backend

```bash
uvicorn src.server.main:app --port 9000
```

API:

```text
http://127.0.0.1:9000
```

Swagger:

```text
http://127.0.0.1:9000/docs
```

## 3. Start the frontend

Open another terminal:

```bash
cd examples/sample_project/frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# Try the Sample

Use:

```text
examples/sample_project/backend/main.py
examples/sample_project/ai_service/main.py
```

Upload both files and click:

```text
RUN ANVAY
```

The interface will show:

```text
ANALYZING
    ↓
INTEGRATING
    ↓
VERIFYING
    ↓
PACKAGING
```

A successful run produces:

```text
✓ VERIFIED
```

along with the generated mappings, mismatch report, runtime verification, and downloadable project.

---

# Generated Project

A successful integration produces a structure similar to:

```text
integrated_project/
│
├── backend/
│   ├── main.py
│   ├── integration_glue.py
│   └── Dockerfile
│
├── ai_service/
│   ├── main.py
│   └── Dockerfile
│
└── docker-compose.yml
```

The generated backend communicates with the AI service through the Docker Compose network.

---

# Current V1

The current version focuses on:

- Python services
- FastAPI APIs
- REST request/response contracts
- Contract mismatch detection
- Request/response field mapping
- Generated adapter code
- Docker-based verification
- End-to-end HTTP testing
- Downloadable integrated artifacts

The goal of V1 is to prove the core integration workflow rather than support every possible project structure.

---

# Limitations

The current version is intentionally limited.

- Primarily designed around Python/FastAPI
- Current interface focuses on Python source files
- Project-wide dependency preservation is limited
- Docker verification currently runs locally
- Contract matching is not yet fully semantic
- The public deployment currently uses an interactive demo mode

---

# Roadmap

### V2 — Full Project Integration

- ZIP uploads
- Project extraction
- Automatic entrypoint detection
- `requirements.txt` support
- Project structure preservation

### V3 — Smarter Integration

- Semantic field matching
- Better mismatch explanations
- Automatic data transformations
- Improved conflict resolution
- More frameworks and languages

### V4 — Developer Workflow

- GitHub repository integration
- Repository analysis
- Generated integration tests
- CI/CD support
- Pull-request based integration

### V5 — Anvay Runner

A local runner that connects the hosted Anvay interface to a developer's local Docker environment.

```text
              ANVAY WEB
                  │
                  ▼
             ANVAY RUNNER
                  │
                  ▼
                DOCKER
             ┌────┴────┐
             ▼         ▼
          BACKEND   AI SERVICE
```

This would allow developers to use a hosted Anvay interface while keeping code execution inside their own environment.

---

# Public Demo

**https://anvay-sigma.vercel.app/**

The public frontend currently provides an interactive demonstration of the Anvay workflow.

The real Docker-backed integration engine is available when running Anvay locally.

---

# Development Philosophy

Anvay started from a simple question:

> **Can service integration be treated as an engineering problem that can be analyzed, generated, and verified automatically?**

The project is built around the idea that integration is more than generating code.

The final system should be able to:

```text
UNDERSTAND
    ↓
CONNECT
    ↓
TEST
    ↓
PROVE
```

---

# Demo

A short demo GIF can be placed here:

```md
![Anvay Demo](docs/anvay-demo.gif)
```

Recommended sequence:

```text
RUN ANVAY
    ↓
ANALYZING
    ↓
INTEGRATING
    ↓
VERIFYING
    ↓
VERIFIED
    ↓
DOWNLOAD ZIP
```

---

# Author

**Dibyasha**

GitHub:  
https://github.com/Dibyasha2305/Anvay

Live Demo:  
https://anvay-sigma.vercel.app/

---

## License

This project is currently a personal engineering project and experimental MVP.
