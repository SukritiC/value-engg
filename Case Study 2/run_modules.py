from modules import (
    DispatchWorkflowModule,
    MassNotificationModule,
    OutageDiagnosticAssistant,
    OutageDetectionModule,
    TechnicianKnowledgeModule,
)


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
