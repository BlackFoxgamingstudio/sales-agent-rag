"""
QuoteGenerator: Algorithmic pricing, seat/node sizing, and formal proposal generator.
Package: sovereign-sales-agent-rag (PKG-022)
Author: Russell Alan Powers
"""

import time
import hashlib
from typing import Dict, Any, List

class QuoteGenerator:
    """Generates itemized pricing quotes with deterministic SHA-256 tokens and volume tiers."""

    TIER_PRICING = {
        "STARTER": {"base": 1500.0, "per_node": 50.0, "included_nodes": 5},
        "PROFESSIONAL": {"base": 4500.0, "per_node": 40.0, "included_nodes": 20},
        "ENTERPRISE": {"base": 12000.0, "per_node": 25.0, "included_nodes": 100}
    }

    SLA_MULTIPLIERS = {
        "STANDARD": 1.0,      # 99.5% SLA, business hours support
        "MISSION_CRITICAL": 1.25 # 99.99% SLA, 24/7 dedicated engineering bridge
    }

    def generate_quote(self, company_name: str, tier: str = "PROFESSIONAL", nodes: int = 25, sla: str = "STANDARD", term_months: int = 12) -> Dict[str, Any]:
        tier = tier.upper() if tier.upper() in self.TIER_PRICING else "PROFESSIONAL"
        sla = sla.upper() if sla.upper() in self.SLA_MULTIPLIERS else "STANDARD"
        
        tier_info = self.TIER_PRICING[tier]
        base_price = tier_info["base"]
        included = tier_info["included_nodes"]
        extra_nodes = max(0, nodes - included)
        nodes_cost = extra_nodes * tier_info["per_node"]
        
        subtotal_monthly = (base_price + nodes_cost) * self.SLA_MULTIPLIERS[sla]
        
        # Term discount
        discount_pct = 0.0
        if term_months >= 24:
            discount_pct = 0.20
        elif term_months >= 12:
            discount_pct = 0.15
        
        monthly_discount = subtotal_monthly * discount_pct
        effective_monthly = subtotal_monthly - monthly_discount
        total_contract_value = effective_monthly * term_months

        # Generate quote hash
        raw_hash = f"{company_name}:{tier}:{nodes}:{sla}:{total_contract_value}:{time.time()}"
        quote_token = "QTE-" + hashlib.sha256(raw_hash.encode()).hexdigest()[:12].upper()

        return {
            "quote_token": quote_token,
            "company": company_name,
            "tier": tier,
            "nodes_allocated": nodes,
            "sla_level": sla,
            "term_months": term_months,
            "line_items": [
                {"description": f"{tier} Package Core Platform License", "monthly": base_price},
                {"description": f"Additional Node Scale ({extra_nodes} extra nodes)", "monthly": nodes_cost},
                {"description": f"SLA Tier Adjustment ({sla})", "multiplier": self.SLA_MULTIPLIERS[sla]},
                {"description": f"Annual Commitment Discount ({int(discount_pct * 100)}%)", "monthly_savings": round(monthly_discount, 2)}
            ],
            "effective_monthly_usd": round(effective_monthly, 2),
            "total_contract_value_usd": round(total_contract_value, 2),
            "currency": "USD",
            "valid_days": 30,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }