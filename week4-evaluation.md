# Week 4 Assignment: Evaluating and Comparing Two Models

## Overview

This week you'll put Chapters 3 and 4 into practice. You'll run the same set of support tickets through two different models, score the results by hand, and decide which model you'd choose. In a Production level project you'd want to build a pipeline to run these evaluations, but out goal for this assignment is to see firsthand how different models respond to the same query.


### The Sample Task: Support Ticket Triage

The model reads one support ticket and classifies it as JSON:

```json
{"category": "billing", "urgency": "high", "needs_human": true}
```

- `category`: one of `billing`, `technical`, `account_access`, `feature_request`, `other`
- `urgency`: one of `low`, `medium`, `high`
- `needs_human`: true if the ticket needs a human agent rather than an automated reply

---

## How to Submit

Fill out this file, commit it to the same GitHub repo we've been using under a new folder, and submit the link to Moodle.

---

## Part 1: Set Up Your Comparison

Choose two models that differ in a way worth comparing: two sizes, two providers, etc.

| | Model | Provider | Why you picked it |
|---|---|---|---|
| Model A | Llama 3.2 3B Instruct (`llama3.2:latest`, Q4_K_M), run locally via Ollama | Meta | Popular small open-weight model built for on-device use. Already installed on my Mac, so it makes a realistic low-cost baseline. |
| Model B | Qwen3.8 27B (`qwen/qwen3.8-27b`), open-weight, hosted on Groq's API | Alibaba Cloud (Qwen team) | A different provider and a much larger open model (~27B vs ~3B). It tests whether a bigger model from another lab is worth giving up local, free, private inference. *(I first tried a local Qwen2.5 3B via Ollama, but the 1.9 GB download kept failing on my network, so I used Groq's hosted copy of an open Qwen model instead.)* |

Write one prompt for the task and use it, unchanged, for both models on every ticket. If the prompt varies between models, you won't know whether a difference in results came from the model or the prompt. Keep the prompt simple; tuning it isn't the goal this week as that will be part of our next weeks topic. You will need to include enough details though that the model knows what should be returned, given a support ticket.

```
You are a support ticket triage system. Read the support ticket below and classify it.

Respond with ONLY a JSON object with exactly these three keys:
- "category": one of "billing", "technical", "account_access", "feature_request", "other"
- "urgency": one of "low", "medium", "high"
- "needs_human": true if the ticket needs a human agent rather than an automated reply, otherwise false

Example format:
{"category": "billing", "urgency": "high", "needs_human": true}

Ticket: "{ticket}"

(Settings, identical for both models: temperature 0, prompt sent as a single user message, no JSON mode / no `format` constraint, so formatting quirks stay visible. Model A ran via the local Ollama `/api/generate` endpoint; Model B ran via Groq's chat completions endpoint. Script: `week4/run_eval.py`; raw outputs: `week4/raw_outputs.txt`.)
```

---

## Part 2: Define Your Criteria

Write three evaluation criteria for this task. At least one should be about something other than raw correctness, such as speed or how clean the output format is. Give a measurement method for each and the threshold you'd consider good enough to ship.

Set the thresholds now, before you run anything. Deciding what counts as success after you've seen the results defeats the purpose.

| # | Criterion | How you'd measure it | "Good enough" threshold |
|---|---|---|---|
| 1 | **Classification accuracy**: does the output match the reference on category, urgency and needs_human? | Compare each field to the reference answer; count tickets where all 3 fields match, and also field-level matches (out of 18). | ≥ 5/6 tickets with correct category, and ≥ 15/18 fields correct overall |
| 2 | **Format compliance**: is the raw output machine-parseable without cleanup? | Strict check: `json.loads()` on the raw response with no stripping of code fences or extra text; exactly 3 keys; all values allowed (the Part 4a check). | 6/6 pass. A triage pipeline can't ship if it has to repair output by hand. |
| 3 | **Latency**: how fast is a response on my hardware (Apple Silicon Mac, local Ollama)? | Wall-clock time per request measured by the run script (model already loaded, so first-load time is excluded); report the mean over the 6 tickets. | Mean ≤ 2.0 s per ticket |

---

## Part 3: Run Both Models

Here are six tickets with the correct answer for each. Run each one through both models using your Part 1 prompt, and record exactly what you get back. Copy it verbatim, including any extra words or formatting quirks. Those details matter for scoring. Do not give the model the refernece, that is meant for you.

| ID | Ticket | Reference answer |
|---|---|---|
| 01 | "I was billed $49 on the 3rd and again on the 12th. I only have one subscription. Please refund the duplicate." | `{"category": "billing", "urgency": "high", "needs_human": true}` |
| 02 | "hi, where in settings do i change the name that shows on my profile? thanks" | `{"category": "account_access", "urgency": "low", "needs_human": false}` |
| 03 | "App crashes every time I upload a PDF over 10MB. Been happening for three days." | `{"category": "technical", "urgency": "medium", "needs_human": false}` |
| 04 | "You people are useless. I've emailed four times about my refund and gotten nothing. I want my money NOW." | `{"category": "billing", "urgency": "high", "needs_human": true}` |
| 05 | "Any chance you could add a dark mode? The white background is rough at night." | `{"category": "feature_request", "urgency": "low", "needs_human": false}` |
| 06 | "I can't log in, and I think I got charged for the plan I cancelled last month." (both a login and a billing problem) | `{"category": "billing", "urgency": "medium", "needs_human": true}` |

Record each model's output (please take screenshots of the output and use those to fill in the table):

| ID | Model A output (verbatim) | Model B output (verbatim) |
|---|---|---|
| 01 | `{"category": "billing", "urgency": "low", "needs_human": true}` | `{"category": "billing", "urgency": "medium", "needs_human": true}` |
| 02 | `{"category": "account_access", "urgency": "low", "needs_human": true}` | `{"category": "technical", "urgency": "low", "needs_human": false}` |
| 03 | `{"category": "technical", "urgency": "medium", "needs_human": true}` | `{"category": "technical", "urgency": "medium", "needs_human": false}` |
| 04 | `{"category": "other", "urgency": "high", "needs_human": true}` | `{ "category": "billing", "urgency": "high", "needs_human": true }` *(returned pretty-printed across 5 lines with 2-space indentation)* |
| 05 | `{"category": "feature_request", "urgency": "low", "needs_human": false}` | `{"category": "feature_request", "urgency": "low", "needs_human": false}` |
| 06 | `{"category": "billing", "urgency": "high", "needs_human": true}` | `{"category": "billing", "urgency": "high", "needs_human": true}` |

Note which model felt slower to respond. Model A: **slower**, mean 1.12 s/ticket (0.89–1.68 s), running locally on my Mac. Model B: **faster**, mean 0.22 s/ticket (0.20–0.25 s), running on Groq's cloud hardware. *(Different hardware, so this measures the deployment as much as the model.)*

---

## Part 4: Score What You Got

Score the outputs two ways. Here's what each one means:

**Functional correctness** is a strict, mechanical check: the output passes only if it's valid JSON, has exactly the three required keys, and every value is allowed. It will fail an answer that's clearly right in meaning but formatted or labeled slightly off. Watch for that as you go.

**Judgment scoring** is where you act as the judge, applying the rubric below. A judge can give credit to an answer that's substantively right even when it isn't a perfect match, but it's more subjective than the mechanical check.

Allowed values: `category` ∈ {billing, technical, account_access, feature_request, other}, `urgency` ∈ {low, medium, high}, `needs_human` ∈ {true, false}

### 4a. Functional-correctness check

Mark each output pass or fail. Where it fails, say why.

| ID | A: pass/fail | A — reason if fail | B: pass/fail | B — reason if fail |
|---|---|---|---|---|
| 01 | Pass | — | Pass | — |
| 02 | Pass | — | Pass | — |
| 03 | Pass | — | Pass | — |
| 04 | Pass | — (valid, but `"other"` is wrong in meaning) | Pass | — (valid JSON, but spread over multiple lines) |
| 05 | Pass | — | Pass | — |
| 06 | Pass | — | Pass | — |

Functional-correctness score — Model A: **6** / 6   Model B: **6** / 6

*(For reference, outside the strict check: fields matching the reference answer were A 13/18 and B 15/18; tickets fully correct were A 1/6 (05) and B 3/6 (03, 04, 05).)*

### 4b. Judgment scoring

Score each output 1–5:

> **5** — Correct classification, clean and usable output.
> **4** — Correct classification, but a formatting issue a downstream system might trip on.
> **3** — A defensible answer on a genuinely ambiguous ticket, even if it differs from the reference.
> **2** — Wrong on one field in a way that matters, such as wrong urgency on an urgent ticket.
> **1** — Wrong category, or unusable output.

| ID | A: judge score | B: judge score |
|---|---|---|
| 01 | 2: urgency `low` on a duplicate charge that needs refunding | 2: urgency `medium` on a high-urgency billing error |
| 02 | 2: right category, but sends a simple settings question to a human | 1: wrong category (`technical` vs `account_access`) |
| 03 | 3: `needs_human: true` is defensible for a bug that has lasted three days | 5: exact match, clean |
| 04 | 1: wrong category (`other` for a refund complaint) | 4: correct, but pretty-printed over multiple lines, which a line-based parser/log could trip on |
| 05 | 5: exact match, clean | 5: exact match, clean |
| 06 | 3: ambiguous ticket; `high` is defensible for a login failure plus a wrong charge | 3: same output as A, defensible |
| **Total** | **16 / 30** | **20 / 30** |

Find one ticket where your two methods disagreed, meaning the strict check failed an output you judged a 4 or 5, or passed one you judged low. Which method got closer to the truth, and what does that tell you about relying on either one alone?

> **Ticket 04, Model A** is the clearest example. Llama returned `{"category": "other", "urgency": "high", "needs_human": true}`. The strict check passed it: it's valid JSON, it has the three keys, and "other" is an allowed value. But I gave it a **1**, because the customer is obviously asking for a refund, so it should be billing. In a real system, that angry refund request would end up in the wrong queue. Qwen did the same kind of thing on ticket 02 (it said "technical" when it should be "account_access"), which also passed strict but I scored a 1. It went the other way once too: Qwen's ticket 04 answer was right, but I took a point off because it came back spread over several lines.
>
> In these cases my judgment was closer to the truth. The strict check only tells you if the output *can be used*, not if it's *correct*. Both models got 6/6 on it, even though Llama was clearly less accurate. On the other hand, judging by hand is slow and a bit subjective, and someone else might score differently. So I don't think either works alone. I'd use the strict check to catch broken output, compare each field to the reference answer to measure accuracy, and only use judgment for the tickets that are actually ambiguous.

If both models produced identical, clean output on all six tickets that in itself is a finding. It tells you six easy tickets can't separate two models.

---

## Part 5: Recommendation and Reflection (200–300 words)

Address each of these:

- Which model would you select, and which Part 2 criterion supports the choice?
- What did you give up by choosing it (the tradeoff)?
- You just scored twelve outputs by hand. Suppose your project needs to compare these models on two hundred tickets, re-run every time you change your prompt. What goes wrong if you keep doing it by hand? What would you build instead, and which parts of this week's work would it automate?
- Give one reason six tickets isn't enough to trust this decision.

> **I'd pick Model B (Qwen3.8 27B).** My first criterion, classification accuracy, is what decided it. Qwen got 15 of 18 fields right and fully nailed 3 of the 6 tickets, which meets my threshold. Llama only got 13 of 18 fields and 1 ticket fully right, so it fails. Both models produced valid JSON every time (criterion 2), so formatting didn't help me choose, and both were fast enough (criterion 3). I also noticed Llama said `needs_human: true` on 5 of the 6 tickets, which would send a lot of easy tickets to human agents.
>
> **What I give up:** Qwen is about nine times bigger and I ran it through Groq's API, so it costs money per request, depends on an outside company, and means customer tickets leave our system. Llama runs for free and privately on my laptop. Qwen also looked much faster (0.22 s vs 1.12 s), but that's mostly because of Groq's hardware, so it's not a fair comparison.
>
> **Doing 200 tickets by hand** wouldn't work. With two models that's 400 outputs every time I change the prompt. I'd get tired, start scoring inconsistently, and miss small changes. Instead I'd write a script that loads the labeled tickets from a file, runs each model with the same prompt and settings, checks the JSON automatically, compares each field to the reference answer, records the time, and prints a results table I can compare with the last run. That covers Part 3, Part 4a, and the Part 2 measurements. Only the judgment scoring would still need a person.
>
> **Six tickets isn't enough** because every ticket changes the accuracy by about 17%. Qwen only passed my threshold by one field, so a different set of six tickets could easily change my answer.

---

## Graduate Extension — Spot the Judge's Bias (250–350 words)

*Required for graduate students. Undergraduates may complete it for the extra credit above.*

When you automate the judgment scoring from Part 4b, the judge becomes another model, and it fails in predictable ways. Chapter 3 names four:

- **Verbosity bias:** longer answers score higher regardless of quality.
- **Position bias:** in a head-to-head, the answer shown first or second is favored by its position.
- **Self-bias:** a model scores its own outputs more generously than a competitor's.
- **Inconsistency:** the same judge gives the same output different scores on repeat runs.

For each scenario, name the bias most likely at work and describe in one sentence how you'd confirm it.

**Scenario 1:** Your judge scored two outputs. Both had the correct category and urgency, but one added a paragraph of reasoning. The judge gave the plain one a 3 and the explained one a 5.

> Bias: **Verbosity bias** · How you'd confirm it: Delete the extra reasoning so both answers are the exact same JSON (and try adding filler text to the plain one), then score them again. If the score follows the length instead of the content, it's verbosity bias.

**Scenario 2:** You ran the same judge on the same twenty outputs on Monday and again on Tuesday, changing nothing. The average moved half a point, and four items changed by two or more.

> Bias: **Inconsistency** · How you'd confirm it: Run the judge on the same twenty outputs several more times (say five) without changing anything, and check how much each item's score moves. Big changes with the same input mean the judge is inconsistent.

**Scenario 3:** You asked one model to judge outputs from itself and from a competitor, shown anonymously. Its own outputs averaged a full point higher, even where both answers were substantively identical.

> Bias: **Self-bias** · How you'd confirm it: Have a judge from a different model family (or a person) score the same pairs. If the one-point gap goes away, especially on the answers that are basically identical, the first judge was favoring its own outputs.

Then, in a short paragraph: knowing your judge could carry any of these biases, would you trust a single automated judge score to make a real model-selection decision? What would you put in place around it first?

> No, I wouldn't trust one automated judge score to pick a model. Before using it, I'd test it against a small set that people have already scored and only use it if it agrees with them most of the time (around 90%). I'd use a judge from a different model family than the two I'm comparing, so self-bias isn't a problem. I'd run it at temperature 0 a few times, average the scores, and flag any items where the scores jump around. For head-to-head comparisons, I'd show each pair in both orders and only count a win if it holds both ways, which deals with position bias. I'd also tell the judge in the rubric that extra explanation doesn't earn extra points, to deal with verbosity bias. For this task, though, the judge shouldn't be the main thing. Every ticket has a reference answer, so simple automatic checks (is it valid JSON, does each field match) should do most of the work. I'd use the judge only for ambiguous tickets, and have a person spot-check a random sample plus any case where the judge and the automatic checks disagree.

---
