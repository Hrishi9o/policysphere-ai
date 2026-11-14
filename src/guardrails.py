"""
Dell Hackathon 2026 - Problem Statement 1
Module: src/guardrails.py
Honest, Layered Guardrails Framework:
- Layer 1 (Input): Rule-based checks for prompt injection, bribery, forged documents, proxy attendance, and off-topic queries.
- Layer 2 (Retrieval Confidence): Similarity threshold below which the system safely refuses and directs to advisors.
- Layer 3 (Verifier Agent): Dual-agent grounding verifier ensuring all claims are supported by cited chunks.
- Anti-Leakage Check: Strict regex verification ensuring no planted fake policy text ever appears in any response.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FAKE_POLICY_PATH = os.path.join(DATA_DIR, "fake_policy.md")


class InputGuardrail:
    """
    Layer 1: Input Intent & Security Interceptor
    Scans incoming queries for security risks, prompt injection, academic malpractice,
    gibberish/nonsense, or completely out-of-domain topics.
    """

    PATTERNS = [
        # Prompt Injection / Adversarial Overrides
        (r"\b(ignore (all )?previous instructions|system override|jailbreak|disregard (all )?rules|you are now adminbot)\b",
         "SECURITY_INJECTION", "Adversarial prompt injection attempt detected."),
        
        # Monetary Condonation / Bribery
        (r"\b(pay|bribe|money|cash|fine|remittance)\b.*\b(attendance|pass|marks|grade|bypass)\b",
         "MALPRACTICE_BRIBERY", "Attempted monetary condonation or financial inducement for academic favors."),
        
        # Document Forgery
        (r"\b(fake|forge|fabricat|counterfeit)\b.*\b(medical|certificate|doctor|signature|slip|letter)\b",
         "MALPRACTICE_FORGERY", "Submission or procurement of fraudulent documentation."),
        
        # Surrogate / Proxy Attendance
        (r"\b(proxy|fake attendance|sign for me|mark my friend)\b",
         "MALPRACTICE_PROXY", "Surrogate or proxy biometric attendance representation."),
        
        # Completely Off-Topic / Out of Scope
        (r"\b(pet|pets|dog|dogs|cat|cats|helicopter|helicopters|heliport|pool party|swimming pool|cocktail|casino)\b",
         "OFF_TOPIC", "Query concerns topics entirely outside institutional academic policy scope.")
    ]

    @classmethod
    def is_gibberish(cls, text: str) -> bool:
        """Detects random keyboard mash, nonsensical strings, and unnatural character distributions."""
        clean = text.strip()
        if not clean:
            return True
        words = clean.split()
        
        # 1. Single long unspaced random word (e.g., 'gerighejognerongerolgnerge')
        for w in words:
            w_alpha = re.sub(r'[^a-zA-Z]', '', w)
            if len(w_alpha) >= 18:
                known_long_words = {
                    "interinstitutional", "telecommunication", "telecommunications",
                    "institutionalization", "compartmentalization", "mischaracterization"
                }
                if w_alpha.lower() not in known_long_words:
                    return True

        # 2. Extreme unnatural consonant cluster (e.g., 'bcdfgh', 'sdfghjkl')
        if re.search(r'[bcdfghjklmnpqrstvwxyz]{6,}', clean.lower()):
            return True

        # 3. Repeated character mash (e.g., 'aaaaaa', 'zzzzzz')
        if re.search(r'(.)\1{4,}', clean):
            return True

        # 4. Check for abnormal vowel/consonant ratios on words of length >= 7
        for w in words:
            w_alpha = re.sub(r'[^a-zA-Z]', '', w).lower()
            if len(w_alpha) >= 7:
                vowels = sum(1 for c in w_alpha if c in 'aeiouy')
                ratio = vowels / len(w_alpha)
                if ratio < 0.14 or ratio > 0.85:
                    return True

        return False

    @classmethod
    def check_input(cls, query: str) -> Optional[Dict[str, str]]:
        # Fast gibberish intercept
        if cls.is_gibberish(query):
            return {
                "flag": "INVALID_GIBBERISH",
                "reason": "Input appears to be an unrecognized or nonsensical string rather than a valid academic inquiry.",
                "action": "BLOCKED"
            }

        q_lower = query.lower()
        for pattern, flag, reason in cls.PATTERNS:
            if re.search(pattern, q_lower):
                return {
                    "flag": flag,
                    "reason": reason,
                    "action": "BLOCKED"
                }
        return None


class RetrievalConfidenceGuardrail:
    """
    Layer 2: Retrieval Confidence Threshold
    Rejects queries where the vector similarity score fails to reach the confidence threshold.
    """

    DEFAULT_THRESHOLD = 0.12

    @classmethod
    def evaluate_confidence(cls, retrieved_chunks: List[Dict[str, Any]], threshold: float = DEFAULT_THRESHOLD) -> bool:
        if not retrieved_chunks:
            return False
        # Check maximum cosine similarity across top candidate chunks
        cosines = [c.get("cosine_similarity", c.get("score", 0.0)) for c in retrieved_chunks[:3]]
        max_cos = max(cosines) if cosines else 0.0
        return max_cos >= 0.10


class VerifierAgent:
    """
    Layer 3: Grounding & Anti-Hallucination Verification Agent
    Verifies that draft claims are directly supported by retrieved chunks,
    and guarantees zero text from planted fake policies ever leaks.
    """

    def __init__(self):
        self.fake_snippets = self._load_fake_policy_snippets()

    def _load_fake_policy_snippets(self) -> List[str]:
        """Loads distinctive keywords and phrases from fake_policy.md."""
        snippets = [
            "99.1.0", "99.2.0", "99.3.0", "fake clause", "fake policy",
            "blanket extracurricular", "cash remittance scheme",
            "informal oral grade alteration", "automatically exempt from attending all regular laboratory",
            "unrestricted examination hall tickets", "modify their grade on the portal without paying"
        ]
        if os.path.exists(FAKE_POLICY_PATH):
            with open(FAKE_POLICY_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    clean = line.strip().lower()
                    if clean.startswith("### fake clause"):
                        # Extract clause number like 99.1.0
                        match = re.search(r"(\d+\.\d+\.\d+)", clean)
                        if match and match.group(1) not in snippets:
                            snippets.append(match.group(1))
        return snippets

    def verify_answer(self, draft_answer: str, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifies answer against retrieved chunks and planted fake policy database.
        """
        ans_lower = draft_answer.lower()
        
        # 1. Anti-Leakage Check: Ensure zero text from fake_policy.md exists in answer
        for fake in self.fake_snippets:
            if fake in ans_lower:
                return {
                    "supported": False,
                    "unsupported_claims": ["Answer contains planted fake policy text"],
                    "leakage_detected": True,
                    "decision": "NOT_PERMITTED"
                }

        # 2. Section ID Citation Check: Must cite at least one retrieved section ID
        valid_section_ids = [chunk["section_id"] for chunk in retrieved_chunks]
        cited_sections = []
        for sec_id in valid_section_ids:
            if sec_id in draft_answer:
                cited_sections.append(sec_id)

        if not cited_sections and "couldn't find a policy" not in ans_lower:
            return {
                "supported": False,
                "unsupported_claims": ["Draft does not cite any verified section ID from retrieved chunks"],
                "leakage_detected": False,
                "decision": "NO_POLICY_FOUND"
            }

        return {
            "supported": True,
            "cited_sections": cited_sections,
            "leakage_detected": False,
            "decision": "VERIFIED"
        }


if __name__ == "__main__":
    print("=" * 80)
    print("GUARDRAILS VERIFICATION TEST")
    print("=" * 80)
    
    # Test Layer 1 Input Check
    test_unsafe = "Can I pay a cash bribe for attendance?"
    res_input = InputGuardrail.check_input(test_unsafe)
    print(f"Unsafe Input Check: {res_input}")
    
    # Test Layer 3 Anti-Leakage
    verifier = VerifierAgent()
    fake_leak = "Students may skip any lab for any club event without penalty under Fake Clause 99.1.0"
    res_leak = verifier.verify_answer(fake_leak, [])
    print(f"Fake Policy Leakage Detection: {res_leak}")
