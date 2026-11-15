# BrandVoice — Product Backlog

Granular tasks for GitHub Projects. Generated for a 5-person academic team (4 juniors + 1 Tech Lead).

**Total tasks:** 123

| Wave | Focus | Tasks |
|------|--------|------:|
| 0 | Tech Lead foundation (repo, Docker, CI, skeletons) | 20 |
| 1 | Core vertical slices (auth, brand, ingest, RAG, text agent, library) | 45 |
| 2 | Full MVP (formats, critic, editor, media, approvals, admin) | 37 |
| 3 | Eval, deploy, polish, bonus | 21 |

## Suggested GitHub Project columns

`Backlog` → `Wave 0` → `Wave 1` → `Wave 2` → `Wave 3` → `Done` (or map labels to views).

## How to import

1. Ensure `gh auth login` is active.
2. Run: `bash scripts/create-backlog-issues.sh`
3. Create a GitHub Project: `gh project create --owner TomSebty --title "BrandVoice Kanban"` (requires your user token, not the bot).
4. Link and import: `GH_PROJECT_NUMBER=<n> bash scripts/add-issues-to-project.sh`

## Label legend

- `wave-0-foundation` … `wave-3-polish`
- `layer-db`, `layer-backend`, `layer-ai`, `layer-frontend`, `layer-qa`, `layer-devops`
- `bonus` for nice-to-have

## Wave 0

### [Wave 0] [Layer: DevOps] Initialize monorepo folder structure

**Goal:** Establish clear backend/frontend/infra paths for the team.

**Step-by-step checklist:**
- [ ] Create `backend/`, `frontend/`, `infra/`, `docs/` at repo root
- [ ] Add root `README.md` with stack overview and local dev pointers
- [ ] Add `.gitignore` for Python, Node, `.env`, `.netlify`
- [ ] Document branch naming in `docs/CONTRIBUTING.md`

**Acceptance criteria (DoD):** All folders exist; README links to each package; git status clean.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: DevOps] Add backend Python project with uv/poetry or pip-tools

**Goal:** Give juniors a one-command backend dependency install.

**Step-by-step checklist:**
- [ ] Create `backend/pyproject.toml` with FastAPI, uvicorn, sqlalchemy, sqlmodel, pydantic
- [ ] Pin Python 3.11+ in `.python-version`
- [ ] Add `backend/requirements.txt` or lockfile
- [ ] Add `make install-backend` or document `pip install -e .`

**Acceptance criteria (DoD):** `pip install` succeeds; `import fastapi` works in venv.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: DevOps] Add frontend Next.js 14+ App Router skeleton

**Goal:** Bootstrap deployable Next.js app with TypeScript.

**Step-by-step checklist:**
- [ ] Run `npx create-next-app@latest` in `frontend/` with TS, ESLint, Tailwind
- [ ] Set `src/` app directory structure
- [ ] Add `.env.example` with `NEXT_PUBLIC_API_URL`
- [ ] Verify `npm run dev` starts on port 3000

**Acceptance criteria (DoD):** Home page loads locally; no TypeScript errors.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: Frontend] Install and configure shadcn/ui + Tailwind theme

**Goal:** Shared UI kit for all screens.

**Step-by-step checklist:**
- [ ] Run `npx shadcn@latest init` in `frontend/`
- [ ] Add Button, Input, Card, Label, Toast components
- [ ] Set brand-neutral CSS variables in `globals.css`
- [ ] Create `components/ui/` re-export barrel if needed

**Acceptance criteria (DoD):** shadcn Button renders on a test page.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-frontend`

---


### [Wave 0] [Layer: DevOps] Docker Compose for Postgres 16 + pgvector

**Goal:** Local DB matching production vector search needs.

**Step-by-step checklist:**
- [ ] Create `infra/docker-compose.yml` with `pgvector/pgvector:pg16` image
- [ ] Expose port 5432; set POSTGRES_USER/PASSWORD/DB
- [ ] Add volume for data persistence
- [ ] Document `docker compose up -d` in README

**Acceptance criteria (DoD):** psql connects; `CREATE EXTENSION vector` succeeds.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: DB] Create initial Alembic migration bootstrap

**Goal:** Versioned schema changes for the team.

**Step-by-step checklist:**
- [ ] Add Alembic to backend; `alembic init` under `backend/alembic`
- [ ] Wire `DATABASE_URL` from env in `alembic.ini` / `env.py`
- [ ] Add empty initial revision
- [ ] Document `alembic upgrade head` in docs

**Acceptance criteria (DoD):** `alembic upgrade head` runs without error on empty DB.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-db`

---


### [Wave 0] [Layer: Backend] FastAPI app factory and health endpoint

**Goal:** Runnable API entrypoint for Render later.

**Step-by-step checklist:**
- [ ] Create `backend/app/main.py` with FastAPI app + CORS middleware
- [ ] Mount `GET /health` returning `{"status":"ok"}`
- [ ] Create `backend/app/core/config.py` using pydantic-settings
- [ ] Add `uvicorn app.main:app --reload` run command in README

**Acceptance criteria (DoD):** Swagger at `/docs` shows health; curl returns 200.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: Backend] SQLModel engine and session dependency

**Goal:** Reusable DB session for all routes.

**Step-by-step checklist:**
- [ ] Create `backend/app/db/session.py` with engine from `DATABASE_URL`
- [ ] Implement `get_session()` FastAPI dependency
- [ ] Add connection pool settings (pool_pre_ping)
- [ ] Test session in a dummy route

**Acceptance criteria (DoD):** Dependency injects session; no leak on request end.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: Backend] Define shared Pydantic API error schema

**Goal:** Consistent error JSON across endpoints.

**Step-by-step checklist:**
- [ ] Create `backend/app/schemas/common.py` with `ErrorDetail`, `APIError`
- [ ] Add global exception handler mapping HTTPException
- [ ] Map validation errors to 422 structured body
- [ ] Document shape in OpenAPI

**Acceptance criteria (DoD):** Invalid body returns consistent 422 JSON.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: Backend] Define Role enum and JWT payload contract

**Goal:** Single source of truth for RBAC types.

**Step-by-step checklist:**
- [ ] Create `backend/app/schemas/auth.py` with `Role` enum (owner, creator, admin)
- [ ] Define `TokenPayload` with sub, role, brand_id optional
- [ ] Define `LoginRequest` / `TokenResponse`
- [ ] Export types for route modules

**Acceptance criteria (DoD):** Types import cleanly; enum values documented.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: Frontend] API client wrapper with fetch + base URL

**Goal:** Central HTTP layer for all screens.

**Step-by-step checklist:**
- [ ] Create `frontend/src/lib/api.ts` with `apiFetch(path, options)`
- [ ] Read `NEXT_PUBLIC_API_URL`; attach JSON headers
- [ ] Parse error responses into typed errors
- [ ] Add simple retry off (document later)

**Acceptance criteria (DoD):** Mock call to `/health` succeeds from browser.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-frontend`

---


### [Wave 0] [Layer: Frontend] Auth token storage helper (memory + cookie pattern)

**Goal:** Prepare JWT attachment without exposing secrets in logs.

**Step-by-step checklist:**
- [ ] Create `frontend/src/lib/auth-storage.ts`
- [ ] Store access token in httpOnly cookie via Route Handler OR sessionStorage (document tradeoff)
- [ ] Implement `getAccessToken`, `setAccessToken`, `clearAccessToken`
- [ ] Never log token values

**Acceptance criteria (DoD):** Unit-level manual test: set/get/clear works.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-frontend`

---


### [Wave 0] [Layer: DevOps] GitHub Actions: backend lint + pytest stub

**Goal:** CI gate before merge.

**Step-by-step checklist:**
- [ ] Add `.github/workflows/backend-ci.yml`
- [ ] Steps: checkout, setup Python, install deps, ruff/black check, pytest
- [ ] Add placeholder test `test_health`
- [ ] Fail on lint errors

**Acceptance criteria (DoD):** CI green on main branch push.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: DevOps] GitHub Actions: frontend lint + build

**Goal:** Prevent broken Vercel deploys.

**Step-by-step checklist:**
- [ ] Add `.github/workflows/frontend-ci.yml`
- [ ] Steps: checkout, setup Node, npm ci, lint, `next build`
- [ ] Cache node_modules
- [ ] Use dummy API URL in build env

**Acceptance criteria (DoD):** CI build passes on PR.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: DevOps] Environment variable documentation matrix

**Goal:** Junior-safe secrets checklist.

**Step-by-step checklist:**
- [ ] Create `docs/ENV_VARS.md` listing backend/frontend vars
- [ ] Mark which are required for local vs Render/Vercel
- [ ] Note Gemini, Supabase, JWT secret placeholders
- [ ] Cross-link from README

**Acceptance criteria (DoD):** Doc reviewed; no secrets committed.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-devops`

---


### [Wave 0] [Layer: Backend] Structured logging setup

**Goal:** Debuggable API in Render logs.

**Step-by-step checklist:**
- [ ] Add `logging` config in `backend/app/core/logging.py`
- [ ] JSON or plain format with request_id middleware
- [ ] Log startup, DB errors at ERROR
- [ ] Document log levels in README

**Acceptance criteria (DoD):** Request logs include method + path.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: AI] LangGraph project skeleton module

**Goal:** Isolate agent code from HTTP layer.

**Step-by-step checklist:**
- [ ] Create `backend/app/ai/graph/` package
- [ ] Add `requirements` pin for `langgraph`, `langchain-google-genai`
- [ ] Stub `build_graph()` returning pass-through state
- [ ] Env var `GEMINI_API_KEY` in config

**Acceptance criteria (DoD):** Import graph module without API key in tests (mocked).

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-0-foundation`, `layer-ai`

---


### [Wave 0] [Layer: Backend] CORS allowlist for local Next.js origin

**Goal:** Enable browser calls during dev.

**Step-by-step checklist:**
- [ ] Read `CORS_ORIGINS` from env (comma-separated)
- [ ] Add middleware in FastAPI
- [ ] Allow credentials if using cookies
- [ ] Test preflight from localhost:3000

**Acceptance criteria (DoD):** Browser fetch from frontend no CORS error.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-backend`

---


### [Wave 0] [Layer: Frontend] Root landing page marketing stub

**Goal:** Public entry.

**Step-by-step checklist:**
- [ ] `app/page.tsx` hero BrandVoice
- [ ] CTA Login / Register
- [ ] Tailwind layout
- [ ] No auth required

**Acceptance criteria (DoD):** Landing renders.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-frontend`

---


### [Wave 0] [Layer: Backend] OpenAPI tags and route module split

**Goal:** Navigable Swagger for juniors.

**Step-by-step checklist:**
- [ ] Split routers: auth, brands, posts, admin
- [ ] Include in main
- [ ] Tag metadata
- [ ] Brief descriptions

**Acceptance criteria (DoD):** Swagger grouped by tag.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-0-foundation`, `layer-backend`

---


## Wave 1

### [Wave 1] [Layer: DB] Create User SQLModel with role enum column

**Goal:** Persist users and roles.

**Step-by-step checklist:**
- [ ] Add `backend/app/models/user.py` with id, email, hashed_password, role
- [ ] Use SQLAlchemy Enum for Role
- [ ] Unique index on email
- [ ] Register model in metadata

**Acceptance criteria (DoD):** Table created via migration.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: DB] Create Brand SQLModel linked to owner

**Goal:** One brand per owner baseline (multi-brand later).

**Step-by-step checklist:**
- [ ] Fields: id, name, owner_user_id, created_at
- [ ] FK to users
- [ ] Relationship owner -> brands
- [ ] Alembic migration

**Acceptance criteria (DoD):** Migration applies; FK enforced.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: DB] Create UserBrandMembership for creators

**Goal:** Attach creators to a brand with role.

**Step-by-step checklist:**
- [ ] Model: user_id, brand_id, role
- [ ] Unique (user_id, brand_id)
- [ ] Migration + indexes
- [ ] Seed doc example in docs

**Acceptance criteria (DoD):** Creator can belong to one brand in v1.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: Backend] Password hashing utilities with bcrypt

**Goal:** Secure credential storage.

**Step-by-step checklist:**
- [ ] Add `passlib` or `bcrypt` helper hash/verify
- [ ] Never log plaintext passwords
- [ ] Unit tests for verify roundtrip
- [ ] Use in registration service

**Acceptance criteria (DoD):** Tests pass; hash differs from password.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] POST /auth/register endpoint

**Goal:** New users can sign up.

**Step-by-step checklist:**
- [ ] Route in `routes/auth.py`
- [ ] Validate email format + password min length
- [ ] Reject duplicate email 409
- [ ] Return user DTO without password

**Acceptance criteria (DoD):** Swagger test creates user row.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] POST /auth/login endpoint returning JWT

**Goal:** Authenticated sessions.

**Step-by-step checklist:**
- [ ] Verify credentials
- [ ] Issue JWT with exp, sub, role using `python-jose`
- [ ] Return `TokenResponse`
- [ ] Configurable `JWT_SECRET` + TTL

**Acceptance criteria (DoD):** Login returns token; wrong password 401.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] JWT dependency get_current_user

**Goal:** Protect routes.

**Step-by-step checklist:**
- [ ] Decode Bearer token
- [ ] Load user from DB or fail 401
- [ ] Attach `CurrentUser` to request state
- [ ] Handle expired token

**Acceptance criteria (DoD):** Protected dummy route requires valid JWT.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] RBAC dependency require_roles

**Goal:** Enforce role gates.

**Step-by-step checklist:**
- [ ] Factory `require_roles([Role.OWNER])`
- [ ] Return 403 if role mismatch
- [ ] Use on brand routes
- [ ] Add tests for owner vs creator

**Acceptance criteria (DoD):** Creator blocked from admin-only route.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Frontend] Login page UI with shadcn form

**Goal:** User login screen.

**Step-by-step checklist:**
- [ ] Page `app/login/page.tsx`
- [ ] Email/password fields + submit
- [ ] Call POST /auth/login via api client
- [ ] Show toast on error

**Acceptance criteria (DoD):** Valid creds redirect to dashboard.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Frontend] Registration page UI

**Goal:** Signup flow.

**Step-by-step checklist:**
- [ ] Page `app/register/page.tsx`
- [ ] Fields: email, password, confirm, role selector (owner/creator) per product rules
- [ ] POST /auth/register
- [ ] Link to login

**Acceptance criteria (DoD):** New user can register and then login.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Frontend] Attach JWT to API client requests

**Goal:** Authenticated API calls.

**Step-by-step checklist:**
- [ ] Read token from storage
- [ ] Set `Authorization: Bearer` header
- [ ] On 401 redirect to login
- [ ] Clear token on logout

**Acceptance criteria (DoD):** Authenticated fetch works after login.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Frontend] Auth guard layout for dashboard routes

**Goal:** Block unauthenticated access.

**Step-by-step checklist:**
- [ ] Create `app/(dashboard)/layout.tsx`
- [ ] Check token client-side or middleware
- [ ] Redirect to /login if missing
- [ ] Optional loading state

**Acceptance criteria (DoD):** Direct URL to dashboard without token redirects.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: QA] Auth API integration tests

**Goal:** Regression safety for auth.

**Step-by-step checklist:**
- [ ] pytest + TestClient
- [ ] Tests: register, login, protected 401, wrong password
- [ ] Use test DB or transaction rollbacks
- [ ] Run in CI

**Acceptance criteria (DoD):** CI auth tests green.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-qa`

---


### [Wave 1] [Layer: DB] BrandProfile model (tone, audience, business_type)

**Goal:** Store brand voice settings.

**Step-by-step checklist:**
- [ ] Extend brand or separate `brand_profiles` table
- [ ] JSON or text fields for tone, audience, business_type
- [ ] Migration
- [ ] Relationship brand 1:1 profile

**Acceptance criteria (DoD):** CRUD possible at ORM level.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: DB] BannedWord model as child of brand

**Goal:** Enforce prohibited terms.

**Step-by-step checklist:**
- [ ] Table brand_id + word (unique per brand)
- [ ] Index on brand_id
- [ ] Migration
- [ ] Cascade delete with brand

**Acceptance criteria (DoD):** Duplicate word per brand rejected.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: Backend] GET /brands/{id}/profile

**Goal:** Read brand voice.

**Step-by-step checklist:**
- [ ] Owner/creator/admin authz on brand
- [ ] Return profile + banned words list
- [ ] 404 if no profile
- [ ] OpenAPI schema

**Acceptance criteria (DoD):** Swagger GET works for member.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] PUT /brands/{id}/profile (owner only)

**Goal:** Update brand voice.

**Step-by-step checklist:**
- [ ] Creator gets 403
- [ ] Upsert profile fields
- [ ] Replace banned words list transactionally
- [ ] Validate non-empty tone

**Acceptance criteria (DoD):** Owner update persists; creator 403.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] POST /brands create brand (owner)

**Goal:** Onboarding new brand.

**Step-by-step checklist:**
- [ ] Create brand + empty profile
- [ ] Set current user as owner
- [ ] Return brand id
- [ ] Validate name length

**Acceptance criteria (DoD):** Owner has one brand created.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Frontend] Brand profile settings page

**Goal:** UI for voice + banned words.

**Step-by-step checklist:**
- [ ] Route `app/(dashboard)/brand/settings/page.tsx`
- [ ] Form fields tone, audience, business type
- [ ] Tag input for banned words
- [ ] Save calls PUT profile

**Acceptance criteria (DoD):** Owner saves; refresh shows data.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Frontend] Read-only brand profile for creators

**Goal:** Creators see but cannot edit rules.

**Step-by-step checklist:**
- [ ] Same page hides Save when role=creator
- [ ] Show tooltip explaining restriction
- [ ] Fetch profile on load
- [ ] Handle 403 gracefully

**Acceptance criteria (DoD):** Creator sees fields disabled.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: DB] PastPost model for ingested rows

**Goal:** Store raw past posts.

**Step-by-step checklist:**
- [ ] Fields: brand_id, text, source_row, created_at
- [ ] Optional metadata JSON
- [ ] Migration
- [ ] Index brand_id

**Acceptance criteria (DoD):** Rows insert after CSV parse.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: DB] PostEmbedding model with pgvector column

**Goal:** Vector storage for RAG.

**Step-by-step checklist:**
- [ ] Enable vector extension in migration
- [ ] Column `embedding vector(768)` or per Gemini dim
- [ ] FK to past_post_id
- [ ] IVFFlat or HNSW index note in migration comment

**Acceptance criteria (DoD):** Similarity query runs in SQL.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: Backend] CSV upload endpoint multipart

**Goal:** Accept past posts file.

**Step-by-step checklist:**
- [ ] POST /brands/{id}/ingest/csv
- [ ] Parse UTF-8 CSV with pandas or csv module
- [ ] Required column `text`
- [ ] Return row count + validation errors

**Acceptance criteria (DoD):** Invalid CSV returns 400 with details.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] Excel upload support (.xlsx)

**Goal:** Second file format.

**Step-by-step checklist:**
- [ ] Detect xlsx via openpyxl
- [ ] Map first sheet rows
- [ ] Same validation as CSV
- [ ] Max file size limit

**Acceptance criteria (DoD):** Sample xlsx ingests.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Backend] Row validation service for ingest

**Goal:** Reject bad rows early.

**Step-by-step checklist:**
- [ ] Skip empty text
- [ ] Max length per post
- [ ] Collect error report array
- [ ] Transactional insert valid rows only (configurable)

**Acceptance criteria (DoD):** Mixed file returns summary counts.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: AI] Gemini Embeddings-1 batch embed job

**Goal:** Generate vectors for new rows.

**Step-by-step checklist:**
- [ ] Service `embedding_service.py` calling Google API
- [ ] Batch N texts per request
- [ ] Store vectors in PostEmbedding
- [ ] Handle rate limits with backoff

**Acceptance criteria (DoD):** After ingest, embeddings row count matches posts.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: Backend] Background task trigger for embedding generation

**Goal:** Non-blocking HTTP response.

**Step-by-step checklist:**
- [ ] FastAPI BackgroundTasks or simple async queue
- [ ] POST ingest returns job_id
- [ ] GET job status endpoint
- [ ] Log failures per row

**Acceptance criteria (DoD):** Upload returns before embed completes; status shows done.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Frontend] CSV upload UI with drag-drop

**Goal:** Brand owner uploads knowledge.

**Step-by-step checklist:**
- [ ] Page under brand settings or ingest tab
- [ ] File input + progress indicator
- [ ] Display validation report
- [ ] Poll job status

**Acceptance criteria (DoD):** Successful upload shows row count.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: AI] RAG retrieve_top_k service function

**Goal:** Fetch similar past posts.

**Step-by-step checklist:**
- [ ] Query pgvector with cosine distance
- [ ] Parameter K default 5
- [ ] Filter by brand_id
- [ ] Return text snippets for prompt

**Acceptance criteria (DoD):** Unit test with fixed vectors returns expected order.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: AI] Format few-shot context block from retrieved posts

**Goal:** Prompt-ready string.

**Step-by-step checklist:**
- [ ] Template with numbered examples
- [ ] Truncate total tokens budget
- [ ] Include in agent state
- [ ] Log retrieval ids for debug

**Acceptance criteria (DoD):** Output string under char limit.

**Estimated effort:** 1h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: Backend] GET /brands/{id}/rag/preview debug endpoint

**Goal:** Verify retrieval without full generation.

**Step-by-step checklist:**
- [ ] Query param `q`
- [ ] Return top-K posts + scores
- [ ] Owner/creator only
- [ ] Disable in production flag optional

**Acceptance criteria (DoD):** Swagger preview returns matches.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: DB] ContentPost model (draft baseline)

**Goal:** Persist generated content.

**Step-by-step checklist:**
- [ ] Fields: brand_id, author_id, format enum (text), title, body_json, status
- [ ] Status enum: draft, pending, approved, rejected
- [ ] Migration
- [ ] Timestamps

**Acceptance criteria (DoD):** Insert draft row.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-db`

---


### [Wave 1] [Layer: Backend] Pydantic schema Standard Text Post output

**Goal:** Structured generation contract.

**Step-by-step checklist:**
- [ ] `TextPostOutput` with hook, body, cta
- [ ] Validators for min/max length
- [ ] Export JSON schema
- [ ] Unit test validation failures

**Acceptance criteria (DoD):** Invalid JSON rejected by Pydantic.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: AI] LangGraph node: Researcher extracts brief angles

**Goal:** Agent 1 implementation.

**Step-by-step checklist:**
- [ ] State fields: goal, audience, angles
- [ ] Prompt template using brand profile
- [ ] Gemini call with structured output
- [ ] Parse into state

**Acceptance criteria (DoD):** Given brief, state populated.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: AI] LangGraph node: Creator generates TextPost JSON

**Goal:** Agent 2 for wave 1 scope.

**Step-by-step checklist:**
- [ ] Use Researcher output + RAG context
- [ ] Structured output to TextPostOutput
- [ ] Temperature config
- [ ] Save raw LLM response in state for debug

**Acceptance criteria (DoD):** Valid Pydantic object produced.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: AI] Wire minimal linear graph Researcher -> Creator

**Goal:** First pipeline without critic.

**Step-by-step checklist:**
- [ ] Define StateGraph
- [ ] Compile graph
- [ ] Single entry `run_text_post_pipeline(brief)`
- [ ] Integration test with mocked LLM

**Acceptance criteria (DoD):** Graph runs end-to-end mocked.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-1-core`, `layer-ai`

---


### [Wave 1] [Layer: Backend] POST /brands/{id}/generate/text

**Goal:** HTTP trigger for generation.

**Step-by-step checklist:**
- [ ] Body: user brief string
- [ ] Invoke graph; persist ContentPost as draft
- [ ] Return post id + content
- [ ] Timeout handling

**Acceptance criteria (DoD):** Swagger generates draft in DB.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Frontend] Create text post page with brief textarea

**Goal:** Primary creation UX.

**Step-by-step checklist:**
- [ ] Page `content/new/text`
- [ ] Brief input + Generate button
- [ ] Loading skeleton
- [ ] Show generated preview card

**Acceptance criteria (DoD):** Generate shows hook/body/cta.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Frontend] Content library list page (basic)

**Goal:** View drafts.

**Step-by-step checklist:**
- [ ] Table/cards: title, status, date
- [ ] GET /brands/{id}/posts
- [ ] Link to detail
- [ ] Empty state UI

**Acceptance criteria (DoD):** Lists posts after generation.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Backend] GET /brands/{id}/posts list with filters

**Goal:** API for library.

**Step-by-step checklist:**
- [ ] Query params status, date_from, date_to
- [ ] Pagination limit/offset
- [ ] Sort by updated_at desc
- [ ] Authz brand member

**Acceptance criteria (DoD):** Filters work in Swagger.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: QA] Document Wave 1 vertical slice ownership matrix

**Goal:** Clarify who ships which slice.

**Step-by-step checklist:**
- [ ] Create `docs/WAVES.md` with 4 slice names
- [ ] Map DB+API+UI per developer
- [ ] Definition of done per slice
- [ ] Review in standup

**Acceptance criteria (DoD):** Matrix approved by lead.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-qa`

---


### [Wave 1] [Layer: Frontend] Dashboard home shell with sidebar nav

**Goal:** Navigation skeleton.

**Step-by-step checklist:**
- [ ] Layout sidebar: Library, New Post, Brand, Settings
- [ ] Highlight active route
- [ ] User menu logout
- [ ] Brand name in header

**Acceptance criteria (DoD):** All links route correctly.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Backend] GET /posts/{id} detail endpoint

**Goal:** Single post fetch.

**Step-by-step checklist:**
- [ ] Include body_json, status, author
- [ ] Brand authz
- [ ] 404 handling
- [ ] Embed media attachments

**Acceptance criteria (DoD):** Detail JSON complete.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-backend`

---


### [Wave 1] [Layer: Frontend] Post detail page read-only view

**Goal:** View single draft.

**Step-by-step checklist:**
- [ ] Route `content/[id]`
- [ ] Render text post structure
- [ ] Status badge
- [ ] Back link

**Acceptance criteria (DoD):** Opens from library.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-1-core`, `layer-frontend`

---


### [Wave 1] [Layer: Backend] System Admin bootstrap CLI

**Goal:** Create first admin user.

**Step-by-step checklist:**
- [ ] `python -m app.cli create-admin email`
- [ ] Hash password prompt
- [ ] Role admin
- [ ] Doc one-time use

**Acceptance criteria (DoD):** Admin can login.

**Estimated effort:** 1h | **Difficulty:** Medium

**Labels:** `wave-1-core`, `layer-backend`

---


## Wave 2

### [Wave 2] [Layer: Backend] Pydantic CarouselPost schema

**Goal:** Carousel structured output.

**Step-by-step checklist:**
- [ ] Fields: hook, slides[], cta
- [ ] Each slide: title, body
- [ ] Max slides validator
- [ ] JSON schema export

**Acceptance criteria (DoD):** Validation tests pass.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] Pydantic ImagePost schema with image prompt

**Goal:** Image post + generation prompt fields.

**Step-by-step checklist:**
- [ ] Caption, hashtags, image_prompt object (style, lighting, angle, aspect_ratio)
- [ ] Validators for prompt completeness
- [ ] Tests
- [ ] Document in docs/SCHEMAS.md

**Acceptance criteria (DoD):** Sample JSON validates.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] Pydantic ReelsScript schema

**Goal:** Reels production script structure.

**Step-by-step checklist:**
- [ ] hook_3s, shots[], on_screen_text, voiceover, editing_cues, caption, hashtags
- [ ] Shot: angle, duration_sec, action
- [ ] Max duration sanity check
- [ ] Tests

**Acceptance criteria (DoD):** Complex sample validates.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: DB] Extend ContentPost format enum + body_json

**Goal:** Support all formats in one table.

**Step-by-step checklist:**
- [ ] Migration add format values
- [ ] Ensure body_json flexible
- [ ] Backfill default text
- [ ] Index format

**Acceptance criteria (DoD):** All formats storable.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-db`

---


### [Wave 2] [Layer: AI] Creator node branch by content format

**Goal:** Route generation by type.

**Step-by-step checklist:**
- [ ] Parameter `content_format` in state
- [ ] Select output model class
- [ ] Update prompts per format
- [ ] Tests per format mocked

**Acceptance criteria (DoD):** Three formats produce distinct shapes.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: Backend] POST generate endpoints for carousel/image/reels

**Goal:** HTTP for each format.

**Step-by-step checklist:**
- [ ] Routes `/generate/carousel` etc.
- [ ] Shared pipeline invoke
- [ ] Persist with correct format enum
- [ ] OpenAPI examples

**Acceptance criteria (DoD):** Each endpoint creates row.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Frontend] Content format picker on new post flow

**Goal:** UX to select type.

**Step-by-step checklist:**
- [ ] Tabs or radio: Text, Carousel, Image, Reels
- [ ] Route per format
- [ ] Pass format to API
- [ ] Keep shared brief component

**Acceptance criteria (DoD):** Picker switches forms.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Frontend] Carousel preview component

**Goal:** Display slides.

**Step-by-step checklist:**
- [ ] Card per slide
- [ ] Hook + CTA highlighted
- [ ] Responsive layout
- [ ] Storybook optional

**Acceptance criteria (DoD):** Renders sample JSON.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Frontend] Image post preview with prompt panel

**Goal:** Show caption + copy prompt.

**Step-by-step checklist:**
- [ ] Copy-to-clipboard for image prompt
- [ ] Display aspect ratio badge
- [ ] Caption area
- [ ] Placeholder image

**Acceptance criteria (DoD):** Copy works.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Frontend] Reels script preview with shot timeline

**Goal:** Readable shot list.

**Step-by-step checklist:**
- [ ] Vertical timeline UI
- [ ] Duration labels
- [ ] Sections: hook, VO, music cues
- [ ] Mobile-friendly

**Acceptance criteria (DoD):** Sample script renders.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: AI] Deterministic critic: banned words check

**Goal:** Regex/list scan on output text.

**Step-by-step checklist:**
- [ ] Flatten JSON text fields
- [ ] Case-insensitive banned word match
- [ ] Return violations list
- [ ] Unit tests

**Acceptance criteria (DoD):** Banned word fails check.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: AI] Deterministic critic: length and CTA rules

**Goal:** Enforce min/max lengths.

**Step-by-step checklist:**
- [ ] Per-format rules config
- [ ] CTA required for text/carousel
- [ ] Return structured feedback
- [ ] Tests edge lengths

**Acceptance criteria (DoD):** Too short fails with message.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: AI] LLM critic node with pass/fail + feedback

**Goal:** Agent 3 semantic quality gate.

**Step-by-step checklist:**
- [ ] Prompt with rubric + brand tone
- [ ] Output pass boolean + notes
- [ ] Merge with deterministic results
- [ ] Log decision

**Acceptance criteria (DoD):** Mock test fail triggers feedback.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: AI] Conditional edge Creator retry max 2

**Goal:** Loop control in LangGraph.

**Step-by-step checklist:**
- [ ] Increment retry counter in state
- [ ] Route fail -> creator if retries < 2 else end
- [ ] Attach critic feedback to creator prompt
- [ ] Graph diagram in docs

**Acceptance criteria (DoD):** Third fail exits with last draft.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: Backend] Expose critic violations in generate response

**Goal:** Frontend visibility.

**Step-by-step checklist:**
- [ ] Include `warnings` array in API response
- [ ] Optional strict mode 422 on fail
- [ ] Document behavior
- [ ] Swagger example

**Acceptance criteria (DoD):** Failed critic shows warnings.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] POST /posts/{id}/edit-ai quick actions

**Goal:** Shorter / More formal transforms.

**Step-by-step checklist:**
- [ ] Enum action + optional custom_prompt
- [ ] Load post body; call Gemini edit
- [ ] Validate still matches Pydantic schema
- [ ] Save new version or overwrite draft

**Acceptance criteria (DoD):** Shorter reduces length.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: AI] AI edit prompt templates per format

**Goal:** Consistent edits.

**Step-by-step checklist:**
- [ ] Template files in `prompts/edit/`
- [ ] Preserve JSON structure
- [ ] Temperature low
- [ ] Tests with mock

**Acceptance criteria (DoD):** Edit returns valid schema.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-ai`

---


### [Wave 2] [Layer: Frontend] Inline editor toolbar on post detail

**Goal:** Quick actions UI.

**Step-by-step checklist:**
- [ ] Buttons Shorter, More formal
- [ ] Custom prompt dialog
- [ ] Optimistic loading state
- [ ] Refresh preview

**Acceptance criteria (DoD):** Edit updates preview.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: DevOps] Supabase Storage bucket setup documentation

**Goal:** Team configures bucket.

**Step-by-step checklist:**
- [ ] Doc steps in `docs/SUPABASE.md`
- [ ] Bucket name, public vs signed URLs
- [ ] RLS policy outline
- [ ] Env vars SUPABASE_URL, KEY

**Acceptance criteria (DoD):** Lead confirms bucket exists.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-devops`

---


### [Wave 2] [Layer: DB] MediaAttachment model

**Goal:** Link files to posts.

**Step-by-step checklist:**
- [ ] Fields: post_id, storage_path, mime, kind (image|video)
- [ ] Migration
- [ ] FK cascade
- [ ] created_at

**Acceptance criteria (DoD):** Row links to post.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-db`

---


### [Wave 2] [Layer: Backend] Supabase signed upload URL endpoint

**Goal:** Secure client uploads.

**Step-by-step checklist:**
- [ ] POST /posts/{id}/media/upload-url
- [ ] Validate post belongs to user
- [ ] Return signed URL + path
- [ ] MIME allowlist

**Acceptance criteria (DoD):** curl gets upload URL.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] POST /posts/{id}/media/complete

**Goal:** Finalize attachment record.

**Step-by-step checklist:**
- [ ] Body: path, mime, kind
- [ ] Insert MediaAttachment
- [ ] Return public/signed read URL
- [ ] Max size validation message

**Acceptance criteria (DoD):** DB row after upload.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Frontend] Media upload widget on post detail

**Goal:** Attach image/video.

**Step-by-step checklist:**
- [ ] File picker + progress
- [ ] PUT to signed URL
- [ ] Call complete endpoint
- [ ] Thumbnail preview

**Acceptance criteria (DoD):** Image shows on post.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: DB] ApprovalDecision model with comments

**Goal:** Audit trail.

**Step-by-step checklist:**
- [ ] post_id, reviewer_id, decision enum, comment, created_at
- [ ] Migration
- [ ] Latest decision drives status
- [ ] Index post_id

**Acceptance criteria (DoD):** History stored.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-db`

---


### [Wave 2] [Layer: Backend] POST /posts/{id}/submit for approval

**Goal:** Creator submits draft.

**Step-by-step checklist:**
- [ ] Status draft -> pending
- [ ] 403 if not creator or already pending
- [ ] Notify owner hook stub
- [ ] Return updated post

**Acceptance criteria (DoD):** Status changes.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] POST /posts/{id}/approve and /reject (owner)

**Goal:** Owner decisions.

**Step-by-step checklist:**
- [ ] Require comment on reject
- [ ] approve -> approved
- [ ] Owner self-post auto-approve on create path
- [ ] Admin read-only override optional

**Acceptance criteria (DoD):** Owner approve works.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] Auto-approve when Brand Owner creates post

**Goal:** Business rule.

**Step-by-step checklist:**
- [ ] In generate endpoint detect role
- [ ] Set status approved immediately
- [ ] Skip pending
- [ ] Test both roles

**Acceptance criteria (DoD):** Owner post never pending.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Frontend] Submit for approval button (creator)

**Goal:** Workflow action.

**Step-by-step checklist:**
- [ ] Visible when draft + creator
- [ ] Confirmation dialog
- [ ] Toast success
- [ ] Update status badge

**Acceptance criteria (DoD):** Submits correctly.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Frontend] Owner approval queue page

**Goal:** Pending list.

**Step-by-step checklist:**
- [ ] Filter status=pending
- [ ] Approve/Reject with comment modal
- [ ] Refresh list
- [ ] Empty state

**Acceptance criteria (DoD):** Owner clears queue.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Frontend] Content library status filters + date range

**Goal:** Full library filters.

**Step-by-step checklist:**
- [ ] Filter chips for all statuses
- [ ] Date picker
- [ ] Sync to query params
- [ ] Persist in URL

**Acceptance criteria (DoD):** URL ?status=pending works.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Backend] GET /admin/users (system admin)

**Goal:** List all users.

**Step-by-step checklist:**
- [ ] require Role.ADMIN
- [ ] Pagination
- [ ] Mask sensitive fields
- [ ] Search email

**Acceptance criteria (DoD):** Non-admin 403.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Backend] POST /admin/users/{id}/block

**Goal:** Block user login.

**Step-by-step checklist:**
- [ ] Set is_blocked flag on user
- [ ] Invalidate tokens optional stub
- [ ] Audit log
- [ ] Tests

**Acceptance criteria (DoD):** Blocked user login 403.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Frontend] Admin users table page

**Goal:** Admin UI.

**Step-by-step checklist:**
- [ ] Route `/admin/users` guarded
- [ ] Block button with confirm
- [ ] Search input
- [ ] Role badges

**Acceptance criteria (DoD):** Admin sees all users.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: Backend] PATCH /posts/{id} manual save draft

**Goal:** Human edits without AI.

**Step-by-step checklist:**
- [ ] Validate schema per format
- [ ] Only draft editable
- [ ] Creator/owner rules
- [ ] updated_at bump

**Acceptance criteria (DoD):** Manual edit persists.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-backend`

---


### [Wave 2] [Layer: Frontend] Editable fields on post detail for drafts

**Goal:** Manual content tweak.

**Step-by-step checklist:**
- [ ] Controlled inputs per format
- [ ] Save button
- [ ] Disable when pending/approved
- [ ] Validation errors

**Acceptance criteria (DoD):** Save updates API.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-frontend`

---


### [Wave 2] [Layer: QA] Seed script for demo brand + users

**Goal:** Demo data for presentation.

**Step-by-step checklist:**
- [ ] Script `scripts/seed_demo.py`
- [ ] Owner, creator, sample posts
- [ ] Document credentials in `.env.example` only
- [ ] Idempotent run

**Acceptance criteria (DoD):** Seed runs twice safely.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-2-mvp`, `layer-qa`

---


### [Wave 2] [Layer: Backend] Email notification stub on submit

**Goal:** Placeholder for owner alert.

**Step-by-step checklist:**
- [ ] Log INFO on submit with owner email
- [ ] Interface NotificationService
- [ ] No-op impl default
- [ ] Swappable later

**Acceptance criteria (DoD):** Log line appears.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-2-mvp`, `layer-backend`

---


## Wave 3

### [Wave 3] [Layer: QA] Evaluation dataset file with 30 fixed prompts

**Goal:** Benchmark input fixture.

**Step-by-step checklist:**
- [ ] Create `eval/prompts.json` with 30 briefs
- [ ] Tag by format mix
- [ ] Version field
- [ ] README how to extend

**Acceptance criteria (DoD):** File committed; 30 entries.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-qa`

---


### [Wave 3] [Layer: AI] Naive baseline single-prompt generator

**Goal:** Comparison arm.

**Step-by-step checklist:**
- [ ] Function ignoring agents/RAG
- [ ] Same output schemas
- [ ] Log latency + token usage
- [ ] CLI entrypoint

**Acceptance criteria (DoD):** Runs 1 prompt mocked.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-ai`

---


### [Wave 3] [Layer: AI] Run multi-agent+RAG eval harness

**Goal:** Batch evaluation runner.

**Step-by-step checklist:**
- [ ] Loop 30 prompts through full graph
- [ ] Capture outputs to `eval/results/`
- [ ] Record pass/fail critic stats
- [ ] Configurable via env

**Acceptance criteria (DoD):** Produces JSON results file.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-3-polish`, `layer-ai`

---


### [Wave 3] [Layer: AI] Ragas or DeepEval metrics integration

**Goal:** Quantitative scores.

**Step-by-step checklist:**
- [ ] Install ragas/deepeval
- [ ] Metrics: faithfulness, relevancy per format
- [ ] Compare baseline vs pipeline
- [ ] Save scores CSV

**Acceptance criteria (DoD):** CSV has 30 rows metrics.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-3-polish`, `layer-ai`

---


### [Wave 3] [Layer: QA] Generate comparison charts script

**Goal:** Visual report for paper/demo.

**Step-by-step checklist:**
- [ ] Python matplotlib/plotly script
- [ ] Bar charts latency, pass rate, metric means
- [ ] Output PNG to `eval/charts/`
- [ ] Document in eval README

**Acceptance criteria (DoD):** PNG files generated.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-qa`

---


### [Wave 3] [Layer: DevOps] Render backend deploy blueprint

**Goal:** Production API hosting.

**Step-by-step checklist:**
- [ ] Add `render.yaml` or manual doc
- [ ] Build command, start command
- [ ] Env vars checklist
- [ ] Health check path /health

**Acceptance criteria (DoD):** Deploy succeeds on Render.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-devops`

---


### [Wave 3] [Layer: DevOps] Vercel frontend project link + env

**Goal:** Production UI.

**Step-by-step checklist:**
- [ ] Document vercel.json if needed
- [ ] Set NEXT_PUBLIC_API_URL production
- [ ] Preview env for PRs
- [ ] Smoke test login

**Acceptance criteria (DoD):** Production URL loads.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-devops`

---


### [Wave 3] [Layer: DevOps] Production Postgres + pgvector provisioning

**Goal:** Live database.

**Step-by-step checklist:**
- [ ] Document Supabase/Neon/RDS choice
- [ ] Run migrations on prod
- [ ] Rotate JWT secret
- [ ] Backup note

**Acceptance criteria (DoD):** App connects to prod DB.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-3-polish`, `layer-devops`

---


### [Wave 3] [Layer: QA] End-to-end smoke test checklist

**Goal:** Pre-demo validation.

**Step-by-step checklist:**
- [ ] Markdown checklist: register, brand, ingest, generate, approve
- [ ] Assign owners per step
- [ ] Sign-off section
- [ ] Link to eval charts

**Acceptance criteria (DoD):** Team completes once.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-qa`

---


### [Wave 3] [Layer: Frontend] Polish loading/error states app-wide

**Goal:** UX hardening.

**Step-by-step checklist:**
- [ ] Audit pages for error boundaries
- [ ] Consistent toast messages
- [ ] 404 page
- [ ] Skeleton loaders missing screens

**Acceptance criteria (DoD):** No blank screens on error.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-frontend`

---


### [Wave 3] [Layer: Frontend] Responsive layout pass for dashboard

**Goal:** Mobile-friendly demo.

**Step-by-step checklist:**
- [ ] Tailwind breakpoints on sidebar
- [ ] Collapse nav
- [ ] Test library table scroll
- [ ] Fix overflow issues

**Acceptance criteria (DoD):** 375px width usable.

**Estimated effort:** 2h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-frontend`

---


### [Wave 3] [Layer: DB] Multi-brand membership for social managers

**Goal:** User belongs to many brands.

**Step-by-step checklist:**
- [ ] Adjust queries for active_brand_id on user session
- [ ] Migration if needed
- [ ] Document limitation removal
- [ ] Indexes

**Acceptance criteria (DoD):** User switches context.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-db`, `bonus`

---


### [Wave 3] [Layer: Frontend] Brand switcher dropdown in header

**Goal:** Multi-brand UX.

**Step-by-step checklist:**
- [ ] List brands from API
- [ ] Set active brand in context
- [ ] Reload data on switch
- [ ] Persist selection localStorage

**Acceptance criteria (DoD):** Switch updates library.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-frontend`, `bonus`

---


### [Wave 3] [Layer: Backend] GET /users/me/brands list endpoint

**Goal:** Brands for switcher.

**Step-by-step checklist:**
- [ ] Return id, name, role
- [ ] Auth required
- [ ] Pagination if many
- [ ] Tests

**Acceptance criteria (DoD):** Switcher populated.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-backend`, `bonus`

---


### [Wave 3] [Layer: AI] Diff-based learning from user edits

**Goal:** Suggest banned word updates.

**Step-by-step checklist:**
- [ ] Compare pre/post edit text
- [ ] Extract added words/phrases
- [ ] Propose ban list additions endpoint
- [ ] Owner confirm before save

**Acceptance criteria (DoD):** Suggestion list appears.

**Estimated effort:** 3h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-3-polish`, `layer-ai`, `bonus`

---


### [Wave 3] [Layer: AI] LangSmith tracing optional wrapper

**Goal:** Observability.

**Step-by-step checklist:**
- [ ] Env `LANGSMITH_API_KEY`
- [ ] Wrap graph invoke with tracing
- [ ] Document dashboard link
- [ ] Disable by default

**Acceptance criteria (DoD):** Traces appear when enabled.

**Estimated effort:** 2h | **Difficulty:** Hard - Tech Lead

**Labels:** `wave-3-polish`, `layer-ai`, `bonus`

---


### [Wave 3] [Layer: Frontend] Monthly calendar view of posts

**Goal:** Planning UI.

**Step-by-step checklist:**
- [ ] Calendar component
- [ ] Posts by scheduled/approved date
- [ ] Month navigation
- [ ] Click to open post

**Acceptance criteria (DoD):** Posts show on dates.

**Estimated effort:** 3h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-frontend`, `bonus`

---


### [Wave 3] [Layer: Backend] Auto-publish webhook stub

**Goal:** Future social API.

**Step-by-step checklist:**
- [ ] POST /posts/{id}/publish stub returns 501
- [ ] Document future integration
- [ ] Feature flag
- [ ] No-op safe

**Acceptance criteria (DoD):** Returns documented message.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-backend`, `bonus`

---


### [Wave 3] [Layer: AI] Direct AI image generation endpoint stub

**Goal:** Future image API.

**Step-by-step checklist:**
- [ ] POST /posts/{id}/generate-image stub
- [ ] Validate image post format
- [ ] Return 501 or mock URL
- [ ] Feature flag

**Acceptance criteria (DoD):** Swagger documents endpoint.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-ai`, `bonus`

---


### [Wave 3] [Layer: Backend] Rate limit middleware on generate endpoints

**Goal:** Protect Gemini quota.

**Step-by-step checklist:**
- [ ] slowapi or custom per-user limit
- [ ] 429 response
- [ ] Config RATE_LIMIT
- [ ] Test exceed

**Acceptance criteria (DoD):** 6th rapid call 429.

**Estimated effort:** 2h | **Difficulty:** Medium

**Labels:** `wave-3-polish`, `layer-backend`

---


### [Wave 3] [Layer: QA] Security review checklist JWT + RBAC

**Goal:** Academic security sign-off.

**Step-by-step checklist:**
- [ ] Doc checklist in docs/SECURITY.md
- [ ] Verify HTTPS only prod
- [ ] Confirm secrets not in repo
- [ ] Role matrix table

**Acceptance criteria (DoD):** Checklist complete.

**Estimated effort:** 1h | **Difficulty:** Easy

**Labels:** `wave-3-polish`, `layer-qa`

---

