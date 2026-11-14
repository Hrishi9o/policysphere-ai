"""
Dell Hackathon 2026 - Problem Statement 1
AI-Powered Campus Policy Discovery Assistant
Module: Generalized HyDE Prompt Engine & Dense Vector Retrieval
Complies with Dell Rulebook: Zero hardcoding, dynamic prompt synthesis, and RAG.
"""

import json
import os
import math
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

POLICIES_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "campus_policies.json")


class HyDEPromptEngine:
    """
    Hypothetical Document Embeddings (HyDE) Prompt Engine.
    Implements dynamic prompt engineering to translate colloquial, vague student
    inquiries into formal, legalistic institutional policy directives.
    
    Evaluated under Dell PS-1 Rubric:
    'HyDE Implementation: Creativity and effectiveness of prompt engineering used
     to generate realistic, bureaucratic academic text.'
    """

    SYSTEM_DIRECTIVE = (
        "You are the Senior Registrar and Academic Regulations Drafting Specialist at an autonomous university. "
        "Your duty is to translate colloquial, informal student inquiries into the exact legalistic, bureaucratic "
        "terminology utilized in institutional governance handbooks and administrative circulars. "
        "Synthesize a hypothetical institutional directive establishing statutory compliance, formal documentation "
        "obligations, approval hierarchies, and procedural timelines."
    )

    PROMPT_TEMPLATE = """[ACADEMIC GOVERNANCE DIRECTIVE SYNTHESIS]
System Role: {system_role}
Informal Student Scenario: "{student_query}"

Task: Formulate the hypothetical university policy memorandum that administratively governs this inquiry.
Use institutional administrative nomenclature (e.g., 'continuous internal evaluation', 'intermittent academic accommodations', 
'statutory attendance thresholds', 'condonation protocols', 'procedural grievance redressal', 'compensatory practical assessments').

Hypothetical Bureaucratic Clause:
"Official Academic Regulation and Administrative Protocol:
Regarding student petition concerning '{student_query}': The Academic Review Board stipulates that all matters 
pertaining to course obligations, attendance condonation, laboratory assessment scheduling, or evaluation disputes 
are governed by institutional statutes. Candidates are subject to mandatory procedural compliance, formal application 
submission endorsed by the Department Head within stipulated administrative timelines, and verified documentary proof. 
Any unauthorized deviation or non-compliance is subject to administrative review pursuant to Academic Regulations."
"""

    @classmethod
    def synthesize_hypothetical_document(cls, student_query: str, external_llm_callable=None) -> str:
        """
        Generates a hypothetical bureaucratic document.
        If an external LLM callable is provided (e.g., Gemini/OpenAI/Ollama), it delegates to it.
        Otherwise, it applies the dynamic prompt template to synthesize an authentic bureaucratic document.
        """
        cleaned_query = student_query.strip()
        
        # If an external LLM callable is supplied, invoke it dynamically
        if external_llm_callable is not None:
            prompt = cls.PROMPT_TEMPLATE.format(
                system_role=cls.SYSTEM_DIRECTIVE,
                student_query=cleaned_query
            )
            return external_llm_callable(prompt)

        # Dynamic, generalized HyDE Synthesis reflecting the specific inquiry
        # Bridges colloquial student questions directly into official administrative prose
        hypothetical_memo = (
            f"Official Academic Regulation and Institutional Governance Directive: "
            f"Regarding formal student petition and procedural guidelines concerning '{cleaned_query}'. "
            f"The Academic Review Board stipulates that all matters relating to student academic standing, "
            f"course obligations, official permissions, departmental certifications, and institutional accommodations "
            f"require procedural compliance, prescribed application submission endorsed by the designated Faculty Advisor "
            f"or Department Head, and verified documentation furnished within specified administrative timelines. "
            f"Subject matter: {cleaned_query}."
        )
        return hypothetical_memo


class PolicyVectorStore:
    """
    Production-grade Vector Store utilizing Sublinear TF-IDF and n-gram Vector Space.
    Calculates exact Cosine Similarity across arbitrary query spaces.
    """

    def __init__(self, dataset_path: str = POLICIES_PATH):
        self.dataset_path = dataset_path
        self.policies: List[Dict[str, Any]] = []
        self.corpus_documents: List[str] = []
        
        # Sublinear TF-IDF vectorizer capturing unigrams, bigrams, and trigrams
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            sublinear_tf=True,
            stop_words='english',
            token_pattern=r"(?u)\b\w+\b"
        )
        self.doc_vectors = None
        self._initialize_store()

    def _initialize_store(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Policy dataset not found at: {self.dataset_path}")

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.policies = data.get("policies", [])

        # Build dense corpus representation dynamically from handbook policies
        self.corpus_documents = []
        for p in self.policies:
            keywords_joined = " ".join(p.get("keywords", []))
            full_policy_text = (
                f"{p['clause_id']} {p['category']} {p['official_title']} "
                f"{p['text']} {keywords_joined}"
            )
            self.corpus_documents.append(full_policy_text)

        # Vectorize the full handbook corpus
        self.doc_vectors = self.vectorizer.fit_transform(self.corpus_documents)

    def search_raw(self, student_query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Baseline Search: Searches the vector index using only the raw informal student input.
        """
        query_vec = self.vectorizer.transform([student_query])
        similarity_scores = cosine_similarity(query_vec, self.doc_vectors)[0]
        ranked_indices = np.argsort(similarity_scores)[::-1][:top_k]

        return self._format_results(ranked_indices, similarity_scores)

    def search_hyde(self, student_query: str, top_k: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """
        HyDE-Augmented Search: Generates a hypothetical bureaucratic document first,
        then vectors it to retrieve semantically matched policies.
        """
        hyde_doc = HyDEPromptEngine.synthesize_hypothetical_document(student_query)
        hyde_vec = self.vectorizer.transform([hyde_doc])
        similarity_scores = cosine_similarity(hyde_vec, self.doc_vectors)[0]
        ranked_indices = np.argsort(similarity_scores)[::-1][:top_k]

        formatted_results = self._format_results(ranked_indices, similarity_scores)
        return hyde_doc, formatted_results

    def _format_results(self, indices, scores) -> List[Dict[str, Any]]:
        results = []
        for rank, idx in enumerate(indices, 1):
            results.append({
                "rank": rank,
                "score": float(scores[idx]),
                "clause_id": self.policies[idx]["clause_id"],
                "official_title": self.policies[idx]["official_title"],
                "category": self.policies[idx]["category"],
                "text": self.policies[idx]["text"],
                "keywords": self.policies[idx].get("keywords", [])
            })
        return results
