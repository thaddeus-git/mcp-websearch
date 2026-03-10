# MCP Web Search

MCP server for Google web search using Bright Data API.

## Installation

### For users
```bash
pip install git+https://github.com/thaddeus/mcp-websearch.git
```

### For development
```bash
git clone https://github.com/thaddeus/mcp-websearch.git
cd mcp-websearch
pip install -e .
```

## Configuration

Set your Bright Data API token as an environment variable:

```bash
export BRIGHTDATA_API_TOKEN=your_token_here
```

Or add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export BRIGHTDATA_API_TOKEN=your_token_here
```

**Never commit your API token to git.** The `.env` file is for local development only.

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
