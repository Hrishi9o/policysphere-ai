# 🚀 HACKATHON MASTER MISSION CHARTER (v2.0)
**Project:** AI-Powered Campus Policy Discovery Assistant  
**Event:** Dell Campus Recruitment Drive 2026 — Eliminative Hackathon Round  
**Candidate Affiliation:** Ramaiah Institute of Technology (MSRIT)  
**Submission Deadline:** Tomorrow 4:00 PM IST | Contact: `Pratistha.Sharma@dell.com`  

---

## 🎯 MISSION STATEMENT
You are my autonomous engineering agent for a 24-hour hackathon that is the eliminative round of a Dell campus recruitment drive. I'm a student at MSRIT. Build the complete project inside this workspace: code, tests, benchmark, demo app, presentation and documentation. Run and verify everything yourself in the terminal and browser. Do not just show me code.

---

## ❓ PROBLEM STATEMENT
"AI-Powered Campus Policy Discovery Assistant". Students ask casual or hypothetical questions (e.g. "My band has a gig next Friday, can I skip my lab and make it up later?"). Official handbooks use dense jargon (e.g. "Intermittent Academic Accommodations"), so standard search fails. Build a conversational assistant that translates vague informal scenarios into precise academic policy matches and returns accurate, source-verified answers WITHOUT hallucinating false permissions.

---

## ⚖️ EVALUATION CRITERIA (OPTIMIZE FOR THESE)
- **HyDE Implementation:** Creative, effective prompt engineering that generates realistic bureaucratic academic text using few-shot prompt synthesis.
- **Retrieval Accuracy:** Benchmarked improvement of HyDE vs the raw student query.
- **Guardrails & Safety:** Final answers rely ONLY on real university data and completely ignore a planted fake policy.
- **Weightage Breakdown:**
  - Solutioning: **25%** (architecture, end-to-end data flow, edge cases, error handling)
  - Technology: **25%** (HyDE, RAG, MCP understanding, code optimization, tool selection maturity)
  - Reasoning: **20%** (trade-offs, latency, cost-benefit)
  - Innovation: **15%** (novel prompt strategies, out-of-the-box features)
  - Presentation: **15%** (production-ready docs, architecture diagrams, crisp pitch)

---

## 📦 REQUIRED SUBMISSIONS
1. **Working Product (Demo):** FastAPI backend + React frontend.
2. **PPT, MAX 10 slides:** Working product, solution approach, tech stack. Naming: `name_surname_problem statement_MSRIT`.
3. **Prompt Documentation:** All prompts used for solution finalization, code generation, building the demo, generating the presentation in `PROMPT_LOG.md`.
4. **Demo Video Script:** 3-minute script with second-by-second on-screen actions.

---

## 🛠️ TECH STACK
- **Language & Runtime:** Python 3.11+, virtual environment, running locally on candidate's laptop.
- **LLM:** Google Gemini via `google-genai` SDK (Flash model; key in `.env` as `GEMINI_API_KEY`) with few-shot prompt synthesis and graceful fallback.
- **Vector Space & Retrieval:** Persistent, sublinear n-gram semantic vector index (Scikit-Learn TF-IDF + Cosine Similarity) optimized for institutional policy corpora (sub-10ms retrieval, zero heavy framework crashes, 100% explainable).
- **Backend API:** FastAPI (`api.py`) exposing `POST /api/ask`, `GET /api/benchmark`, and `GET /api/health` with CORS support for `localhost:5173`.
- **Frontend UI:** Modern React frontend (Vite/Tailwind) with chat interface, side-by-side raw vs. HyDE results, expandable citations, confidence indicators, latency breakdown, preset scenario buttons, and live Benchmark tab.
- **Presentation:** `python-pptx` (programmatic 10-slide deck with speaker notes and embedded charts).
- **Architecture Integration:** Model Context Protocol (MCP) standardized tool interface.

---

## 📜 WORKING RULES
1. **PLAN FIRST:** Produce an implementation plan and task list and wait for candidate approval before writing code. Include architecture, data flow, tech justification, trade-offs (quantify latency and cost), edge cases, and ONE innovative feature (Multi-Hypothesis HyDE generating 2–3 formal paraphrases with reciprocal rank fusion + "why this matched" explanation).
2. **PROMPT LOG:** Maintain `PROMPT_LOG.md` at repo root throughout. Append an entry for every instruction: number, phase, exact prompt, and one-line outcome. Also log every internal prompt embedded in the product with design choices.
3. **Simplicity & Explainability:** Clean, well-commented code that can be explained smoothly in a 5-minute presentation + 5-minute Q&A.
4. **Test As You Go:** Fix errors automatically and log fixes under "debugging".
5. **Zero Invented Numbers:** All benchmark metrics must come directly from executing `benchmark.py`.
6. **Zero Hardcoded Secrets:** Provide `.env.example`.

---

## 🏁 BUILD STEPS & MILESTONES

### M1 - Plan & Architecture Setup *(Completed)*
- Master plan & task list, Mermaid architecture diagram saved to `docs/architecture.md`.

### M2 - Dataset (`data/`) *(Completed)*
- `data/handbook.md`: Realistic synthetic MSRIT handbook (~25 numbered sections in dense formal jargon).
- `data/fake_policy.md`: 3 plausible but FAKE policies that contradict the handbook (planted to test guardrails).
- `data/test_questions.json`: 15 casual student questions mapped to correct section IDs, plus 3 unanswerable questions, plus 2 prompt injection attempts.

### M3 - Core Modular Pipeline (`src/`)
- `ingest.py`: Chunk by section ID with metadata (section_id, title), build vector index. Ingest ONLY `handbook.md`, with explicit assertion blocking `fake_policy.md`.
- `hyde.py`: Real few-shot prompt (3 diverse examples: attendance, exams, hostel) turning casual queries into formal hypothetical handbook paragraphs. Includes Multi-Hypothesis HyDE mode (3 diverse paragraphs merged via Reciprocal Rank Fusion) and graceful fallback.
- `retrieve.py`: Raw-query mode vs. HyDE mode vs. Multi-Hypothesis mode, top-k with similarity scores.
- `answer.py`: Answers strictly from retrieved chunks with section citations; decision classes: `CONDITIONAL_APPROVAL`, `NOT_PERMITTED`, `NO_POLICY_FOUND`.
- `guardrails.py`: 
  - Layer 1 (Input): Regex & keyword interceptor for prompt injection, bribery, forgery, proxy, and off-topic queries.
  - Layer 2 (Confidence): Similarity threshold below which safe refusal is returned.
  - Layer 3 (Verifier Agent): Dual-agent grounding verifier that confirms every claim is supported by a cited chunk, plus assertion that no fake policy text ever appears.
- Terminal smoke test to verify all 5 modules work seamlessly.

### M4 - Benchmark (`benchmark.py`)
- Runs all 20 questions in `data/test_questions.json` through: Raw, Single HyDE, and Multi-Hypothesis HyDE.
- Reports: Hit@1, Hit@3, MRR, latency per stage, token cost, refusal rate, injection block rate, and fake-policy leakage count.
- Outputs real audited data to `results/benchmark.md`, `results/benchmark.csv`, and `results/benchmark.png`.

### M5 - Demo UI (FastAPI + React)
- **FastAPI (`api.py`):** Wraps `src/` modules, exposes endpoints (`/api/ask`, `/api/benchmark`, `/api/health`).
- **React Frontend:**
  - Modern, responsive chat box.
  - Side-by-side Raw vs. HyDE results with similarity scores.
  - Expandable generated HyDE paragraph.
  - Final answer with expandable citations showing exact policy text.
  - Confidence indicator and latency breakdown.
  - 4 quick preset buttons (including guardrail test and fake-policy test).
  - Benchmark tab loading live data from `/api/benchmark`.
- Browser verification and screenshots saved to `docs/screenshots/`.

### M6 - Presentation (Max 10 Slides)
- Programmatic PowerPoint deck (`<Name>_<Surname>_PS1_MSRIT.pptx`) built with `python-pptx`:
  - 10 slides strictly aligned with Dell's 5 evaluation dimensions.
  - Minimal text, clean aesthetic, speaker notes on every slide.
  - Real benchmark numbers and charts embedded from `results/`.

### M7 - Documentation & Video Script
- `README.md`: Complete setup, run instructions, architecture.
- `docs/video_script.md`: 3-minute video script with on-screen cues.
- `docs/panel_qna.md`: 15 likely interview questions & crisp answers.
- Finalize `PROMPT_LOG.md`.
