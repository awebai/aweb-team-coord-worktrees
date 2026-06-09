# Deploy this operating pattern

This is an explicit, reviewable deployment. It does not create `.aw` state,
identities, worktrees, or branches for you.

Assumption: you already have a git repo for your project.

## 1. Install resources into your project

```bash
git clone https://github.com/awebai/aweb-team-coord-worktrees.git
./aweb-team-coord-worktrees/scripts/install-local.sh /path/to/your/project
cd /path/to/your/project
```

Review the copied files:

```bash
git status --short
find souls team-operating-patterns/coordinator-with-dev-review .agents/skills -maxdepth 3 -type f | sort
```

The install step should create identity-free pattern resources only. It should
not create `.aw`, `instances/`, git branches, or git worktrees.

## 2. Keep future instances local

Concrete instances are local workspaces, not pattern source. Ignore them locally:

```bash
printf '/instances/\n' >> .git/info/exclude
```

Use `.git/info/exclude` for the first setup so the helper does not silently edit
your project `.gitignore`. If your team wants `/instances/` to be a repo-wide
convention, you can later add it to `.gitignore` deliberately in a normal commit.

## 3. Commit the reusable pattern resources

Commit only reviewable, identity-free files:

```bash
git add souls .agents/skills team-operating-patterns/coordinator-with-dev-review
git commit -m "Add coordinator/developer/reviewer operating pattern"
```

Never commit `.aw`, invite tokens, private keys, generated certificates, or local
instance/worktree directories.

## 4. Create your first concrete instance: coordinator

The coordinator is a concrete workspace under `instances/`, with its instructions
linked to the durable coordinator soul:

```bash
mkdir -p instances/coordinator
cd instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../.. work
```

Do **not** link the coordinator soul into the project root as `AGENTS.md`; many
repos already use that file for their own instructions.

## 5. Connect the coordinator to aweb

Use the dashboard for hosted setup. Create a team or choose an existing one, then
use the dashboard's connect-agent flow for the coordinator.

The dashboard will print a released-safe command shaped like:

```bash
AWEB_API_KEY=... AWEB_URL=... aw init ...
```

Run that exact command from `instances/coordinator/`. Do not commit the generated
`.aw` directory.

## 6. Publish shared instructions and roles

From the project root after the coordinator workspace is connected:

```bash
cd ../..
aw instructions set --body-file team-operating-patterns/coordinator-with-dev-review/instructions.md
aw roles set --bundle-file team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
aw roles show --all-roles
```

The Markdown role sources are also copied for review at:

```text
team-operating-patterns/coordinator-with-dev-review/roles/
```

## 7. Start the coordinator

```bash
cd instances/coordinator
claude
```

If you use Pi, Codex, or another harness, see `adapters/` and adapt the final
launch command. The identity/workspace setup stays explicit either way.

## 8. Add developer or reviewer instances later

Create them only when needed. See [create-instance.md](create-instance.md).
