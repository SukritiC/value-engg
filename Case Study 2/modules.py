from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None


if load_dotenv is not None:
    load_dotenv(Path(__file__).with_name(".env"))

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None


def _call_openai(prompt: str, api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> Optional[str]:
    """Call the OpenAI API when a key is available; otherwise return None."""
    if not api_key and not os.getenv("OPENAI_API_KEY"):
        return None
    if OpenAI is None:
        return None
    try:
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        response = client.responses.create(model=model, input=prompt)
        return getattr(response, "output_text", None) or str(response)
    except Exception:
        return None


@dataclass
class IncidentContext:
    outage_detected: bool = True
    severity: str = "critical"
    region: str = "North"
    service: str = "4G"
    affected_customers: int = 25000
    eta: str = "90 minutes"
    confidence: float = 0.4


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
            ai_text = _call_openai(prompt, api_key=self.api_key)
            if ai_text:
                result["ai_summary"] = ai_text[:180]
        return result


class TechnicianKnowledgeModule:
    """RAG-style retrieval over static procedural knowledge with optional OpenAI assistance."""

    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None) -> None:
        self.use_openai = use_openai
        self.api_key = api_key
        self.documents = [
            {
                "id": "manual-1",
                "title": "Valve Housing Manual",
                "content": "Valve housing torque setting is 15 Nm.",
                "source": "manual",
                "effective_date": "2024-01-01",
            },
            {
                "id": "bulletin-1",
                "title": "Valve Housing Bulletin",
                "content": "For the new valve housing, use 18 Nm torque. The manual section is superseded.",
                "source": "bulletin",
                "effective_date": "2025-02-01",
            },
        ]

    def answer_procedure(self, question: str) -> Dict[str, Any]:
        matched = None
        for doc in self.documents:
            if "torque" in question.lower() and "valve" in question.lower():
                if doc["source"] == "bulletin":
                    matched = doc
                    break
                matched = doc
        if matched is None:
            matched = self.documents[0]
        content = matched["content"]
        if "18 Nm" in content:
            answer = "18 Nm"
        elif "15 Nm" in content:
            answer = "15 Nm"
        else:
            answer = content
        if self.use_openai:
            prompt = (
                "You are a field operations assistant. Answer the technician's procedural question using the best available source. "
                f"Question: {question}"
            )
            ai_text = _call_openai(prompt, api_key=self.api_key)
            if ai_text:
                answer = ai_text[:120]
        return {
            "answer": answer,
            "source": matched["source"],
            "document_id": matched["id"],
        }


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
            ai_text = _call_openai(prompt, api_key=self.api_key)
            if ai_text:
                result["ai_rationale"] = ai_text[:180]
        return result


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
            ai_text = _call_openai(prompt, api_key=self.api_key)
            if ai_text:
                hypothesis = ai_text[:180]
        return {
            "hypothesis": hypothesis,
            "evidence_collected": True,
            "evidence": evidence,
            "state": self.state,
        }


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
            ai_text = _call_openai(prompt, api_key=self.api_key)
            if ai_text:
                message = ai_text[:220]
        return {
            "incident_id": incident.get("incident_id"),
            "message": message,
            "escalated": escalated,
            "status": "escalated" if escalated else "notified",
        }


if __name__ == "__main__":
    print("Running demo for all five modules...\n")

    outage_detector = OutageDetectionModule(use_openai=True)
    print("Module 1 - Outage Detection:")
    print(outage_detector.detect_outage())
    print()

    technician_assistant = TechnicianKnowledgeModule(use_openai=True)
    print("Module 2 - Technician Knowledge:")
    print(technician_assistant.answer_procedure("What torque should I use for the new valve housing?"))
    print()

    dispatcher = DispatchWorkflowModule(use_openai=True)
    print("Module 3 - Dispatch Workflow:")
    print(dispatcher.assign_technician({"required_skill": "fiber", "location": "North Sector", "priority": "high"}))
    print()

    diagnostic_agent = OutageDiagnosticAssistant(use_openai=True)
    print("Module 4 - Diagnostic Assistant:")
    print(diagnostic_agent.run_diagnostic({"region": "North", "weather": "storm", "service": "4G"}))
    print()

    notifier = MassNotificationModule(use_openai=True)
    print("Module 5 - Mass Notification:")
    print(notifier.run_notification({"incident_id": "INC-9001", "affected_customers": 25000, "severity": "critical", "eta": "90 minutes", "confidence": 0.4}))
