---
title: "Codex MCP Setup (mirrored from Claude)"
type: setup-guide
status: active
created: "2025-08-30"
updated: "2025-08-30"
tags:
  - "documentation/setup"
  - "setup/configuration"
---

# Codex MCP Setup (mirrored from Claude)

This workspace includes a helper to mirror your existing Claude Desktop MCP server setup for use with Codex CLI.

## Generate config from Claude

1) Run the generator (reads your Claude config and writes local files):

```
node scripts/generate-codex-mcp-config.mjs
```

This creates:
- `codex.mcp.local.json` — MCP servers copied from Claude
- `.env.codex.local` — exported environment variables gathered from each server

Note: These files are gitignored by default.

## Using with Codex

- Load API keys into your shell:

```
source ./.env.codex.local
```

- Point Codex to the MCP config file using your CLI’s mechanism for MCP server configuration. Many MCP-compatible clients accept a JSON with a top-level `mcpServers` object of the same shape as Claude Desktop. If Codex supports a flag or config path for this, supply `codex.mcp.local.json`.

If you’d like, share how your Codex CLI expects MCP configuration (flag, env var, or config path), and I can wire it up precisely.

## Safety
- No secrets are committed to git; they remain local.
- You can re-run the generator whenever you update Claude’s MCP servers.

## Troubleshooting
- If `claude_desktop_config.json` is not found, confirm the path:
  `~/Library/Application Support/Claude/claude_desktop_config.json`
- After changing `.env.codex.local`, re-run `source ./.env.codex.local` in active shells.

---

## 関連ドキュメント

### セットアップ・設定
- [[bybit_mcp_setup_log]]

