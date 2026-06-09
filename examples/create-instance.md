# Create a concrete instance

A soul is the durable body in `agents/souls/<role>/`. An instance is a
runnable copy in `agents/instances/<name>/` with its own aweb identity: a
**home** (body symlinked to the soul, `.aw` identity) plus a **work**
location (the main checkout, or its own git worktree for code agents).

The canonical procedure is the `spawn-instance` skill installed at
`.agents/skills/spawn-instance/` — a connected instance invites the new one
and wires everything in one block. This file shows the manual shape of what
it does, and the dashboard fallback when no connected instance exists yet.

Instances are gitignored (`/agents/instances/` in `.gitignore`). Aliases:
bare role for standing singletons (`coordinator`), `<role>-<purpose>` for
work-specific instances (`developer-authflow`, `reviewer-pr-142`).

## From a connected instance (normal path)

Run the prepare block in `.agents/skills/spawn-instance/SKILL.md` from your
own instance home. It invites the new member (`aw id team invite`), accepts
in the new home (`aw id team accept-invite` + `aw init`), links the body to
the soul, and creates the work location the soul calls for.

## Dashboard fallback (first instance, or no inviter available)

```bash
cd /path/to/your/project
mkdir -p agents/instances/developer-authflow
cd agents/instances/developer-authflow
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md   # only if using Claude Code

# Run the dashboard-generated AWEB_API_KEY=... AWEB_URL=... aw init ... here.
```

Then the work location, per the soul's `soul.yaml`:

```bash
# work: worktree (developer) — its own branch, checked out in work/
git -C /path/to/your/project worktree add agents/instances/developer-authflow/work -b developer-authflow

# work: main (coordinator, reviewer) — symlink to the main checkout
ln -sfn ../../.. work
```

Commit or stash project changes before adding a git worktree.

## Launch

From the instance home, with the soul's runtime:

```bash
cd agents/instances/developer-authflow
claude        # or pi, per soul.yaml runtime
```

Or use the shared helper:

```bash
.agents/bin/launch-session.sh agents/instances/developer-authflow --claude --tmux
```

> ⚠️ Never move or rename an instance home after `aw init` — the workspace
> is registered at its path. Re-mint in place to relocate.

## Retire

One-shot instances are retired when their job is done. From the spawner,
after consuming the result:

```bash
name=developer-authflow
inst="agents/instances/$name"
( cd "$inst" && aw workspace delete "$name" )
git worktree remove "$inst/work" --force 2>/dev/null
rm -rf "$inst"
git branch -D "$name" 2>/dev/null; git worktree prune
```

Preserve useful branch or soul changes first. Use `aw workspace delete`, not
`aw id team leave` (leave refuses an identity's only team).
