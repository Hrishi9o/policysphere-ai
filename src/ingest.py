"""
Dell Hackathon 2026 - Problem Statement 1
Module: src/ingest.py
Chunks official university handbook (data/handbook.md) by Section ID and builds persistent vector index.
Explicitly asserts and guarantees that data/fake_policy.md is NEVER ingested.
"""

import os
import re
import pickle
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HANDBOOK_PATH = os.path.join(DATA_DIR, "handbook.md")
FAKE_POLICY_PATH = os.path.join(DATA_DIR, "fake_policy.md")
INDEX_PATH = os.path.join(DATA_DIR, "vector_index.pkl")


def load_and_verify_sources():
    """Verifies that handbook exists and checks fake policy is isolated."""
    if not os.path.exists(HANDBOOK_PATH):
        raise FileNotFoundError(f"Official handbook not found at: {HANDBOOK_PATH}")
    
    fake_texts = []
    if os.path.exists(FAKE_POLICY_PATH):
        with open(FAKE_POLICY_PATH, "r", encoding="utf-8") as f:
            fake_texts = [line.strip().lower() for line in f if len(line.strip()) > 20]
    return fake_texts


def parse_handbook_sections(handbook_text: str, fake_text_samples: List[str]) -> List[Dict[str, Any]]:
    """
    Parses handbook.md into discrete sections by section ID (e.g., 1.1.0, 2.1.0).
    Enforces strict assertion preventing any planted fake policy ingestion.
    """
    sections = []
    current_category = "General Regulations"
    
    # Split text into lines
    lines = handbook_text.split("\n")
    current_section = None
    buffer = []

    for line in lines:
        line_clean = line.strip()
        
        # Track category headers (### SECTION X: ...)
        if line_clean.startswith("### SECTION"):
            current_category = line_clean.replace("###", "").strip()
            continue

        # Detect section headers (#### X.X.X Title)
        header_match = re.match(r"^####\s+(\d+\.\d+\.\d+)\s+(.+)$", line_clean)
        if header_match:
            # Save previous section if exists
            if current_section and buffer:
                section_text = " ".join(buffer).strip()
                # Strict assertion: Never ingest fake policy text
                for fake in fake_text_samples:
                    assert fake not in section_text.lower(), f"CRITICAL SECURITY ALERT: Fake policy leaked into ingestion: {fake[:40]}"
                
                current_section["text"] = section_text
                current_section["content"] = f"{current_section['section_id']} {current_section['title']} {current_category} {section_text}"
                sections.append(current_section)
                buffer = []

            sec_id = header_match.group(1)
            title = header_match.group(2)
            current_section = {
                "section_id": sec_id,
                "title": title,
                "category": current_category,
                "source": "data/handbook.md (VERIFIED OFFICIAL)"
            }
        elif current_section:
            if line_clean and not line_clean.startswith("#"):
                buffer.append(line_clean)

    # Save last section
    if current_section and buffer:
        section_text = " ".join(buffer).strip()
        for fake in fake_text_samples:
            assert fake not in section_text.lower(), f"CRITICAL SECURITY ALERT: Fake policy leaked into ingestion: {fake[:40]}"
        current_section["text"] = section_text
        current_section["content"] = f"{current_section['section_id']} {current_section['title']} {current_category} {section_text}"
        sections.append(current_section)

    return sections


def build_and_persist_index():
    """Ingests handbook, extracts sections, fits vectorizer, and persists index."""
    fake_samples = load_and_verify_sources()
    
    with open(HANDBOOK_PATH, "r", encoding="utf-8") as f:
        handbook_content = f.read()

    sections = parse_handbook_sections(handbook_content, fake_samples)
    print(f"✅ Ingestion Verified: Parsed {len(sections)} official handbook sections.")
    assert len(sections) >= 20, f"Expected at least 20 sections, found {len(sections)}"

    # Fit persistent sublinear TF-IDF trigram vectorizer
    corpus = [s["content"] for s in sections]
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        sublinear_tf=True,
        stop_words='english',
        token_pattern=r"(?u)\b\w+\b"
    )
    doc_vectors = vectorizer.fit_transform(corpus)

    index_payload = {
        "sections": sections,
        "vectorizer": vectorizer,
        "doc_vectors": doc_vectors
    }

    with open(INDEX_PATH, "wb") as f:
        pickle.dump(index_payload, f)
    
    print(f"💾 Vector Index successfully persisted to: {INDEX_PATH}")
    return index_payload


if __name__ == "__main__":
    build_and_persist_index()

