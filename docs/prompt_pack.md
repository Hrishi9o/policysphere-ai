# Campus Policy Discovery Assistant: Hackathon Prompt Pack

Prompts for the Dell hackathon round (Problem Statement 1), ordered by build phase.

## How to use this document

Paste the prompts one at a time, in order. After each one, save the prompt text, the date and time, and a one-line note on what it produced. The submission asks for all prompts covering solution finalization, code generation, demo building and presentation, and detailed prompt logs are graded for systematic problem-solving and reproducibility.

**Submission checklist**

- PPT, max 10 slides, renamed **name\_surname\_problem statement\_MSRIT**
- Complete prompt documentation (this log, filled in)
- Short, concise demo video showing functionality and design decisions
- Send individually to Pratistha.Sharma@dell.com by **tomorrow 4 PM**

## Prompt 1: Solution finalization

```
I'm building an "AI-Powered Campus Policy Discovery Assistant" for a 24-hour hackathon. 
Problem: students ask casual questions ("My band has a gig next Friday, can I skip 
my lab and make it up later?") but university handbooks use formal jargon 
("Intermittent Academic Accommodations"), so normal search fails. The system must 
translate casual queries into precise policy matches and give source-verified answers 
without hallucinating permissions.

Evaluation: Solutioning 25% (architecture, data flow, edge cases, error handling), 
Technology 25% (HyDE, RAG, MCP, tool choice), Reasoning 20% (trade-offs, latency, 
cost), Innovation 15%, Presentation 15%.

Propose a final architecture using HyDE + RAG + guardrails. Include:
1. End-to-end data flow (step by step)
2. Tech stack with a one-line justification for each choice, using only free or 
   cheap tools (Python, Streamlit, ChromaDB, an embedding model, one LLM API)
3. Edge cases: no matching policy, ambiguous query, conflicting policies, 
   prompt injection, a fake/hallucinated policy planted in the data
4. Trade-offs (HyDE latency and cost vs retrieval accuracy)
5. One innovative feature that goes beyond the basics
Keep it practical enough to build in about 8 hours.
```

## Prompt 2: Dataset

```
Create a realistic synthetic university handbook for "MSRIT" as a markdown file 
with about 25 policy sections covering: attendance, medical leave, lab absences, 
extracurricular/event participation, exam rescheduling, academic accommodations, 
backlog/re-evaluation, hostel rules, fee refunds, and grievance redressal. 
Use dense, formal bureaucratic language with section numbers (e.g., 4.2.1). 

Also create:
- fake_policy.md: 3 plausible-sounding but FAKE policies (e.g., "students may skip 
  labs for any club event without penalty") to test that my guardrails ignore 
  anything not in the official source
- test_questions.json: 15 casual student questions, each with the correct 
  section ID, plus 3 questions that have NO answer in the handbook
```

## Prompt 3: Code generation (core pipeline)

```
Write a modular Python project with these files:
- ingest.py: chunk handbook.md by section (keep section ID as metadata), embed, 
  store in ChromaDB. Only ingest the official handbook, never fake_policy.md.
- hyde.py: take a casual query and generate a formal hypothetical policy 
  paragraph in handbook style (use a strong few-shot prompt with 2 examples)
- retrieve.py: retrieve top-k using (a) raw query and (b) the HyDE paragraph
- answer.py: generate the final answer ONLY from retrieved chunks, with section 
  citations; if the chunks don't support an answer, reply exactly "I couldn't 
  find a policy covering this" and suggest who to contact
- guardrails.py: input check (prompt injection, off-topic) and output check 
  (every claim must be traceable to a retrieved chunk; add a similarity threshold 
  for "no answer")
Use try/except with clear error handling, config in .env, and short comments. 
Show the folder structure and requirements.txt.
```

## Prompt 4: Benchmark (your strongest differentiator)

```
Write benchmark.py that runs all questions in test_questions.json through both 
raw-query retrieval and HyDE retrieval. Report Hit@1, Hit@3, and MRR for each, 
average latency, and approximate token cost. Also verify that the 3 no-answer 
questions trigger the refusal and that none of the fake policies ever appear in 
answers. Output a results table (markdown + CSV) and a bar chart as PNG.
```

## Prompt 5: Demo UI

```
Build app.py in Streamlit with: a chat box; a side-by-side panel showing 
"Raw query results" vs "HyDE results"; the generated HyDE paragraph shown in an 
expander; the final answer with clickable citations showing the exact policy text; 
a confidence indicator; and a clear "no policy found" state. Add 4 example 
question buttons, including one guardrail test.
```

## Prompt 6: Presentation (max 10 slides)

```
Create a 10-slide PPT for this project: 1) Title and problem, 2) Why normal search 
fails, 3) Solution overview, 4) Architecture diagram, 5) HyDE prompt design, 
6) Tech stack and justification, 7) Guardrails and edge cases, 8) Benchmark results 
(raw vs HyDE) [I will paste my numbers], 9) Demo screenshots, 10) Trade-offs 
and future work. Clean, minimal design, little text per slide, speaker notes 
on each. Name it name_surname_problem statement_MSRIT.
```

## Prompt 7: Video script

```
Write a 3-minute demo video script for this project: 20s problem, 30s architecture, 
90s live demo (one successful query, the raw vs HyDE comparison, one guardrail 
refusal), 30s benchmark results, 10s closing. Include what to show on screen 
at each moment.
```

## Prompt 8: Prompt log

```
Here are all my prompts from this project: [paste]. Organize them into a clean 
document grouped by phase (solution finalization, code generation, demo, 
presentation), with a one-line purpose and outcome for each.
```

## Tips

- Replace the synthetic handbook with real MSRIT text if you can get it. It makes the demo more convincing.
- Run Prompt 4 for real and put the actual numbers on slide 8. Do not invent them.
- If code from Prompt 3 errors out, paste the error back to the model and log that as a prompt too. Debugging prompts show systematic problem-solving.
- Submit early. Late or incomplete submission determines eligibility for the interview phase.

## Prompt log template

Copy this table as you work and fill it in for every prompt you run, including debugging prompts.

| # | Phase | Prompt (short title) | Tool used | Outcome | Time |
| --- | --- | --- | --- | --- | --- |
| 1 | Solution finalization | Architecture with HyDE + RAG |  |  |  |
| 2 | Dataset | Synthetic handbook and test set |  |  |  |
| 3 | Code generation | Core pipeline |  |  |  |
| 4 | Code generation | Benchmark script |  |  |  |
| 5 | Demo | Streamlit UI |  |  |  |
| 6 | Presentation | 10-slide deck |  |  |  |
| 7 | Presentation | Video script |  |  |  |
| 8 | Documentation | Final prompt log |  |  |  |
