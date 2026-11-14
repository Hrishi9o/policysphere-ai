# 📊 Comprehensive Benchmark Report (Audited Data)

### Evaluation Summary (15 Standard Inquiries, 3 Unanswerable, 2 Adversarial Injections)

| Retrieval Mode | Hit@1 (%) | Hit@3 (%) | MRR (Mean Reciprocal Rank) | Avg Latency (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Raw Query Baseline** | 66.7% | 73.3% | 0.7 | 5.36 ms |
| **Single HyDE** | 86.7% | 93.3% | 0.9 | 7298.89 ms |
| **Multi-Hypothesis HyDE (RRF)** | **66.7%** | **93.3%** | **0.802** | 3917.24 ms |

### 🛡️ Safety & Guardrail Performance
- **Out-of-Scope Safe Refusal Rate:** 3/3 (100.0%)
- **Prompt Injection Interception Rate:** 2/2 (100.0%)
- **Planted Fake Policy Leakage:** 0 (Zero Leakage / 100% Isolation)
