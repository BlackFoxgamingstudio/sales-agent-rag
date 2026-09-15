"""
CRMSyncer: SQLite-backed CRM lead qualification ledger and BANT scoring engine.
Package: sovereign-sales-agent-rag (PKG-022)
Author: Russell Alan Powers
"""

import os
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

class CRMSyncer:
    """Manages persistent lead records, BANT qualification metrics, and pipeline status."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            data_dir = Path(__file__).resolve().parent.parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = str(data_dir / "sales_crm.db")
        else:
            self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                lead_id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                contact_email TEXT,
                budget_status TEXT,
                authority_status TEXT,
                need_status TEXT,
                timeline_status TEXT,
                bant_score INTEGER DEFAULT 0,
                stage TEXT DEFAULT 'PROSPECT',
                estimated_deal_size REAL DEFAULT 0.0,
                created_at REAL,
                updated_at REAL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS lead_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                details TEXT,
                timestamp REAL,
                FOREIGN KEY(lead_id) REFERENCES leads(lead_id)
            );
        """)
        conn.commit()
        conn.close()

    def evaluate_bant_score(self, budget: str, authority: str, need: str, timeline: str) -> int:
        score = 0
        if budget and any(w in budget.lower() for w in ["yes", "approved", "k", "k", "allocated", "available", "have budget"]):
            score += 25
        elif budget and any(w in budget.lower() for w in ["exploring", "flexible", "tbd"]):
            score += 15

        if authority and any(w in authority.lower() for w in ["yes", "decision maker", "vp", "cto", "ceo", "director", "owner"]):
            score += 25
        elif authority and any(w in authority.lower() for w in ["evaluator", "influencer", "team"]):
            score += 15

        if need and any(w in need.lower() for w in ["urgent", "critical", "replacing", "high priority", "enterprise", "pain point"]):
            score += 25
        elif need:
            score += 15

        if timeline and any(w in timeline.lower() for w in ["immediate", "q1", "q2", "q3", "q4", "this month", "30 days", "90 days"]):
            score += 25
        elif timeline:
            score += 10

        return min(100, score)

    def upsert_lead(self, lead_id: str, company_name: str, contact_email: str = "",
                    budget: str = "", authority: str = "", need: str = "",
                    timeline: str = "", estimated_deal_size: float = 25000.0) -> Dict[str, Any]:
        bant_score = self.evaluate_bant_score(budget, authority, need, timeline)
        
        # Stage auto-promotion
        stage = "PROSPECT"
        if bant_score >= 75:
            stage = "QUALIFIED"
        elif bant_score >= 50:
            stage = "DISCOVERY"

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        now = time.time()
        
        cur.execute("""
            INSERT INTO leads (
                lead_id, company_name, contact_email, budget_status, authority_status,
                need_status, timeline_status, bant_score, stage, estimated_deal_size,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(lead_id) DO UPDATE SET
                company_name=excluded.company_name,
                contact_email=coalesce(nullif(excluded.contact_email, ''), leads.contact_email),
                budget_status=excluded.budget_status,
                authority_status=excluded.authority_status,
                need_status=excluded.need_status,
                timeline_status=excluded.timeline_status,
                bant_score=excluded.bant_score,
                stage=excluded.stage,
                estimated_deal_size=excluded.estimated_deal_size,
                updated_at=excluded.updated_at
        """, (
            lead_id, company_name, contact_email, budget, authority,
            need, timeline, bant_score, stage, estimated_deal_size, now, now
        ))
        
        cur.execute("""
            INSERT INTO lead_interactions (lead_id, interaction_type, details, timestamp)
            VALUES (?, 'BANT_EVALUATION', ?, ?)
        """, (lead_id, f'Score: {bant_score}, Stage: {stage}', now))
        
        conn.commit()
        conn.close()

        return {
            "lead_id": lead_id,
            "company_name": company_name,
            "bant_score": bant_score,
            "stage": stage,
            "estimated_deal_size": estimated_deal_size,
            "is_qualified": bant_score >= 70,
            "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
        }

    def get_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM leads WHERE lead_id = ?", (lead_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_pipeline_summary(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT stage, count(*), sum(estimated_deal_size) FROM leads GROUP BY stage")
        rows = cur.fetchall()
        cur.execute("SELECT count(*), coalesce(sum(estimated_deal_size), 0.0) FROM leads")
        tot_cnt, tot_val = cur.fetchone()
        conn.close()

        stage_breakdown = {r[0]: {"count": r[1], "value": r[2]} for r in rows}
        return {
            "total_leads": tot_cnt,
            "total_pipeline_value_usd": round(float(tot_val), 2),
            "stage_breakdown": stage_breakdown
        }