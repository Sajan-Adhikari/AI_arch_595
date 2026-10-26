# Week 7 Assignment — Agents Course + Your Own Agent

**Chapter:** Huyen, *AI Engineering*, Ch. 6 — Agents & Memory (pg. 275–305)
**External lesson:** Hugging Face *AI Agents Course*, Unit 1: Introduction to Agents — https://huggingface.co/learn/agents-course/unit1
**Points:** 100
**Due:** End of Week 7

---

## Submission Instructions

1. Copy this file into your Assignment 1 repo, keeping the filename **`week7-agents-lab.md`**.
2. Fill in every blank (`_____`) and bracketed placeholder directly in the file.
3. Make sure your Hugging Face Space is public so I can open it.
4. Push your commit, then submit a link to the file as instructed for this course.

**Name:** _____
**Link to your Hugging Face Space:** _____
**Link to (or screenshot of) your Unit 1 certificate:** _____

---

## Overview

This week you'll work through the first unit of Hugging Face's free AI Agents Course, then build on it. Unit 1 covers what agents are, how LLMs act as an agent's "brain," how agents use tools, and the Think → Act → Observe cycle. It ends with building a first agent using `smolagents`, publishing it as a Hugging Face Space, and taking a quiz that earns the course's **Certificate of Fundamentals of Agents**.

Then you'll make the agent your own: give it tools that do something you care about, push it on multi-step tasks, and study how it fails.

## Learning Objectives

- Explain how an agent plans, calls tools, and uses observations to decide its next step.
- Build a working agent with multiple tools, including one you write yourself.
- Identify and categorize agent failures using the failure modes in Huyen Ch. 6.
- Decide whether an agent (as opposed to RAG or a single prompt) is the right design for a given problem.

---

## Setup

1. Create a free Hugging Face account if you don't have one.
2. Start at the Unit 1 link above and work through the unit in order.
3. When you reach the hands-on tutorial ("Let's Create Our First Agent Using smolagents"), duplicate the template Space as instructed and follow along.

If you store any access token or API key, add it as a **Space secret**, never in your code. Your Space is public, and anyone can read its files.

---

## Part 1: Complete Unit 1 and Earn the Certificate (25 pts)

Work through all of Unit 1, including the tutorial, and **pass the end-of-unit quiz** to earn the Certificate of Fundamentals of Agents. Follow the quiz link in the course itself, since the certification app has moved before.

Put the certificate link or screenshot at the top of this file.

**In 2–3 sentences, explain the Think → Act → Observe cycle in your own words, using something your agent actually did as the example:** _____

---

## Part 2: Build Your Agent (40 pts)

Extend the agent in your duplicated Space so that it has:

- **At least 2 tools** in total
- **At least 1 custom tool that you write yourself** (not a pre-made one). Tools related to your term project are recommended, but anything useful works: a unit converter, a calculator for a formula from another class, a lookup over a small dataset, a text formatter, etc.

**Your custom tool:**

| | Value |
|---|---|
| Tool name | _____ |
| What it does | _____ |
| Inputs and output | _____ |

Paste your custom tool's code here:

```python
[your custom tool code]
```

**What did you write in the tool's name, description, and argument descriptions to help the agent know when and how to use it? Did you have to revise them?** _____

Now give your agent **3 multi-step tasks**, meaning tasks that require more than one tool call or more than one step to complete. At least one task should require using **two different tools** together.

| # | Task (short) | Tools the agent called, in order | Number of steps | Succeeded? (yes / partly / no) |
|---|---|---|---|---|
| 1 | _____ | _____ | _____ | _____ |
| 2 | _____ | _____ | _____ | _____ |
| 3 | _____ | _____ | _____ | _____ |

---

## Part 3: Failure Analysis (15 pts)

Find **one clear failure**. If none of your tasks failed, try to make the agent fail: give it an ambiguous request, a task no tool can handle, bad input for your custom tool, or a task that needs many steps.

Paste the relevant part of the agent's step log here (trim it to the steps that matter):

```
[agent log excerpt]
```

**What went wrong?** _____

**Which kind of failure is it, using the categories in Huyen Ch. 6? Explain why it fits that category.** _____

**What change would you make to prevent it (tool description, prompt, a new tool, a limit on steps, etc.)?** _____

---

## Part 4: Reflection (20 pts, 250–350 words)

Answer all four:

- What did the course's explanation of agents make clearer than the textbook did, or vice versa? Point to something specific.
- How much did your tool's description matter to whether the agent used it correctly? What does that suggest about designing tools for agents?
- Last week you built a RAG pipeline. For a question like "what does our policy say about X?" versus "book me a meeting with X," which design fits each, and why?
- Your Milestone 1 is due this week. Would your project benefit from being an agent, or is a simpler design better? Justify your answer.

**Your reflection:**

_____

---

## Part 5: Graduate Extension — MCP Fundamentals (15 pts)

*Graduate students required. Undergraduates are encouraged to read Unit 1 as optional background.*

Complete **Unit 1 of Hugging Face's MCP Course** (MCP Fundamentals, Architecture and Core Concepts) — https://huggingface.co/learn/mcp-course/unit1/introduction — and take its end-of-unit quiz.

**Link to (or screenshot of) your MCP Unit 1 quiz result:** _____

In 200–300 words: look at the tools your agent uses. Which of them, if any, would make more sense exposed through an MCP server instead of defined directly in the agent's code? What would you gain (reuse, access to live systems, other clients using the same tools), and what would you give up (setup, security, trust in the server)? Tie your answer to the host / client / server roles from the unit.

**Your analysis:** _____

---

## Grading

| Component | Undergraduate | Graduate |
|---|---|---|
| Unit 1 and certificate (Part 1) | 25 pts | 20 pts |
| Build your agent (Part 2) | 40 pts | 35 pts |
| Failure analysis (Part 3) | 15 pts | 15 pts |
| Reflection (Part 4) | 20 pts | 15 pts |
| Graduate extension (Part 5) | — | 15 pts |
| **Total** | **100 pts** | **100 pts** |

### Rubric

| Level | Criteria |
|---|---|
| **Full credit** | Certificate earned, and the Think → Act → Observe explanation uses the student's own agent. The public Space runs with at least 2 tools, including a working custom tool with a clear description. All 3 tasks are logged, and at least one uses two tools together. The failure is backed by a log excerpt, categorized correctly with reasoning, and paired with a specific fix. Reflection connects the student's own results to Huyen Ch. 6. |
| **Partial credit** | Certificate missing, or the Space doesn't run. Only pre-made tools are used, or the custom tool doesn't work. Fewer than 3 tasks, or tasks that need only a single step. The failure is described without a log, not categorized, or the fix is vague. Reflection restates the chapter instead of the results. |
| **No credit** | Not submitted, the Space link doesn't work or is private, or results appear fabricated (e.g., logs that don't match what the Space produces). |

---

## A Note on Scope

Agents fail a lot, and yours will too. A clear, well-diagnosed failure is worth more here than a perfect run you can't explain.

Also note: **Project Milestone 1 is due this week.** Unit 1 is a big unit, so start early in the week and don't leave the course and the milestone for the same night.
