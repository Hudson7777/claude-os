# model-coding-benchmark

**Level:** 🔧 configure — requires `claude` CLI (standard for all Claude Code users)

Benchmark multiple LLMs on real coding tasks. Runs 6 standardized tasks (code generation, tool use, debug, code understanding, refactoring, end-to-end), times each model, uses blind evaluation by a third LLM to score results, and outputs a ranked report.

## Design

- **Blind evaluation:** Models are anonymized (X/Y/Z) before scoring to prevent evaluator bias
- **Ground truth verification:** Tasks 2, 3, 5, 6 have `verify_*.py` scripts that objectively check correctness
- **Cross-evaluator consistency:** Spearman correlation matrix measures evaluator agreement — results below 0.5 are flagged
- **Tiered tasks:** 6 core tasks (historically comparable) + optional extended tasks

## Prerequisites

- Claude Code CLI (`claude`) installed
- Python 3.9+
- Sufficient token budget: ~6 tasks × N models × agent-mode cost per task (~1–3 hours total)

## Configuration

Set `CLAUDE_CLI` env var if your CLI is not `claude`:

```bash
export CLAUDE_CLI=/path/to/your/claude-cli
```

## Usage

Ask Claude Code: `benchmark claude-opus-4-5 claude-sonnet-4-5 gpt-4o`

Or: `评测模型编程能力 opus sonnet gemini-2.5-pro`

## Sample Results

| Rank | Model | Avg Score | T1 Gen | T2 Debug | T3 Tool | T4 Read | T5 Refactor | T6 E2E |
|------|-------|-----------|--------|----------|---------|---------|-------------|--------|
| 1 | claude-opus-4-7 | 87.3 | 92 | 85 | 90 | 88 | 84 | 85 |
| 2 | claude-sonnet-4-6 | 81.2 | 88 | 79 | 84 | 82 | 78 | 76 |
| 3 | gpt-4o | 76.8 | 84 | 74 | 78 | 79 | 73 | 71 |

*Sample only — run your own benchmark for current results.*

## Installation

```bash
cp -r model-coding-benchmark ~/.claude/skills/
```
