# Codex adapter

Use the same explicit instance layout as other harnesses: the instance home
holds `AGENTS.md` (symlinked to the soul), which Codex reads natively.
Connect the instance with the dashboard-generated `aw init` command, then
launch Codex from the instance home.

Codex reads skills from `.agents/skills`, which is where the blueprint
installs them — no extra link needed.

Do not copy `.aw` state between instances.
