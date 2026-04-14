# Agent Memory — Shared Memory for AI Coding Agents

Local, persistent, semantic memory for your AI coding agents.

**Works with:** Claude Code, OpenCode, Qwen Code, KiloCode, Antigravity, and any MCP-compatible agent.

## Architecture

```
Global Qdrant (Docker)          Ollama (Embeddings)
      │                              │
      └────── Mem0 MCP Server ───────┘
                    │
    ┌───────┬───────┼───────┬───────────┐
  Qwen   Claude   OpenCode KiloCode  Antigravity
```

- **Qdrant** (Docker) — Vector store, one global instance shared across all projects
- **Ollama** — Local embedding model (`nomic-embed-text`)
- **OpenRouter** — LLM for memory extraction (`nvidia/nemotron-3-nano-30b-a3b:free`)
- **Mem0** — Memory orchestration layer
- **MCP Server** — Exposes memory tools to your agents

## Prerequisites

- **Python 3.11+** with `mem0ai`, `mcp`, `ollama` installed
- **Docker** running (for Qdrant)
- **Ollama** running locally with `nomic-embed-text` model
- **OpenRouter API key**

## Quick Start

### 1. Start Qdrant (one-time, global)

```bash
docker run -d --name qdrant-mem0 --restart unless-stopped \
  -p 6333:6333 -v qdrant_mem0_global:/qdrant/storage \
  qdrant/qdrant:latest
```

### 2. Pull the embedding model

```bash
ollama pull nomic-embed-text
```

### 3. Seed memories for your project

```bash
OPENROUTER_API_KEY=sk-or-v1-... MEM0_COLLECTION=myproject python3 seed_memories.py
```

Edit `seed_memories.py` to add your project-specific memories (TDD rules, architecture decisions, coding conventions, etc.).

### 4. Generate agent configs

```bash
OPENROUTER_API_KEY=sk-or-v1-... python3 generate_configs.py
```

This creates MCP config files for all supported agents in the project root.

### 5. Done — agents auto-load rules

Every agent reads `.agent-memory-rules.md` on startup and automatically:
- **Searches memory** before coding (finds TDD rules, conventions, past decisions)
- **Follows retrieved rules** during coding
- **Updates memory** after coding (stores bug fixes, architecture decisions, learnings)

## How Agents Connect

### The Universal Pattern

Every project gets these files:

| File | Purpose | Loaded by |
|------|---------|-----------|
| `.agent-memory-rules.md` | Universal brain — rules for before/during/after coding | All agents |
| `CLAUDE.md` | Tells Claude Code to load the rules file | Claude Code |
| `AGENTS.md` | Tells OpenCode to load the rules file | OpenCode |
| `.kilocode/mcp.json` | MCP config + native instruction injection | KiloCode |
| `mcp_config.json` | MCP config | Antigravity |
| `.qwen/mcp.json` | MCP config | Qwen Code |

### MCP Server

The `mem0_mcp_server.py` exposes 4 tools to agents:

| Tool | Description |
|------|-------------|
| `mem0_add` | Store a new memory with optional category |
| `mem0_search` | Semantic search across memories |
| `mem0_list` | List all memories for an agent |
| `mem0_delete` | Delete a memory by ID |

## Project Setup

For each new project:

1. **Copy** `mem0_mcp_server.py`, `seed_memories.py`, `generate_configs.py`, and `.agent-memory-rules.md` into the project
2. **Edit** `seed_memories.py` — add your project-specific memories (use a unique `MEM0_COLLECTION` name)
3. **Run** `seed_memories.py` to populate memory
4. **Run** `generate_configs.py` to create agent MCP configs
5. **Done** — all agents in that project share the same memory

## Env Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | — |
| `MEM0_AGENT_ID` | Agent/user identifier | `agent-memory` |
| `MEM0_COLLECTION` | Qdrant collection name | `agent_memory` |
| `LLM_MODEL` | OpenRouter model | `nvidia/nemotron-3-nano-30b-a3b:free` |
| `OLLAMA_BASE_URL` | Ollama URL | `http://localhost:11434` |
| `QDRANT_URL` | Qdrant URL | `http://localhost:6333` |

## License

MIT
