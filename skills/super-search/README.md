# super-search

**Level:** configure — set API keys for the search tools you want to use

A unified search router. Detects what you're looking for and routes to the best tool automatically, with graceful fallback.

## Routing logic

| Use case | Primary tool | Fallback |
|----------|-------------|---------|
| General web search | Serper (Google) | Tavily |
| Article content extraction | WebFetch | Firecrawl |
| WeChat / social media | web-access (CDP) | — |
| GitHub search | `gh` CLI | Serper |
| Academic papers | Serper scholar | WebFetch |
| Video content | Serper video | — |

## Setup: API keys

Set whichever you have. The skill degrades gracefully if a tool isn't available:

```bash
export SERPER_API_KEY="..."      # https://serper.dev — 2500 free queries
export FIRECRAWL_API_KEY="..."   # https://firecrawl.dev — pay-as-you-go
export TAVILY_API_KEY="..."      # https://tavily.com — alternative to Serper
```

## Adding internal platforms

In `references/scene-commands.md`, add your own routing rules:

```markdown
## Scene X: [Your Internal Platform]
Route to [your tool] when URL matches [pattern].
```

## Installation

```bash
cp -r super-search ~/.claude/skills/
```
