# Bright Data Web Search MCP Server Design

## Overview

Minimal MCP server exposing Google web search via Bright Data API.

## Architecture

```
Claude/AI Agent
     │
     ▼
MCP Server (Python)
     │
     ▼
brightdata-sdk
     │
     ▼
Bright Data API → Google Search
```

## Components

| File | Purpose |
|------|---------|
| `src/server.py` | MCP server with `web_search` tool |
| `pyproject.toml` | Dependencies: `mcp`, `brightdata-sdk` |
| `.env` | `BRIGHTDATA_API_TOKEN` storage |
| `README.md` | Installation and usage docs |

## Tool Definition

**Name:** `web_search`

**Description:** Search Google for information

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query |
| `location` | string | No | "United States" | Geographic location |
| `language` | string | No | "en" | Language code |
| `num_results` | integer | No | 10 | Max results to return |

## Data Flow

1. MCP receives tool call with query + options
2. Server initializes `BrightDataClient` (reads token from env)
3. Calls `client.search.google(query, location, language, num_results)`
4. Formats response as MCP content blocks

## Response Format

Returns list of results containing:
- position, title, link, snippet
- displayed_link, cached_page_url

## Error Handling

| Error | Response |
|-------|----------|
| API auth failure | Clear error about token |
| Rate limit | Error with retry suggestion |
| Network timeout | Propagate with context |
| Empty results | "No results found" message |

## Testing

Manual testing via MCP inspector:
```bash
npx @modelcontextprotocol/inspector python src/server.py
```

## Claude Desktop Integration

```json
{
  "mcpServers": {
    "websearch": {
      "command": "python",
      "args": ["-m", "mcp_websearch"]
    }
  }
}
```
