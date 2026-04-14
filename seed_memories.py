"""
Seed memories into Mem0 for a specific project.

Environment Variables:
  OPENROUTER_API_KEY     — Your OpenRouter API key
  MEM0_COLLECTION        — Qdrant collection name (default: agent_memory)
  LLM_MODEL              — OpenRouter model (default: nvidia/nemotron-3-nano-30b-a3b:free)

Usage:
  OPENROUTER_API_KEY=sk-or-v1-... MEM0_COLLECTION=myproject python3 seed_memories.py
"""
import os, time, sqlite3

# Patch sqlite3 BEFORE mem0 import
_orig = sqlite3.connect
def _patch(*a, **k):
    k.setdefault("check_same_thread", False)
    return _orig(*a, **k)
sqlite3.connect = _patch

from mem0 import Memory

openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
os.environ["OPENAI_API_KEY"] = openrouter_key

COLLECTION = os.getenv("MEM0_COLLECTION", "agent_memory")
LLM_MODEL = os.getenv("LLM_MODEL", "nvidia/nemotron-3-nano-30b-a3b:free")

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": LLM_MODEL,
            "openai_base_url": "https://openrouter.ai/api/v1",
            "api_key": openrouter_key,
            "temperature": 0,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": COLLECTION,
            "url": os.getenv("QDRANT_URL", "http://localhost:6333"),
            "embedding_model_dims": 768,
        }
    },
    "history_db_path": ":memory:",
}

print(f"Initializing Mem0 (collection: {COLLECTION})...")
m = Memory.from_config(config)

# ── Define your memories here ──────────────────────────────────
# Edit these lists for your project.

TDD_RULES = [
    ("Always write a failing test (red) before writing any implementation code. Never write production code without a failing test first.", "tdd"),
    ("Write the minimum amount of code to make the failing test pass (green). Do not over-engineer or add extra logic beyond what the test requires.", "tdd"),
    ("After green, refactor the code to improve structure and readability while keeping all tests passing. Never refactor when tests are failing.", "tdd"),
    ("The TDD cycle is strictly: Red → Green → Refactor. Skipping any step is not allowed.", "tdd"),
    ("Never modify a test to make it pass. Fix the implementation instead.", "tdd"),
    ("One failing test at a time. Do not write multiple failing tests simultaneously.", "tdd"),
    ("Test file must exist and test must fail before any implementation file is created or modified.", "tdd"),
]

# Add your project-specific memories below:
# ARCHITECTURE = [
#     ("My project uses FastAPI with PostgreSQL", "architecture"),
#     ("Frontend is Next.js with Tailwind CSS", "architecture"),
# ]

ALL_MEMORIES = TDD_RULES  # + ARCHITECTURE

print(f"\n=== Seeding {len(ALL_MEMORIES)} Memories ===")
for i, (text, category) in enumerate(ALL_MEMORIES, 1):
    try:
        result = m.add(text, user_id="shared_rules", metadata={"type": category, "scope": "global"})
        stored = len(result.get("results", []))
        print(f"[{i}/{len(ALL_MEMORIES)}] ✓ Stored ({stored} entries)")
        time.sleep(1)
    except Exception as e:
        print(f"[{i}/{len(ALL_MEMORIES)}] ✗ Error: {e}")

# ── Verification ───────────────────────────────────────────────
print("\n=== Verification ===")
results = m.search("TDD rules", user_id="shared_rules", limit=5)
print(f"Found {len(results['results'])} memories:")
for i, r in enumerate(results["results"], 1):
    print(f"  {i}. score={r['score']:.3f} | {r['memory'][:80]}")

print("\n✅ Seeding complete!")
