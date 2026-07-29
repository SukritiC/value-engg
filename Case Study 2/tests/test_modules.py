import unittest

import modules


class ModuleTests(unittest.TestCase):
    def test_outage_detection_flags_critical_outage(self):
        detector = modules.OutageDetectionModule()
        result = detector.detect_outage()
        self.assertTrue(result["outage_detected"])
        self.assertEqual(result["severity"], "critical")

    def test_technician_knowledge_prefers_bulletin_over_manual(self):
        assistant = modules.TechnicianKnowledgeModule()
        answer = assistant.answer_procedure("What torque should I use for the new valve housing?")
        self.assertIn("bulletin", answer["source"].lower())
        self.assertIn("18 Nm", answer["answer"])

    def test_dispatch_assigns_best_available_technician(self):
        dispatch = modules.DispatchWorkflowModule()
        assignment = dispatch.assign_technician(
            {
                "required_skill": "fiber",
                "location": "North Sector",
                "priority": "high",
            }
        )
        self.assertEqual(assignment["assigned_technician"], "Mina Singh")
        self.assertEqual(assignment["status"], "assigned")

    def test_diagnostic_agent_builds_hypothesis_from_tools(self):
        agent = modules.OutageDiagnosticAssistant()
        report = agent.run_diagnostic({"region": "North", "weather": "storm", "service": "4G"})
        self.assertIn("maintenance", report["hypothesis"].lower())
        self.assertTrue(report["evidence_collected"])

    def test_notification_system_escalates_large_outage(self):
        notifier = modules.MassNotificationModule()
        result = notifier.run_notification(
            {
                "incident_id": "INC-9001",
                "affected_customers": 25000,
                "severity": "critical",
                "eta": "90 minutes",
                "confidence": 0.4,
            }
        )
        self.assertTrue(result["escalated"])
        self.assertIn("customer", result["message"].lower())

    def test_openai_path_falls_back_cleanly_without_key(self):
        detector = modules.OutageDetectionModule(use_openai=True)
        result = detector.detect_outage()
        self.assertIn("outage_detected", result)


if __name__ == "__main__":
    unittest.main()

