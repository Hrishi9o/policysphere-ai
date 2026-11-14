# TECHNICAL VIDEO PRESENTATION SCRIPT & RECORDING PROTOCOL
**System Name:** PolicySphere™ AI  
**Candidate:** Hrishikesh Shetty  
**Institution:** Ramaiah Institute of Technology (MSRIT)  
**Evaluation Track:** Dell Campus Recruitment Hackathon — Problem Statement 1  
**Target Recipient:** `Pratistha.Sharma@dell.com`  
**Target Run-Time:** Exactly 04:00 minutes (240 seconds total)  
**Total Word Count:** ~395 Words (Paced at 130 WPM with 55 seconds of live UI actions)

---

## 1. Pre-Recording Environment Checklist

| Item | Setup |
| :--- | :--- |
| **PowerPoint Deck** | Open `Hrishikesh_Shetty_PS1_MSRIT.pptx` in Fullscreen (`F5`) on Slide 01. |
| **Web Application** | Open `http://127.0.0.1:8000` in your browser, running full-width in the background. |
| **Notepad Staging** | Have this single unanswerable query ready on your screen to copy-paste: <br>`Can i get ps5 to the hostel??` |
| **Window Switching** | Practice `Alt + Tab` once to verify smooth transition between PowerPoint and your browser. |

---

## 2. Executive Technical Cue Sheet (240 Seconds Total)

### PART 1: Architectural Defense & Methodology (00:00 – 01:45 | 105 Seconds)

#### [00:00 – 00:10] SLIDE 01: Executive Title & Candidate Attribution (10s)
*(Visual: Slide 01 — Cover)*
> "Good morning, members of the technical evaluation panel. My name is Hrishikesh Shetty from Ramaiah Institute of Technology, presenting **PolicySphere™ AI**—an autonomous campus policy discovery and compliance engine engineered to resolve unstructured student inquiries into verified institutional regulations."

*Action:* Press `Right Arrow (→)` to advance to Slide 02.

---

#### [00:10 – 00:25] SLIDE 02: Problem Definition & Semantic Distance (15s)
*(Visual: Slide 02 — Students and handbooks speak differently)*
> "In institutional information retrieval, the primary failure mode is **semantic distance**. Students articulate queries using casual, situational narratives, while university handbooks encode governance in rigid administrative language. Standard keyword search mechanisms fail completely because semantic overlap between these vocabularies is negligible."

*Action:* Press `Right Arrow (→)` to advance to Slide 03.

---

#### [00:25 – 00:40] SLIDE 03: Latency-Bounded Processing Pipeline (15s)
*(Visual: Slide 03 — How a question becomes a cited answer)*
> "To resolve this disparity without hallucination, we engineered a deterministic four-tier pipeline: front-end input sanitization, multi-hypothesis query expansion via HyDE, sublinear vector retrieval in under 5 milliseconds, and an autonomous verification agent."

*Action:* Press `Right Arrow (→)` to advance to Slide 04.

---

#### [00:40 – 00:55] SLIDE 04: Multi-Hypothesis HyDE & Reciprocal Rank Fusion (15s)
*(Visual: Slide 04 — HyDE and reciprocal rank fusion)*
> "Our generative layer synthesizes three distinct institutional perspectives—Academic Affairs, Examinations, and Student Welfare—preserving critical entity fidelity. We then apply Reciprocal Rank Fusion to aggregate these parallel retrieval lists, enforcing a mathematical cosine cutoff of 0.12 to suppress out-of-domain noise."

*Action:* Press `Right Arrow (→)` to advance to Slide 05.

---

#### [00:55 – 01:10] SLIDE 05: Three-Layer Defense-in-Depth Guardrails (15s)
*(Visual: Slide 05 — Three checks before an answer)*
> "Deterministic safety is enforced through defense-in-depth: Layer 1 executes regex and entropy validation to intercept prompt injections at zero token cost. Layer 2 applies our cosine threshold gate, and Layer 3 performs entity-level topic verification to prevent hallucinations."

*Action:* Press `Right Arrow (→)` to advance to Slide 06.

---

#### [01:10 – 01:20] SLIDE 06: Model Context Protocol (MCP) Standard (10s)
*(Visual: Slide 06 — Policy tools for other assistants)*
> "For enterprise integration, we implemented the Model Context Protocol, exposing native search and retrieval tools over JSON-RPC 2.0 for external orchestrators like Claude Desktop or campus ERP bots."

*Action:* Press `Right Arrow (→)` to advance to Slide 07.

---

#### [01:20 – 01:35] SLIDE 07: Empirical Benchmark & Prompt Engineering (15s)
*(Visual: Slide 07 — Single HyDE led on top-result accuracy)*
> "Every stage was driven by systematic prompt engineering, fully logged across sixteen phases in our `PROMPT_LOG.md`. On our audited benchmark, Single HyDE elevated Top-1 precision to **86.7%**, with **93.3%** recall and verified zero fake policy leakage."

*Action:* Press `Right Arrow (→)` to advance to Slide 08.

---

#### [01:35 – 01:45] SLIDE 08: Technology Stack & Architectural Sizing (10s)
*(Visual: Slide 08 — Why we chose this architecture)*
> "We optimized our architecture for production efficiency: our localized Scikit(sigh kit)-Learn vector index delivers sub-5 millisecond retrieval with zero cloud dependencies, while front-end screening eliminates compute waste on malformed inputs."

*Action:* Press `Right Arrow (→)` to advance to Slide 09.

---

### PART 2: Live System Verification & Demonstration (01:45 – 03:40 | 115 Seconds)

#### [01:45 – 01:50] SLIDE 09: Demo Transition (5s)
*(Visual: Slide 09 — A walkthrough of the web app)*
> "Now, let us examine PolicySphere AI operating in a live runtime environment."

*Action:* Press `Alt + Tab` to switch to your browser at `http://127.0.0.1:8000`.

---

#### [01:50 – 02:45] DEMO 01: Extracurricular Accommodations & Live HyDE Synthesis (55s)
*Action:* Click the preset button: `🎸 Band Gig & Lab Makeup` $\rightarrow$ Click `Discover Policy`.

> "Executing our baseline extracurricular scenario:
> 
> PolicySphere immediately maps the inquiry to the Extracurricular Duty Leave policy and Compensatory Lab regulations, granting **CONDITIONAL APPROVAL** under Form-D clearance countersigned by the Department Head.
> 
> Expanding the **HyDE Semantic Translation drawer** reveals the formal administrative directive synthesized in real time by our generative engine, illustrating how our prompt transforms casual student phrasing into dense regulatory language. Comparing Raw Baseline against Multi-HyDE demonstrates a jump from a false negative to a 100% verified match."

---

#### [03:05 – 03:35] DEMO 02: Temporal Constraint & Deadline Reasoning
*Action:* Paste Query 1 from Notepad $\rightarrow$ Click `Discover Policy`.  
*Query:* `I was discharged from the hospital on Monday at 10 AM, but I only submitted my medical papers to the HOD on Thursday afternoon. Will my petition be considered?`

> "Next, let us test complex temporal reasoning: A student discharged from the hospital on Monday morning who submits medical papers on Thursday afternoon.
> 
> Notice the intelligence: PolicySphere identifies the Medical Absence Condonation policy, but renders a determination of **NOT PERMITTED**. The reasoning engine performed temporal deduction: the handbook mandates submission within forty-eight hours of discharge. Because Monday morning to Thursday afternoon exceeds 72 hours, the petition is declared inadmissible based on explicit handbook rules."

---

#### [02:45 – 03:35] DEMO 02: Adversarial Robustness & Entity-Level Topic Verification (50s)
*Action:* Paste `Can i get ps5 to the hostel??` from Notepad into the search box $\rightarrow$ Click `Discover Policy`.

>"Finally, we evaluate anti-hallucination against an unanswerable inquiry: 'Can I get a PS5 to the hostel?'
> Rather than falsely quoting curfew hours because of the word 'hostel', our Entity Verifier prompt detects that consumer gaming devices are completely unmentioned in the handbook. It safely returns **`NO_POLICY_FOUND`**, directing the student to residential administration. Hallucination is completely suppressed."


---

#### [03:35 – 03:40] Transition back to PowerPoint (5s)
*Action:* Press `Alt + Tab` back to PowerPoint, then press `Right Arrow (→)` to advance to Slide 10.

---

### PART 3: Conclusion & Enterprise Scalability (03:40 – 04:00 | 20 Seconds)

#### [03:40 – 04:00] SLIDE 10: Roadmap & Concluding Sign-Off (20s)
*(Visual: Slide 10 — Product Roadmap & Conclusion)*
> "Looking ahead, PolicySphere is architected for multi-tenant campus isolation and automated ERP petition dispatch. 
> 
> In conclusion, PolicySphere AI delivers an enterprise-ready, zero-hallucination compliance engine backed by an audited 86.7% precision and sub-5 millisecond retrieval. All required deliverables—including the presentation deck, prompt documentation, and codebase—are complete and packaged for evaluation.
> 
> Thank you for your time and consideration."

---

## 3. Post-Recording Submission Checklist

- [ ] Confirm video run-time is **04:00 minutes** (±10 seconds).
- [ ] Export container: `Hrishikesh_Shetty_PS1_MSRIT.mp4`.
- [ ] Upload video to Google Drive / OneDrive and set link sharing to: **"Anyone with the link can view"**.
- [ ] Attach `Hrishikesh_Shetty_PS1_MSRIT.pptx` and `PROMPT_LOG.md` directly to your email.
- [ ] Transmit submission email to `Pratistha.Sharma@dell.com`.
