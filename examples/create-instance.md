# Create a concrete instance

A soul is the durable body in `souls/<role>/`. An instance is a concrete
workspace with its own aweb identity and optional git worktree.

Create instances only when you need them. Keep them local with:

```bash
printf '/instances/\n' >> .git/info/exclude
```

## Coordinator instance

The noob-safe coordinator path uses a local instance directory rather than
writing `AGENTS.md` at the project root.

```bash
cd /path/to/your/project
mkdir -p instances/coordinator
cd instances/coordinator
ln -sfn ../../souls/coordinator/AGENTS.md AGENTS.md
ln -sfn ../.. work

# Run the dashboard-generated aw init/connect command here for alias coordinator.
```

If your harness expects a different instruction filename, add that adapter link
explicitly, for example:

```bash
ln -sfn AGENTS.md CLAUDE.md
```

Start it from the instance directory:

```bash
claude
```

## Developer worktree instance

Commit or stash your current project changes before adding a git worktree.

```bash
cd /path/to/your/project
git worktree add instances/dev-task-123 -b dev-task-123
cd instances/dev-task-123
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md  # only if using Claude Code

# Run the dashboard-generated aw init/connect command here for alias dev-task-123.
```

Then launch your chosen harness from `instances/dev-task-123/`.

## Reviewer worktree instance

```bash
cd /path/to/your/project
git worktree add instances/review-task-123 -b review-task-123
cd instances/review-task-123
ln -sfn ../../souls/reviewer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md  # only if using Claude Code

# Run the dashboard-generated aw init/connect command here for alias review-task-123.
```

Reviewers should review the requested branch/ref with fresh eyes and avoid
recording biasing memory about specific changes.

## Clean up

Before deleting an instance, preserve useful branch/soul changes and revoke or
remove the team membership through the dashboard or your team's chosen admin
flow. Then remove the explicit worktree:

```bash
git worktree remove instances/dev-task-123
git branch -D dev-task-123  # only if the branch is no longer needed
```

For a non-worktree instance such as `instances/coordinator`, remove the directory
after preserving any useful local files and revoking/removing membership.
