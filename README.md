# Coordinator + developer/reviewer team blueprint

This repository is a **team blueprint**. The normal use is that a human
points their coding agent at this repo and says:

> Create a team in my repo from this blueprint.

The agent reads the souls, roles, skills, and playbooks here, copies the
identity-free resources into your repo, commits them, connects the first
instance with explicit aweb primitives, and hands you the running team.

Choose this blueprint when you want:

- a long-lived **coordinator** for intake, routing, status, and human
  handoff;
- **developer** instances that implement in explicit git worktrees, one per
  task;
- **reviewer** instances that inspect work independently with fresh eyes.

A blueprint gives you **souls, roles, skills, playbooks, and adapter
notes**. The team then creates concrete instances explicitly, when work
needs them.

## Souls and instances

The model (explained fully in
[resources/docs/team-architecture.md](resources/docs/team-architecture.md)):

- A **soul** (`agents/souls/<role>/` in your repo) is the committed,
  identity-free body of an agent: its operating doc plus accumulated docs,
  decisions, and memory. Souls are living state — they grow with your team
  and are versioned like any other code.
- An **instance** (`agents/instances/<name>/`, gitignored) is a runnable
  copy of a soul with its own aweb identity. One soul can back many
  instances at once (`developer-authflow`, `reviewer-pr-142`).

The blueprint is a **seed**: once copied into your repo, the resources are
yours and evolve there. There is no upstream to stay in sync with.

## What this repo contains

```text
resource-pack.yaml             Manifest for this blueprint
resources/instructions.md      Team-wide operating instructions
resources/roles/*.md           Role playbooks published to aweb roles
resources/souls/*              Durable agent bodies: soul.yaml + AGENTS.md + docs/decisions/memory
resources/docs/                Team architecture doc, copied into your repo
resources/bin/                 launch-session.sh helper
skills/create-team/            The procedure your agent follows to create the team
skills/spawn-instance/         How the team mints new instances (copied into your repo)
skills/self-maintenance/       How agents grow their souls (copied into your repo)
examples/deploy.md             First-run walk-through
examples/create-instance.md    Creating developer/reviewer instances later
adapters/*                     Harness notes for Claude Code, Codex, and Pi
scripts/install-local.sh       Explicit filesystem install helper; no .aw mutation
scripts/build-roles-bundle.py  Builds a roles JSON bundle from Markdown roles
```

## Important boundary

This repo does **not** contain `.aw`, private keys, DIDs, certificates,
aliases, team IDs, invite tokens, generated worktrees, or instance
directories. Nothing here creates identities or git worktrees behind your
back. Applying the blueprint (copying files) and creating identities
(explicit aweb commands) are separate, visible steps.

## Use it

In your own repo, tell your agent:

> Use `https://github.com/awebai/aweb-team-coord-worktrees` as the blueprint
> for this repo. Read its `AGENTS.md`, follow its
> `skills/create-team/SKILL.md`, and set up the coordinator first. Do not
> create developer/reviewer instances until I ask.

The agent will:

1. inspect `resource-pack.yaml`;
2. copy the identity-free souls, roles, docs, and skills into your repo and
   commit them (see the target layout below);
3. create `agents/instances/coordinator` explicitly;
4. have you connect it with the dashboard-generated
   `AWEB_API_KEY=... AWEB_URL=... aw init ...` command, run from that
   instance directory;
5. publish the shared instructions and roles (`aw instructions set`,
   `aw roles set --bundle-file` — or `aw roles add` per role where the
   installed CLI supports it);
6. hand you the launch command.

You then run the team yourself:

```bash
cd agents/instances/coordinator
claude
```

If you prefer to do the filesystem copy yourself, see
[examples/deploy.md](examples/deploy.md) and `scripts/install-local.sh`.

## What lands in your repo

```text
agents/
  souls/{coordinator,developer,reviewer}/
  roles/{coordinator,developer,reviewer}.md
  instructions.md
  docs/team-architecture.md
  roles-bundle.json
  instances/            <- gitignored; created as the team runs
.agents/
  skills/{spawn-instance,self-maintenance}/
  bin/launch-session.sh
.claude/skills -> .agents/skills    (Claude Code only)
```

## Growing the team

The running team spawns developer and reviewer instances itself, when work
needs them, using `.agents/skills/spawn-instance/` — an existing instance
invites the new one (`aw id team invite` → `accept-invite` → `aw init`),
wires its body to the soul, and adds a git worktree if the soul calls for
one. Spawning happens only on explicit human request or a documented
workflow step. See [examples/create-instance.md](examples/create-instance.md).

## Legacy note

Earlier versions of this repository were input for the monolithic
`aw agents bootstrap` command and, briefly, a "team operating pattern"
framing. Both are superseded by this blueprint shape: copy and commit the
resources deliberately, then create identities and worktrees explicitly.

## License

MIT. Fork freely and adapt the blueprint to your team.
