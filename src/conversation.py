"""
ConversationEngine: Multi-turn sales dialog context manager and intent classifier.
Package: sovereign-sales-agent-rag (PKG-022)
Author: Russell Alan Powers
"""

import time
import re
from typing import Dict, Any, List, Optional

class ConversationEngine:
    """Manages multi-turn sales dialogues, extracts qualifying entities, and tracks intent."""

    INTENT_KEYWORDS = {
        "PRICING_REQUEST": ["price", "pricing", "cost", "quote", "how much", "budget", "fees", "tier"],
        "OBJECTION": ["too expensive", "not sure", "competitor", "no time", "can't afford", "alternative", "expensive"],
        "TECHNICAL_QUESTION": ["api", "architecture", "endpoint", "performance", "latency", "security", "self-hosted", "spec", "integration"],
        "QUALIFICATION": ["we need", "our company", "we have", "team size", "looking for", "requirements"],
        "CLOSE_REQUEST": ["sign up", "get started", "contract", "purchase", "demo", "schedule", "pilot", "buy"]
    }

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "session_id": session_id,
                "created_at": time.time(),
                "history": [],
                "entities": {
                    "company": None,
                    "budget": None,
                    "authority": None,
                    "need": None,
                    "timeline": None
                },
                "current_intent": "GREETING",
                "turns_count": 0
            }
        return self._sessions[session_id]

    def process_message(self, session_id: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        session = self.get_or_create_session(session_id)
        session["turns_count"] += 1
        metadata = metadata or {}

        # Classify intent
        detected_intent = "GENERAL_INQUIRY"
        msg_lower = message.lower()
        for intent, kws in self.INTENT_KEYWORDS.items():
            if any(kw in msg_lower for kw in kws):
                detected_intent = intent
                break

        session["current_intent"] = detected_intent

        # Entity Extraction
        if "company" in metadata:
            session["entities"]["company"] = metadata["company"]
        if "budget" in metadata:
            session["entities"]["budget"] = metadata["budget"]
        if "timeline" in metadata:
            session["entities"]["timeline"] = metadata["timeline"]
        if "authority" in metadata:
            session["entities"]["authority"] = metadata["authority"]
        if "need" in metadata:
            session["entities"]["need"] = metadata["need"]

        turn_entry = {
            "turn": session["turns_count"],
            "timestamp": time.time(),
            "message": message,
            "intent": detected_intent
        }
        session["history"].append(turn_entry)

        return {
            "session_id": session_id,
            "detected_intent": detected_intent,
            "turns_count": session["turns_count"],
            "entities": session["entities"],
            "status": "ACTIVE"
        }