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
