# Coordinator + developer/reviewer team operating pattern

This repository replaces the old monolithic team template with a deployable
**team operating pattern**.

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

## Deploy into your project

From this repository:

```bash
./scripts/install-local.sh /path/to/your/project
```

That copies reviewable resources into your project:

```text
/path/to/your/project/
  souls/coordinator/
  souls/developer/
  souls/reviewer/
  .agents/skills/spawn-instance/
  .agents/skills/self-maintenance/
  team-operating-patterns/coordinator-with-dev-review/
    instructions.md
    roles-bundle.json
    resource-pack.yaml
```

Then connect/publish with released aweb flows:

1. Create or choose your team in the dashboard.
2. From each workspace/instance directory, run the exact dashboard-generated
   `AWEB_API_KEY=... AWEB_URL=... aw init ...` command for that agent.
3. Publish shared context from the project root:

   ```bash
   aw instructions set --body-file team-operating-patterns/coordinator-with-dev-review/instructions.md
   aw roles set --bundle-file team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
   aw roles show --all-roles
   ```

See [examples/deploy.md](examples/deploy.md) for the full flow.

## Create instances explicitly

Create concrete agent instances only when needed. For a developer worktree:

```bash
git worktree add instances/dev-task-123 -b dev-task-123
cd instances/dev-task-123
# Run the dashboard-generated aw init/connect command for alias dev-task-123.
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
```

See [examples/create-instance.md](examples/create-instance.md).

## Legacy note

The old version of this repository was input for a monolithic setup command.
That path is obsolete/legacy compatibility. This repository is now a
resource-pack/team-operating-pattern source: copy/publish resources deliberately,
then create identities and worktrees explicitly.

## License

MIT. Fork freely and adapt the pattern to your team.
