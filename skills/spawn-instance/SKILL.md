---
name: spawn-instance
description: Create (and tear down) an instance of a canonical soul — a home (body linked to the soul + its own aweb identity) plus a work location — then hand it to the human or launch it. Only when a human explicitly asks, or a documented workflow step requires it. The reviewer never spawns.
---

# Spawn an instance of a soul

> **When you may spawn — hard rule.** Only when a **human explicitly asks**,
> or when a **documented step in your own workflow requires it**. Never spawn
> agents on your own initiative to "get help." The **reviewer never spawns** —
> it stays independent.

Souls (`agents/souls/<role>/`) are the canonical agent bodies. An
**instance** is a runnable copy with its **own unique aweb identity**, and it
has two parts:

- **Home** — `agents/instances/<name>/` — the directory itself. It holds the
  instance's **body** (`AGENTS.md` symlinked to the soul) and its
  **identity** (`.aw`). The session runs here, and `aw` commands resolve
  their identity here.
- **`work`** — where the instance goes to do its job. The soul's `soul.yaml`
  `work:` field says which:
  - `worktree` (code agents) → `agents/instances/<name>/work/` is a git
    **worktree on the instance's own branch**;
  - `main` (coordination/review agents) → `work` is a **symlink to the main
    checkout**.

**Naming.** The alias is the soul's **role** as the stem. A standing
singleton uses the bare role (`coordinator`). Anything spawned for a
specific piece of work appends a short lowercase-kebab purpose slug —
`<role>-<purpose>` (`developer-authflow`, `reviewer-pr-142`). On a literal
collision, append `-2`.

## 1. Prepare the instance — run this as ONE block

Run it **from your own instance home** (`aw` reads your identity from the
current directory's `.aw`; it does not search upward). It anchors `$REPO` to
the **main checkout**, captures the invite token, builds the home, and sets
up the work location.

```bash
role=<role>; name=<name>          # e.g.  role=developer  name=developer-authflow

# Main checkout root — correct even when you're in a worktree.
# (NOT `git rev-parse --show-toplevel`: from a worktree that returns the worktree root.)
REPO="$(cd "$(git rev-parse --git-common-dir)" && cd .. && pwd)"
inst="$REPO/agents/instances/$name"                                # the instance HOME
work=$(awk -F': *' '/^work:/{print $2}' "$REPO/agents/souls/$role/soul.yaml" | awk '{print $1}')

# 1) Invite — from your own .aw; token captured automatically (no copy/paste).
TOKEN="$(aw id team invite 2>&1 | awk '/^Token:/{print $2}')"
[ -n "$TOKEN" ] || { echo "no token — run from your OWN instance home (the dir with your .aw)"; exit 1; }

# 2) Make the HOME and join the team there (identity + session live here).
mkdir -p "$inst"
( cd "$inst" && aw id team accept-invite "$TOKEN" --alias "$name" && aw init --do-not-touch-agents-md --alias "$name" )

# 3) Wire the BODY into the home — links to the canonical soul.
ln -sfn "$REPO/agents/souls/$role/AGENTS.md" "$inst/AGENTS.md"

# 4) The soul's OWN skills into the home, if it has any (shared skills resolve from the repo root).
soulskills="$REPO/agents/souls/$role/.agents/skills"
if find "$soulskills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | grep -q .; then
  mkdir -p "$inst/.agents/skills"
  find "$soulskills" -mindepth 1 -maxdepth 1 -type d | while IFS= read -r s; do
    ln -sfn "$s" "$inst/.agents/skills/$(basename "$s")"
  done
fi

# 5) Harness links for the runtime that will launch it — for Claude Code:
ln -sfn AGENTS.md "$inst/CLAUDE.md"
[ -d "$inst/.agents/skills" ] && { mkdir -p "$inst/.claude"; ln -sfn ../.agents/skills "$inst/.claude/skills"; }

# 6) Set up WORK — where the agent goes to do its job.
if [ "$work" = worktree ]; then
  git -C "$REPO" worktree add "$inst/work" -b "$name"   # code agent: its OWN branch, checked out in work/
else
  ln -sfn "$REPO" "$inst/work"                          # coordination agent: work/ -> the main checkout
fi

echo "ready — home: $inst"
```

If your CLI predates `aw id team invite`, or the team is dashboard-managed,
use the dashboard's connect-agent flow instead of steps 1–2: create the home
directory and run the dashboard-generated
`AWEB_API_KEY=... AWEB_URL=... aw init ...` from it. The rest is the same.

> ⚠️ **Never move or rename an instance home after `aw init`.** aweb
> registers the workspace at its **path**; if that path disappears, the
> service reaps the identity. It is created at its final location above —
> leave it there. To relocate, re-mint in place.

## 2. Launch — or hand the start back to the human

The session launches from the **home** — that's where the body and identity
are. A code agent then works in `work/`; its AGENTS.md says so.

- **A human asked for it** → **do not launch it yourself.** Report it's
  ready and give the human its launch command (absolute path, works from a
  fresh terminal):

  ```bash
  cd <inst> && claude     # or `pi`, per the soul's runtime
  ```

- **You're spawning it autonomously** under a documented workflow with no
  human waiting → launch it in tmux with the shared helper:

  ```bash
  REPO="$(cd "$(git rev-parse --git-common-dir)" && cd .. && pwd)"
  "$REPO/.agents/bin/launch-session.sh" "$REPO/agents/instances/<name>" --claude --tmux   # or --pi
  ```

  Check on it by reading its pane non-interactively:
  `tmux capture-pane -p -t "<session>:<name>"`. Never `tmux attach` from
  your own session; only the human attaches.

## Tear down (retire the instance)

A one-shot instance is retired the moment its job is done — a reviewer that
has sent its verdict, a developer whose branch has merged. Two parts:

**1. The instance closes its own session** as its final act, right after
sending its result:

```bash
[ -n "$TMUX" ] && tmux kill-window
```

**2. The spawner cleans up identity + directory** once it has consumed the
result:

```bash
name=<name>
REPO="$(cd "$(git rev-parse --git-common-dir)" && cd .. && pwd)"
inst="$REPO/agents/instances/$name"
( cd "$inst" && aw workspace delete "$name" )            # delete workspace + identity (run from its home)
git -C "$REPO" worktree remove "$inst/work" --force 2>/dev/null   # if it had a worktree
rm -rf "$inst"
git -C "$REPO" branch -D "$name" 2>/dev/null; git -C "$REPO" worktree prune
```

Use `aw workspace delete`, **not** `aw id team leave` (leave refuses an
identity's only team). If it answers 409 "Workspace is still active",
wait for the service to mark it stale and retry — never remove the home
while the server still considers the member active, or it orphans in
the roster. Preserve useful branch or soul changes before
removing anything. Standing instances (the coordinator) are long-running and
are not retired this way.
