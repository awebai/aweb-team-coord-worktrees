---
name: bootstrapping-a-team
description: Use this when a human points you at this repository and asks you to bootstrap a coordinator/developer/reviewer aweb team in a repo or directory they own.
---

# Bootstrapping a coordinator/developer/reviewer team

You are bootstrapping a team from a **source pattern** into a human's target repo
or directory. The source pattern gives you souls, roles, skills, playbooks, and
adapter notes. You create concrete team instances with explicit aweb primitives
and explicit filesystem/git steps.

## Hard boundaries

Do not:

- create `.aw` state in this source-pattern repo;
- copy `.aw`, private keys, certificates, invite tokens, DIDs, or aliases from
  anywhere;
- overwrite an existing target `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.aw`,
  `souls/`, `.agents/skills/`, or `team-operating-patterns/` path without asking;
- create git worktrees or branches unless the human asked for that concrete
  instance;
- use a monolithic bootstrap/provision command as the product path.

Prefer small, reviewable filesystem changes and explicit aweb commands.

## 1. Confirm the setup inputs

Ask or infer, then repeat back before mutating files:

- target repo/directory path;
- whether the target is a git repo;
- team source: existing hosted team, new dashboard team, BYOT/admin setup, or
  already-connected workspace;
- first concrete instances to create now, usually `coordinator` only;
- harness for each instance: Claude Code, Codex, Pi, or other;
- whether `/instances/` should be local-only via `.git/info/exclude` or committed
  as a repo `.gitignore` convention.

If the target is not a git repo, you can still install souls/roles/skills, but do
not offer git worktree-backed developer/reviewer instances until git exists.

## 2. Inspect the pattern

From this source-pattern repo, read:

```text
resource-pack.yaml
resources/instructions.md
resources/roles/*.md
resources/souls/*/soul.yaml
resources/souls/*/AGENTS.md
adapters/<harness>/README.md
```

Use `soul.yaml` only as a hint:

- `role`: which published role this soul usually uses;
- `work`: `main`, `worktree`, or `home` preference;
- `runtime`: default harness hint.

It is not identity state.

## 3. Install identity-free resources in the target

Default target shape:

```text
souls/<soul>/...
.agents/skills/<skill>/...
team-operating-patterns/coordinator-with-dev-review/
  instructions.md
  roles/<role>.md
  roles-bundle.json
  resource-pack.yaml
```

You may use `scripts/install-local.sh <target>` after checking it will not
overwrite target paths. The helper only copies identity-free resources and builds
a roles bundle. It must not create `.aw`, instances, branches, or worktrees.

If you copy manually, preserve the same shape and build the roles bundle with:

```bash
scripts/build-roles-bundle.py > <target>/team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
```

Review with the human before committing. In a git repo, commit the reusable
pattern resources, not concrete instances:

```bash
git add souls .agents/skills team-operating-patterns/coordinator-with-dev-review
git commit -m "Add coordinator/developer/reviewer operating pattern"
```

## 4. Keep concrete instances separate

Concrete instances are local workspaces with their own `.aw` state. They are not
part of the pattern source.

For a git target, keep them local unless the human chooses a different policy:

```bash
printf '/instances/\n' >> .git/info/exclude
```

## 5. Create the first instance explicitly

Usually create only the coordinator first:

```bash
cd <target>
mkdir -p instances/coordinator
cd instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../.. work
```

Add harness-specific links only after choosing the harness, for example Claude
Code:

```bash
ln -sfn AGENTS.md CLAUDE.md
```

Do not link the coordinator soul into the target repo root as `AGENTS.md` unless
the human explicitly wants that and the file does not already have project
meaning.

## 6. Connect with aweb primitives

Hosted, released-safe path: ask the human to create or choose the team in the
dashboard and use the dashboard's connect-agent flow. Run the generated command
from the concrete instance directory it should bind:

```bash
AWEB_API_KEY=... AWEB_URL=... aw init ...
```

If the installed CLI supports human-facing team primitives, you may use them
instead when the human asks for CLI-only setup, but keep the steps explicit:
create/invite/join/connect the instance; never hide identity creation inside a
filesystem copy.

Verify from the instance directory:

```bash
aw workspace status
aw mail inbox
```

## 7. Publish shared team context

After at least one workspace is connected, publish from a connected workspace in
or under the target repo:

```bash
aw instructions set --body-file team-operating-patterns/coordinator-with-dev-review/instructions.md
aw roles set --bundle-file team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
aw roles show --all-roles
```

If `aw roles add --playbook-file` is available and the human prefers one role at
a time, publish the Markdown role files explicitly instead of the bundle.

## 8. Create developer/reviewer instances only when needed

For a git repo and a requested developer task:

```bash
cd <target>
git worktree add instances/dev-task-123 -b dev-task-123
cd instances/dev-task-123
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
# optional for Claude Code:
ln -sfn AGENTS.md CLAUDE.md
# run dashboard-generated aw init/connect command here
```

For a reviewer:

```bash
cd <target>
git worktree add instances/review-task-123 -b review-task-123
cd instances/review-task-123
ln -sfn ../../souls/reviewer/AGENTS.md AGENTS.md
# optional for Claude Code:
ln -sfn AGENTS.md CLAUDE.md
# run dashboard-generated aw init/connect command here
```

## Done criteria

You are done when:

- the target has committed, identity-free souls/roles/skills/pattern resources;
- concrete instance directories are local-only or handled according to the
  human's explicit policy;
- at least the requested first instance is connected to aweb;
- instructions and roles are published to the team;
- the human has the exact command/path to start each instance.
