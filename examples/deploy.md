# Create a team from this blueprint

This is an explicit, reviewable setup. Nothing here creates `.aw` state,
identities, worktrees, or branches behind your back.

Assumption: you have a git repo for your project.

## 0. Agent-first prompt

The intended use is that you point your agent at this blueprint:

> Use `https://github.com/awebai/aweb-team-coord-worktrees` as the blueprint
> for this repo. Read its `AGENTS.md` and follow
> `skills/create-team/SKILL.md`. Set up the coordinator first using explicit
> aweb/dashboard init steps; do not create developer/reviewer instances
> until I ask.

The remaining steps are the procedure the agent follows — they work the same
if you run them yourself.

## 1. Install the resources into your repo

```bash
git clone https://github.com/awebai/aweb-team-coord-worktrees.git
./aweb-team-coord-worktrees/scripts/install-local.sh /path/to/your/project
cd /path/to/your/project
```

Review the copied files:

```bash
git status --short
find agents .agents -type f | sort
```

The install copies identity-free team resources only — souls, roles,
instructions, docs, skills, and the launch helper. It does not create `.aw`,
instances, branches, or worktrees. The blueprint clone itself is disposable
after this step.

## 2. Keep instances out of git, commit the rest

Instances carry private identity and are machine-specific. Append to your
`.gitignore`:

```text
/agents/instances/
```

Then commit the team resources:

```bash
git add agents .agents .gitignore
git commit -m "Add coordinator/developer/reviewer team from blueprint"
```

For Claude Code, also link the skills dir before committing:

```bash
ln -sfn .agents/skills .claude/skills
git add .claude
```

Never commit `.aw`, invite tokens, private keys, certificates, or instance
directories.

## 3. Create the first instance: coordinator

```bash
mkdir -p agents/instances/coordinator
cd agents/instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../../.. work
ln -sfn AGENTS.md CLAUDE.md   # only if using Claude Code
```

Do **not** link the coordinator soul into the project root as `AGENTS.md`;
many repos already use that file for their own instructions.

## 4. Connect the coordinator to aweb

Use the dashboard for hosted setup: create a team or choose an existing one,
then use the dashboard's connect-agent flow. It prints a command shaped
like:

```bash
AWEB_API_KEY=... AWEB_URL=... aw init ...
```

Run that exact command from `agents/instances/coordinator/`. Do not commit
the generated `.aw` directory. Verify:

```bash
aw workspace status
aw whoami
```

## 5. Publish shared instructions and roles

From the connected coordinator home:

```bash
aw instructions set --body-file ../../instructions.md
aw roles set --bundle-file ../../roles-bundle.json
aw roles show --all-roles
```

Where the installed CLI supports it, you can publish one role at a time
instead: `aw roles add developer --title "Developer" --playbook-file
../../roles/developer.md`.

## 6. Start the coordinator

```bash
cd agents/instances/coordinator
claude
```

If you use Pi, Codex, or another harness, see `adapters/` and adapt the
launch command. The identity/workspace setup stays explicit either way.

## 7. Grow the team later

Developer and reviewer instances are created when work needs them — by the
running team itself, using the `spawn-instance` skill installed at
`.agents/skills/spawn-instance/`. See
[create-instance.md](create-instance.md).
