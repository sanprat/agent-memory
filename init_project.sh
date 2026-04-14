#!/usr/bin/env bash
# Initialize agent-memory in a target project.
# Usage: ./init_project.sh /path/to/project
#
# What it does:
#   1. Copies .agent-memory-rules.md, CLAUDE.md, AGENTS.md
#   2. Copies mem0_mcp_server.py, seed_memories.py, generate_configs.py
#   3. Runs generate_configs.py (requires OPENROUTER_API_KEY)
#   4. Prints next steps

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:?Usage: $0 /path/to/project}"

if [[ ! -d "$TARGET" ]]; then
    echo "❌ Directory not found: $TARGET"
    exit 1
fi
TARGET="$(cd "$TARGET" && pwd)"

echo "🔧 Initializing agent-memory in: $TARGET"
echo ""

# Copy universal brain + loaders
for f in .agent-memory-rules.md CLAUDE.md AGENTS.md mem0_mcp_server.py seed_memories.py generate_configs.py; do
    cp "$SCRIPT_DIR/$f" "$TARGET/"
    echo "  ✅ $f"
done

# Generate agent configs
if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
    echo ""
    echo "⚙️  Generating agent MCP configs..."
    cd "$TARGET"
    python3 generate_configs.py
    echo ""
else
    echo ""
    echo "⚠️  OPENROUTER_API_KEY not set — skipping config generation."
    echo "   Run: OPENROUTER_API_KEY=sk-or-v1-... python3 $TARGET/generate_configs.py"
fi

echo ""
echo "📋 Next: Seed memories"
echo "   Edit $TARGET/seed_memories.py to add project-specific memories, then:"
echo "   OPENROUTER_API_KEY=sk-or-v1-... python3 $TARGET/seed_memories.py"
