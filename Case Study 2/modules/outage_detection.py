from __future__ import annotations

from typing import Any, Dict, Optional

from .openai_utils import call_openai


class OutageDetectionModule:
    """Outage detector with optional OpenAI augmentation."""

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None) -> None:
        self.sample_data = {
            "sensor_threshold": 85,
            "current_value": 92,
            "region": "North",
            "service": "4G",
        }
        self.use_openai = use_openai
        self.api_key = api_key

    def detect_outage(self) -> Dict[str, Any]:
        result = {
            "outage_detected": self.sample_data["current_value"] >= self.sample_data["sensor_threshold"],
            "severity": "critical" if self.sample_data["current_value"] >= self.sample_data["sensor_threshold"] else "normal",
            "region": self.sample_data["region"],
            "service": self.sample_data["service"],
            "message": "Threshold breach detected; outage declared." if self.sample_data["current_value"] >= self.sample_data["sensor_threshold"] else "No outage detected.",
        }
        if self.use_openai:
            prompt = (
                "You are a telecom operations assistant. Determine whether this outage should be declared. "
                f"Sensor threshold: {self.sample_data['sensor_threshold']}; current value: {self.sample_data['current_value']}."
            )
            ai_text = call_openai(prompt, api_key=self.api_key)
            if ai_text:
                result["ai_summary"] = ai_text[:180]
        return result
