#!/usr/bin/env python3
"""Generate BrandVoice backlog markdown and gh issue import script."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

# Each task: wave, layer, title_suffix, goal, checklist, dod, effort, difficulty, labels (optional)
Task = dict

WAVE_LABELS = {
    0: "wave-0-foundation",
    1: "wave-1-core",
    2: "wave-2-mvp",
    3: "wave-3-polish",
}

LAYER_LABELS = {
    "DB": "layer-db",
    "Backend": "layer-backend",
    "AI": "layer-ai",
    "Frontend": "layer-frontend",
    "QA": "layer-qa",
    "DevOps": "layer-devops",
}


def t(
    wave: int,
    layer: str,
    title: str,
    goal: str,
    checklist: list[str],
    dod: str,
    effort: str,
    difficulty: str,
    extra_labels: list[str] | None = None,
) -> Task:
    return {
        "wave": wave,
        "layer": layer,
        "title": f"[Wave {wave}] [Layer: {layer}] {title}",
        "goal": goal,
        "checklist": checklist,
        "dod": dod,
        "effort": effort,
        "difficulty": difficulty,
        "labels": [WAVE_LABELS[wave], LAYER_LABELS.get(layer, "layer-other")]
        + (extra_labels or []),
    }


TASKS: list[Task] = []

# --- WAVE 0 ---
TASKS += [
    t(0, "DevOps", "Initialize monorepo folder structure", "Establish clear backend/frontend/infra paths for the team.", ["Create `backend/`, `frontend/`, `infra/`, `docs/` at repo root", "Add root `README.md` with stack overview and local dev pointers", "Add `.gitignore` for Python, Node, `.env`, `.netlify`", "Document branch naming in `docs/CONTRIBUTING.md`"], "All folders exist; README links to each package; git status clean.", "1h", "Easy"),
    t(0, "DevOps", "Add backend Python project with uv/poetry or pip-tools", "Give juniors a one-command backend dependency install.", ["Create `backend/pyproject.toml` with FastAPI, uvicorn, sqlalchemy, sqlmodel, pydantic", "Pin Python 3.11+ in `.python-version`", "Add `backend/requirements.txt` or lockfile", "Add `make install-backend` or document `pip install -e .`"], "`pip install` succeeds; `import fastapi` works in venv.", "2h", "Easy"),
    t(0, "DevOps", "Add frontend Next.js 14+ App Router skeleton", "Bootstrap deployable Next.js app with TypeScript.", ["Run `npx create-next-app@latest` in `frontend/` with TS, ESLint, Tailwind", "Set `src/` app directory structure", "Add `.env.example` with `NEXT_PUBLIC_API_URL`", "Verify `npm run dev` starts on port 3000"], "Home page loads locally; no TypeScript errors.", "2h", "Easy"),
    t(0, "Frontend", "Install and configure shadcn/ui + Tailwind theme", "Shared UI kit for all screens.", ["Run `npx shadcn@latest init` in `frontend/`", "Add Button, Input, Card, Label, Toast components", "Set brand-neutral CSS variables in `globals.css`", "Create `components/ui/` re-export barrel if needed"], "shadcn Button renders on a test page.", "2h", "Easy"),
    t(0, "DevOps", "Docker Compose for Postgres 16 + pgvector", "Local DB matching production vector search needs.", ["Create `infra/docker-compose.yml` with `pgvector/pgvector:pg16` image", "Expose port 5432; set POSTGRES_USER/PASSWORD/DB", "Add volume for data persistence", "Document `docker compose up -d` in README"], "psql connects; `CREATE EXTENSION vector` succeeds.", "2h", "Medium"),
    t(0, "DB", "Create initial Alembic migration bootstrap", "Versioned schema changes for the team.", ["Add Alembic to backend; `alembic init` under `backend/alembic`", "Wire `DATABASE_URL` from env in `alembic.ini` / `env.py`", "Add empty initial revision", "Document `alembic upgrade head` in docs"], "`alembic upgrade head` runs without error on empty DB.", "2h", "Medium"),
    t(0, "Backend", "FastAPI app factory and health endpoint", "Runnable API entrypoint for Render later.", ["Create `backend/app/main.py` with FastAPI app + CORS middleware", "Mount `GET /health` returning `{\"status\":\"ok\"}`", "Create `backend/app/core/config.py` using pydantic-settings", "Add `uvicorn app.main:app --reload` run command in README"], "Swagger at `/docs` shows health; curl returns 200.", "2h", "Easy"),
    t(0, "Backend", "SQLModel engine and session dependency", "Reusable DB session for all routes.", ["Create `backend/app/db/session.py` with engine from `DATABASE_URL`", "Implement `get_session()` FastAPI dependency", "Add connection pool settings (pool_pre_ping)", "Test session in a dummy route"], "Dependency injects session; no leak on request end.", "2h", "Medium"),
    t(0, "Backend", "Define shared Pydantic API error schema", "Consistent error JSON across endpoints.", ["Create `backend/app/schemas/common.py` with `ErrorDetail`, `APIError`", "Add global exception handler mapping HTTPException", "Map validation errors to 422 structured body", "Document shape in OpenAPI"], "Invalid body returns consistent 422 JSON.", "1h", "Easy"),
    t(0, "Backend", "Define Role enum and JWT payload contract", "Single source of truth for RBAC types.", ["Create `backend/app/schemas/auth.py` with `Role` enum (owner, creator, admin)", "Define `TokenPayload` with sub, role, brand_id optional", "Define `LoginRequest` / `TokenResponse`", "Export types for route modules"], "Types import cleanly; enum values documented.", "1h", "Easy"),
    t(0, "Frontend", "API client wrapper with fetch + base URL", "Central HTTP layer for all screens.", ["Create `frontend/src/lib/api.ts` with `apiFetch(path, options)`", "Read `NEXT_PUBLIC_API_URL`; attach JSON headers", "Parse error responses into typed errors", "Add simple retry off (document later)"], "Mock call to `/health` succeeds from browser.", "2h", "Easy"),
    t(0, "Frontend", "Auth token storage helper (memory + cookie pattern)", "Prepare JWT attachment without exposing secrets in logs.", ["Create `frontend/src/lib/auth-storage.ts`", "Store access token in httpOnly cookie via Route Handler OR sessionStorage (document tradeoff)", "Implement `getAccessToken`, `setAccessToken`, `clearAccessToken`", "Never log token values"], "Unit-level manual test: set/get/clear works.", "2h", "Medium"),
    t(0, "DevOps", "GitHub Actions: backend lint + pytest stub", "CI gate before merge.", ["Add `.github/workflows/backend-ci.yml`", "Steps: checkout, setup Python, install deps, ruff/black check, pytest", "Add placeholder test `test_health`", "Fail on lint errors"], "CI green on main branch push.", "2h", "Medium"),
    t(0, "DevOps", "GitHub Actions: frontend lint + build", "Prevent broken Vercel deploys.", ["Add `.github/workflows/frontend-ci.yml`", "Steps: checkout, setup Node, npm ci, lint, `next build`", "Cache node_modules", "Use dummy API URL in build env"], "CI build passes on PR.", "2h", "Medium"),
    t(0, "DevOps", "Environment variable documentation matrix", "Junior-safe secrets checklist.", ["Create `docs/ENV_VARS.md` listing backend/frontend vars", "Mark which are required for local vs Render/Vercel", "Note Gemini, Supabase, JWT secret placeholders", "Cross-link from README"], "Doc reviewed; no secrets committed.", "1h", "Easy"),
    t(0, "Backend", "Structured logging setup", "Debuggable API in Render logs.", ["Add `logging` config in `backend/app/core/logging.py`", "JSON or plain format with request_id middleware", "Log startup, DB errors at ERROR", "Document log levels in README"], "Request logs include method + path.", "2h", "Hard - Tech Lead"),
]

TASKS += [
    t(0, "AI", "LangGraph project skeleton module", "Isolate agent code from HTTP layer.", ["Create `backend/app/ai/graph/` package", "Add `requirements` pin for `langgraph`, `langchain-google-genai`", "Stub `build_graph()` returning pass-through state", "Env var `GEMINI_API_KEY` in config"], "Import graph module without API key in tests (mocked).", "2h", "Hard - Tech Lead"),
    t(0, "Backend", "CORS allowlist for local Next.js origin", "Enable browser calls during dev.", ["Read `CORS_ORIGINS` from env (comma-separated)", "Add middleware in FastAPI", "Allow credentials if using cookies", "Test preflight from localhost:3000"], "Browser fetch from frontend no CORS error.", "1h", "Easy"),
]

# --- WAVE 1: AUTH ---
TASKS += [
    t(1, "DB", "Create User SQLModel with role enum column", "Persist users and roles.", ["Add `backend/app/models/user.py` with id, email, hashed_password, role", "Use SQLAlchemy Enum for Role", "Unique index on email", "Register model in metadata"], "Table created via migration.", "2h", "Easy"),
    t(1, "DB", "Create Brand SQLModel linked to owner", "One brand per owner baseline (multi-brand later).", ["Fields: id, name, owner_user_id, created_at", "FK to users", "Relationship owner -> brands", "Alembic migration"], "Migration applies; FK enforced.", "2h", "Easy"),
    t(1, "DB", "Create UserBrandMembership for creators", "Attach creators to a brand with role.", ["Model: user_id, brand_id, role", "Unique (user_id, brand_id)", "Migration + indexes", "Seed doc example in docs"], "Creator can belong to one brand in v1.", "2h", "Medium"),
    t(1, "Backend", "Password hashing utilities with bcrypt", "Secure credential storage.", ["Add `passlib` or `bcrypt` helper hash/verify", "Never log plaintext passwords", "Unit tests for verify roundtrip", "Use in registration service"], "Tests pass; hash differs from password.", "1h", "Easy"),
    t(1, "Backend", "POST /auth/register endpoint", "New users can sign up.", ["Route in `routes/auth.py`", "Validate email format + password min length", "Reject duplicate email 409", "Return user DTO without password"], "Swagger test creates user row.", "2h", "Easy"),
    t(1, "Backend", "POST /auth/login endpoint returning JWT", "Authenticated sessions.", ["Verify credentials", "Issue JWT with exp, sub, role using `python-jose`", "Return `TokenResponse`", "Configurable `JWT_SECRET` + TTL"], "Login returns token; wrong password 401.", "2h", "Medium"),
    t(1, "Backend", "JWT dependency get_current_user", "Protect routes.", ["Decode Bearer token", "Load user from DB or fail 401", "Attach `CurrentUser` to request state", "Handle expired token"], "Protected dummy route requires valid JWT.", "2h", "Medium"),
    t(1, "Backend", "RBAC dependency require_roles", "Enforce role gates.", ["Factory `require_roles([Role.OWNER])`", "Return 403 if role mismatch", "Use on brand routes", "Add tests for owner vs creator"], "Creator blocked from admin-only route.", "2h", "Medium"),
    t(1, "Frontend", "Login page UI with shadcn form", "User login screen.", ["Page `app/login/page.tsx`", "Email/password fields + submit", "Call POST /auth/login via api client", "Show toast on error"], "Valid creds redirect to dashboard.", "2h", "Easy"),
    t(1, "Frontend", "Registration page UI", "Signup flow.", ["Page `app/register/page.tsx`", "Fields: email, password, confirm, role selector (owner/creator) per product rules", "POST /auth/register", "Link to login"], "New user can register and then login.", "2h", "Easy"),
    t(1, "Frontend", "Attach JWT to API client requests", "Authenticated API calls.", ["Read token from storage", "Set `Authorization: Bearer` header", "On 401 redirect to login", "Clear token on logout"], "Authenticated fetch works after login.", "2h", "Easy"),
    t(1, "Frontend", "Auth guard layout for dashboard routes", "Block unauthenticated access.", ["Create `app/(dashboard)/layout.tsx`", "Check token client-side or middleware", "Redirect to /login if missing", "Optional loading state"], "Direct URL to dashboard without token redirects.", "2h", "Medium"),
    t(1, "QA", "Auth API integration tests", "Regression safety for auth.", ["pytest + TestClient", "Tests: register, login, protected 401, wrong password", "Use test DB or transaction rollbacks", "Run in CI"], "CI auth tests green.", "2h", "Medium"),
]

# WAVE 1: BRAND PROFILE
TASKS += [
    t(1, "DB", "BrandProfile model (tone, audience, business_type)", "Store brand voice settings.", ["Extend brand or separate `brand_profiles` table", "JSON or text fields for tone, audience, business_type", "Migration", "Relationship brand 1:1 profile"], "CRUD possible at ORM level.", "2h", "Easy"),
    t(1, "DB", "BannedWord model as child of brand", "Enforce prohibited terms.", ["Table brand_id + word (unique per brand)", "Index on brand_id", "Migration", "Cascade delete with brand"], "Duplicate word per brand rejected.", "1h", "Easy"),
    t(1, "Backend", "GET /brands/{id}/profile", "Read brand voice.", ["Owner/creator/admin authz on brand", "Return profile + banned words list", "404 if no profile", "OpenAPI schema"], "Swagger GET works for member.", "2h", "Easy"),
    t(1, "Backend", "PUT /brands/{id}/profile (owner only)", "Update brand voice.", ["Creator gets 403", "Upsert profile fields", "Replace banned words list transactionally", "Validate non-empty tone"], "Owner update persists; creator 403.", "2h", "Medium"),
    t(1, "Backend", "POST /brands create brand (owner)", "Onboarding new brand.", ["Create brand + empty profile", "Set current user as owner", "Return brand id", "Validate name length"], "Owner has one brand created.", "2h", "Easy"),
    t(1, "Frontend", "Brand profile settings page", "UI for voice + banned words.", ["Route `app/(dashboard)/brand/settings/page.tsx`", "Form fields tone, audience, business type", "Tag input for banned words", "Save calls PUT profile"], "Owner saves; refresh shows data.", "3h", "Medium"),
    t(1, "Frontend", "Read-only brand profile for creators", "Creators see but cannot edit rules.", ["Same page hides Save when role=creator", "Show tooltip explaining restriction", "Fetch profile on load", "Handle 403 gracefully"], "Creator sees fields disabled.", "1h", "Easy"),
]

# WAVE 1: CSV + EMBEDDINGS
TASKS += [
    t(1, "DB", "PastPost model for ingested rows", "Store raw past posts.", ["Fields: brand_id, text, source_row, created_at", "Optional metadata JSON", "Migration", "Index brand_id"], "Rows insert after CSV parse.", "2h", "Easy"),
    t(1, "DB", "PostEmbedding model with pgvector column", "Vector storage for RAG.", ["Enable vector extension in migration", "Column `embedding vector(768)` or per Gemini dim", "FK to past_post_id", "IVFFlat or HNSW index note in migration comment"], "Similarity query runs in SQL.", "2h", "Hard - Tech Lead"),
    t(1, "Backend", "CSV upload endpoint multipart", "Accept past posts file.", ["POST /brands/{id}/ingest/csv", "Parse UTF-8 CSV with pandas or csv module", "Required column `text`", "Return row count + validation errors"], "Invalid CSV returns 400 with details.", "2h", "Medium"),
    t(1, "Backend", "Excel upload support (.xlsx)", "Second file format.", ["Detect xlsx via openpyxl", "Map first sheet rows", "Same validation as CSV", "Max file size limit"], "Sample xlsx ingests.", "2h", "Medium"),
    t(1, "Backend", "Row validation service for ingest", "Reject bad rows early.", ["Skip empty text", "Max length per post", "Collect error report array", "Transactional insert valid rows only (configurable)"], "Mixed file returns summary counts.", "2h", "Medium"),
    t(1, "AI", "Gemini Embeddings-1 batch embed job", "Generate vectors for new rows.", ["Service `embedding_service.py` calling Google API", "Batch N texts per request", "Store vectors in PostEmbedding", "Handle rate limits with backoff"], "After ingest, embeddings row count matches posts.", "3h", "Hard - Tech Lead"),
    t(1, "Backend", "Background task trigger for embedding generation", "Non-blocking HTTP response.", ["FastAPI BackgroundTasks or simple async queue", "POST ingest returns job_id", "GET job status endpoint", "Log failures per row"], "Upload returns before embed completes; status shows done.", "2h", "Medium"),
    t(1, "Frontend", "CSV upload UI with drag-drop", "Brand owner uploads knowledge.", ["Page under brand settings or ingest tab", "File input + progress indicator", "Display validation report", "Poll job status"], "Successful upload shows row count.", "2h", "Easy"),
]

# WAVE 1: RAG
TASKS += [
    t(1, "AI", "RAG retrieve_top_k service function", "Fetch similar past posts.", ["Query pgvector with cosine distance", "Parameter K default 5", "Filter by brand_id", "Return text snippets for prompt"], "Unit test with fixed vectors returns expected order.", "3h", "Hard - Tech Lead"),
    t(1, "AI", "Format few-shot context block from retrieved posts", "Prompt-ready string.", ["Template with numbered examples", "Truncate total tokens budget", "Include in agent state", "Log retrieval ids for debug"], "Output string under char limit.", "1h", "Medium"),
    t(1, "Backend", "GET /brands/{id}/rag/preview debug endpoint", "Verify retrieval without full generation.", ["Query param `q`", "Return top-K posts + scores", "Owner/creator only", "Disable in production flag optional"], "Swagger preview returns matches.", "2h", "Easy"),
]

# WAVE 1: BASIC AGENT + CONTENT
TASKS += [
    t(1, "DB", "ContentPost model (draft baseline)", "Persist generated content.", ["Fields: brand_id, author_id, format enum (text), title, body_json, status", "Status enum: draft, pending, approved, rejected", "Migration", "Timestamps"], "Insert draft row.", "2h", "Easy"),
    t(1, "Backend", "Pydantic schema Standard Text Post output", "Structured generation contract.", ["`TextPostOutput` with hook, body, cta", "Validators for min/max length", "Export JSON schema", "Unit test validation failures"], "Invalid JSON rejected by Pydantic.", "2h", "Medium"),
    t(1, "AI", "LangGraph node: Researcher extracts brief angles", "Agent 1 implementation.", ["State fields: goal, audience, angles", "Prompt template using brand profile", "Gemini call with structured output", "Parse into state"], "Given brief, state populated.", "3h", "Hard - Tech Lead"),
    t(1, "AI", "LangGraph node: Creator generates TextPost JSON", "Agent 2 for wave 1 scope.", ["Use Researcher output + RAG context", "Structured output to TextPostOutput", "Temperature config", "Save raw LLM response in state for debug"], "Valid Pydantic object produced.", "3h", "Hard - Tech Lead"),
    t(1, "AI", "Wire minimal linear graph Researcher -> Creator", "First pipeline without critic.", ["Define StateGraph", "Compile graph", "Single entry `run_text_post_pipeline(brief)`", "Integration test with mocked LLM"], "Graph runs end-to-end mocked.", "2h", "Hard - Tech Lead"),
    t(1, "Backend", "POST /brands/{id}/generate/text", "HTTP trigger for generation.", ["Body: user brief string", "Invoke graph; persist ContentPost as draft", "Return post id + content", "Timeout handling"], "Swagger generates draft in DB.", "2h", "Medium"),
    t(1, "Frontend", "Create text post page with brief textarea", "Primary creation UX.", ["Page `content/new/text`", "Brief input + Generate button", "Loading skeleton", "Show generated preview card"], "Generate shows hook/body/cta.", "3h", "Medium"),
    t(1, "Frontend", "Content library list page (basic)", "View drafts.", ["Table/cards: title, status, date", "GET /brands/{id}/posts", "Link to detail", "Empty state UI"], "Lists posts after generation.", "2h", "Easy"),
    t(1, "Backend", "GET /brands/{id}/posts list with filters", "API for library.", ["Query params status, date_from, date_to", "Pagination limit/offset", "Sort by updated_at desc", "Authz brand member"], "Filters work in Swagger.", "2h", "Medium"),
]

# --- WAVE 2 ---
# Multi-format schemas
TASKS += [
    t(2, "Backend", "Pydantic CarouselPost schema", "Carousel structured output.", ["Fields: hook, slides[], cta", "Each slide: title, body", "Max slides validator", "JSON schema export"], "Validation tests pass.", "2h", "Medium"),
    t(2, "Backend", "Pydantic ImagePost schema with image prompt", "Image post + generation prompt fields.", ["Caption, hashtags, image_prompt object (style, lighting, angle, aspect_ratio)", "Validators for prompt completeness", "Tests", "Document in docs/SCHEMAS.md"], "Sample JSON validates.", "2h", "Medium"),
    t(2, "Backend", "Pydantic ReelsScript schema", "Reels production script structure.", ["hook_3s, shots[], on_screen_text, voiceover, editing_cues, caption, hashtags", "Shot: angle, duration_sec, action", "Max duration sanity check", "Tests"], "Complex sample validates.", "3h", "Medium"),
    t(2, "DB", "Extend ContentPost format enum + body_json", "Support all formats in one table.", ["Migration add format values", "Ensure body_json flexible", "Backfill default text", "Index format"], "All formats storable.", "1h", "Easy"),
    t(2, "AI", "Creator node branch by content format", "Route generation by type.", ["Parameter `content_format` in state", "Select output model class", "Update prompts per format", "Tests per format mocked"], "Three formats produce distinct shapes.", "3h", "Hard - Tech Lead"),
    t(2, "Backend", "POST generate endpoints for carousel/image/reels", "HTTP for each format.", ["Routes `/generate/carousel` etc.", "Shared pipeline invoke", "Persist with correct format enum", "OpenAPI examples"], "Each endpoint creates row.", "2h", "Medium"),
    t(2, "Frontend", "Content format picker on new post flow", "UX to select type.", ["Tabs or radio: Text, Carousel, Image, Reels", "Route per format", "Pass format to API", "Keep shared brief component"], "Picker switches forms.", "2h", "Easy"),
    t(2, "Frontend", "Carousel preview component", "Display slides.", ["Card per slide", "Hook + CTA highlighted", "Responsive layout", "Storybook optional"], "Renders sample JSON.", "2h", "Easy"),
    t(2, "Frontend", "Image post preview with prompt panel", "Show caption + copy prompt.", ["Copy-to-clipboard for image prompt", "Display aspect ratio badge", "Caption area", "Placeholder image"], "Copy works.", "2h", "Easy"),
    t(2, "Frontend", "Reels script preview with shot timeline", "Readable shot list.", ["Vertical timeline UI", "Duration labels", "Sections: hook, VO, music cues", "Mobile-friendly"], "Sample script renders.", "3h", "Medium"),
]

# Critic loop
TASKS += [
    t(2, "AI", "Deterministic critic: banned words check", "Regex/list scan on output text.", ["Flatten JSON text fields", "Case-insensitive banned word match", "Return violations list", "Unit tests"], "Banned word fails check.", "2h", "Medium"),
    t(2, "AI", "Deterministic critic: length and CTA rules", "Enforce min/max lengths.", ["Per-format rules config", "CTA required for text/carousel", "Return structured feedback", "Tests edge lengths"], "Too short fails with message.", "2h", "Medium"),
    t(2, "AI", "LLM critic node with pass/fail + feedback", "Agent 3 semantic quality gate.", ["Prompt with rubric + brand tone", "Output pass boolean + notes", "Merge with deterministic results", "Log decision"], "Mock test fail triggers feedback.", "3h", "Hard - Tech Lead"),
    t(2, "AI", "Conditional edge Creator retry max 2", "Loop control in LangGraph.", ["Increment retry counter in state", "Route fail -> creator if retries < 2 else end", "Attach critic feedback to creator prompt", "Graph diagram in docs"], "Third fail exits with last draft.", "2h", "Hard - Tech Lead"),
    t(2, "Backend", "Expose critic violations in generate response", "Frontend visibility.", ["Include `warnings` array in API response", "Optional strict mode 422 on fail", "Document behavior", "Swagger example"], "Failed critic shows warnings.", "1h", "Easy"),
]

# Inline editor
TASKS += [
    t(2, "Backend", "POST /posts/{id}/edit-ai quick actions", "Shorter / More formal transforms.", ["Enum action + optional custom_prompt", "Load post body; call Gemini edit", "Validate still matches Pydantic schema", "Save new version or overwrite draft"], "Shorter reduces length.", "2h", "Medium"),
    t(2, "AI", "AI edit prompt templates per format", "Consistent edits.", ["Template files in `prompts/edit/`", "Preserve JSON structure", "Temperature low", "Tests with mock"], "Edit returns valid schema.", "2h", "Medium"),
    t(2, "Frontend", "Inline editor toolbar on post detail", "Quick actions UI.", ["Buttons Shorter, More formal", "Custom prompt dialog", "Optimistic loading state", "Refresh preview"], "Edit updates preview.", "2h", "Easy"),
]

# Supabase media
TASKS += [
    t(2, "DevOps", "Supabase Storage bucket setup documentation", "Team configures bucket.", ["Doc steps in `docs/SUPABASE.md`", "Bucket name, public vs signed URLs", "RLS policy outline", "Env vars SUPABASE_URL, KEY"], "Lead confirms bucket exists.", "1h", "Easy"),
    t(2, "DB", "MediaAttachment model", "Link files to posts.", ["Fields: post_id, storage_path, mime, kind (image|video)", "Migration", "FK cascade", "created_at"], "Row links to post.", "1h", "Easy"),
    t(2, "Backend", "Supabase signed upload URL endpoint", "Secure client uploads.", ["POST /posts/{id}/media/upload-url", "Validate post belongs to user", "Return signed URL + path", "MIME allowlist"], "curl gets upload URL.", "2h", "Medium"),
    t(2, "Backend", "POST /posts/{id}/media/complete", "Finalize attachment record.", ["Body: path, mime, kind", "Insert MediaAttachment", "Return public/signed read URL", "Max size validation message"], "DB row after upload.", "2h", "Medium"),
    t(2, "Frontend", "Media upload widget on post detail", "Attach image/video.", ["File picker + progress", "PUT to signed URL", "Call complete endpoint", "Thumbnail preview"], "Image shows on post.", "3h", "Medium"),
]

# Approval workflow
TASKS += [
    t(2, "DB", "ApprovalDecision model with comments", "Audit trail.", ["post_id, reviewer_id, decision enum, comment, created_at", "Migration", "Latest decision drives status", "Index post_id"], "History stored.", "2h", "Easy"),
    t(2, "Backend", "POST /posts/{id}/submit for approval", "Creator submits draft.", ["Status draft -> pending", "403 if not creator or already pending", "Notify owner hook stub", "Return updated post"], "Status changes.", "2h", "Easy"),
    t(2, "Backend", "POST /posts/{id}/approve and /reject (owner)", "Owner decisions.", ["Require comment on reject", "approve -> approved", "Owner self-post auto-approve on create path", "Admin read-only override optional"], "Owner approve works.", "2h", "Medium"),
    t(2, "Backend", "Auto-approve when Brand Owner creates post", "Business rule.", ["In generate endpoint detect role", "Set status approved immediately", "Skip pending", "Test both roles"], "Owner post never pending.", "1h", "Easy"),
    t(2, "Frontend", "Submit for approval button (creator)", "Workflow action.", ["Visible when draft + creator", "Confirmation dialog", "Toast success", "Update status badge"], "Submits correctly.", "1h", "Easy"),
    t(2, "Frontend", "Owner approval queue page", "Pending list.", ["Filter status=pending", "Approve/Reject with comment modal", "Refresh list", "Empty state"], "Owner clears queue.", "3h", "Medium"),
    t(2, "Frontend", "Content library status filters + date range", "Full library filters.", ["Filter chips for all statuses", "Date picker", "Sync to query params", "Persist in URL"], "URL ?status=pending works.", "2h", "Medium"),
]

# Admin RBAC
TASKS += [
    t(2, "Backend", "GET /admin/users (system admin)", "List all users.", ["require Role.ADMIN", "Pagination", "Mask sensitive fields", "Search email"], "Non-admin 403.", "2h", "Medium"),
    t(2, "Backend", "POST /admin/users/{id}/block", "Block user login.", ["Set is_blocked flag on user", "Invalidate tokens optional stub", "Audit log", "Tests"], "Blocked user login 403.", "2h", "Medium"),
    t(2, "Frontend", "Admin users table page", "Admin UI.", ["Route `/admin/users` guarded", "Block button with confirm", "Search input", "Role badges"], "Admin sees all users.", "3h", "Medium"),
]

# --- WAVE 3 ---
TASKS += [
    t(3, "QA", "Evaluation dataset file with 30 fixed prompts", "Benchmark input fixture.", ["Create `eval/prompts.json` with 30 briefs", "Tag by format mix", "Version field", "README how to extend"], "File committed; 30 entries.", "2h", "Easy"),
    t(3, "AI", "Naive baseline single-prompt generator", "Comparison arm.", ["Function ignoring agents/RAG", "Same output schemas", "Log latency + token usage", "CLI entrypoint"], "Runs 1 prompt mocked.", "2h", "Medium"),
    t(3, "AI", "Run multi-agent+RAG eval harness", "Batch evaluation runner.", ["Loop 30 prompts through full graph", "Capture outputs to `eval/results/`", "Record pass/fail critic stats", "Configurable via env"], "Produces JSON results file.", "3h", "Hard - Tech Lead"),
    t(3, "AI", "Ragas or DeepEval metrics integration", "Quantitative scores.", ["Install ragas/deepeval", "Metrics: faithfulness, relevancy per format", "Compare baseline vs pipeline", "Save scores CSV"], "CSV has 30 rows metrics.", "3h", "Hard - Tech Lead"),
    t(3, "QA", "Generate comparison charts script", "Visual report for paper/demo.", ["Python matplotlib/plotly script", "Bar charts latency, pass rate, metric means", "Output PNG to `eval/charts/`", "Document in eval README"], "PNG files generated.", "2h", "Medium"),
    t(3, "DevOps", "Render backend deploy blueprint", "Production API hosting.", ["Add `render.yaml` or manual doc", "Build command, start command", "Env vars checklist", "Health check path /health"], "Deploy succeeds on Render.", "2h", "Medium"),
    t(3, "DevOps", "Vercel frontend project link + env", "Production UI.", ["Document vercel.json if needed", "Set NEXT_PUBLIC_API_URL production", "Preview env for PRs", "Smoke test login"], "Production URL loads.", "2h", "Easy"),
    t(3, "DevOps", "Production Postgres + pgvector provisioning", "Live database.", ["Document Supabase/Neon/RDS choice", "Run migrations on prod", "Rotate JWT secret", "Backup note"], "App connects to prod DB.", "2h", "Hard - Tech Lead"),
    t(3, "QA", "End-to-end smoke test checklist", "Pre-demo validation.", ["Markdown checklist: register, brand, ingest, generate, approve", "Assign owners per step", "Sign-off section", "Link to eval charts"], "Team completes once.", "1h", "Easy"),
    t(3, "Frontend", "Polish loading/error states app-wide", "UX hardening.", ["Audit pages for error boundaries", "Consistent toast messages", "404 page", "Skeleton loaders missing screens"], "No blank screens on error.", "3h", "Medium"),
    t(3, "Frontend", "Responsive layout pass for dashboard", "Mobile-friendly demo.", ["Tailwind breakpoints on sidebar", "Collapse nav", "Test library table scroll", "Fix overflow issues"], "375px width usable.", "2h", "Easy"),
]

# Bonus / nice-to-have
TASKS += [
    t(3, "DB", "Multi-brand membership for social managers", "User belongs to many brands.", ["Adjust queries for active_brand_id on user session", "Migration if needed", "Document limitation removal", "Indexes"], "User switches context.", "2h", "Medium", ["bonus"]),
    t(3, "Frontend", "Brand switcher dropdown in header", "Multi-brand UX.", ["List brands from API", "Set active brand in context", "Reload data on switch", "Persist selection localStorage"], "Switch updates library.", "2h", "Medium", ["bonus"]),
    t(3, "Backend", "GET /users/me/brands list endpoint", "Brands for switcher.", ["Return id, name, role", "Auth required", "Pagination if many", "Tests"], "Switcher populated.", "1h", "Easy", ["bonus"]),
    t(3, "AI", "Diff-based learning from user edits", "Suggest banned word updates.", ["Compare pre/post edit text", "Extract added words/phrases", "Propose ban list additions endpoint", "Owner confirm before save"], "Suggestion list appears.", "3h", "Hard - Tech Lead", ["bonus"]),
    t(3, "AI", "LangSmith tracing optional wrapper", "Observability.", ["Env `LANGSMITH_API_KEY`", "Wrap graph invoke with tracing", "Document dashboard link", "Disable by default"], "Traces appear when enabled.", "2h", "Hard - Tech Lead", ["bonus"]),
    t(3, "Frontend", "Monthly calendar view of posts", "Planning UI.", ["Calendar component", "Posts by scheduled/approved date", "Month navigation", "Click to open post"], "Posts show on dates.", "3h", "Medium", ["bonus"]),
    t(3, "Backend", "Auto-publish webhook stub", "Future social API.", ["POST /posts/{id}/publish stub returns 501", "Document future integration", "Feature flag", "No-op safe"], "Returns documented message.", "1h", "Easy", ["bonus"]),
    t(3, "AI", "Direct AI image generation endpoint stub", "Future image API.", ["POST /posts/{id}/generate-image stub", "Validate image post format", "Return 501 or mock URL", "Feature flag"], "Swagger documents endpoint.", "2h", "Medium", ["bonus"]),
]

# Additional granular tasks to round out junior slices - split across team members
EXTRA = [
    # Wave 1 vertical slice assignments documentation
    t(1, "QA", "Document Wave 1 vertical slice ownership matrix", "Clarify who ships which slice.", ["Create `docs/WAVES.md` with 4 slice names", "Map DB+API+UI per developer", "Definition of done per slice", "Review in standup"], "Matrix approved by lead.", "1h", "Easy"),
    t(1, "Frontend", "Dashboard home shell with sidebar nav", "Navigation skeleton.", ["Layout sidebar: Library, New Post, Brand, Settings", "Highlight active route", "User menu logout", "Brand name in header"], "All links route correctly.", "2h", "Easy"),
    t(1, "Backend", "GET /posts/{id} detail endpoint", "Single post fetch.", ["Include body_json, status, author", "Brand authz", "404 handling", "Embed media attachments"], "Detail JSON complete.", "1h", "Easy"),
    t(1, "Frontend", "Post detail page read-only view", "View single draft.", ["Route `content/[id]`", "Render text post structure", "Status badge", "Back link"], "Opens from library.", "2h", "Easy"),
    t(2, "Backend", "PATCH /posts/{id} manual save draft", "Human edits without AI.", ["Validate schema per format", "Only draft editable", "Creator/owner rules", "updated_at bump"], "Manual edit persists.", "2h", "Medium"),
    t(2, "Frontend", "Editable fields on post detail for drafts", "Manual content tweak.", ["Controlled inputs per format", "Save button", "Disable when pending/approved", "Validation errors"], "Save updates API.", "3h", "Medium"),
    t(2, "QA", "Seed script for demo brand + users", "Demo data for presentation.", ["Script `scripts/seed_demo.py`", "Owner, creator, sample posts", "Document credentials in `.env.example` only", "Idempotent run"], "Seed runs twice safely.", "2h", "Medium"),
    t(2, "Backend", "Email notification stub on submit", "Placeholder for owner alert.", ["Log INFO on submit with owner email", "Interface NotificationService", "No-op impl default", "Swappable later"], "Log line appears.", "1h", "Easy"),
    t(1, "Backend", "System Admin bootstrap CLI", "Create first admin user.", ["`python -m app.cli create-admin email`", "Hash password prompt", "Role admin", "Doc one-time use"], "Admin can login.", "1h", "Medium"),
    t(3, "Backend", "Rate limit middleware on generate endpoints", "Protect Gemini quota.", ["slowapi or custom per-user limit", "429 response", "Config RATE_LIMIT", "Test exceed"], "6th rapid call 429.", "2h", "Medium"),
    t(3, "QA", "Security review checklist JWT + RBAC", "Academic security sign-off.", ["Doc checklist in docs/SECURITY.md", "Verify HTTPS only prod", "Confirm secrets not in repo", "Role matrix table"], "Checklist complete.", "1h", "Easy"),
    t(0, "Frontend", "Root landing page marketing stub", "Public entry.", ["`app/page.tsx` hero BrandVoice", "CTA Login / Register", "Tailwind layout", "No auth required"], "Landing renders.", "1h", "Easy"),
    t(0, "Backend", "OpenAPI tags and route module split", "Navigable Swagger for juniors.", ["Split routers: auth, brands, posts, admin", "Include in main", "Tag metadata", "Brief descriptions"], "Swagger grouped by tag.", "1h", "Easy"),
]

TASKS += EXTRA


def format_task_md(task: Task) -> str:
    checks = "\n".join(f"- [ ] {c}" for c in task["checklist"])
    labels = ", ".join(f"`{l}`" for l in task["labels"])
    return (
        f"### {task['title']}\n\n"
        f"**Goal:** {task['goal']}\n\n"
        f"**Step-by-step checklist:**\n{checks}\n\n"
        f"**Acceptance criteria (DoD):** {task['dod']}\n\n"
        f"**Estimated effort:** {task['effort']} | **Difficulty:** {task['difficulty']}\n\n"
        f"**Labels:** {labels}\n\n---\n"
    )


def format_issue_body(task: Task) -> str:
    checks = "\n".join(f"- [ ] {c}" for c in task["checklist"])
    return (
        f"## Goal\n{task['goal']}\n\n"
        f"## Step-by-step checklist\n{checks}\n\n"
        f"## Acceptance criteria (DoD)\n{task['dod']}\n\n"
        f"## Estimated effort\n{task['effort']}\n\n"
        f"## Difficulty\n{task['difficulty']}\n"
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    scripts = root / "scripts"
    docs.mkdir(exist_ok=True)

    by_wave: dict[int, list[Task]] = {}
    for task in TASKS:
        by_wave.setdefault(task["wave"], []).append(task)

    wave_counts = {w: len(by_wave[w]) for w in sorted(by_wave)}
    md_parts = [
        "# BrandVoice — Product Backlog",
        "",
        "Granular tasks for GitHub Projects. Generated for a 5-person academic team (4 juniors + 1 Tech Lead).",
        "",
        f"**Total tasks:** {len(TASKS)}",
        "",
        "| Wave | Focus | Tasks |",
        "|------|--------|------:|",
        f"| 0 | Tech Lead foundation (repo, Docker, CI, skeletons) | {wave_counts.get(0, 0)} |",
        f"| 1 | Core vertical slices (auth, brand, ingest, RAG, text agent, library) | {wave_counts.get(1, 0)} |",
        f"| 2 | Full MVP (formats, critic, editor, media, approvals, admin) | {wave_counts.get(2, 0)} |",
        f"| 3 | Eval, deploy, polish, bonus | {wave_counts.get(3, 0)} |",
        "",
        "## Suggested GitHub Project columns",
        "",
        "`Backlog` → `Wave 0` → `Wave 1` → `Wave 2` → `Wave 3` → `Done` (or map labels to views).",
        "",
        "## How to import",
        "",
        "1. Ensure `gh auth login` is active.",
        "2. Run: `bash scripts/create-backlog-issues.sh`",
        "3. Add issues to your GitHub Project board (bulk select in Issues tab).",
        "",
        "## Label legend",
        "",
        "- `wave-0-foundation` … `wave-3-polish`",
        "- `layer-db`, `layer-backend`, `layer-ai`, `layer-frontend`, `layer-qa`, `layer-devops`",
        "- `bonus` for nice-to-have",
        "",
    ]

    for wave in sorted(by_wave):
        md_parts.append(f"## Wave {wave}")
        md_parts.append("")
        for task in by_wave[wave]:
            md_parts.append(format_task_md(task))
            md_parts.append("")

    backlog_path = docs / "BRANDVOICE_BACKLOG.md"
    backlog_path.write_text("\n".join(md_parts), encoding="utf-8")

    # Shell script
    sh_lines = [
        "#!/usr/bin/env bash",
        "# Create all BrandVoice backlog issues via GitHub CLI",
        "set -euo pipefail",
        'REPO="${GITHUB_REPOSITORY:-TomSebty/urban-octo-winner}"',
        'cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"',
        "",
        "echo 'Creating labels (ignore errors if they exist)...'",
        "for lb in wave-0-foundation wave-1-core wave-2-mvp wave-3-polish \\",
        "  layer-db layer-backend layer-ai layer-frontend layer-qa layer-devops bonus; do",
        '  gh label create "$lb" --repo "$REPO" --force 2>/dev/null || true',
        "done",
        "",
    ]

    issues_json = scripts / "backlog_issues.json"
    serializable = []
    for i, task in enumerate(TASKS):
        serializable.append(
            {
                "title": task["title"],
                "body": format_issue_body(task),
                "labels": task["labels"],
            }
        )
    issues_json.write_text(json.dumps(serializable, indent=2, ensure_ascii=False), encoding="utf-8")

    sh_lines += [
        "SCRIPT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"",
        "JSON=\"$SCRIPT_DIR/backlog_issues.json\"",
        'if ! command -v jq &>/dev/null; then',
        '  echo "jq is required. Install jq or use: python3 scripts/generate_backlog.py"',
        "  exit 1",
        "fi",
        'COUNT=$(jq length "$JSON")',
        'echo "Creating $COUNT issues in $REPO ..."',
        'for i in $(seq 0 $((COUNT - 1))); do',
        '  TITLE=$(jq -r ".[$i].title" "$JSON")',
        '  BODY=$(jq -r ".[$i].body" "$JSON")',
        '  LABELS=$(jq -r ".[$i].labels | join(\",\")" "$JSON")',
        '  gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY" --label "$LABELS"',
        '  echo "Created: $TITLE"',
        "done",
        'echo "Done. Open GitHub Projects and add these issues to the board."',
        "",
    ]

    sh_path = scripts / "create-backlog-issues.sh"
    sh_path.write_text("\n".join(sh_lines), encoding="utf-8")
    sh_path.chmod(0o755)

    print(f"Wrote {backlog_path} ({len(TASKS)} tasks)")
    print(f"Wrote {sh_path}")
    print(f"Wrote {issues_json}")


if __name__ == "__main__":
    main()