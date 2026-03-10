# Bright Data Web Search MCP Server Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a minimal MCP server that exposes Google web search via Bright Data API.

**Architecture:** Single-file Python MCP server wrapping brightdata-sdk's Google search. The server exposes one `web_search` tool with query, location, language, and num_results parameters.

**Tech Stack:** Python 3.10+, mcp package, brightdata-sdk

---

### Task 1: Project Setup

**Files:**
- Create: `pyproject.toml`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "mcp-websearch"
version = "0.1.0"
description = "MCP server for web search using Bright Data API"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
    "brightdata-sdk>=2.0.0",
]

[project.scripts]
mcp-websearch = "mcp_websearch:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 2: Create package structure**

Run: `mkdir -p src/mcp_websearch && touch src/mcp_websearch/__init__.py`

**Step 3: Install dependencies**

Run: `pip install -e .`

Expected: Dependencies installed successfully

**Step 4: Commit**

```bash
git add pyproject.toml src/
git commit -m "chore: initialize project with dependencies"
```

---

### Task 2: Create MCP Server

**Files:**
- Create: `src/mcp_websearch/server.py`
- Modify: `src/mcp_websearch/__init__.py`

**Step 1: Write the MCP server**

```python
import os
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from brightdata import BrightDataClient

server = Server("websearch")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="web_search",
            description="Search Google for information",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "location": {
                        "type": "string",
                        "description": "Geographic location",
                        "default": "United States",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language code",
                        "default": "en",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Max results to return",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name != "web_search":
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    token = os.environ.get("BRIGHTDATA_API_TOKEN")
    if not token:
        return [TextContent(type="text", text="Error: BRIGHTDATA_API_TOKEN not set")]

    try:
        client = BrightDataClient(token=token)
        result = client.search.google(
            query=arguments["query"],
            location=arguments.get("location", "United States"),
            language=arguments.get("language", "en"),
            num_results=arguments.get("num_results", 10),
        )

        if not result.success:
            return [TextContent(type="text", text=f"Search failed: {result.error}")]

        if not result.data:
            return [TextContent(type="text", text="No results found")]

        lines = []
        for item in result.data:
            lines.append(f"{item['position']}. {item['title']}")
            lines.append(f"   {item['link']}")
            lines.append(f"   {item.get('snippet', '')}")
            lines.append("")

        return [TextContent(type="text", text="\n".join(lines))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    import asyncio
    asyncio.run(run())
```

**Step 2: Update __init__.py**

```python
from .server import main

__all__ = ["main"]
```

**Step 3: Verify syntax**

Run: `python -c "from mcp_websearch import main; print('OK')"`

Expected: `OK`

**Step 4: Commit**

```bash
git add src/mcp_websearch/
git commit -m "feat: add MCP server with web_search tool"
```

---

### Task 3: Add Environment Configuration

**Files:**
- Create: `.env.example`

**Step 1: Create .env.example**

```
BRIGHTDATA_API_TOKEN=your_token_here
```

**Step 2: Create .gitignore**

```
.env
__pycache__/
*.pyc
.venv/
```

**Step 3: Commit**

```bash
git add .env.example .gitignore
git commit -m "chore: add environment config template"
```

---

### Task 4: Add README Documentation

**Files:**
- Create: `README.md`

**Step 1: Write README**

```markdown
# MCP Web Search

MCP server for Google web search using Bright Data API.

## Installation

```bash
pip install -e .
```

## Configuration

Set your Bright Data API token:

```bash
export BRIGHTDATA_API_TOKEN=your_token_here
```

Or create a `.env` file:

```
BRIGHTDATA_API_TOKEN=your_token_here
```

## Usage

Run the MCP server:

```bash
mcp-websearch
```

### Claude Desktop Integration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "websearch": {
      "command": "mcp-websearch"
    }
  }
}
```

## Tool: web_search

Search Google for information.

**Parameters:**
- `query` (string, required): Search query
- `location` (string, optional): Geographic location, default "United States"
- `language` (string, optional): Language code, default "en"
- `num_results` (integer, optional): Max results, default 10

**Example:**
```json
{
  "query": "best Python web frameworks 2024",
  "location": "United States",
  "num_results": 5
}
```
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with installation and usage"
```

---

### Task 5: Final Verification

**Step 1: Run MCP inspector to verify**

Run: `npx @modelcontextprotocol/inspector mcp-websearch`

Expected: Inspector opens, shows `web_search` tool in tools list

**Step 2: Test with a search query**

In inspector, call `web_search` with:
```json
{"query": "test"}
```

Expected: Returns search results or appropriate error message

**Step 3: Final commit (if any changes)**

```bash
git status
# If clean, no action needed
```
