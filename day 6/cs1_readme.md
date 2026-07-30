# BMAD Benchmark Brief: Telecom Chatbot Cost, Latency, and Quality

## Business Scenario
A telecom chatbot’s AI spend is growing faster than contact volume. The team is considering three options:
- Keep the current large model unchanged.
- Route simple requests to a smaller model.
- Keep the current model but use a shortened prompt and caching.

The goal is to benchmark these options using real evidence, not intuition, and use the results to inform a BMAD recommendation.

---

## B — Is this a real, worthwhile problem?
Yes. This is a worthwhile problem because:
- AI spend is rising faster than usage, which suggests inefficient scaling.
- Chatbots often spend a large share of their cost on prompt size and repeated inference.
- The business impact is direct: lower cost and lower latency can improve margin and customer experience at the same time.
- The problem is also low-risk to investigate because a small benchmark can be run quickly with a limited dataset.

### Why it matters
If we can reduce token usage without hurting answer quality, we can cut cost while preserving service quality. This is a strong candidate for a practical optimization effort.

### Brief implementation plan for B
1. Define the business question clearly: “Can we reduce AI cost and latency without lowering customer experience?”
2. Set a simple success rule: reduce estimated cost and latency while keeping answer quality above a minimum threshold.
3. Run a small, time-boxed benchmark using 5 representative customer questions.
4. Use the benchmark results to decide whether to invest in a larger rollout.

---

## M — Which option should we benchmark first, and why?
We should benchmark the shortened prompt plus caching first.

### Why this option first
- It is the lowest-risk change.
- It is usually the fastest to implement.
- It can reduce token volume immediately, which lowers both estimated cost and latency.
- It provides a strong baseline before introducing more complex routing logic.

### Recommended benchmark order
1. First: same model with a shortened prompt and caching.
2. Second: tiered routing to a smaller model for simple requests.
3. Third: current large model unchanged as the control baseline.

### Brief implementation plan for M
1. Create three test variants:
   - Control: current long prompt, current large model.
   - Variant A: shortened prompt, same model, caching enabled.
   - Variant B: tiered routing to a smaller model for simple requests.
2. Keep all other settings constant: temperature, max output length, and evaluation rubric.
3. Compare results across the same test questions.
4. If Variant A improves cost/latency without hurting quality, it becomes the best near-term action. If not, move to Variant B.

---

## A — How should the benchmark be designed?
The benchmark should measure three things:
- Latency
- Approximate cost
- Answer quality

### Test questions
Use 5 representative telecom customer questions covering simple lookups, medium complexity, and complaint handling:
1. “What is my current bill amount and due date?”
2. “How do I switch to a plan with more data?”
3. “Why is my internet service down in my area?”
4. “I was charged twice for the same repair visit; can you help?”
5. “My service has been unstable for three days and I want a refund or compensation; what should I do?”

### Metrics to capture
- Latency: p50 and p95 response time per request.
- Token count: input tokens, output tokens, and total tokens.
- Estimated cost: derived from token count and model pricing.
- Quality: score each response on a simple rubric.

### Quality rubric
Score each answer from 1 to 5:
- 5 = correct, complete, action-oriented, and safe.
- 4 = correct with minor omissions.
- 3 = partially correct but missing key information.
- 2 = weak or incomplete.
- 1 = incorrect or unsafe.

### Experimental design
- Run each prompt against each option.
- Repeat each test at least 3 times to reduce randomness.
- Use the same system prompt structure and temperature setting for fairness.
- If API access allows, run against two real models; if not, use token-based estimated cost as a proxy.
- For caching, include a repeated query scenario to measure cache-hit benefits clearly.

### Brief implementation plan for A
1. Prepare the dataset of 5 questions.
2. Implement a benchmark harness that sends each question to each option.
3. Capture response time, token usage, and quality score per run.
4. Record results in a simple CSV or JSON file.
5. Aggregate results into a summary table for comparison.

---

## D — What counts as “good enough evidence” to make a decision?
Good enough evidence should be practical, not perfect. The benchmark should be strong enough to justify a rollout decision without becoming a major research project.

### Decision threshold
A configuration is worth adopting if it meets all of the following:
- Cost drops materially, such as 20–30% or more.
- Latency improves meaningfully, such as 15–25% faster p50 response time.
- Quality stays at or above the minimum threshold, such as an average score of 4/5 or higher.
- No safety or policy regressions appear.

### Recommended stop rule
Stop once the benchmark shows one option clearly meets the threshold across most questions, especially the simple ones. There is no need to over-invest in a large benchmark if the signal is already strong.

### Brief implementation plan for D
1. Define a minimum acceptance bar before running the tests.
2. Review the results by question type: simple lookup, moderate request, and complaint.
3. Prefer the lowest-cost option that still preserves quality.
4. If the result is mixed, keep the current model for complex complaints and use the cheaper option only for simple requests.
5. Document the final recommendation with the evidence and any follow-up experiments.

---

## Recommended BMAD Summary
- B: This is a real and worthwhile problem because cost is growing faster than value created.
- M: Benchmark the shortened prompt plus caching first because it is the lowest-risk and most practical first step.
- A: Measure latency, token cost, and quality across 5 representative customer questions using a simple, repeatable benchmark harness.
- D: Adopt the option if it reduces cost and latency while preserving quality above a defined threshold.

## Final Recommendation
Use the benchmark to support a phased rollout:
1. Start with the shortened prompt and caching.
2. Evaluate whether routing simple requests to a smaller model is justified.
3. Keep the current large model for complex complaint-handling tasks where answer quality matters most.
