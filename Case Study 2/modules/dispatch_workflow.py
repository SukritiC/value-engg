from __future__ import annotations

from typing import Any, Dict, Optional

from .openai_utils import call_openai


class DispatchWorkflowModule:
    """Fixed workflow dispatch assignment with deterministic rules and optional AI ranking."""

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None) -> None:
        self.use_openai = use_openai
        self.api_key = api_key
        self.technicians = [
            {"name": "Ava Patel", "skill": "wireless", "location": "South Sector", "available": False},
            {"name": "Mina Singh", "skill": "fiber", "location": "North Sector", "available": True},
            {"name": "Luis Gomez", "skill": "fiber", "location": "West Sector", "available": True},
        ]

    def assign_technician(self, outage: Dict[str, Any]) -> Dict[str, Any]:
        eligible = [t for t in self.technicians if t["available"] and t["skill"] == outage["required_skill"]]
        if not eligible:
            return {"assigned_technician": None, "status": "unassigned", "reason": "No eligible technician"}
        ranked = sorted(
            eligible,
            key=lambda t: (
                0 if t["location"] == outage["location"] else 1,
                0 if outage.get("priority") == "high" else 1,
            ),
        )
        chosen = ranked[0]
        result = {
            "assigned_technician": chosen["name"],
            "status": "assigned",
            "location": chosen["location"],
            "skill": chosen["skill"],
        }
        if self.use_openai:
            prompt = (
                "You are a dispatch assistant. Recommend the best technician for this outage based on skill and location. "
                f"Outage: {outage}"
            )
            ai_text = call_openai(prompt, api_key=self.api_key)
            if ai_text:
                result["ai_rationale"] = ai_text[:180]
        return result
