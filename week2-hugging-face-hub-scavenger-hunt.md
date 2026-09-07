# Week 2 Assignment: Hugging Face Hub Scavenger Hunt

**Graduate Extension Included**

## Overview

Same fields I walked through in Monday's demo: parameter count/size, architecture family, license, tokenizer/vocab size. Pick 3 models, record those fields, run a tokenizer comparison across languages, check context window against this week's reading, then write a short reflection tying it back to a real project decision.

*Same order I used in Monday's demo: parameter count/size near the top of the card, architecture family in the description, license in the metadata, tokenizer/vocab size in tokenizer_config.json (or just test the model directly in a tokenizer tool).*

## How to Submit

1. Fill out this file directly (replace the `_____` placeholders and bracketed instructions with your answers).
2. Commit this file to the same GitHub repo you created for Assignment 1, using this exact filename: `week2-tokenizer-model-comparison.md`.
3. Push your commit, then submit a link to the file as instructed for this course.

---

## Part 1: Choose 3 Models

1. Go to huggingface.co/models.
2. Pick 3 models that actually make a meaningful comparison — not three near-identical variants of the same model. At least 2 different organizations/families, ideally a mix of sizes (small under ~3B, mid-size, larger).
3. Pick based on your own interests. Got a project idea? Use models you'd actually consider for it.

## Part 2: Record Your Findings

Where to find each field, if you get stuck:
- **Parameter count / size** — near the top of the card, sometimes right in the model's name (e.g. "7B" = 7 billion parameters).
- **Architecture family** — in the description text, or config.json under "Files and Versions."
- **License** — shown as a tag near the top, and always in the YAML metadata block.
- **Tokenizer / vocab size** — check tokenizer_config.json or config.json under "Files and Versions" for vocab_size. Can't find it? Note "not published" — that's a useful observation on its own.

| Model | Link | Parameter count / size | Architecture family | License | Tokenizer / vocab size |
|---|---|---|---|---|---|

| Model 1: deepseek-ai/DeepSeek-R1| https://huggingface.co/deepseek-ai/DeepSeek-R1| 685B params |DeepseekV3ForCausalLM|MIT License|129280|

| Model 2:  GPT-2 |https://huggingface.co/openai-community/gpt2|0.1B params |GPT2LMHeadModel| MIT License| 50257|

| Model 3: Qwen/Qwen2.5-72B |https://huggingface.co/Qwen/Qwen-72B| 72B params | Qwen2ForCausalLM |Qwen LICENSE AGREEMENT | 152064 |

## Part 3: Tokenizer Comparison Exercise

Use a tokenizer tool that supports multiple model families (tiktokenizer.vercel.app works) and test all 3 models with the same three inputs:

- **Test sentence (use this exact sentence for all 3 models):** "I love learning about artificial intelligence."
- **Language A:** translate the test sentence into a Latin-script European language — Spanish, French, German, whatever. Same translation across all 3 models.
- **Language B:** translate it into a non-Latin-script language — Japanese, Arabic, Korean, Hindi, your call. Same translation across all 3 models.

| Model | Test sentence tokens | Language A used | Language A tokens | Language B used | Language B tokens |
|---|---|---|---|---|---|
| Model 1 | ___6__ | __German___ | ___15__ | __Nepali___ | __25___ |
| Model 2 | ___6__ | __German___ | __25___ | _Nepali____ | __73___ |
| Model 3 | ___6__ | ___German__ | __16___ | _Nepali____ | __38___ |

## Part 4: Context Window Check

For each model, look up its context window — the max tokens it can handle in one request. Usually on the card or in the config file.

| Model | Context window (tokens) | Source (URL or where you found it) |
|---|---|---|
| Model 1 | __163840___ | https://huggingface.co/deepseek-ai/DeepSeek-R1/blob/main/config.json |
| Model 2 | __1024___ | https://huggingface.co/openai-community/gpt2/blob/main/config.json |
| Model 3 | __131072___ | https://huggingface.co/Qwen/Qwen2.5-72B/blob/main/config.json |

**Now do the math for at least one model:** Chapter 2 is roughly 62 pages. Using ~500–600 words/page and ~0.75 words/token, estimate the total token count. Would the whole reading fit in that model's context window in one API call, with room left for a response? Show your work and your conclusion.

Let's do for deepseek-ai. Roughly 62 pages with 600 words per page makes 37200 word count. That equals 49600 token count. It's context window is 163840 which is 3 times the total token count. So it has fair room left for the response in the context length. 

*I used AI to search through this answer. Many hosted api provider cap their context length lower than the architecture max. Every platform has their limitation. But I didn't find the exact reason behind this.*

## Part 5: Comparison Reflection (300–400 words)

Answer all four:

- What's the biggest difference between your 3 models — size, architecture, license, tokenizer, something else?
- If you had to pick one for a real project, which one and why? Don't just say "the biggest one" — factor in license restrictions and whether the project actually needs that much size.
- Would your pick change for a multilingual or cost-sensitive use case, based on what you found in Part 3? Why or why not?
- Would your pick change for a use case involving long documents (full reports, long transcripts), based on the context window math in Part 4? Why or why not?

> [Write your reflection here]
1.)
License is the sharpest divide,but it's tied to the architecture/scale:
DeepSeek-R1: 685B total params,Mixture-of-Experts, MIT license — fully permissive, no usage caps.
Qwen2.5-72B: 72B dense params, Tongyi Qianwen License — commercial use allowed but requires a separate Alibaba Cloud agreement for products exceeding 
100 million monthly active users, so it's not truly unrestricted. 
GPT-2: 124M dense params, Modified MIT — permissive but the model is small enough that license almost doesn't matter; capability is the real constraint.

2.)
For mostly real-world projects today,I would pick Qwen2.5-72B.
The DeepSeek-R1 is a reasoning-specialized model;its 685B size (even at 37B active) needs serious multi-GPU infrastructure to self-host, and its strength (long chain-of-thought reasoning) is overkill for typical production tasks like chat, summarization, or RAG.
GPT-2 is too weak for a modern product — 124M params can't reliably follow instructions or handle nuanced tasks.
Qwen2.5-72B is dense, well-documented, strong on standard benchmarks, and easier to deploy at moderate scale. Its license is a real friction point, but only if you cross 100M MAU.
If we need complex multistep reasoning like for math,code etc and prepared for the infra cost, Deepseek MIT lisence is the safest and most favourable one for the
long term goals.

3.)
My pick would shift toward Qwen2.5-72B even more strongly here, or down to a smaller Qwen/GPT-2-class model if cost is the dominant constraint.
Qwen2.5 was trained with multilingual support for over 29 languages, including Chinese, English, French, Spanish, Portuguese, German, Italian, Russian, Japanese, Korean, Vietnamese, Thai, Arabic, and more — genuinely built for multilingual coverage.
GPT-2 was trained almost entirely on English web text, so it's a poor multilingual choice regardless of cost.
DeepSeek-R1 has decent multilingual ability but its reasoning-heavy generation style (long chain-of-thought before answering) burns far more tokens per response, which is a real cost driver at scale — a bad fit if you're cost-sensitive.
If cost is the only constraint and quality bar is low, GPT-2 is the cheapest to run (tiny, fast, no GPU cluster needed) — but only for narrow, low-stakes tasks.

4.)
This is where the GPT-2 get eliminates outright, and it reshapes the DeepSeek-R1 vs. Qwen2.5 tradeoff:
GPT-2's context window is pretrained on a very large corpus of English data but architecturally limited to 1,024 tokens — roughly 700-800 words. That can't hold a full report or transcript; it's disqualifying for this use case.
Qwen2.5-72B supports a 131k tokens context window, and DeepSeek-R1 similarly supports around 128K tokens — both comfortably fit long documents (a 128K-token window is roughly 90,000-100,000 words)
Given equal context length, the deciding factor becomes reasoning depth vs. cost: DeepSeek-R1 is stronger for documents requiring multi-step synthesis or cross-referencing (e.g., legal/financial analysis across a long report), but its chain-of-thought generation means higher token cost and slower responses at that context length. Qwen2.5-72B is the more cost-efficient choice for straightforward long-document tasks like summarization or extraction where deep multi-step reasoning isn't the bottleneck.

So my pick would flex based on task depth: Qwen2.5-72B for cost-efficient long-document processing, DeepSeek-R1 if the long document requires heavy analytical reasoning.

## Part 6: Graduate Extension — Paper / Technical Report Analysis (300–400 words)

*Graduate students required.*

Pick one of your 3 models that has a linked paper or technical report on its card (most do). Read enough of it to answer:

- One real detail from the paper that's not on the model card — training data composition, a specific benchmark, a stated limitation, whatever you find.
- At least one limitation or tradeoff the authors admit to themselves.
- Your own take: does reading the paper change how much you'd trust this model for a real project vs. just reading the card? Why or why not?

> [Write your analysis here]
DeepSeek-R1
1.)
A particularly interesting detail is how DeepSeek-R1 was trained to improve reasoning.
The researchers first experimented with DeepSeek-R1-Zero, which was trained using large-scale reinforcement learning without supervised fine-tuning first. They found that the model spontaneously developed behaviors such as self-verification, reflection, and exploring alternative approaches. However, R1-Zero also produced problems such as repetitive responses, poor readability, and mixing languages.
For the final DeepSeek-R1, they therefore added thousands of “cold-start” examples before reinforcement learning. They then used multiple stages involving RL, rejection sampling, and supervised fine-tuning.
Another specific detail I found interesting: during RL, they used a language-consistency reward to discourage the model from mixing languages. The authors explicitly say this reward caused a slight degradation in model performance, but they kept it because it made responses more readable and aligned better with human preferences.

2.)Limitation/tradeoff 
One important limitation is that DeepSeek-R1 was not extensively optimized for software-engineering tasks.
The authors explain that software-engineering evaluations take a long time, which makes large-scale RL expensive and inefficient. Consequently, DeepSeek-R1 did not show a huge improvement over DeepSeek-V3 on software-engineering benchmarks.
Another interesting limitation is prompt sensitivity. The authors found that few-shot prompting consistently degraded R1's performance. They recommend describing the problem directly and specifying the desired output format using zero-shot prompting instead.There's also a practical tradeoff: the second RL stage had to reduce the temperature from the earlier setting because higher temperatures produced incoherent generations.

3.)Yes,after reading the paper it has changed in some way. Before reading the paper, I would mainly trust DeepSeek-R1 because of its reported benchmark performance. After reading the paper, I have more confidence in it as a reasoning model, because the authors explain why they designed the training pipeline the way they did and openly describe several failures encountered during development.In particular, I think the fact that they acknowledge things like:language mixing,
poor readability,prompt sensitivity,reward hacking,limited improvement on software-engineering tasks,makes the report more useful than a model card that only emphasizes benchmark scores. Personally rewarding the model against mixing the language in order to improve the reasoning feels exiciting to me.

## Grading (10 pts total)

| Component | Undergrad | Grad |
|---|---|---|
| Findings table (Part 2, incl. tokenizer field) | 3 pts | 3 pts |
| Tokenizer comparison exercise (Part 3) | 2 pts | 1 pt |
| Context window check (Part 4) | 2 pts | 1 pt |
| Comparison reflection (Part 5) | 3 pts | 2 pts |
| Graduate extension (Part 6) | — | 3 pts |
| **Total** | **10 pts** | **10 pts** |

*If a model's license, architecture, or vocab size isn't clearly labeled, say so in your reflection — not every card is well documented, and noticing that is a useful takeaway on its own.*
