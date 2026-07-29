# Complaint Resolution Escalation Dataset Trust Recovery Plan

## Problem Statement

The QA team spent several weeks curating an 800-case ground-truth dataset for the complaint resolution agent’s escalation decision. This dataset is the reference set on which every accuracy metric in the evaluation program depends. A routine audit found that two independent reviewers disagreed on 30% of the labels in a 50-case sample. That means every evaluation score reported against this dataset is now in question.

Leadership wants a systematic fix within one month, not a perfect solution that takes six months. The goal is to restore trust in the data while recognizing that some disagreements are due to simple labelling mistakes, while others may reflect genuinely ambiguous cases where reasonable people disagree.

## Core Issues

1. The true disagreement rate across all 800 cases is still unknown.
2. Some disagreements may be ordinary labelling errors, while others may be legitimate ambiguity.
3. The escalation policy is documented, but no one has checked whether disputed labels actually violate the policy.
4. The business needs a trustworthy evaluation dataset quickly, not a perfect one later.

## Recommended Approach

The fix should combine deterministic workflow controls, policy-grounded retrieval, multi-agent coordination, and human-in-the-loop review. The aim is not to replace human judgment but to make the review process faster, more consistent, and more evidence-based.

---

## 1. Fixed-Sequence AI Workflow for Flagging Likely Inconsistent Labels

### Objective

Create a workflow that automatically identifies cases most likely to have inconsistent labels and routes them for review.

### Proposed Workflow

1. Intake the existing 800-case dataset.
2. Run a rule-based and model-assisted review process on each case.
3. Flag cases that show one or more of the following signals:
   - conflicting reviewer notes,
   - policy-sensitive language,
   - borderline severity or ambiguity,
   - unusual label patterns compared with similar cases,
   - missing rationale or weak evidence.
4. Send only the flagged cases to a structured review queue.

### Why this helps

This creates a practical first-pass triage system. Instead of reviewing all 800 cases manually, the team can focus on the subset most likely to be problematic. That is a good fit for a fixed workflow because the sequence is repeatable and auditable.

### Design Guidance

- Use deterministic rules for hard checks such as missing labels, missing rationale, or policy contradiction.
- Use a bounded AI step only to rank cases by likelihood of inconsistency.
- Keep the workflow fixed so it is predictable and explainable.

---

## 2. RAG-Based Knowledge Base for Policy and Precedent Checking

### Objective

Replace opinion-only review with evidence-based review by grounding disputed labels against policy and precedent.

### Proposed Design

Build a retrieval-augmented knowledge base containing:
- the official escalation policy,
- approved examples of escalation vs non-escalation,
- prior reviewed disputes and their resolutions,
- precedent cases from similar complaint categories,
- annotated guidance for ambiguity and edge cases.

### How it works

When a disputed label is reviewed, the system retrieves the most relevant policy passages and precedent examples and presents them to the reviewer. The reviewer can then decide whether the current label is consistent with the documented policy.

### Why this is important

This avoids relying only on human memory or personal interpretation. It creates a shared reference point and makes the review process more defensible.

### Key Principle

The RAG system should not decide the label by itself. It should provide grounded evidence so humans can make a better-informed decision.

---

## 3. Multi-Agent Coordination for Reviewing Many Flagged Cases

### Objective

Coordinate the review of many flagged cases efficiently without losing control over quality.

### Proposed Multi-Agent Roles

1. Planner
   - creates the review sequence and prioritizes the most urgent or high-impact cases.

2. Retriever
   - gathers the relevant policy passages and precedent examples.

3. Validator
   - checks whether the proposed label is consistent with policy and evidence.

4. Escalation
   - decides when a case should be moved to a senior reviewer or human consensus panel.

5. Reporting
   - logs the review decision, supporting evidence, and outcome for auditability.

### Why multi-agent is useful

A single agent would be too general for this task. The review process has multiple distinct responsibilities: retrieving evidence, validating the label, deciding escalation, and recording the result. Multi-agent coordination makes these steps more organized and traceable.

### Governance Rule

The system should maintain a shared review state for each case so that no agent acts in isolation. The final decision should still belong to the human review process.

---

## 4. Human-in-the-Loop Consensus Process for Genuinely Disputed Cases

### Objective

Handle the cases that remain genuinely disputed even after policy and precedent checking.

### Proposed Process

For cases that remain ambiguous after policy review:
1. Send the case to a small panel of reviewers.
2. Require each reviewer to provide:
   - the chosen label,
   - the policy rule or precedent used,
   - a short rationale.
3. Use a structured consensus process to resolve the case.
4. If consensus is still not reached, escalate to a senior QA lead or policy owner.

### Why this matters

Some disagreements are not technical errors; they reflect genuine ambiguity. A structured human consensus process is the right way to handle these cases without pretending they are simple mistakes.

### Recommended Decision Rules

- If policy clearly applies, resolve directly.
- If the case is ambiguous but policy is relevant, resolve through panel review.
- If the case remains unresolved, mark it as a policy gap and update the guidance.

---

## Delivery Plan for the One-Month Recovery Program

### Week 1: Stabilize and Diagnose

- Inventory the 800-case dataset.
- Identify the 50-case sample disagreement pattern.
- Extract the disputed cases and map them to policy categories.
- Create a simple triage rule set for likely inconsistent labels.

### Week 2: Build the Policy and Precedent Layer

- Create the RAG knowledge base from policy documents and prior examples.
- Link each disputed case to likely relevant policy passages.
- Prepare the initial review interface for human users.

### Week 3: Implement the Review Workflow

- Deploy the fixed-sequence flagging workflow.
- Add multi-agent coordination for batching and prioritizing reviews.
- Start reviewing the highest-risk flagged cases.

### Week 4: Run Consensus Review and Publish Trusted Labels

- Resolve the remaining ambiguous cases through human consensus.
- Publish the corrected dataset with a confidence flag for each label.
- Document the changes and update the evaluation program to use the revised reference set.

---

## Expected Outcome

Within one month, the team should be able to produce a more trustworthy evaluation dataset by:
- reducing obvious labelling errors,
- grounding disputed labels in policy and precedent,
- routing ambiguous cases to structured human review,
- and creating auditability for every recovered label.

This will not create a perfect dataset overnight, but it will create a credible, defensible, and operationally useful one for the evaluation program.
