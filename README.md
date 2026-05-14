# AI PM Lab

Goal: Build a AI PM product in small, shippable slices.

## Current MVP Idea
**Insight2Spec** — Convert raw user feedback (tickets, reviews, support chats) into:
1. clustered themes
2. opportunity statements
3. draft PRD sections
4. experiment ideas

## Why this product
- Extremely PM-relevant (discovery, prioritization, PRD quality)
- Strong LLM fit (summarization, clustering, synthesis)
- Teaches practical AI product engineering (prompting, evals, latency/cost/quality tradeoffs)

## MVP Scope (v0)
- Upload/copy feedback text
- Generate top themes + confidence
- Generate 3 opportunity statements
- Generate draft PRD outline
- Save run history as JSON

## Stack
- Python 3.12
- FastAPI backend
- OpenRouter for model calls
- Simple local JSON storage for now

## Learning outcomes for Asif
- Prompt design and iteration
- Structured output validation
- Failure handling and guardrails
- Evaluation loops for quality
- Shipping incrementally with measurable outcomes

## Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
