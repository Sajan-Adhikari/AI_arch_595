import math
import os
import re
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# The corpus: Northwind Inc. employee handbook (fictional)
# Each document is one "chunk" for now. Friday we talk about chunking.
# ---------------------------------------------------------------------------
DOCS = {
    "pto": "Paid time off (PTO). Full-time employees accrue 18 PTO days per calendar year, "
           "earned at 1.5 days per month. Up to 5 unused PTO days roll over into the next year. "
           "Request PTO in the HR portal at least two weeks ahead for absences longer than three days.",
    "holidays": "Company holidays. Northwind observes 10 paid company holidays each year, "
                "published in the HR portal every December. Holidays do not count against your PTO balance.",
    "sick": "Sick leave. Sick leave is separate from PTO. Employees receive 6 sick days per year, "
            "which do not roll over. A doctor's note is required for absences longer than three consecutive days.",
    "parental": "Parental leave. Birth, adoptive and foster parents receive 12 weeks of fully paid leave, "
                "usable any time in the first year after the child arrives. Notify HR 30 days before leave begins when possible.",
    "travel": "Travel booking. Book flights and hotels through the Northwind travel portal. "
              "For business trips longer than five nights you may book a vacation rental instead of a hotel "
              "if the nightly cost is lower. Vacation rental bookings need manager approval.",
    "expenses": "Expense reports. Submit expense reports in the finance portal within 30 days of the purchase. "
                "Attach an itemized receipt for any expense over $25. Late reports may not be reimbursed.",
    "remote": "Home office stipend. Remote employees are eligible for a one-time $500 home office stipend "
              "for a desk, chair or monitor. Claim it through an expense report within your first 90 days.",
    "contractors": "Contractor eligibility. Contractors are not eligible for the home office stipend, "
                   "company health benefits, or PTO. Contractor equipment is provided by the staffing agency.",
    "equipment": "Laptop refresh. Employees receive a new laptop every three years. "
                 "IT emails you when your laptop is due for replacement; return the old laptop within 14 days.",
    "passwords": "Password policy. Passwords must be at least 14 characters and are rotated every 90 days. "
                 "IT will never ask for your password by email, chat or phone.",
    "benefits": "Benefits enrollment. Open enrollment for health, dental and vision plans runs November 1-15. "
                "New hires have 30 days from their start date to enroll.",
    "reviews": "Performance reviews. Reviews happen twice a year, in April and October. "
               "Employees write a self-assessment and meet with their manager to set goals for the next cycle.",
}

# ---------------------------------------------------------------------------
# Test questions. The last field is the doc that SHOULD come back.
# TODO 1 (Monday): replace each None with the doc id that answers the question.
#                  Read the corpus above to decide. This is your test set.
# ---------------------------------------------------------------------------
QUESTIONS = [
    ("How long do I have to submit an expense report?", expenses),
    ("How many vacation days do I get each year?", holidays),
    ("Can contractors get the home office stipend?", contractors),
    ("When will my computer be replaced?", equipment),
    ("How much paid leave do new parents get?",parental)
]

# ---------------------------------------------------------------------------
# Retrieval: BM25 (term-based search). Already written for you.
# ---------------------------------------------------------------------------
STOPWORDS = set("a an the and or of to in on for is are be do does i my me you your we "
                "our it its at by with how what when can will get each any this that from "
                "much many long".split())


def tokenize(text):
    words = re.findall(r"[a-z0-9$]+", text.lower())
    return [w for w in words if w not in STOPWORDS]


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.ids = list(docs)
        self.tokens = {d: tokenize(docs[d]) for d in self.ids}
        self.k1, self.b = k1, b
        self.avg_len = sum(len(t) for t in self.tokens.values()) / len(self.ids)
        df = Counter(w for t in self.tokens.values() for w in set(t))
        n = len(self.ids)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def score(self, query, doc_id):
        tf = Counter(self.tokens[doc_id])
        dl = len(self.tokens[doc_id])
        s = 0.0
        for w in tokenize(query):
            if w not in tf:
                continue
            num = tf[w] * (self.k1 + 1)
            den = tf[w] + self.k1 * (1 - self.b + self.b * dl / self.avg_len)
            s += self.idf[w] * num / den
        return s

    def search(self, query, k=3):
        scored = [(d, self.score(query, d)) for d in self.ids]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


# ---------------------------------------------------------------------------
# TODO 2 (Monday): return True if expected_id is among the top-k results.
#   results looks like: [("pto", 3.2), ("sick", 1.1), ("holidays", 0.4)]
# ---------------------------------------------------------------------------
def hit_at_k(results, expected_id, k=3):
    # your code here (2-3 lines)
    raise NotImplementedError("TODO 2: write hit_at_k")


# ---------------------------------------------------------------------------
# Generation (Friday)
# ---------------------------------------------------------------------------
def call_llm(prompt, model="gpt-4o-mini"):
    """Send one prompt, return the text. Swap this out if you use another provider."""
    from openai import OpenAI
    client = OpenAI()  # reads OPENAI_API_KEY from the environment
    r = client.chat.completions.create(
        model=model,
        temperature=0,  # hold sampling still so you're testing retrieval + prompt, not luck
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip()


# TODO 3 (Friday): build the prompt the model sees.
#   Use what you learned in Chapter 5 and the prompting course:
#   - put the retrieved docs in clearly marked blocks
#   - tell the model to answer ONLY from those docs
#   - tell it what to say if the docs don't contain the answer
#   - ask it to name which doc id it used
def build_prompt(question, retrieved_ids):
    context = "\n\n".join(DOCS[d] for d in retrieved_ids)
    return f"{context}\n\n{question}"   # replace this naive version


def answer(question, retriever, k=3):
    results = retriever.search(question, k=k)
    ids = [d for d, _ in results]
    prompt = build_prompt(question, ids)
    if not os.environ.get("OPENAI_API_KEY"):
        return ids, "[no API key set - dry run]\n--- prompt the model would see ---\n" + prompt
    return ids, call_llm(prompt)


# ---------------------------------------------------------------------------
def main():
    generate = "--generate" in sys.argv
    retriever = BM25(DOCS)
    print(f"Corpus: {len(DOCS)} docs\n")
    hits = 0
    labeled = 0
    for q, expected in QUESTIONS:
        results = retriever.search(q, k=3)
        shown = ", ".join(f"{d} ({s:.2f})" for d, s in results)
        print(f"Q: {q}")
        print(f"   top 3: {shown}")
        if expected is not None:
            labeled += 1
            try:
                ok = hit_at_k(results, expected)
                hits += ok
                print(f"   expected: {expected}  ->  {'HIT' if ok else 'MISS'}")
            except NotImplementedError as e:
                print(f"   ({e})")
        if generate:
            _, ans = answer(q, retriever)
            print("   answer:", ans.replace("\n", "\n           "))
        print()
    if labeled:
        print(f"hit@3: {hits}/{labeled}")
    else:
        print("Label your questions (TODO 1) to get a hit@3 score.")


if __name__ == "__main__":
    main()