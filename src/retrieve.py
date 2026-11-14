"""
Dell Hackathon 2026 - Problem Statement 1
Module: src/retrieve.py
Implements Multi-Mode Retrieval:
1. Raw Query Retrieval (Baseline)
2. Single-Hypothesis HyDE Retrieval
3. Multi-Hypothesis HyDE Retrieval with Reciprocal Rank Fusion (RRF)
"""

import os
import pickle
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from hyde import HyDEEngine

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INDEX_PATH = os.path.join(DATA_DIR, "vector_index.pkl")


class PolicyRetriever:
    """
    Multi-Mode Semantic Policy Retriever supporting Raw, HyDE, and Multi-Hypothesis RRF.
    """

    def __init__(self, index_path: str = INDEX_PATH):
        self.index_path = index_path
        self.sections = []
        self.vectorizer = None
        self.doc_vectors = None
        self.hyde_engine = HyDEEngine()
        self._load_index()

    def _load_index(self):
        if not os.path.exists(self.index_path):
            from ingest import build_and_persist_index
            payload = build_and_persist_index()
        else:
            with open(self.index_path, "rb") as f:
                payload = pickle.load(f)

        self.sections = payload["sections"]
        self.vectorizer = payload["vectorizer"]
        self.doc_vectors = payload["doc_vectors"]

    def retrieve_raw(self, student_query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Baseline Search: Directly searches using the raw, informal query."""
        query_vec = self.vectorizer.transform([student_query])
        similarities = cosine_similarity(query_vec, self.doc_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return self._format_results(top_indices, similarities)

    def retrieve_hyde(self, student_query: str, top_k: int = 3) -> Tuple[str, List[Dict[str, Any]], bool]:
        """Single HyDE Retrieval: Synthesizes a formal hypothetical paragraph, then retrieves."""
        hyde_text, used = self.hyde_engine.generate_single_hyde(student_query)
        hyde_vec = self.vectorizer.transform([hyde_text])
        similarities = cosine_similarity(hyde_vec, self.doc_vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]

        return hyde_text, self._format_results(top_indices, similarities), used

    def retrieve_multi_hyde(self, student_query: str, top_k: int = 3) -> Tuple[List[str], List[Dict[str, Any]], bool]:
        """
        Multi-Hypothesis HyDE Retrieval:
        Generates 3 diverse formal interpretations, retrieves candidates for each,
        and fuses rankings via Reciprocal Rank Fusion (RRF).
        """
        hypotheses, used = self.hyde_engine.generate_multi_hypothesis(student_query)
        rrf_scores: Dict[int, float] = {}
        max_cosines: Dict[int, float] = {}

        for h_text in hypotheses:
            h_vec = self.vectorizer.transform([h_text])
            sims = cosine_similarity(h_vec, self.doc_vectors)[0]
            # Rank all candidates for this hypothesis
            ranked_idx = np.argsort(sims)[::-1][:10]
            
            # Accumulate RRF score: 1 / (60 + rank)
            for rank_pos, idx in enumerate(ranked_idx, 1):
                rrf_scores[idx] = rrf_scores.get(idx, 0.0) + (1.0 / (60.0 + rank_pos))
                max_cosines[idx] = max(max_cosines.get(idx, 0.0), float(sims[idx]))

        # Sort combined documents by aggregated RRF score
        sorted_indices = sorted(rrf_scores.keys(), key=lambda i: rrf_scores[i], reverse=True)[:top_k]
        
        # Format results with normalized RRF score
        max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0
        results = []
        for rank, idx in enumerate(sorted_indices, 1):
            normalized_score = float(rrf_scores[idx] / max_rrf)
            sec = self.sections[idx]
            results.append({
                "rank": rank,
                "score": round(normalized_score, 4),
                "cosine_similarity": round(max_cosines.get(idx, 0.0), 4),
                "section_id": sec["section_id"],
                "title": sec["title"],
                "category": sec["category"],
                "text": sec["text"],
                "source": sec["source"]
            })
        return hypotheses, results, used

    def _format_results(self, indices, scores) -> List[Dict[str, Any]]:
        results = []
        for rank, idx in enumerate(indices, 1):
            sec = self.sections[idx]
            results.append({
                "rank": rank,
                "score": round(float(scores[idx]), 4),
                "cosine_similarity": round(float(scores[idx]), 4),
                "section_id": sec["section_id"],
                "title": sec["title"],
                "category": sec["category"],
                "text": sec["text"],
                "source": sec["source"]
            })
        return results


if __name__ == "__main__":
    retriever = PolicyRetriever()
    test_q = "My band has a gig next Friday, can I skip my lab and make it up later?"
    print("=" * 80)
    print(f"MULTI-MODE RETRIEVAL TEST FOR: \"{test_q}\"")
    print("=" * 80)

    # 1. Raw Baseline
    raw_res = retriever.retrieve_raw(test_q, top_k=2)
    print("\n[1] RAW QUERY RETRIEVAL:")
    for r in raw_res:
        print(f"  Rank {r['rank']} | Score: {r['score']} | Section {r['section_id']}: {r['title']}")

    # 2. Single HyDE
    h_text, hyde_res, _ = retriever.retrieve_hyde(test_q, top_k=2)
    print("\n[2] SINGLE HyDE RETRIEVAL:")
    for r in hyde_res:
        print(f"  Rank {r['rank']} | Score: {r['score']} | Section {r['section_id']}: {r['title']}")

    # 3. Multi-Hypothesis HyDE (RRF)
    multi_h, multi_res, _ = retriever.retrieve_multi_hyde(test_q, top_k=2)
    print(f"\n[3] MULTI-HYPOTHESIS HyDE (Fused {len(multi_h)} hypotheses):")
    for r in multi_res:
        print(f"  Rank {r['rank']} | RRF Score: {r['score']} | Section {r['section_id']}: {r['title']}")

