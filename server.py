import asyncio
import os
from typing import Optional
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import httpx

# The Forensic Vault Distiller MCP Server
# Branded for the "Master Specialist" workflow

server = Server("forensic-vault-distiller")

BUFFER_API_BASE = "https://api.bufferapp.com/1"
BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for the Forensic Vault Distiller.
    """
    return [
        types.Tool(
            name="distill_vault_item",
            description="Analyzes a local technical vault file and distills it into social content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the markdown file in the vault."},
                    "platform": {"type": "string", "enum": ["linkedin", "twitter", "mastodon"], "description": "Target social platform."}
                },
                "required": ["file_path", "platform"],
            },
        ),
        types.Tool(
            name="buffer_list_profiles",
            description="Lists all social profiles connected to the Buffer account.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="buffer_schedule_update",
            description="Schedules a post via Buffer.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The content of the post."},
                    "profile_ids": {"type": "array", "items": {"type": "string"}, "description": "List of Buffer profile IDs."},
                    "now": {"type": "boolean", "description": "Whether to post immediately."}
                },
                "required": ["text", "profile_ids"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool calls for vault distillation and Buffer integration.
    """
    if not arguments:
        raise ValueError("Missing arguments")

    if name == "distill_vault_item":
        # Placeholder for vault reading logic
        file_path = arguments.get("file_path")
        return [
            types.TextContent(
                type="text",
                text=f"Forensic Analysis: Distilling {file_path}. (Implementation in progress: Reading local vault files and generating high-signal insights...)"
            )
        ]

    elif name == "buffer_list_profiles":
        if not BUFFER_ACCESS_TOKEN:
            return [types.TextContent(type="text", text="Error: BUFFER_ACCESS_TOKEN not found in environment.")]
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BUFFER_API_BASE}/profiles.json",
                params={"access_token": BUFFER_ACCESS_TOKEN}
            )
            return [types.TextContent(type="text", text=response.text)]

    elif name == "buffer_schedule_update":
        # Logic to call Buffer API /updates/create.json
        return [
            types.TextContent(
                type="text",
                text="Post successfully queued for Buffer. (Mock response while in 'Actively Building' phase)"
            )
        ]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="forensic-vault-distiller",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
