# Project Overview
- **Purpose**: Node.js/TypeScript agent that automates collection and structured reporting of n8n case studies (web search → crawl → LLM extraction → CSV/Markdown/Notion outputs).
- **Key features**: 20-column schema, ROI-focused summaries, deduplication, multiple export formats, optional Notion sync.
- **Architecture**: CLI entry in `src/cli.ts`; functional modules in `src/modules` for search/fetch/extraction/normalization/output; shared types under `src/types`; prompts under `src/prompts`; utilities in `src/utils`.
- **External services**: OpenAI or Anthropic for LLM extraction; optional Notion API integration.
- **Runtime requirements**: Node.js >= 18, environment-configured API keys.