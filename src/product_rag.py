"""
ProductKnowledgeRAG: Semantic retrieval over product specifications and API catalogs.
Package: sovereign-sales-agent-rag (PKG-022)
Author: Russell Alan Powers
"""

import re
import math
from typing import Dict, Any, List, Tuple

class ProductKnowledgeRAG:
    """Self-contained semantic retrieval engine with TF-IDF vector indexing over product specs."""

    DEFAULT_KNOWLEDGE_BASE = [
        {
            "doc_id": "DOC-SBB-01",
            "title": "Sovereign Mainframe and Protocol Engine",
            "category": "Core Platform & FSM",
            "content": "Sovereign Mainframe provides SQLite Merkle-chain append-only event journals, multi-session protocol state machines, and decentralized peer-to-peer agent mailboxes with zero external message broker dependencies. Supports RPG simulation loops and dynamic DAG intent classification."
        },
        {
            "doc_id": "DOC-SBB-02",
            "title": "Raspberry Pi Edge Telemetry Daemon",
            "category": "Edge Computing & IoT",
            "content": "Low-overhead daemon reading Linux sysfs thermal zones, CPU frequency, and memory usage. Integrates I2C hardware sensors, kinematic trajectory gesture detection, and automated crash dump bundling with SHA-256 integrity verification."
        },
        {
            "doc_id": "DOC-SBB-03",
            "title": "Native Apple Swift Ecosystem Suite",
            "category": "Mobile & Native UI",
            "content": "Generates production-ready SwiftUI components across 10 view types including Swift Charts. Provides offline-first SwiftData delta sync with deterministic conflict resolution and APNs push notification dispatching."
        },
        {
            "doc_id": "DOC-SBB-04",
            "title": "Real-Time 3D Avatar Agents",
            "category": "3D Graphics & Audio AI",
            "content": "Three.js WebGL 3D avatar rendering with real-time lip-sync, TalkingHead viseme generation, and FastAudio synchronization for interactive customer experience and autonomous SRE remediation."
        },
        {
            "doc_id": "DOC-SBB-05",
            "title": "Enterprise Security & Zero-Trust Auth",
            "category": "Security & Compliance",
            "content": "All Sovereign microservices enforce strict X-SBB-Auth shared-secret token validation. Every execution emits deterministic SHA-256 idempotency tokens preventing replay attacks and duplicate executions across n8n distributed networks."
        },
        {
            "doc_id": "DOC-SBB-06",
            "title": "Licensing, Pricing & Deployment Economics",
            "category": "Commercial & Pricing",
            "content": "Sovereign Biz Box packages are licensed under 100% perpetual sovereignty models. Eliminates recurring third-party SaaS per-seat licenses. Deployable on self-hosted bare-metal, private AWS VPCs, or edge Raspberry Pi clusters."
        }
    ]

    def __init__(self, corpus: List[Dict[str, str]] = None):
        self.corpus = corpus or self.DEFAULT_KNOWLEDGE_BASE
        self.vocab = {}
        self.doc_vectors = []
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        # Split on non-alphanumeric characters and lowercase
        return [w for w in re.findall(r"[a-zA-Z0-9_-]{2,}", text.lower())]

    def _build_index(self):
        doc_freq = {}
        tokenized_docs = []

        for doc in self.corpus:
            tokens = self._tokenize(doc["title"] + " " + doc["content"])
            tokenized_docs.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self.vocab = {t: idx for idx, t in enumerate(sorted(doc_freq.keys()))}
        n_docs = len(self.corpus)

        for tokens in tokenized_docs:
            vec = [0.0] * len(self.vocab)
            t_counts = {}
            for t in tokens:
                t_counts[t] = t_counts.get(t, 0) + 1
            for t, count in t_counts.items():
                if t in self.vocab:
                    tf = count / len(tokens)
                    idf = math.log((1 + n_docs) / (1 + doc_freq[t])) + 1.0
                    vec[self.vocab[t]] = tf * idf
            # Normalize vector
            norm = math.sqrt(sum(x * x for x in vec))
            if norm > 0:
                vec = [x / norm for x in vec]
            self.doc_vectors.append(vec)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q_tokens = self._tokenize(query)
        q_vec = [0.0] * len(self.vocab)
        q_counts = {}
        for t in q_tokens:
            q_counts[t] = q_counts.get(t, 0) + 1
        for t, count in q_counts.items():
            if t in self.vocab:
                q_vec[self.vocab[t]] = count / max(1, len(q_tokens))
        
        q_norm = math.sqrt(sum(x * x for x in q_vec))
        if q_norm > 0:
            q_vec = [x / q_norm for x in q_vec]

        scores = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            dot_product = sum(a * b for a, b in zip(q_vec, doc_vec))
            scores.append((dot_product, idx))

        scores.sort(reverse=True, key=lambda x: x[0])

        results = []
        for score, idx in scores[:top_k]:
            doc = self.corpus[idx]
            results.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "category": doc["category"],
                "similarity_score": round(float(score), 4),
                "snippet": doc["content"][:200] + ("..." if len(doc["content"]) > 200 else "")
            })
        return results