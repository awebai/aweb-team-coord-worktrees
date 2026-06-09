# Deploy this operating pattern

This is an explicit, reviewable deployment. It does not create `.aw` state,
identities, worktrees, or branches for you.

## 1. Install resources into your project

```bash
git clone https://github.com/awebai/aweb-team-coord-worktrees.git
cd aweb-team-coord-worktrees
./scripts/install-local.sh /path/to/your/project
```

Review the copied files before committing them:

```bash
cd /path/to/your/project
git status --short
find souls team-operating-patterns/coordinator-with-dev-review .agents/skills -maxdepth 3 -type f | sort
```

## 2. Create or choose your aweb team

Use the dashboard for hosted setup. Create a team or choose an existing one, then
use the dashboard's connect-agent flow for each concrete workspace you want to
connect.

The dashboard will print a released-safe command shaped like:

```bash
AWEB_API_KEY=... AWEB_URL=... aw init ...
```

Run that command from the workspace/instance directory it should bind. Do not
commit the generated `.aw` directory.

## 3. Publish shared instructions and roles

From the project root after one workspace is connected:

```bash
aw instructions set --body-file team-operating-patterns/coordinator-with-dev-review/instructions.md
aw roles set --bundle-file team-operating-patterns/coordinator-with-dev-review/roles-bundle.json
aw roles show --all-roles
```

## 4. Commit the pattern resources

Commit only reviewable, identity-free files:

```bash
git add souls .agents/skills team-operating-patterns/coordinator-with-dev-review
git commit -m "Add coordinator/developer/reviewer operating pattern"
```

Never commit `.aw`, invite tokens, private keys, generated certificates, or local
instance/worktree directories unless your team deliberately tracks a non-secret
part of that layout.
