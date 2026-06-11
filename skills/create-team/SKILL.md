---
name: create-team
description: Use this when a human points you at this blueprint and asks you to create a coordinator/developer/reviewer aweb team in a repo they own.
---

# Create a team from this blueprint

You are creating a team from a **blueprint** into a human's repo. The
blueprint gives you souls, roles, skills, playbooks, and adapter notes. You
copy the identity-free resources into the target repo, commit them, connect
the first instance with explicit aweb primitives, and hand the team to the
human.

You are a transient creator: **you will have no role in the finished team.**
Your job ends when the first instance is connected and the human has its
launch command.

## Hard boundaries

Do not:

- create `.aw` state in this blueprint repo;
- copy `.aw`, private keys, certificates, invite tokens, DIDs, or aliases
  from anywhere;
- overwrite an existing target `AGENTS.md`, `CLAUDE.md`, `.gitignore` entry,
  `.aw`, `agents/`, or `.agents/` path without asking;
- create git worktrees or branches unless the human asked for that concrete
  instance;
- use a monolithic bootstrap/provision command.

Prefer small, reviewable filesystem changes and explicit aweb commands.

**Fast path:** `scripts/create-team.py <target>` performs this whole
procedure in one go (prompts for counts and team source, shows every `aw`
command it runs, prints launch commands). Prefer it for the standard setup;
follow the manual steps when the human wants to adapt along the way.

## 1. Confirm the setup inputs

Ask or infer, then repeat back before mutating files:

- target repo path (must be a git repo for worktree-backed developers; you
  can still install souls/roles/skills in a plain directory);
- team source: existing hosted team, new dashboard team, or BYOT/admin setup
  (BYOT is protocol/admin — hand it to the team's administrator);
- the first instance to create now — usually `coordinator` only;
- harness for the first instance: Claude Code, Codex, Pi, or other.

## 2. Inspect the blueprint

From this blueprint repo, read:

```text
resource-pack.yaml
resources/instructions.md
resources/roles/*.md
resources/souls/*/soul.yaml
resources/souls/*/AGENTS.md
resources/docs/team-architecture.md
adapters/<harness>/README.md
```

`soul.yaml` declares `role` (which published role the soul uses), `work`
(`main` or `worktree`), and `runtime` (default harness hint). It is not
identity state.

## 3. Install the resources into the target

The blueprint is a seed: the copies you make are owned by the team from then
on. Souls are living state — they will accumulate docs, decisions, and
memory — so they belong in the team's repo, committed and reviewed.

Target shape:

```text
agents/
  souls/<role>/...          from resources/souls/
  roles/<role>.md           from resources/roles/
  instructions.md           from resources/instructions.md
  docs/team-architecture.md from resources/docs/
  roles-bundle.json         built by scripts/build-roles-bundle.py
.agents/
  skills/spawn-instance/      from skills/
  skills/get-code-reviewed/   from skills/
  skills/self-maintenance/    from skills/
  bin/launch-session.sh       from resources/bin/
```

You may run `scripts/install-local.sh <target>` after checking it will not
overwrite existing target paths; it copies exactly the shape above and
nothing else. If you copy manually, preserve the same shape and build the
roles bundle with:

```bash
scripts/build-roles-bundle.py > <target>/agents/roles-bundle.json
```

Do not copy this `create-team` skill into the target; it belongs to the
blueprint, not the team.

Add the harness adapter for the chosen harness. For Claude Code:

```bash
cd <target>
ln -sfn .agents/skills .claude/skills
```

Keep instances out of git. Append to the target `.gitignore` (show the human
the diff):

```text
/agents/instances/
```

Review with the human, then commit the team resources:

```bash
git add agents .agents .claude .gitignore
git commit -m "Add coordinator/developer/reviewer team from blueprint"
```

## 4. Create the first instance

Usually the coordinator. Its home holds its body (symlink to the soul) and,
after connection, its identity:

```bash
cd <target>
mkdir -p agents/instances/coordinator
cd agents/instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../../.. work
```

Add harness-specific links only for the chosen harness — for Claude Code:

```bash
ln -sfn AGENTS.md CLAUDE.md
```

## 5. Connect with aweb primitives

Hosted, released-safe path: ask the human to create or choose the team in
the dashboard and use the dashboard's connect-agent flow. Run the generated
command from the instance home it should bind:

```bash
cd <target>/agents/instances/coordinator
AWEB_API_KEY=... AWEB_URL=... aw init ...
```

If the installed CLI supports human-facing team primitives (`aw team
create`, `aw team invite`, `aw team join`, `aw workspace connect`), you may
use them when the human asks for CLI-only setup — but keep each step
explicit; never hide identity creation inside a filesystem copy.

Verify from the instance home:

```bash
aw workspace status
aw whoami
```

## 6. Publish shared team context

From the connected instance home:

```bash
aw instructions set --body-file ../../instructions.md
aw roles set --bundle-file ../../roles-bundle.json
aw roles show --all-roles
```

If `aw roles add --playbook-file` is available and the human prefers one
role at a time:

```bash
aw roles add coordinator --title "Coordinator" --playbook-file ../../roles/coordinator.md
aw roles add developer --title "Developer" --playbook-file ../../roles/developer.md
aw roles add reviewer --title "Reviewer" --playbook-file ../../roles/reviewer.md
```

## 7. Hand the team to the human

Do not create developer or reviewer instances now — the team spawns them
when work needs them, using the `spawn-instance` skill you installed.

Report:

- what was committed and where;
- the launch command for the first instance, e.g.:

  ```bash
  cd <target>/agents/instances/coordinator && claude
  ```

- that `agents/docs/team-architecture.md` explains the team model;
- that new instances are created with `.agents/skills/spawn-instance/`.

## Done criteria

You are done when:

- the target has committed, identity-free souls, roles, instructions, docs,
  and skills under `agents/` and `.agents/`;
- `/agents/instances/` is gitignored;
- the first instance is connected to aweb and verified;
- instructions and roles are published to the team;
- the human has the exact command to start the first instance.
