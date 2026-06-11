---
name: review-agent-setup
description: Review a change to an agent's OWN setup — its skills, memory, decisions, or docs (under agents/souls/<role>/ and agents/roles/<role>.md). Use when an agent commits a self-setup change and asks you to review that specific commit.
---

# Review an agent's setup change

Agents grow their own souls (skills, memory, decisions, docs) as they learn.
When one does, it isolates that change in its **own commit** and asks you to
review it by commit SHA. This skill reviews that commit. It is distinct from
`code-review` (product code) — here the "code" is an agent's body, and a bad
change quietly degrades every future session of that agent.

## Get the change

The requester gives you a commit SHA. Review exactly that commit:

```bash
git show <sha> --stat
git show <sha>
```

Confirm it is **scoped to that one agent's own setup** — it should touch
only `agents/souls/<role>/…` (and optionally `agents/roles/<role>.md`). Flag
immediately if it edits another agent's soul, shared docs, or product code
without coordination, or mixes setup changes with feature code (those belong
in separate commits).

## Verify against the bar

**1. Consistent with the repo's conventions and architecture.**

- Skills are `.agents/skills/<name>/SKILL.md` with valid frontmatter
  (`name`, and a trigger-style `description` that says *when to use it*);
  memory is one-fact files indexed in `memory/MEMORY.md`; harness links
  (e.g. `CLAUDE.md`) stay symlinks to `AGENTS.md`.
- Doesn't contradict `agents/docs/team-architecture.md`, the published
  roles/instructions, the team's definition of done or merge policy, or
  another agent's role and boundaries.
- Doesn't duplicate what the code, git history, or another agent already
  owns.

**2. Within self-maintenance limits.**

- The agent did **not** edit its own `AGENTS.md` or role definition — those
  are human/review-owned (see the `self-maintenance` skill).
- Durable and behavior-changing: the recorded fact/procedure would actually
  change what a future instance does. Routine-work journaling, stale notes,
  or restating chat belongs out.
- No secrets, invite tokens, private keys, `.aw` state, DIDs, addresses, or
  certificates anywhere in the soul.
- Reviewer soul specifically: no memory/decisions, only generalized
  `patterns/` entries — never verdicts about a specific change.

**3. Small and true.**

- Prefer pruning over growing; a small, true soul beats a large, rotting
  one. Flag additions that future instances must read but that won't change
  their behavior.

## Report

Reply over chat with ACK or amendments, exactly as in `code-review`:
file:line findings, why each matters, and the concrete fix. A setup change
with blocking findings should not merge until amended.
