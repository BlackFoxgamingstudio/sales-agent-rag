#!/usr/bin/env python3
"""
Unit & Integration Test Suite for sovereign-sales-agent-rag (PKG-022)
Tests all 5 production domain components with zero external dependencies.
"""
import sys
import unittest
from pathlib import Path

SOLUTION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOLUTION_ROOT))

from src.core import CoreEngine
from src.conversation import ConversationEngine
from src.product_rag import ProductKnowledgeRAG
from src.objection_handler import ObjectionHandler
from src.quote_generator import QuoteGenerator
from src.crm_syncer import CRMSyncer

class TestSalesAgentRAG(unittest.TestCase):
    def setUp(self):
        self.engine = CoreEngine()

    def test_01_health_check_and_metrics(self):
        health = self.engine.health_check()
        self.assertEqual(health["status"], "HEALTHY")
        self.assertEqual(health["service"], "sovereign-sales-agent-rag")
        self.assertGreaterEqual(health["indexed_rag_documents"], 5)

    def test_02_conversation_intent_classification(self):
        res = self.engine.execute_feature("conversation_turn", {
            "session_id": "test_sess_01",
            "message": "What is the pricing for enterprise deployments?",
            "metadata": {"company": "Acme Corp", "budget": "k"}
        })
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"]["detected_intent"], "PRICING_REQUEST")
        self.assertEqual(res["result"]["entities"]["company"], "Acme Corp")

    def test_03_product_rag_semantic_search(self):
        res = self.engine.execute_feature("query_product_knowledge", {
            "query": "thermal zones and raspberry pi hardware",
            "top_k": 2
        })
        self.assertEqual(res["status"], "SUCCESS")
        matches = res["result"]["results"]
        self.assertGreaterEqual(len(matches), 1)
        self.assertIn("Raspberry Pi", matches[0]["title"])
        self.assertGreater(matches[0]["similarity_score"], 0.0)

    def test_04_objection_handling_classification(self):
        res = self.engine.execute_feature("handle_objection", {
            "objection": "This seems too expensive compared to standard SaaS solutions."
        })
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["result"]["category"], "PRICING_BUDGET")
        self.assertGreaterEqual(len(res["result"]["talking_points"]), 2)
        self.assertIn("sovereignty", res["result"]["talking_points"][0].lower())

    def test_05_quote_generation_calculation(self):
        res = self.engine.execute_feature("generate_quote", {
            "company": "Vanguard Logistics",
            "tier": "ENTERPRISE",
            "nodes": 150,
            "sla": "MISSION_CRITICAL",
            "term_months": 12
        })
        self.assertEqual(res["status"], "SUCCESS")
        quote = res["result"]
        self.assertEqual(quote["tier"], "ENTERPRISE")
        self.assertEqual(quote["nodes_allocated"], 150)
        self.assertIn("QTE-", quote["quote_token"])
        self.assertGreater(quote["total_contract_value_usd"], 0.0)

    def test_06_lead_qualification_and_crm_sync(self):
        res = self.engine.execute_feature("qualify_sales_lead", {
            "company": "Apex Defense Labs",
            "email": "chief@apexlabs.mil",
            "budget": "k approved budget",
            "authority": "CTO and Vice President of Infrastructure",
            "need": "Urgent self-hosted mission-critical telemetry broker",
            "timeline": "Immediate rollout this month",
            "estimated_deal_size": 75000.0
        })
        self.assertEqual(res["status"], "SUCCESS")
        lead = res["result"]
        self.assertEqual(lead["company_name"], "Apex Defense Labs")
        self.assertEqual(lead["bant_score"], 100)
        self.assertEqual(lead["stage"], "QUALIFIED")
        self.assertTrue(lead["is_qualified"])

    def test_07_pipeline_aggregation(self):
        res = self.engine.execute_feature("get_pipeline_summary", {})
        self.assertEqual(res["status"], "SUCCESS")
        pipeline = res["result"]
        self.assertGreaterEqual(pipeline["total_leads"], 1)
        self.assertGreaterEqual(pipeline["total_pipeline_value_usd"], 25000.0)

    def test_08_deterministic_idempotency(self):
        p = {"company": "Test Inc", "nodes": 10}
        r1 = self.engine.execute_feature("generate_quote", p)
        r2 = self.engine.execute_feature("generate_quote", p)
        self.assertEqual(r1["idempotency_token"], r2["idempotency_token"])

if __name__ == "__main__":
    unittest.main(verbosity=2)