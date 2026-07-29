# Executive Summary and Module 1: Outage Detection and Communication Platform

## Executive Summary

The telecom operator’s Network Operations division is modernizing outage detection, diagnosis, field-technician coordination, and customer communication into a connected platform. As the network has grown more complex, outage resolution has become slower and more difficult to manage, while customer trust erodes further when delays are compounded by vague or late communication.

This initiative should be evaluated as a mission-critical operations capability, not as an AI project by default. As with the billing and complaint platform, the CIO has required that each capability be assessed on its own merits. Where a deterministic engineering solution can deliver the required reliability, transparency, and control, it should be preferred over a probabilistic AI approach simply because AI is available.

## Module 1: BMAD Review of Outage Detection

### B — Breakthrough Opportunity

The core problem is not just that outages occur; it is that the organization struggles to detect, diagnose, and communicate them quickly and consistently at scale. Current processes are often fragmented across monitoring tools, incident workflows, and customer communication channels, leading to delayed awareness, slower response, and inconsistent customer messaging.

This presents a strong operational improvement opportunity because the business value is clear:
- faster outage detection and triage,
- reduced mean time to resolution,
- better field-technician coordination,
- more reliable customer communication, and
- improved regulatory and service-level compliance.

However, the opportunity does not automatically imply that AI is the right solution. In this case, the most valuable investment is likely a robust real-time monitoring and incident management capability built on deterministic rules, streaming analytics, and strong operational controls.

#### Why probabilistic AI is inappropriate for a customer-facing threshold monitoring service

A probabilistic AI model is not the right primary control mechanism for a monitoring service that consumes live sensor streams and triggers operational actions. This is because:
- the service must make clear, auditable decisions under strict operating conditions;
- false positives and false negatives carry real operational and customer impact;
- probabilistic outputs can drift over time and may be hard to explain to operators or regulators;
- threshold monitoring requires predictable, deterministic behavior rather than “best guess” predictions.

For this use case, the priority is reliability, explainability, and operational accountability, not model novelty.

### M — Model Strategy

The recommended model strategy is a deterministic operations architecture rather than a probabilistic AI-first approach.

#### Proposed strategy
- Use rule-based threshold monitoring for core alerting.
- Use time-series and streaming analytics to detect deviation from baseline behavior.
- Apply event correlation and state-based incident logic to identify likely outage patterns.
- Use AI only as an optional support layer for secondary tasks such as summarizing incident context, drafting customer communications, or suggesting next-best actions after the core monitoring logic has already identified the issue.

#### Why this is the correct strategy
- The primary decision is operational and safety-critical, not inferential.
- The organization needs consistent alerting, bounded latency, and transparent logic.
- A deterministic model provides stronger auditability and easier governance than a probabilistic model.
- AI should be used where it adds value without undermining the integrity of the monitoring system.

### A — Application Engineering Approach

The application engineering approach should focus on building a real-time threshold monitoring service that consumes network sensor streams and converts them into actionable incident signals.

#### Core application components
1. Data ingestion layer
   - Receive continuous telemetry from network sensors, field systems, and operational data sources.
   - Normalize event formats and timestamps.
   - Handle backpressure, buffering, and replay capability.

2. Stream processing and threshold evaluation
   - Apply real-time thresholds and rolling-window calculations.
   - Detect abnormal patterns, sustained degradation, and service-impacting conditions.
   - Support configurable severity rules.

3. Correlation and incident logic
   - Group related events into a single incident.
   - Correlate alerts across devices, regions, and services.
   - Determine whether the condition represents a localized issue or a broader outage.

4. Workflow and orchestration
   - Trigger incident creation.
   - Route the incident to the appropriate operations team or field technicians.
   - Coordinate updates to customer communication workflows.

5. Observability and control layer
   - Track latency, alert volume, false positives, and false negatives.
   - Provide dashboards for operators and management.
   - Ensure the system can be audited and reviewed by internal and external stakeholders.

#### Engineering principles
- Build for low-latency stream processing.
- Make the logic transparent and explainable.
- Ensure resilience through failover, replay, and recovery mechanisms.
- Separate detection logic from communication logic so that each can evolve independently.
- Design the system so humans remain in control of operational decisions.

### D — Delivery Checklist

The delivery checklist for this capability should reflect the needs of a regulated monitoring and incident management system rather than an AI project checklist.

#### Delivery priorities
- Latency guarantees for detection and alert propagation
- Performance targets under peak load and network stress conditions
- False positive and false negative tracking with clear operational thresholds
- Audit trail for alert generation, escalation, and incident resolution
- Change control for monitoring rules and threshold updates
- Incident review and post-event analysis capabilities
- Security, access control, and data integrity controls
- Traceability from sensor input to operational action and customer communication
- Compliance reporting for regulator-facing service performance and outage handling

#### What should not be the primary checklist
This should not be delivered as a standard “AI implementation” project with a checklist centered on model accuracy, explainability of a black-box model, or experimentation alone. The success criteria are operational reliability, regulatory readiness, and measurable service performance.

## Pros and Cons of the Decision

### Pros
- Stronger operational reliability because the system is based on transparent, deterministic logic rather than probabilistic outputs.
- Better auditability and regulatory fit, since threshold-based monitoring can be explained and justified more easily.
- Lower risk of unpredictable behavior during live incidents, which is critical for customer-facing services.
- Faster implementation of core monitoring capabilities because the solution can rely on established engineering and rules-based controls.
- Clearer accountability for operators and incident teams, since decisions can be traced to explicit rules and workflows.

### Cons
- Less flexibility than a fully AI-driven system when dealing with complex, ambiguous, or previously unseen outage patterns.
- May require more upfront engineering effort to design robust thresholds, correlation rules, and monitoring logic.
- Potentially weaker performance in situations where patterns are subtle and historical data could reveal hidden relationships that rules alone may miss.
- AI is underused for advanced analysis, which may limit opportunities for more intelligent forecasting or automated recommendations.

## Conclusion

For outage detection, the strongest path forward is a disciplined engineering program that combines real-time monitoring, deterministic rule logic, and operational workflow integration. AI may support parts of the experience, but it should not be the core mechanism for threshold-based outage detection. The platform should be judged by its ability to improve service continuity, reduce resolution time, and maintain transparent, auditable operations.

---

# Module 2 — Field Technician Knowledge Assistant (Decision: RAG)

## Business Context

Field technicians carry tablets into the field and need fast answers to procedural questions such as torque specifications, safety lockout steps, and part compatibility. Today, those answers are scattered across a 400-page technical manual PDF and several bulletins issued after the manual’s last revision. This creates delays in the field, increases the likelihood of inconsistent execution, and raises safety and compliance risk when technicians rely on outdated or incomplete instructions.

## B — Breakthrough Opportunity

The breakthrough opportunity is to reduce technician time spent searching for information and to improve adherence to safety procedures. When a technician can quickly retrieve the correct instruction from a trusted knowledge assistant, the organization benefits from faster job completion, lower rework, fewer errors, and improved safety compliance. The value is not only efficiency; it is also risk reduction, because the right procedure is more likely to be followed the first time.

## M — Model Strategy

The recommended decision is to use a Retrieval-Augmented Generation (RAG) approach rather than simply improving the PDF search function or building an agentic system.

### Why RAG is better than improving PDF search

A traditional PDF search experience is often too weak for this use case because it is keyword-based, lacks context awareness, and does not distinguish between authoritative and superseded content. A RAG system can retrieve the most relevant procedural passages from a curated knowledge base and present them with source attribution, which is far more useful for field technicians.

### Why an agentic system is not warranted

An agentic system is not the right first choice for answering procedural questions because the task is narrow, operationally sensitive, and requires high trust. The ideal behavior is not to “reason through” the problem independently, but to retrieve the correct documented instruction and present it clearly. An agentic approach adds unnecessary complexity, latency, and risk, especially when the assistant is being used for safety-critical tasks. The system should be precise, grounded, and easy to audit.

## A — Application Engineering Approach

The application engineering approach should focus on building a reliable knowledge retrieval pipeline that can serve the technician with the most current and relevant procedural guidance.

### 1. Document ingestion and preparation

The system should ingest the 400-page technical manual and all related bulletins as structured source documents. Each document should be parsed, cleaned, and preserved with metadata such as:
- document title,
- revision date,
- issue date,
- section number,
- document type, and
- source authority.

### 2. Chunking strategy

The documents should be chunked in a way that preserves procedural meaning. A good approach is to split content by section and subsection, while keeping short procedural steps intact. Tables, checklists, and safety instructions should be preserved as units where possible. Overlapping chunks can be used to avoid losing context at boundaries.

### 3. Retrieval tuning

The retrieval layer should be tuned for procedural accuracy rather than general relevance. A hybrid retrieval approach is appropriate, combining:
- keyword search for precise terms such as part names, torque values, and error codes, and
- semantic search for paraphrased technician questions.

The retrieval system should return a small set of relevant chunks ranked by authority, recency, and relevance.

### 4. Handling superseding bulletins

A major requirement is to handle cases where a bulletin supersedes a section of the manual. This should be modeled explicitly in the data pipeline. Each chunk should carry metadata for effective date and authority level, and the retrieval layer should prioritize newer, higher-authority instructions when they conflict with older manual content.

A practical implementation would include:
- version-aware indexing,
- explicit supersession rules,
- metadata-based ranking so newer bulletins outrank older manual sections, and
- clear citation of the authoritative source in the assistant’s response.

### 5. Response generation and grounding

The assistant should generate answers only from retrieved source chunks and should include citations to the relevant manual section or bulletin. This keeps the response grounded and makes it easy for technicians to verify the instruction. If multiple sources are relevant, the system should present the most current and authoritative one first.

## D — Delivery Checklist

The delivery checklist should focus on groundedness, reliability, and operational safety rather than generic AI experimentation.

### Groundedness evaluation

The system should be evaluated using a curated test set of technician questions that reflect real field scenarios. Each test case should include:
- the user question,
- the expected answer,
- the authoritative source that should be retrieved, and
- the correct handling of conflicts between manual sections and bulletins.

### Specific conflict test: bulletin versus outdated manual section

A critical evaluation should test that the assistant surfaces the newer bulletin over an outdated manual section when they conflict. For example:
- a technician asks for the correct torque value or lockout procedure,
- the manual contains an older instruction,
- a bulletin issued later supersedes it,
- the assistant must retrieve and present the bulletin-based instruction.

The test should verify that:
- the bulletin is ranked above the outdated manual section,
- the answer cites the bulletin as the authoritative source,
- the response clearly indicates that the older manual section is superseded, and
- the assistant does not present stale information as current guidance.

### Additional delivery criteria

- retrieval accuracy for procedural questions,
- citation correctness,
- low hallucination rate,
- response latency suitable for field use,
- support for offline or degraded operation where possible,
- logging and auditability for safety reviews.

## Conclusion

The strongest approach for the technician knowledge assistant is a grounded RAG system that retrieves the correct procedural guidance from a vetted knowledge base and presents it with clear citations. This is more appropriate than a PDF search upgrade or an agentic workflow because the use case requires trust, precision, and auditable decision support in a safety-sensitive environment.

---

# Module 3 — Technician Dispatch Workflow (Decision: Fixed AI Workflow)

## Business Context

Once Module 1 declares an outage, a technician must be identified based on the right skill set, nearest availability, and shift-hour constraints, then assigned and notified. Today, a dispatcher manually cross-references a skills spreadsheet, a location map, and a shift calendar. This process is slow, inconsistent, and prone to human error, particularly when outage volume is high or technician availability changes quickly.

## B — Breakthrough Opportunity

The breakthrough opportunity is to reduce dispatch time and improve assignment quality. A faster and more consistent dispatch process would shorten response time, reduce the risk of assigning the wrong technician, and improve first-time resolution. The business value is measured not only in speed, but also in better utilization of technician capacity and stronger service continuity.

## M — Model Strategy

The recommended approach is a fixed AI workflow rather than a fully agentic system.

### Why this is a fixed AI workflow

The dispatch process is fundamentally a structured operational workflow: parse outage details, check availability, rank candidates, assign, and notify. The deterministic parts of this process should remain deterministic. A model should only be used in one bounded step where it adds value without taking control over the full decision.

### Where the model adds value

The most appropriate place for AI is in the candidate ranking step. In this step, the system can use a model to assist with skill-matching against free-text technician profiles, recent experience, and job-history notes. This is valuable because technician profiles are often unstructured and difficult to align using simple rules alone. The model helps interpret free-text information, but it does not decide the entire workflow on its own.

### Why not a fully agentic system

A fully agentic system is not warranted because dispatching is a constrained business process with clear guardrails, compliance expectations, and operational accountability. The system must be predictable, auditable, and controllable. An agentic approach could introduce unnecessary autonomy, inconsistent behavior, and poor traceability. The workflow should remain fixed, with a single bounded AI-assisted step inside it.

## A — Application Engineering Approach

The application engineering approach should be implemented as a fixed sequence of steps.

### 1. Parse outage details

The workflow begins by ingesting structured outage information such as:
- outage type,
- service impact,
- required skill category,
- location,
- priority level, and
- required response window.

This creates a clear dispatch request with explicit constraints.

### 2. Query technician availability (deterministic)

The next step is to query technician availability from authoritative systems such as:
- shift calendars,
- time-off records,
- current assignments,
- location data, and
- skill inventory.

This stage should be deterministic and rule-based. It should return only candidates who are currently eligible based on hard constraints such as shift hours, current assignment load, and location proximity.

### 3. Rank candidates (bounded scoring step, potentially model-assisted)

Once eligible candidates are identified, the system ranks them using a bounded scoring model. The scoring logic can combine deterministic factors such as:
- travel distance,
- availability window,
- skill match,
- prior assignment success, and
- workload balance.

A model may assist in the skill-matching step when technician profiles are stored as free text rather than structured fields. For example, a language model can help infer whether a technician’s profile suggests relevant experience for a given outage type. However, this step remains bounded because the final ranking is still based on a controlled scoring framework.

### 4. Assign

The top-ranked candidate is selected according to the scoring logic, subject to business rules and override policies. The assignment should be logged with the reasoning behind the decision so that dispatchers and supervisors can review it.

### 5. Notify

The final step notifies the assigned technician and relevant stakeholders through the appropriate channel, such as mobile app notification, email, or dispatch console message.

## D — Delivery Checklist

The delivery checklist for this workflow should reflect the needs of a governed operational process with one bounded AI-assisted step.

### Core workflow requirements

- deterministic handling of availability and shift constraints,
- clear logging of assignment decisions,
- support for dispatcher override and manual intervention,
- escalation logic for no suitable candidate,
- auditability of the assignment history,
- integration with dispatch and notification systems.

### AI-specific requirements for the bounded ranking step

- validation that the model improves skill-matching quality over simple rule-based matching,
- measurable accuracy or agreement with dispatcher-approved assignments,
- clear fallback behavior when the model is unavailable or low confidence,
- explainability of why a candidate was ranked highly,
- monitoring for bias, drift, or inconsistent ranking behavior.

### Operational evaluation criteria

- dispatch time reduction versus the manual process,
- assignment quality and first-time resolution rate,
- workload balance across technicians,
- false assignment risk,
- override rate by dispatchers,
- human acceptance and trust in the workflow.

## Conclusion

The best design for technician dispatch automation is a fixed workflow with one bounded AI-assisted step. The deterministic sequence ensures reliability and accountability, while the model adds value in candidate ranking where unstructured technician data makes simple rules insufficient. This approach is more practical and governable than a fully agentic system for a process that must remain transparent and controllable.

---

# Module 4 — Outage Diagnostic Assistant (Decision: Agentic)

## Business Context

Beyond confirming that an outage exists and dispatching a technician, a senior network engineer still needs to form a hypothesis about the root cause before the technician arrives. This requires reviewing recent maintenance history, correlated sensor anomalies, and weather data, often in whichever order the specific outage scenario suggests. The challenge is that the investigation path is not fixed; it depends on the evidence that emerges during analysis.

## B — Breakthrough Opportunity

The breakthrough opportunity is to reduce engineer time spent assembling evidence and to improve technician preparedness before arrival on site. If the diagnostic assistant can quickly combine multiple data sources and surface a strong hypothesis, the engineer can make faster decisions, the technician can be sent with better context, and the overall time to diagnosis and resolution can improve significantly.

## M — Model Strategy

The recommended approach is an agentic system rather than a fixed workflow.

### Why agentic is justified here

This investigation is genuinely case-dependent. A single outage may be best explained by a recent maintenance event, while another may be more strongly associated with correlated sensor anomalies or environmental conditions such as severe weather. The correct investigative sequence depends on the evidence at hand, and an agentic approach allows the system to adapt its tool use and reasoning path to the specific incident.

### Why a fixed workflow is not sufficient

A fixed workflow would force the engineer through the same sequence every time, even when the evidence suggests a different path. For example, if weather data clearly aligns with a regional degradation pattern, the system should be able to pivot there early rather than follow a rigid sequence. The diagnostic process requires flexibility, prioritization, and iterative reasoning.

## A — Application Engineering Approach

The application engineering design should be built around a tool-using agent that can investigate an incident through a flexible sequence of actions.

### Tool set

The agent should have access to a small, explicit set of tools:
- check_maintenance_history
- check_correlated_sensors
- check_weather_data

These tools represent the core evidence sources an engineer would use during diagnosis.

### State carried between steps

The agent should maintain state across steps so that it can build a cumulative understanding of the incident. Relevant state may include:
- outage location and affected service,
- timestamp of incident onset,
- anomalies detected so far,
- maintenance events already reviewed,
- weather conditions relevant to the region,
- candidate hypotheses and their supporting evidence.

This state allows the agent to refine its reasoning as it gathers more evidence.

### Hard rule that still applies

Even though the agent can choose its own investigation path, one hard rule should remain non-negotiable: the assistant must not present a root-cause hypothesis as confirmed unless it is supported by evidence from the available tools and the incident context. In other words, the system may propose a hypothesis, but it must keep the level of confidence and evidence quality explicit.

### Example interaction pattern

A typical diagnostic sequence may look like this:
1. The agent reviews the outage details and identifies likely affected segments.
2. It checks correlated sensor anomalies to see whether the issue is part of a broader pattern.
3. It then checks maintenance history to see whether recent work could explain the symptoms.
4. If the incident appears weather-related, it invokes weather data to test that hypothesis.
5. It updates its hypothesis and presents the strongest explanation with supporting evidence.

## D — Delivery Checklist

The delivery checklist for this agentic system should focus on trustworthiness, evidence quality, and usefulness for engineers.

### Core agent requirements

- the agent should use the available tools appropriately and in a sensible order,
- it should preserve state between steps,
- it should explain why it chose a particular investigation path,
- it should clearly distinguish between confirmed facts and tentative hypotheses,
- it should avoid unsupported claims or overconfident conclusions.

### Evaluation of hypothesis quality

Hypothesis quality should be evaluated against real historical outages. A strong validation set would include past incidents with known root causes and the evidence that was available at the time. The system should be tested on whether it:
- identifies the correct root cause hypothesis,
- prioritizes the most relevant evidence first,
- narrows the candidate causes efficiently,
- provides a well-supported explanation,
- refrains from making unsupported assertions.

### Suggested evaluation metrics

- hypothesis accuracy against historical incidents,
- evidence coverage of the final explanation,
- precision of tool usage,
- time to reach a useful hypothesis,
- engineer acceptance and usefulness of the output,
- rate of false confidence or unsupported conclusions.

### Operational safeguards

- require evidence-backed summaries before presenting a root cause hypothesis,
- log every tool call and intermediate reasoning step for auditability,
- support human override and review by senior network engineers,
- provide a confidence level tied to the evidence collected.

## Conclusion

The outage diagnostic assistant is best implemented as an agentic system because the investigation path is inherently case-dependent and requires flexible, evidence-driven reasoning. The design should remain grounded in a controlled tool set, explicit state, and clear safeguards so that the system helps engineers diagnose faster without sacrificing trust or accountability.

---

# Module 5 — Mass Customer Notification & NOC Escalation (Decision: Multi-Agent)

## Business Context

A large-scale outage affecting thousands of customers requires several tasks to happen in parallel: verifying real-time status and estimated time of restoration, drafting an accurate customer-facing message, validating that message against tone and factual-accuracy guidelines, deciding whether the scale justifies escalating to a human NOC supervisor, and logging the full response for post-incident review. The cost of a wrong or delayed mass notification is high because it can damage customer trust, increase call-center volume, and create compliance and reputational risk.

## B — Breakthrough Opportunity

The breakthrough opportunity is to reduce the cost of a wrong or delayed mass notification at scale. A single poor message sent to thousands of customers can trigger customer churn, increase complaint volume, and force costly manual intervention. A well-orchestrated notification system can improve speed, consistency, and confidence while reducing the operational cost of manual coordination during major incidents.

## M — Model Strategy

The recommended approach is a multi-agent system rather than a single agent.

### Why multi-agent is justified

This use case has multiple distinct responsibilities that are better handled by specialized roles than by one general-purpose agent. The work is not just drafting text; it involves gathering current incident facts, validating correctness, deciding when escalation is warranted, and recording the outcome for audit. These are different functions with different failure modes, so separation of concerns is valuable.

### Which canonical roles are genuinely needed

The following roles are needed:

1. Planner
   - coordinates the overall response,
   - decides the sequence of actions,
   - ensures the workflow stays aligned with the incident context.

2. Retriever
   - gathers up-to-date incident facts such as affected regions, system status, and estimated restoration time,
   - pulls the latest policy or template guidance needed for the message.

3. Validator
   - checks the draft message for tone, factual accuracy, policy compliance, and consistency with the latest incident status.

4. Escalation
   - evaluates whether the incident scale, uncertainty, or business risk exceeds a predefined threshold,
   - routes the case to a human NOC supervisor when appropriate.

5. Reporting
   - logs the full incident response, including message content, validation results, escalation decision, and timestamps.

These roles are necessary because mass notification requires both content-generation and control-oriented safeguards. A single agent would be less reliable in balancing speed with accuracy and oversight.

## A — Application Engineering Approach

The application engineering design should use a coordinated multi-agent protocol with explicit control points.

### Coordination protocol

The workflow should run as follows:
1. Planner receives the incident context and creates a task plan.
2. Retriever gathers the latest facts and relevant communication templates.
3. Drafting or message-generation logic uses those facts to create a customer-facing message.
4. Validator reviews the draft and returns approval, revision, or rejection.
5. Escalation evaluates the incident against hard thresholds.
6. Reporting records the full transaction for post-incident review.

### Where the escalation threshold is enforced in code

The escalation threshold must be enforced in code rather than left to any agent’s judgment. A deterministic threshold policy should evaluate factors such as:
- affected customer count,
- incident severity,
- confidence in the current restoration estimate,
- number of unresolved unknowns, and
- time elapsed since incident detection.

For example, the system may be configured to escalate automatically when:
- affected customers exceed a defined threshold, or
- severity is critical and confidence in the ETA is below a minimum level, or
- the incident remains unresolved beyond a defined time window.

This logic should be implemented in a centralized controller or policy engine so that all agents follow the same rule. The Escalation role should not make the decision independently; it should execute the coded policy and route the case to a human supervisor when required.

### State shared across agents

The agents should share a common incident state that includes:
- incident ID,
- affected regions,
- current status,
- ETA,
- customer impact estimate,
- draft message versions,
- validation result,
- escalation decision, and
- audit timestamp trail.

This shared state ensures consistency and makes the workflow auditable.

## D — Delivery Checklist

The delivery checklist for this multi-agent system should emphasize reliability, governance, and measurable operating value.

### Core system requirements

- the planner must create a coherent execution plan for the incident,
- the retriever must pull the latest facts and policies,
- the validator must enforce tone and factual-accuracy checks,
- the escalation policy must be deterministic and code-enforced,
- the reporting layer must capture every decision and communication action,
- the system must support human review and override when needed.

### Evaluation criteria

- message accuracy against confirmed incident facts,
- compliance with approved tone and factual-accuracy guidelines,
- time from incident detection to customer notification,
- reduction in manual coordination effort,
- rate of correct escalation to human supervisors,
- quality of the post-incident audit trail.

### Cost and governance metrics

- cost-per-incident for notification processing,
- average handling time for major incidents,
- number of escalations avoided versus required,
- percentage of incidents with complete audit logs,
- review findings from post-incident audits and incident reviews.

### Post-incident audit review process

A formal post-incident review should be conducted after each major incident. The review should examine:
- whether the message was accurate and timely,
- whether the escalation policy fired correctly,
- whether any agent produced incorrect or low-quality output,
- what delays or failures occurred in the workflow,
- and what improvements should be made to templates, policies, or routing logic.

This review process should produce actionable learnings for future incidents and support continuous improvement of the system.

## Conclusion

The mass customer notification and NOC escalation capability is best handled by a multi-agent system because it combines distinct functions that require both speed and control. A planner, retriever, validator, escalation component, and reporting layer together provide a stronger operating model than a single agent, especially when the workflow is governed by code-enforced escalation rules and supported by rigorous post-incident review.
