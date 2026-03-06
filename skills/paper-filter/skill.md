# paper-filter

Filter academic papers by research interest relevance.

## Trigger

Use when given a list of papers (title, summary, keywords) to filter by relevance to specific research interests.

## Interest Areas

- LLM inference (optimization, serving, quantization, speculative decoding, KV cache, batching, latency, throughput)
- Agent (autonomous agents, tool use, planning, multi-agent, agent frameworks, agent evaluation)
- Edge LLM (on-device deployment, mobile inference, model compression, pruning, distillation, small language models, edge computing, TinyML, ONNX, CoreML, memory-efficient inference)

## Instructions

1. You will receive a JSON list of papers, each with: arxiv_id, title, summary, ai_keywords
2. Score each paper 0-10 on relevance to the interest areas above
3. Select the top 10 papers (score >= 5, sorted by score descending)
4. If fewer than 10 papers score >= 5, return however many qualify (could be 0)

## Output Format

Return ONLY a valid JSON array of selected arxiv_ids, no other text:

```json
["2603.04304", "2603.04305", "2603.04306"]
```

## Scoring Guidelines

- 10: Directly about LLM inference optimization, agent architecture, or on-device LLM deployment
- 7-9: Strongly related (e.g., reasoning with inference implications, tool-use benchmarks, model compression techniques)
- 4-6: Tangentially related (e.g., general LLM training that may impact inference, small model training)
- 0-3: Unrelated (e.g., pure vision, biology, robotics without agent aspects)
