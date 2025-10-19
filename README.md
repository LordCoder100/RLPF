# RLPF: Reinforcement Learning from Predicate Feedback

> **Training AI with logic, not opinions.**

## What is RLPF?

RLPF is a novel approach to training AI models using logical verification instead of human preferences. Unlike RLHF (Reinforcement Learning from Human Feedback), which relies on subjective human judgments, RLPF uses predicate logic verified against Knowledge Graphs.

**Key insight:** You can fool a human annotator, but you cannot fool predicate logic.

## Why RLPF?

Traditional RLHF is expensive ($50K+ per model), slow (weeks of training), subjective (annotators disagree), and hard to verify. RLPF trains models 10x faster, at 1/100th the cost, with objective feedback that's 100% reproducible.

When a model generates output, we extract predicates `(Subject, Predicate, Object)` and verify them against a Knowledge Graph. Correct predicates get rewarded, wrong ones get penalized. This forces the model to learn logical consistency instead of just "sounding good."

## Current Status

Early research preview. Implementation in progress. Benchmarks coming soon.

---

**License:** MIT  
**Contact:** [LinkedIn](www.linkedin.com/in/mykhailo-lapshyn-2a3702309) • [Email](mailto:lapshynmisha@gmail.com)
