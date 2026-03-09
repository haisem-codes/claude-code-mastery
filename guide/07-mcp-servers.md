# Chapter 7: MCP Servers — Extending Claude's Capabilities

The Model Context Protocol (MCP) is a standard that lets Claude Code connect to external tools and data sources through local servers. Instead of Claude being limited to reading files and running shell commands, MCP servers give it access to browsers, databases, APIs, documentation libraries, and more.

This chapter covers how MCP works, how to configure it, and which servers are most useful.

---

## What Is MCP?

MCP is a client-server protocol. Claude Code acts as the client. MCP servers are lightweight processes that expose tools Claude can call — just like the built-in `Read`, `Write`, and `Bash` tools, but provided by external programs.

```
Claude Code (client)
  ├── Built-in tools: Read, Write, Edit, Bash, Grep, Glob
  └── MCP tools:
      ├── sequential-thinking server → think tool
      ├── playwright server → browser_navigate, browser_click, ...
      ├── context7 server → resolve-library-id, get-library-docs
      └── filesystem server → list_directory, read_file, ...
```

Each MCP server runs as a local process. Claude discovers available tools at startup and can call them throughout the session.

---

## Configuring MCP Servers

MCP servers are configured in JSON files at two levels:

### Project-Level (`.mcp.json`)

Place a `.mcp.json` file in your project root. These servers are available only when working in that project.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### Global-Level (`~/.claude/settings.json`)

Add servers to your global settings. These are available in every project.

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    }
  }
}
```

### Server Entry Format

Each server entry has:

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | The executable to run (`npx`, `node`, `python`, `docker`) |
| `args` | Yes | Command-line arguments |
| `env` | No | Environment variables for the server process |
| `cwd` | No | Working directory for the server |

---

## Recommended MCP Servers

### 1. Sequential Thinking (Complex Reasoning)

**What it does:** Provides a `think` tool that gives Claude a dedicated space for multi-step reasoning before acting. Useful for complex debugging, architecture decisions, or any task requiring careful analysis.

**When to use:** Tasks where Claude needs to reason through multiple possibilities before committing to an approach.

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    }
  }
}
```

**Example usage in practice:** When debugging a race condition, Claude can use the `think` tool to map out all concurrent paths before proposing a fix, rather than jumping to the first plausible solution.

### 2. Context7 (Library Documentation)

**What it does:** Fetches up-to-date documentation for libraries and frameworks. Claude's training data has a cutoff — Context7 bridges that gap by pulling current docs on demand.

**When to use:** Working with libraries that have changed since Claude's training cutoff, or when you need exact API signatures.

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

**Example:** When Claude needs to use a new Pydantic v2 feature, it can fetch the current Pydantic docs rather than relying on potentially outdated training data.

### 3. Playwright (Browser Testing)

**What it does:** Gives Claude a full browser it can control — navigate pages, click elements, fill forms, take screenshots, and inspect the DOM.

**When to use:** Testing web applications, scraping structured data, verifying UI changes, debugging frontend issues.

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"]
    }
  }
}
```

**Tools provided:**

| Tool | What it does |
|------|-------------|
| `browser_navigate` | Go to a URL |
| `browser_click` | Click an element |
| `browser_fill_form` | Fill form fields |
| `browser_take_screenshot` | Capture the current page |
| `browser_snapshot` | Get the accessibility tree (DOM structure) |
| `browser_evaluate` | Run JavaScript in the page |

### 4. Filesystem (Extended File Access)

**What it does:** Provides file operations beyond Claude's built-in tools. Useful when you need directory listing, file metadata, or operations on files outside the project directory.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@anthropic/mcp-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

The filesystem server restricts access to the directories you specify in the args. This is a security boundary — Claude cannot access files outside those paths through this server.

### 5. Docker (Containerized MCP)

**What it does:** Runs MCP servers inside Docker containers. This is the recommended approach when you want isolation, reproducibility, or when a server has complex dependencies.

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "mcp/server-image:latest"
      ]
    }
  }
}
```

---

## Complete `.mcp.json` Example

A practical project configuration combining multiple servers:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"]
    }
  }
}
```

---

## Security Considerations

### The `enableAllProjectMcpServers` Flag

By default, Claude Code prompts you to approve project-level MCP servers the first time they appear. You can bypass this with:

```json
{
  "enableAllProjectMcpServers": true
}
```

**Use with caution.** This flag auto-approves any `.mcp.json` in any project you open. Only enable it if:

- You control all repositories you work with
- You trust the MCP server packages being referenced
- You understand that `npx` will download and run code

### Server Trust Model

MCP servers run as local processes with your user permissions. They can:

- Access the filesystem (within configured paths)
- Make network requests
- Execute arbitrary code

**Best practices:**

- **Pin versions** in `.mcp.json` args instead of using `@latest`
  ```json
  "args": ["-y", "@upstash/context7-mcp@1.2.3"]
  ```
- **Review new servers** before adding them. Check the package source
- **Use Docker** for servers from untrusted sources to add an isolation layer
- **Limit filesystem paths** to only the directories the server needs
- **Never pass secrets** in MCP server args — use `env` for API keys
  ```json
  {
    "command": "npx",
    "args": ["-y", "some-mcp-server"],
    "env": {
      "API_KEY": "${SOME_API_KEY}"
    }
  }
  ```

### Environment Variable Interpolation

MCP server configs support `${VAR_NAME}` syntax for environment variables. Use this for any sensitive values:

```json
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@mcp/postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

---

## Managing MCP Servers

### Checking Server Status

When Claude Code starts, it connects to all configured MCP servers. You will see connection status in the startup output. If a server fails to start, Claude continues without it — no tools from that server will be available.

### Adding Servers at Runtime

Some setups support adding MCP servers during a session using management tools like `mcp-add`, `mcp-remove`, and `mcp-find`. These are available when using Docker-based MCP configurations.

### Debugging Connection Issues

Common problems and fixes:

| Problem | Cause | Fix |
|---------|-------|-----|
| Server not found | Package not installed | Run `npx` command manually to verify |
| Connection timeout | Server crashed on startup | Check server logs, verify args |
| Tools not appearing | Server connected but no tools registered | Check server implementation |
| Permission denied | Filesystem restrictions | Verify allowed paths in server config |

---

## Global vs. Project Configuration

| Aspect | Global (`~/.claude/settings.json`) | Project (`.mcp.json`) |
|--------|------------------------------------|-----------------------|
| Scope | All projects | Single project |
| Use case | General-purpose tools (thinking, docs) | Project-specific tools (DB, API) |
| Security | You control the config | Anyone can commit `.mcp.json` |
| Versioning | Not in git | Committed with the project |

**Recommended setup:**

- **Global:** `sequential-thinking` (useful everywhere)
- **Project:** `context7`, `playwright`, database servers (project-specific needs)

---

## Writing Custom MCP Servers

If no existing server meets your needs, you can write your own. An MCP server is any process that speaks the MCP protocol over stdin/stdout.

The simplest approach is using the MCP SDK:

```typescript
// minimal-server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({ name: "my-tools", version: "1.0.0" });

server.tool(
  "greet",
  { name: { type: "string", description: "Name to greet" } },
  async ({ name }) => ({
    content: [{ type: "text", text: `Hello, ${name}!` }],
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

Register it in `.mcp.json`:

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["tsx", "./tools/minimal-server.ts"]
    }
  }
}
```

For most teams, the existing community servers cover common needs. Write custom servers only when you need to expose internal APIs, proprietary databases, or domain-specific tools.

---

Next: [Chapter 8 — GitHub Actions](./08-github-actions.md)
