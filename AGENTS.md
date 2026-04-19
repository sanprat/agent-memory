# Agent Instructions

## Memory System (MANDATORY)

Before starting ANY task:
1. Call `mem0_search` with a query describing what you're about to do
2. Read `.agent_memory/current_handoff.md` if it exists — it has context from previous sessions
3. Follow all retrieved rules, conventions, and patterns

After completing ANY task:
1. Call `mem0_add` to store what you learned (bug fixes, architecture decisions, conventions)
2. Update `.agent_memory/current_handoff.md` with a summary of what you did
