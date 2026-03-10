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
        async with BrightDataClient(token=token) as client:
            result = await client.search.google(
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
            lines.append(f"   {item['url']}")
            lines.append(f"   {item.get('description', '')}")
            lines.append("")

        return [TextContent(type="text", text="\n".join(lines))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def main():
    import asyncio

    asyncio.run(run())
