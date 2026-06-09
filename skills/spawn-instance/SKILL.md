---
name: spawn-instance
description: Create or retire a concrete instance of a durable soul using explicit dashboard/init and git/filesystem steps.
---

# Spawn an instance of a soul

Use this only when a human asks or a documented workflow requires it. Do not
create identities or worktrees on your own initiative.

A soul lives in `souls/<role>/`. An instance is a concrete workspace with its own
`.aw` identity and optional git worktree.

## Worktree-backed instance

```bash
role=developer
name=dev-task-123
cd /path/to/project
git worktree add "instances/$name" -b "$name"
cd "instances/$name"

# Run the dashboard-generated aw init/connect command for alias $name.
ln -sfn "../../souls/$role/AGENTS.md" AGENTS.md
```

Add harness-specific links deliberately, for example `ln -sfn AGENTS.md
CLAUDE.md` for Claude Code.

## Main-checkout instance

```bash
role=coordinator
cd /path/to/project
# Run the dashboard-generated aw init/connect command for the coordinator alias.
ln -sfn "souls/$role/AGENTS.md" AGENTS.md
```

## Retire

Preserve useful branch/soul changes first. Revoke/remove the team membership
through the team's admin flow, then remove the explicit worktree or instance
directory.
