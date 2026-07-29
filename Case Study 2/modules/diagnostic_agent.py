from __future__ import annotations

from typing import Any, Dict, Optional

from .openai_utils import call_openai


class OutageDiagnosticAssistant:
    """Agentic-style diagnostic assistant with a small tool interface and optional OpenAI summarization."""

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None) -> None:
        self.use_openai = use_openai
        self.api_key = api_key
        self.state: Dict[str, Any] = {}

    def _check_maintenance_history(self, region: str) -> str:
        if region == "North":
            return "Recent maintenance on fiber trunk line 17."
        return "No recent maintenance found."

    def _check_correlated_sensors(self, region: str, service: str) -> str:
        if region == "North" and service == "4G":
            return "Correlated sensor anomalies detected in the northern 4G cluster."
        return "No correlated anomalies."

    def _check_weather_data(self, weather: str) -> str:
        if weather == "storm":
            return "Severe weather is present in the region."
        return "Weather is stable."

    def run_diagnostic(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.state = {
            "region": context.get("region", "North"),
            "service": context.get("service", "4G"),
            "weather": context.get("weather", "clear"),
        }
        evidence = [
            self._check_maintenance_history(self.state["region"]),
            self._check_correlated_sensors(self.state["region"], self.state["service"]),
            self._check_weather_data(self.state["weather"]),
        ]
        hypothesis = "Likely maintenance-related failure with correlated sensor anomalies."
        if self.use_openai:
            prompt = (
                "You are a network operations assistant. Summarize the most likely root cause hypothesis based on evidence. "
                f"Evidence: {evidence}"
            )
            ai_text = call_openai(prompt, api_key=self.api_key)
            if ai_text:
                hypothesis = ai_text[:180]
        return {
            "hypothesis": hypothesis,
            "evidence_collected": True,
            "evidence": evidence,
            "state": self.state,
        }
