"""
HarnessNotes — field performance observations for AI agent harnesses.

Each harness is an application or framework that runs models. These notes
come from real production usage during SuperInstance operations (Aug 2026).
Updated continuously as we learn more.

Key insight: the model is the voice. The harness is the body. A great model
in a bad harness is like a great singer in a room with no microphone.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class HarnessProfile:
    """Everything we know about a harness from field usage."""
    name: str
    cli_path: str
    best_for: list[str]
    poor_for: list[str]
    notes: str  # field observations
    session_mgmt: str  # how it handles context
    speed: str  # observed speed characteristics
    reliability: str  # observed failure modes


HARNESS_NOTES: list[HarnessProfile] = [
    HarnessProfile(
        name="KimiCode",
        cli_path="~/.npm-global/bin/kimi",
        best_for=["spatial_reasoning", "lua_code", "design_systems", "standalone_repos",
                  "test_frameworks", "lua_mock_infrastructure"],
        poor_for=["creative_writing", "deep_philosophy"],
        notes=(
            "K3 model. Med plan. Excellent at spatial decomposition and Lua. "
            "Built batten-spline package (pip-installable, 25 tests) in one session. "
            "Built roblox-testkit (Lua mock framework) in one session. "
            "Built superinstance-design-system (CSS+Lua dual implementation) in one session. "
            "CLI: -p for prompt mode, -y for yolo (auto-approve), --auto conflicts with -p. "
            "Resume sessions with: kimi -r <session_id>"
        ),
        session_mgmt="Session-based with resume capability. Context window adequate "
                     "for single-repo tasks.",
        speed="Fast for code generation. Completes multi-file repo builds in 3-8 min.",
        reliability="Solid. API rate-limited once during heavy multi-agent session.",
    ),
    HarnessProfile(
        name="Claude Code (Fable)",
        cli_path="~/.local/bin/claude",
        best_for=["strategic_thinking", "architecture", "literary_writing",
                  "implementation_plans", "product_vision", "deep_essays"],
        poor_for=["bulk_code_generation", "repetitive_tasks"],
        notes=(
            "Opus 5 / Sonnet 5 / Fable 5 models. Pro plan for Opus/Sonnet/Haiku "
            "(renewing). Fable non-renewing — reserve for golden-ticket moments. "
            "As Fable: wrote 'The Organ Plays Itself' (2916 words) — the company "
            "thesis. Also wrote 30-day implementation plan with exit criteria. "
            "CLI: --model fable/opus/sonnet. -p for non-interactive prompt mode. "
            "Note: claude.ai connectors need manual auth."
        ),
        session_mgmt="Session-based. -c to continue previous. Good context retention.",
        speed="Slower than GLM but much deeper. 3-10 min for complex strategic docs.",
        reliability="Excellent. Never failed. Connector auth can be finicky.",
    ),
    HarnessProfile(
        name="OpenCode",
        cli_path="~/.opencode/bin/opencode",
        best_for=["systems_engineering", "memory_systems", "structured_docs",
                  "verification"],
        poor_for=["creative_writing", "tasks_needing_web_access"],
        notes=(
            "Pay-per-use (GLM-4.6/4.5-air). Used for processor/memory verification "
            "(146K tokens in one session). CLI: 'opencode run <message>' for "
            "non-interactive. Server errors (err_034f1b79, err_501bf734, err_dc49a145) "
            "encountered on multiple attempts during heavy sessions. May be "
            "load-sensitive."
        ),
        session_mgmt="TUI mode + 'run' subcommand for non-interactive.",
        speed="When working: fast and thorough. When erroring: hard failure.",
        reliability="INCONSISTENT. Multiple server errors during Aug 4 session. "
                    "Works well when API is stable. Worth retrying.",
    ),
    HarnessProfile(
        name="MMX (MiniMax)",
        cli_path="~/.npm-global/bin/mmx",
        best_for=["image_generation", "music_generation", "voice_synthesis",
                  "video_generation", "creative_media"],
        poor_for=["code", "reasoning", "text_analysis"],
        notes=(
            "Starter plan (quota-limited). Music: 'mmx music generate' (not 'mmx music'). "
            "Image: 'mmx image generate'. Network errors on WSL2 — may need proxy "
            "config (HTTPS_PROXY env var). Quota: 99% remaining as of Aug 4. "
            "When working: excellent quality media output."
        ),
        session_mgmt="CLI subcommands. No session management — stateless.",
        speed="Media generation is async with task polling.",
        reliability="Network errors on WSL2. Intermittent. Worth retrying.",
    ),
    HarnessProfile(
        name="Ollama (Local GPU)",
        cli_path="~/.local/bin/ollama",
        best_for=["local_inference", "distillation_student", "embeddings",
                  "privacy_sensitive", "overnight_forge", "continuous_cognition"],
        poor_for=["complex_reasoning", "long_context", "knowledge_post_2024"],
        notes=(
            "v0.9.6 on WSL2. RTX 4050 Laptop GPU: CUDA 12, compute 8.9, 6GB VRAM. "
            "Models loaded: granite3.1-dense:2b (1.6GB), qwen2.5:0.5b (397MB), "
            "nomic-embed-text (274MB), llama3.2:1b (1.3GB). "
            "GPU performance: Granite 76.8 tok/s, Qwen 178.8 tok/s. "
            "CPU fallback: Granite 1.49 tok/s, Qwen 3.79 tok/s. "
            "WSL2 dxgkrnl bug can crash GPU sync — was intermittent, resolved "
            "in later sessions. Use --keepalive 30m to keep model loaded."
        ),
        session_mgmt="Stateless API at localhost:11434. Models load/unload "
                     "based on keepalive timer.",
        speed="GPU: excellent (76-178 tok/s). CPU: marginal (1.5-3.8 tok/s).",
        reliability="GPU mode stable once WSL2 kernel bug resolved. "
                    "Monitor thermals at 70-85C range.",
    ),
    HarnessProfile(
        name="DeepInfra MCP",
        cli_path="/home/eileen/mcp-deeinfra/",
        best_for=["multi_model_dispatch", "research", "image_generation",
                  "embeddings", "model_experimentation"],
        poor_for=["real_time_tasks", "low_latency"],
        notes=(
            "179 models available. API key: env DEEPINFRA_API_KEY. "
            "Hermes-3-Llama-3.1-405B produced excellent philosophical analysis "
            "via chat API. Qwen3-Coder-480B returned empty responses on some "
            "calls — may need different prompting. Seed-2.0-mini worked for "
            "short creative tasks. MCP server entry point had config issues "
            "(wrong module path). Direct API calls via curl work reliably."
        ),
        session_mgmt="Stateless API calls. No session concept.",
        speed="Varies by model. Seed-mini: fast. Hermes-405B: 30-90s for long outputs.",
        reliability="API reliable once authenticated. Model availability varies. "
                    "Some models return empty on certain prompt types.",
    ),
    HarnessProfile(
        name="DeepSeek API",
        cli_path="api.deepseek.com (direct)",
        best_for=["cheap_analysis", "quick_code_gen", "architectural_guidance",
                  "bulk_text_processing"],
        poor_for=["multimodal", "real_time_interaction"],
        notes=(
            "Model 'deepseek-chat' returns 'deepseek-v4-flash'. "
            "Extremely cost-effective: 5 engineering tasks for $0.16. "
            "Produced 1756-word architectural guidance for 5 systems in one call. "
            "Good at structured analysis and code generation. "
            "API: curl or openai-compatible client with base_url=api.deepseek.com."
        ),
        session_mgmt="Stateless API. OpenAI-compatible.",
        speed="Fast. Most calls complete in 5-30s.",
        reliability="Reliable. Auth works consistently once key is set.",
    ),
    HarnessProfile(
        name="GLM Subagents (Z.ai Max)",
        cli_path="OpenClaw sessions_spawn",
        best_for=["bulk_work", "repo_extraction", "creative_writing", "quality_audits",
                  "ideation", "documentation", "parallel_dispatch"],
        poor_for=["multi_file_tasks_5plus", "specialist_depth", "time_critical_tasks"],
        notes=(
            "Z.ai Max plan: unlimited tokens. The deck crew of the operation. "
            "Consistent timeout pattern: multi-file agent tasks (5+ files) time "
            "out at 5-12 min. Single-file or 2-file scopes with 'write immediately' "
            "instructions succeed. Resource Economy retry was the exception "
            "(19m24s, 6 files, 98K tokens). Best practice: dispatch for bulk, "
            "write critical files directly for time-sensitive work. "
            "12 agents dispatched simultaneously worked fine — Z.ai handles "
            "concurrency well."
        ),
        session_mgmt="OpenClaw sessions_spawn with mode='run'. Auto-announce "
                     "push-based completion. Max 5 concurrent per session.",
        speed="Variable. Single-file: 2-5 min. Multi-file: 5-12 min or timeout.",
        reliability="Reliable for appropriately-scoped tasks. Timeout is the "
                    "primary failure mode. Retry with tighter scope usually works.",
    ),
]


def get_harness(name: str) -> Optional[HarnessProfile]:
    """Look up a harness by name."""
    for h in HARNESS_NOTES:
        if h.name.lower() == name.lower():
            return h
    return None


def all_harnesses() -> list[HarnessProfile]:
    """Return all harness profiles."""
    return list(HARNESS_NOTES)
