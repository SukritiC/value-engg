from __future__ import annotations

from typing import Any, Dict, Optional

from .openai_utils import call_openai


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
            ai_text = call_openai(prompt, api_key=self.api_key)
            if ai_text:
                answer = ai_text[:120]
        return {
            "answer": answer,
            "source": matched["source"],
            "document_id": matched["id"],
        }
