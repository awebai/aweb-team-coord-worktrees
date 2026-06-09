# Coordinator + developer/reviewer team operating pattern

This repository is a deployable **team operating pattern**.

Choose this pattern when you want:

- a long-lived coordinator for intake, routing, status, and human handoff;
- developer instances that implement in explicit git worktrees;
- reviewer instances that inspect work independently before merge/release.

The pattern gives you **souls, roles, skills, playbooks, and adapter notes**. You
then explicitly create concrete instances when you need them.

## What this repo contains

```text
resource-pack.yaml             Manifest for the operating pattern
resources/instructions.md      Team-wide operating instructions
resources/roles/*.md           Role playbooks for aweb roles
resources/souls/*              Durable agent bodies: soul.yaml + AGENTS.md + memory dirs
skills/*                       Reusable procedures agents may load
examples/deploy.md             How to install the pattern into your project
examples/create-instance.md    How to create one concrete agent instance
adapters/*                     Harness notes for Claude Code, Codex, and Pi
scripts/install-local.sh       Explicit filesystem install helper; no .aw mutation
scripts/build-roles-bundle.py  Builds a roles JSON bundle from Markdown roles
```

## Important boundary

This repo does **not** contain `.aw`, private keys, DIDs, certificates, aliases,
team IDs, invite tokens, generated worktrees, or generated instance directories.
It does not create identities or git worktrees behind your back.

## Quick start from an existing git repo

```bash
git clone https://github.com/awebai/aweb-team-coord-worktrees.git
./aweb-team-coord-worktrees/scripts/install-local.sh /path/to/your/project
cd /path/to/your/project
```

Keep concrete instances local:

```bash
printf '/instances/\n' >> .git/info/exclude
```

Review and commit the reusable pattern files:

```bash
git status --short
git add souls .agents/skills team-operating-patterns/coordinator-with-dev-review
git commit -m "Add coordinator/developer/reviewer operating pattern"
```

Create the first concrete instance, usually the coordinator:

```bash
mkdir -p instances/coordinator
cd instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../.. work
```

Use the dashboard to create or choose your team, then run the dashboard-generated
`AWEB_API_KEY=... AWEB_URL=... aw init ...` command from
`instances/coordinator/`. Do not commit the generated `.aw` directory.

Publish shared context after the coordinator workspace is connected:

```bash
cd ../..
aw instructions set --body-file team-operating-patterns/coordinator-with-dev-review/instructions.md
aw roles set --bundle-file team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
aw roles show --all-roles
```

Start the coordinator from its instance directory:

```bash
cd instances/coordinator
claude
```

See [examples/deploy.md](examples/deploy.md) for the full first-run path and
[examples/create-instance.md](examples/create-instance.md) for developer/reviewer
instances.

## What gets copied into your project

```text
/path/to/your/project/
  souls/coordinator/
  souls/developer/
  souls/reviewer/
  .agents/skills/spawn-instance/
  .agents/skills/self-maintenance/
  team-operating-patterns/coordinator-with-dev-review/
    instructions.md
    roles/
      coordinator.md
      developer.md
      reviewer.md
    roles-bundle.json
    resource-pack.yaml
```

## Create more instances explicitly

Create concrete agent instances only when needed. For a developer worktree:

```bash
cd /path/to/your/project
git worktree add instances/dev-task-123 -b dev-task-123
cd instances/dev-task-123
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md  # only if using Claude Code
# Run the dashboard-generated aw init command here for alias dev-task-123.
```

## Legacy note

The old version of this repository was input for a monolithic setup command.
That path is obsolete/legacy compatibility. This repository is now a
resource-pack/team-operating-pattern source: copy/publish resources deliberately,
then create identities and worktrees explicitly.

## License

MIT. Fork freely and adapt the pattern to your team.
