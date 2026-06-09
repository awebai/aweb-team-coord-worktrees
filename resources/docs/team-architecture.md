# Team architecture

This team was created from the `coordinator-with-dev-review` blueprint. This
doc explains how the team is structured, who does what, and how work flows
from a human request to the main branch. It is committed so that every agent
— and every human — can understand the system they are running.

## Team at a glance

- **Coordinator** — long-lived planning and routing surface. Turns human
  requests into small tasks with acceptance criteria and drives developer
  instances. Does not make routine code edits.
- **Developer** — implements one task at a time in its own git worktree on
  its own branch. One instance per task.
- **Reviewer** — independent, fresh-eyes review of a branch or commit.
  Ephemeral: spawn one for a review, retire it after its verdict.

## Souls and instances

The team is defined as **souls** and run as **instances** — two distinct
things:

- A **soul** (`agents/souls/<role>/`) is the canonical *body* of an agent:
  its `AGENTS.md` (operating doc), `soul.yaml`, and its accumulated `docs/`,
  `decisions/`, and `memory/`. Souls hold **no identity**. They are
  committed, and they travel and grow with the repo. The soul is the part we
  version.
- An **instance** (`agents/instances/<name>/`) is a *runnable copy* of a
  soul with its **own unique aweb identity**. It has two parts:
  - a **home** — the directory itself — holding the instance's **body**
    (`AGENTS.md` symlinked to the soul) and its **identity** (`.aw`). The
    session runs here, and `aw` commands resolve their identity here.
  - a **`work`** location — where it goes to do the job.

  Instances are **gitignored** (private identity, machine-specific) and
  never travel with the repo.

A soul's `soul.yaml` records `role`, `runtime` (claude | pi), and `work`:

- `work: worktree` — `work/` is the instance's **own git worktree on its own
  branch** (named after the instance). Code agents work this way: the
  session runs in the home, then works in `work/` to build and commit on its
  branch. `aw` runs from the home, `git` from `work/`.
- `work: main` — `work` is a **symlink to the main checkout**. Coordination
  and review agents work this way.

### One soul, many instances

A soul is a class; instances are its live objects. Any soul can back several
instances at once, each with its own identity and alias:

- a standing singleton uses the bare role as its alias: `coordinator`;
- anything spawned for a specific piece of work appends a short
  lowercase-kebab purpose slug, `<role>-<purpose>`: `developer-authflow`,
  `developer-feed`, `reviewer-pr-142`;
- on a literal collision, append `-2`.

Purpose slugs beat counters: the alias tells you what the instance is *for*
in `aw mail` and `aw chat`.

## How work flows

1. A human asks the **coordinator** for something. The coordinator turns it
   into small, reviewable tasks with acceptance criteria.
2. A **developer** instance implements one task in its `work/` worktree on
   its own branch, keeping changes small and reporting evidence/tests.
3. The coordinator (or the developer, if the team prefers) asks a
   **reviewer** instance for an independent review of the branch.
4. The reviewer reports blocking findings or an ACK.
5. The coordinator decides: merge, request amendments, or escalate to the
   human.

## Who may spawn an instance

Spawning is deliberately constrained (see the `spawn-instance` skill):

- Only when a **human explicitly asks**, or when a **documented workflow
  step requires it** (e.g. requesting review spawns a reviewer). No agent
  spawns on its own initiative to "get help."
- The **reviewer never spawns** — staying independent is its whole job.
- When a human asks for an instance, prepare it and hand back the launch
  command; don't auto-launch a session the human is expected to drive.

### Retiring an instance

One-shot instances (a reviewer after its verdict, a developer after its
branch lands) are retired by their spawner: `aw workspace delete` from the
instance home, then remove the home, worktree, and branch. The full
procedure is in the `spawn-instance` skill.

> ⚠️ Never **move or rename** an instance home after `aw init` — aweb
> registers the workspace at its path. Re-mint in place to relocate.

## Maintaining a soul

As an agent works, it grows its soul's `docs/`, `decisions/`, and `memory/`
so knowledge persists across sessions — but it **never** edits its own
`AGENTS.md` or role. The `self-maintenance` skill is the how-to. The
reviewer is the exception: it keeps no memory, only a generalized
`patterns/` checklist, to protect its fresh eyes.

## Layout

```text
agents/souls/<role>/        committed canonical bodies (AGENTS.md, soul.yaml, docs/, decisions/, memory/)
agents/roles/<role>.md      role playbooks published to aweb (aw roles)
agents/instructions.md      shared team instructions published to aweb
agents/docs/                this doc and other shared team docs
agents/instances/<name>/    gitignored instance homes: .aw identity + body -> soul + work
.agents/skills/             shared skills: spawn-instance, self-maintenance
.agents/bin/                shared helpers (launch-session.sh)
.claude/skills              symlink to .agents/skills (Claude Code adapter)
```
