import asyncio
import os
from pathlib import Path
from typing import Optional
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

server = Server("forensic-vault-distiller")

BUFFER_GRAPHQL_ENDPOINT = "https://api.buffer.com"
BUFFER_ACCESS_TOKEN = os.environ.get("BUFFER_ACCESS_TOKEN")
VAULT_PATH = Path(os.environ.get("VAULT_PATH", "./vault"))

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="distill_vault_item",
            description="Reads a local forensic vault file and generates a high-signal social media draft.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_name": {"type": "string", "description": "The name of the markdown file (e.g., debugging-gtm-engine.md)."},
                    "platform": {"type": "string", "enum": ["linkedin", "x", "mastodon"], "description": "Target social platform."}
                },
                "required": ["file_name", "platform"],
            },
        ),
        types.Tool(
            name="buffer_list_organizations",
            description="Fetches organizations connected to your Buffer account via GraphQL.",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="buffer_create_post",
            description="Creates a post draft in a specific Buffer organization.",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization_id": {"type": "string", "description": "The target organization ID."},
                    "text": {"type": "string", "description": "The post content."},
                    "channel_ids": {"type": "array", "items": {"type": "string"}, "description": "List of channel IDs to post to."}
                },
                "required": ["organization_id", "text", "channel_ids"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    if not arguments:
        raise ValueError("Missing arguments")

    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    if name == "distill_vault_item":
        file_name = arguments.get("file_name")
        platform = arguments.get("platform")
        file_path = VAULT_PATH / file_name

        if not file_path.exists():
            return [types.TextContent(type="text", text=f"Error: Vault file '{file_name}' not found.")]

        content = file_path.read_text()
        
        distillation_prompt = (
            f"SYSTEM: You are the 'Master Specialist' AI. \n"
            f"SOURCE: \n{content}\n\n"
            f"TASK: Distill into a {platform} post focusing on forensic technical value."
        )

        return [types.TextContent(type="text", text=distillation_prompt)]

    elif name == "buffer_list_organizations":
        query = """
        query GetOrganizations {
          account {
            organizations {
              id
            }
          }
        }
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(BUFFER_GRAPHQL_ENDPOINT, json={"query": query}, headers=headers)
            return [types.TextContent(type="text", text=response.text)]

    elif name == "buffer_create_post":
        # Placeholder for GraphQL mutation (following their developer roadmap/docs)
        org_id = arguments.get("organization_id")
        text = arguments.get("text")
        return [
            types.TextContent(
                type="text",
                text=f"Request received to create post for Org {org_id}. (Mutation implementation in progress based on Buffer's GraphQL roadmap)."
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            InitializationOptions(
                server_name="forensic-vault-distiller",
                server_version="0.1.0",
                capabilities=server.get_capabilities(),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

