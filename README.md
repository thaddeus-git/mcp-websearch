# MCP Web Search

MCP server providing Google web search via Bright Data API.

## What This Provides

A single tool `web_search` that allows AI agents to search Google for up-to-date information.

## Prerequisites

- Python 3.10+
- Bright Data API token ([get one here](https://brightdata.com))

## Installation

```bash
pip install git+https://github.com/thaddeus-git/mcp-websearch.git
```

Verify installation:
```bash
mcp-websearch --help
```

## Configuration

### Step 1: Get Bright Data API Token

1. Sign up at [brightdata.com](https://brightdata.com)
2. Get your API token from the dashboard

### Step 2: Set Environment Variable

```bash
export BRIGHTDATA_API_TOKEN=your_token_here
```

For persistence, add to `~/.zshrc` or `~/.bashrc`.

## Adding to AI Agents

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "websearch": {
      "command": "mcp-websearch",
      "env": {
        "BRIGHTDATA_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### OpenCode

Add to your OpenCode MCP configuration:

```json
{
  "mcpServers": {
    "websearch": {
      "command": "mcp-websearch",
      "env": {
        "BRIGHTDATA_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Cursor / Other MCP Clients

Use the same pattern - add `mcp-websearch` as a command with `BRIGHTDATA_API_TOKEN` in env.

## Tool Reference

### web_search

Search Google for information.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| query | string | Yes | - | Search query |
| location | string | No | "United States" | Geographic location for results |
| language | string | No | "en" | Language code |
| num_results | integer | No | 10 | Maximum results to return |

**Example request:**
```json
{
  "query": "latest Python 3.12 features",
  "location": "United States",
  "num_results": 5
}
```

**Example response:**
```
1. What's New in Python 3.12
   https://docs.python.org/3.12/whatsnew/3.12.html
   Python 3.12 introduces improved error messages, performance optimizations...

2. Python 3.12 Release Notes
   https://www.python.org/downloads/release/python-3120/
   Official release notes for Python 3.12.0...
```

## Development

```bash
git clone https://github.com/thaddeus-git/mcp-websearch.git
cd mcp-websearch
pip install -e .
```

## Security

- Never commit your API token to git
- The `.env` file is gitignored for local development
- Store tokens in environment variables or secure secret managers
