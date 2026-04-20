# The Forensic Vault Distiller (MCP)

**The Forensic Vault Distiller** is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server designed to bridge the gap between high-fidelity technical documentation (the "Vault") and professional social presence via [Buffer](https://buffer.com).

## The Problem: The Specialist's Dilemma
Technical specialists often face a choice: spend time in "deep work" mode creating forensic-level project documentation, or spend time in "content creator" mode manually distilling that work for social media. 

Most people choose the former and become invisible, or choose the latter and lose their technical edge.

## The Solution
This MCP server allows an AI agent (Claude, Cursor, etc.) to:
1. **Analyze:** Read deep-dive markdown files from a local "Technical Vault."
2. **Distill:** Extract high-signal insights, lessons learned, and "forensic" evidence of mastery.
3. **Draft:** Generate platform-specific drafts (LinkedIn, X, etc.) that maintain the author's technical voice.
4. **Schedule:** Directly interface with the Buffer API to queue content for distribution.

## Features (In Progress)
- [ ] **Vault Context Tool:** Allows the AI to search and read local project post-mortems.
- [ ] **Distillation Tool:** AI-driven extraction of technical insights into social-ready formats.
- [ ] **Buffer Integration:** Native tools for `list_profiles`, `create_update`, and `get_sent_updates`.
- [ ] **Forensic Branding:** Automatic formatting to ensure content matches the "Master Specialist" persona.

## Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set your `BUFFER_ACCESS_TOKEN` in a `.env` file.
4. Run the server: `python server.py`.

## Why Buffer?
We believe in Buffer's mission of transparency and remote-first excellence. This tool is built by a "Master Specialist" who uses Buffer to protect their deep-work time while building a global career.
