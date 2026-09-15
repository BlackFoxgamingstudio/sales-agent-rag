"""
ObjectionHandler: Automated sales objection classification and strategic response generator.
Package: sovereign-sales-agent-rag (PKG-022)
Author: Russell Alan Powers
"""

import re
from typing import Dict, Any, List

class ObjectionHandler:
    """Classifies customer hesitation/objections and provides authoritative value rebuttals."""

    OBJECTION_PLAYBOOKS = {
        "PRICING_BUDGET": {
            "keywords": [r"cost", r"expensive", r"budget", r"afford", r"cheap", r"pricey"],
            "classification": "Budget & Cost Justification",
            "counter_strategy": "Demonstrate 10-year Total Cost of Ownership (TCO) savings by eliminating SaaS seat subscriptions.",
            "talking_points": [
                "SBB packages provide perpetual sovereignty with zero per-seat monthly subscription tax.",
                "Typical enterprise deployments pay for themselves within 90 days of replacing third-party API tiers.",
                "Flexible deployment on local edge hardware or private clouds eliminates variable egress fees."
            ]
        },
        "SECURITY_COMPLIANCE": {
            "keywords": [r"security", r"cloud", r"compliance", r"leak", r"privacy", r"hipaa", r"soc2", r"data"],
            "classification": "Security & Data Sovereignty",
            "counter_strategy": "Highlight zero external cloud telemetry, self-hosted Merkle audit trails, and strict X-SBB-Auth.",
            "talking_points": [
                "Customer data never leaves your infrastructure; 100% self-hosted on bare-metal or private VPC.",
                "Every execution generates deterministic SHA-256 cryptographic audit tokens in immutable SQLite ledgers.",
                "Zero-trust API header isolation prevents unauthenticated sidecar invocations."
            ]
        },
        "TIME_IMPLEMENTATION": {
            "keywords": [r"time", r"slow", r"months", r"bandwidth", r"busy", r"resources", r"onboard"],
            "classification": "Deployment Velocity & Engineering Bandwidth",
            "counter_strategy": "Showcase pre-built Docker containers, n8n custom drag-and-drop nodes, and zero external dependencies.",
            "talking_points": [
                "Turnkey deployment via Docker and pre-registered n8n workflow canvas nodes in under 15 minutes.",
                "Zero external database or cloud queue dependencies—operates instantly on local standard library.",
                "Comprehensive SOPs, OpenAPI 3.1 Swagger endpoints, and pre-packaged test suites ensure rapid verification."
            ]
        },
        "COMPETITOR_INCUMBENT": {
            "keywords": [r"competitor", r"alternative", r"zapier", r"workato", r"salesforce", r"hubspot", r"servicetitan"],
            "classification": "Incumbent Platform Comparison",
            "counter_strategy": "Position as an autonomous sovereign bridge that complements or liberates from walled-garden lock-in.",
            "talking_points": [
                "Sovereign microservices integrate directly into existing tools while granting complete IP ownership.",
                "No vendor lock-in, arbitrary rate-limiting, or forced version upgrades.",
                "Direct bidirectional synchronization with ServiceTitan, CRM, and bespoke ERP databases."
            ]
        }
    }

    def classify_and_resolve(self, objection_text: str) -> Dict[str, Any]:
        text_lower = objection_text.lower()
        matched_category = "GENERAL_UNCERTAINTY"
        playbook = None

        for cat, data in self.OBJECTION_PLAYBOOKS.items():
            if any(re.search(kw, text_lower) for kw in data["keywords"]):
                matched_category = cat
                playbook = data
                break

        if not playbook:
            return {
                "category": "GENERAL_HESITATION",
                "confidence": 0.50,
                "response": "We understand enterprise transitions require rigorous validation. We recommend running our automated test suite and staging our pre-built n8n workflow to observe deterministic latency firsthand.",
                "recommended_next_step": "Schedule a 15-minute live technical walkthrough or inspect the open-source repository."
            }

        return {
            "category": matched_category,
            "classification": playbook["classification"],
            "confidence": 0.92,
            "counter_strategy": playbook["counter_strategy"],
            "talking_points": playbook["talking_points"],
            "recommended_next_step": "Offer custom ROI calculation or self-hosted technical sandbox trial."
        }