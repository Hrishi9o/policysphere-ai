# 🎓 Dell Campus Recruitment 2026 — Eliminative Hackathon Round (MSRIT)
## Problem Statement 1: AI-Powered Campus Policy Discovery Assistant

---

## 📌 1. Exact Requirements from Official Briefing Sheets

### A. The Challenge
Build an intelligent conversational assistant that translates vague, informal student scenarios into precise corporate/academic policy matches to deliver accurate, source-verified answers. The system must successfully bridge the gap between casual student language and formal institutional rules without hallucinating false permissions.

### B. Possible Technology Stack Options (Flexible & Combined)
*Students can select and combine any relevant tools to build their solution:*
* **Core Patterns:** Hypothetical Document Embeddings (HyDE), Retrieval-Augmented Generation (RAG)
* **AI & Architecture:** Large Language Models (LLMs), AI Agents, Agent-to-Agent (A2A) workflows
* **Infrastructure & Integration:** Model Context Protocol (MCP), Vector Databases, Guardrail Frameworks (e.g., NeMo Guardrails, Llama Guard)

### C. Specific Evaluation Criteria for PS-1
1. **HyDE Implementation:** Creativity and effectiveness of the prompt engineering used to generate realistic, bureaucratic academic text.
2. **Retrieval Accuracy:** Benchmark improvement in search relevance when using the HyDE snippet versus the raw student query.
3. **Guardrails & Safety:** System robustness in ensuring the final response relies **only on real university data**, completely ignoring any hallucinated assumptions from the fake policy.

---

## 🏆 2. Official Evaluation Matrix (100% Weightage Breakdown)

| Dimension | Weight | Target Criteria & Focus Areas |
| :--- | :---: | :--- |
| **1. Solutioning** | **25%** | System architecture, end-to-end data flows, edge-case resilience, and error handling. |
| **2. Technology** | **25%** | Core pattern understanding (HyDE, RAG, MCP), code optimization, and tool selection maturity. |
| **3. Reasoning** | **20%** | Justification of architectural trade-offs, latency awareness, and cost-benefit analysis. |
| **4. Innovation** | **15%** | Creative problem-solving, novel prompt strategies, and out-of-the-box features. |
| **5. Presentation** | **15%** | Production-ready documentation, system architecture diagrams, and a crisp technical pitch. |

---

## 📦 3. Submission Deliverables & Verified Artifacts

1. **PowerPoint Presentation (10 Slides):**
   * File: [Hrishikesh_Shetty_PS1_MSRIT.pptx](file:///e:/Dell/Hrishikesh_Shetty_PS1_MSRIT.pptx)
   * Formatted in 16:9 widescreen, strictly aligned with Dell's 5 evaluation dimensions, with embedded benchmark chart and speaker notes.
2. **Comprehensive Prompt Documentation:**
   * File: [PROMPT_LOG.md](file:///e:/Dell/PROMPT_LOG.md)
   * Complete 16-phase chronological audit log of all prompts, design rationales, and benchmark tables.
3. **Video Presentation Materials:**
   * Walkthrough Script: [docs/video_script.md](file:///e:/Dell/docs/video_script.md) (Second-by-second 3-minute screen recording guide).
   * Interview Defense Guide: [docs/panel_qna.md](file:///e:/Dell/docs/panel_qna.md) (15 technical Q&As for the panel interview).
4. **Submission Protocol:**
   * **Email To:** `Pratistha.Sharma@dell.com`
   * **Subject Format:** `Hrishikesh_Shetty_PS1_MSRIT`
   * **Deadline:** Today by **4:00 PM IST** (Recommended buffer: Submit by 12:30 PM).

---

## 🚀 4. How to Start the Engine (Quick Start Guide)

### Option A: One-Click Launch (Recommended)

**On Windows (PowerShell):**
```powershell
.\run.ps1
```
*This automatically checks your Python installation, verifies/builds the vector index from `data/handbook.md`, and launches the FastAPI server at `http://localhost:8000`.*

**On Linux / macOS (Bash):**
```bash
chmod +x run.sh
./run.sh
```

---

### Option B: Step-by-Step Manual Launch

1. **Install Prerequisites:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file (or copy from `.env.example`):
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Build the Policy Vector Index:**
   ```bash
   python src/ingest.py
   ```
   *(Parses 25 official clauses from `data/handbook.md` into `data/vector_index.pkl` with 0 fake policy leakage).*

4. **Start the Web Application & REST API:**
   ```bash
   python api.py
   ```
   * Open your browser at: **`http://localhost:8000`**
   * OpenAPI Swagger docs available at: **`http://localhost:8000/docs`**

5. **Run the Empirical Benchmark Suite:**
   ```bash
   python benchmark.py
   ```
   *(Evaluates all 20 standardized scenarios across Raw, Single HyDE, and Multi-HyDE modes; writes results to `results/benchmark.md` and `results/benchmark.png`).*

---

### Option C: Production Docker Launch

```bash
docker-compose up --build
```
*Launches containerized PolicySphere AI on port `8000` with volume-mounted vector index and health-check monitoring.*

---

### Option D: Model Context Protocol (MCP) Server

**Run as Standard Stdio JSON-RPC 2.0 Server:**
```bash
python src/mcp_server.py
```
*Exposes 3 standard MCP tools (`search_campus_policies`, `get_policy_by_section`, `list_all_policy_sections`) for external agents (Claude Desktop, Cursor, enterprise sidecars).*

**Access via HTTP REST Endpoints:**
* `GET /api/mcp/manifest` — Returns complete MCP tool schema definitions
* `POST /api/mcp/call` — Executes an MCP tool call remotely

---

## 🏗️ 5. End-to-End System Architecture

```
                                  +---------------------------------------+
                                  |         Informal Student Query        |
                                  | ("My band has a gig, can I skip lab?")|
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |     Layer 1: Input Safety Guardrail   |
                                  |  (Blocks Bribery, Proxy, Forgery)     |
                                  +-------------------+-------------------+
                                                      | Clean Query
                                                      v
                                  +---------------------------------------+
                                  |      Layer 2: HyDE Generator Engine   |
                                  |  (Prompt Engineering: Translates to   |
                                  |   Bureaucratic Academic Directive)    |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |     Layer 3: Dense Vector Store       |
                                  |     (TF-IDF + Cosine Similarity)      |
                                  |     Exposed via MCP Tool Protocol     |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  | Layer 4: Verification Agent (A2A)     |
                                  | - Checks institutional compliance     |
                                  | - Enforces strict handbook citations  |
                                  | - Eliminates hallucinated permissions |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |        Final Source-Verified Answer   |
                                  | (Section 1.3.0 + Procedural Steps)    |
                                  +---------------------------------------+
```

---

