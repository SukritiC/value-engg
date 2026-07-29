from __future__ import annotations

from typing import Any, Dict, Optional

from .openai_utils import call_openai


class MassNotificationModule:
    """Multi-agent style incident notification orchestrator with enforced escalation and optional OpenAI drafting."""

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None) -> None:
        self.use_openai = use_openai
        self.api_key = api_key
        self.escalation_thresholds = {
            "customer_count": 10000,
            "critical_severity": True,
            "min_confidence": 0.5,
        }

    def run_notification(self, incident: Dict[str, Any]) -> Dict[str, Any]:
        escalated = (
            incident.get("affected_customers", 0) >= self.escalation_thresholds["customer_count"]
            or (
                incident.get("severity") == "critical"
                and incident.get("confidence", 0.0) < self.escalation_thresholds["min_confidence"]
            )
        )
        message = (
            "Customer notification drafted: We are investigating a major outage and will share updates as soon as they are confirmed."
        )
        if self.use_openai:
            prompt = (
                "You are a customer communication assistant. Draft a concise outage update for affected customers. "
                f"Incident: {incident}"
            )
            ai_text = call_openai(prompt, api_key=self.api_key)
            if ai_text:
                message = ai_text[:220]
        return {
            "incident_id": incident.get("incident_id"),
            "message": message,
            "escalated": escalated,
            "status": "escalated" if escalated else "notified",
        }
