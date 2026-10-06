# Week 6 Assignment — RAG Codelab + Your Own Documents

**Chapter:** Huyen, *AI Engineering*, Ch. 6 — RAG (pg. 253–274)
**External lesson:** Google & Kaggle *5-Day Gen AI Intensive*, Day 2: Embeddings and Vector Stores — https://www.kaggle.com/learn-guide/5-day-genai
**Points:** 100
**Due:** End of Week 6

---

## Submission Instructions

1. Copy this file into your Assignment 1 repo, keeping the filename **`week6-rag-lab.md`**.
2. Fill in every blank (`_____`) and bracketed placeholder directly in the file.
3. Make sure your Kaggle notebook is saved with its outputs showing, and that it's either public or shared with me.
https://www.kaggle.com/code/sajanadhikari0/day-2-document-q-a-with-rag
4. Push your commit, then submit a link to the file as instructed for this course.

**Name:** _____
**Link to your completed Kaggle notebook:** _____

---

## Overview

This week you'll work through a RAG lesson built by Google and Kaggle, then make it your own. Part 1 is completing their RAG question-answering codelab as written. In Part 2, you'll point that same pipeline at your own documents and test it with questions you write yourself. The reflection connects what you built back to Huyen's Chapter 6.

## Learning Objectives

- Build and run a working RAG pipeline: embed documents, store them, retrieve relevant passages, and generate grounded answers.
- Adapt an existing pipeline to a new set of documents.
- Evaluate retrieval separately from generation, so you can tell which part failed.
- Connect a hands-on implementation to the RAG architecture described in the textbook.

---

## Setup

1. Open the Kaggle Learn Guide linked above and go to **Day 2**.
2. Create a free Kaggle account if you don't have one. Kaggle may ask you to verify your account with a phone number before it allows internet access in notebooks, which the codelabs need.
3. Get a free Gemini API key from Google AI Studio.
4. Store your key using **Kaggle Secrets**, as the codelab instructs. **Never paste your key into a notebook cell.** Your notebook will be shared, and anyone who sees the key can use it.

If a cell fails, check the course's troubleshooting guide for the codelabs before spending a long time debugging.

---

## Part 1: Complete the RAG Codelab (30 pts)

Find the Day 2 codelab that builds a **RAG question-answering system over documents**. Copy it into your own Kaggle account and run it from top to bottom, with every cell executing successfully.

Record what the pipeline uses:

| | Value |
|---|---|
| Embedding model | _gemini-embedding-001____ |
| Where the embeddings are stored (vector store/database) | _Chroma db____ |
| Generation model | _gemini-3.8-flash____ |
| Number of passages retrieved per query | __1___ |

**In 2–3 sentences, describe what happens between the moment a question is asked and the moment an answer comes back:** _____
At first, the documents are converted into the document embeddings and stored in the vector store. The query also get converted to the embedding when user asks. The query and the similar 
document are retrieved through semantic similarity. Then the document is attached in the query to generate the good answer from the llm model.
---

## Part 2: Make It Yours (40 pts)

In your copy of the notebook, **replace the sample documents with 3–5 short documents of your own.** Documents related to your term project are recommended. Course materials, public documentation for a tool you use, or articles on a topic you know well also work. Avoid anything private or sensitive.

Keep the rest of the pipeline the same. Your notebook should show your documents, your questions, and the outputs.

**Your documents:**

| | Value |
|---|---|
| What the documents are | ___ProblemStatement,TargetUser,Approach,Evaluation(this are the initial project draft)__ |
| Number of documents | __4___ |
| Why you chose them | __I want to include them as my document so that i can tweak it and see what changes._Actually these 4 topics fulfills the document required in this assignment.__ |

Write **5 test questions** and run each through the pipeline. Your set must include:

- **2 keyword questions** that use exact names, terms, numbers, or codes from your documents
- **2 paraphrase questions** that ask about something in your documents without using its wording
- **1 unanswerable question** whose answer is **not** in your documents

| # | Question (short) | Type | Retrieved the right passage? (Yes / No / N/A) | Generated answer (correct / partly / wrong / correctly declined) |
|---|---|---|---|---|
| 1 | _What does ATS stand for in the context of the project?____ | _keyword____ | yes_____ | _correct____ |
| 2 | _ what is the project problem statement____ | _paraphrase____ | _yes____ | _correct____ |
| 3 | _Who is the initial target user of the proposed tool?____ | __paraphrase___ | _yes____ | correct_____ |
| 4 | What 1–5 usability score will be used to evaluate the generated outputs?_____ | keyword_____ | _yes____ | _correct____ |
| 5 | How many job offers will the tool generate for the user_____ | unanswerable_____ | __no___ | _wrong____ |

**Pick one question where the result wasn't fully correct (or, if everything worked, the one that came closest to failing). Was the weak point retrieval or generation? How can you tell from the notebook's output?** _____

---The last question gave the incorrect answer since it was unanswerable one. I think the weak point here is the retrieval one. Since the answer was not present in the document the llm gave a random answer to the question which was obvious incorrect. On the other hand, generation in some answer had a problem since it was just paraphrasing the retrieved word. I think this can done with better prompting.

## Part 3: Reflection (30 pts, 250–350 words)

Answer all four:

- Huyen describes two families of retrievers: term-based and embedding-based. Which kind does the codelab use? Based on your keyword questions, where might the other kind have done better or worse?
- How did the pipeline handle your unanswerable question? What would happen in a real application if it handled that badly, and what would you change to fix it?
- The codelab was designed to work well on its own sample documents. What, if anything, got harder when you switched to yours?
- Your project evaluation plan is due next week with Milestone 1. Does your project need RAG? If so, what would the documents be, and if not, why not?

**Your reflection:**
1.The codelab used an embedding-based retriever. In my tests, it retrieved the right passages for both keyword questions: “What does ATS stand for?” and the question about the 1–5 usability score.

A term-based retriever might have worked equally well for these questions because they used exact terms and numbers from the documents. However, I cannot conclude that it would have performed better without testing it. The ATS answer was correct but unnecessarily long; that was an issue with answer generation rather than retrieval. For my paraphrase questions, embedding-based retrieval worked well even though the questions did not repeat the wording in the documents.

2.The pipeline handled my unanswerable question poorly. When I asked how many job offers the tool would generate, it produced an incorrect answer instead of explaining that the documents did not contain that information.

My initial interpretation was that retrieval failed, but the more important weakness was generation: the model answered without supporting evidence. There was no correct passage to retrieve because the answer was absent from the documents. To diagnose this more precisely, I would inspect the retrieved chunks and compare them with the generated answer.

In a real application, this could mislead users into believing that the tool guarantees job offers. I would strengthen the prompt to require answers supported by the retrieved documents and explicitly decline unsupported questions. For this question, the expected response would be: “The documents do not specify how many job offers the tool will generate.” Before deployment, I would evaluate the pipeline on additional unanswerable questions, not just questions with known answers.

3.I did not observe a major drop in performance when switching from the sample documents to my own project documents. The pipeline retrieved the right passages and generated correct answers for all four answerable questions.

However, the answers to my documents seemed more heavily paraphrased and sometimes longer than necessary. The main difficulty was therefore controlling the generated response rather than finding the relevant information. I would adjust the prompt to favor concise answers, preserve exact terms and numbers when appropriate, and avoid adding unsupported details. These five tests are encouraging, but they are not enough to establish that the pipeline works reliably across all questions.

4.
Yes, my proposed project will use RAG to ground resume tailoring in the user’s actual experience. The resume will be the source of truth, while the job description will guide retrieval; it will not serve as evidence that the user possesses a particular qualification.

The resume will be divided into smaller units, such as individual experience bullets, project descriptions, education details, and skills. The system will retrieve the information most relevant to a job posting, and the language model will rephrase and reorganize that information without introducing unsupported achievements, qualifications, or metrics.

For the Milestone 1 evaluation plan, I will assess whether the system retrieves relevant resume content, preserves factual accuracy, and produces useful tailored outputs. I will also test cases where the job description requests a qualification absent from the resume, checking that the system does not invent it. Finally, I will compare a hosted frontier model with a smaller, less expensive model to determine whether similar output quality can be achieved at lower cost.
_____

---

## Part 4: Graduate Extension — Term-Based Retrieval Comparison (20 pts)

*Graduate students required.*

In the same notebook, add a **BM25 retriever** (for example, with the `rank_bm25` library) over the same documents. Run your 4 answerable questions through it and compare which passages it retrieves against the codelab's embedding retriever.

| # | Question (short) | Embedding retriever found it? | BM25 found it? |
|---|---|---|---|
| 1 | _What does ATS stand for in the context of the project?____ | _t____ | ___f__ |
| 2 | what is the project problem statement_____ | ___f__ | _t____ |
| 3 | __Who is the initial target user of the proposed tool___ | __t___ | __t___ |
| 4 | _What 1–5 usability score will be used to evaluate the generated outputs?____ | _t____ | _t____ |


In 200–300 words: where did the two retrievers agree and disagree, and does the pattern match what Huyen predicts for keyword versus paraphrase queries? If you were building this for real, would you use one, the other, or both?

**Your analysis:** _____
The retrievers agreed on Q3 and Q4, both correctly retrieving the Target Users and Evaluation passages. These questions share distinctive vocabulary ("target user," "usability score") with exactly one passage, so lexical and semantic matching point to the same answer.

They disagreed on Q1 and Q2, in the opposite direction from Huyen's prediction. Term-based retrieval should excel on keyword queries and embeddings on paraphrases. Instead, BM25 missed Q1, a keyword query built around "ATS," which appears in only one passage, while the embedding retriever found it. On Q2, a paraphrase whose key phrase "problem statement" appears in no passage, BM25 succeeded and the embedding retriever failed.

The tiny corpus likely explains much of this. With four documents, BM25's IDF weights are unstable: words appearing in two or more passages contribute almost nothing, so rankings hinge on one or two tokens, and near-ties can be decided by document order. The Problem Statement is the first document, which may account for BM25's Q2 result. The embedding miss on Q2 is understandable too, since the question asks about a passage's role rather than its content, and "the project" is discussed in every passage. These results don't confirm Huyen's pattern, but four documents is too small a sample to contradict it either.

For a real resume tool, I would use both. Embeddings handle skills described in different words ("CI/CD" versus "deployment pipelines"), while BM25 reliably matches exact technology names like "Kubernetes." A hybrid using reciprocal rank fusion would combine these strengths.
---

## Optional (Not Graded)

If you want to go further, the rest of Day 2 is worth your time: the **Embeddings and Vector Stores whitepaper**, the summary podcast, the other two codelabs (text similarity and embedding-based classification), and the recorded livestream with Google engineers.

---

## Grading

| Component | Undergraduate | Graduate |
|---|---|---|
| Complete the RAG codelab (Part 1) | 30 pts | 20 pts |
| Make it yours (Part 2) | 40 pts | 40 pts |
| Reflection (Part 3) | 30 pts | 20 pts |
| Graduate extension (Part 4) | — | 20 pts |
| **Total** | **100 pts** | **100 pts** |

### Rubric

| Level | Criteria |
|---|---|
| **Full credit** | The codelab runs completely with outputs showing, and the pipeline summary is accurate. The notebook uses the student's own documents. All 5 questions are present with the required mix of types, and the retrieval-vs-generation diagnosis is supported by evidence from the notebook. Reflection connects the student's own results to Huyen Ch. 6. |
| **Partial credit** | The codelab is incomplete or outputs are missing. Sample documents were not replaced, or fewer than 5 questions are included, or the required question types are missing. The diagnosis is a guess without evidence. Reflection restates the chapter instead of the results. |
| **No credit** | Not submitted, the notebook link doesn't work or isn't shared, or results appear fabricated (e.g., table entries that don't match the notebook's outputs). |

---

## A Note on Scope

Your pipeline won't answer everything correctly on your own documents, and that's expected. What's being graded is whether you can look at a failure and say which part of the pipeline caused it.

Also note: **Quiz 3 is this week too.** Start the codelab early, since setup (accounts, API key, phone verification) can take longer than you'd expect.
