# Job Scrapy (MCP Server)

This is a Model Context Protocol (MCP) server that provides job scraping capabilities. It allows AI assistants like Claude, Antigravity, and ChatGPT to search for and scrape job listings across various platforms (LinkedIn, Indeed, Glassdoor, ZipRecruiter) and remote-specific job boards (Remotive, RemoteOK, Himalayas, etc.).

## Features

- **JobSpy Integration**: Scrape standard job boards for a specific search term and location.
- **Remote APIs Integration**: Search across 10+ remote job boards.
- **MCP Standard**: Built with `mcp` (FastMCP), meaning it integrates natively with any MCP client using `stdio`.

## Prerequisites

- Python 3.10+
- (Optional) API keys for sources like Findwork, Jooble, Adzuna, etc., in a `.env` file.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/job-scrapy.git
   cd job-scrapy
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (if you have API keys for remote boards):
   - Copy `.env.example` to `.env` (if applicable) and fill in your keys.

## Connecting to AI Assistants

### 1. Claude Desktop
Edit your `claude_desktop_config.json` file (usually located at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "job-scrapy": {
      "command": "/path/to/your/python/environment/bin/python",
      "args": ["/path/to/job-scrapy/server.py"]
    }
  }
}
```
Restart Claude Desktop, and you can now ask Claude to "Find me business analyst jobs in Dubai".

### 2. Antigravity IDE
Antigravity supports MCP natively. You can add the server to your `mcp_config.json` inside your Antigravity customizations directory (e.g., `~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "job_scrapy": {
      "command": "/path/to/your/python/environment/bin/python",
      "args": ["/path/to/job-scrapy/server.py"]
    }
  }
}
```

### 3. ChatGPT
ChatGPT does not natively support the MCP protocol yet. However, you can wrap this MCP server with a fast API using tools like `mcp-proxy` or build a custom GPT Action. Alternatively, you can use frameworks that bridge MCP to OpenAI's function calling.

## Development

You can test the MCP tools locally using the MCP Inspector:

```bash
mcp dev server.py
```
This will open a web interface where you can test the `search_jobspy` and `search_remote_apis` tools.
