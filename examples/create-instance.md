# Create a concrete instance

A soul is the durable body in `souls/<role>/`. An instance is a concrete
workspace with its own aweb identity and optional git worktree.

Create instances only when you need them.

## Coordinator instance

A coordinator often works from the main checkout:

```bash
cd /path/to/your/project
# Run the dashboard-generated aw init/connect command for alias coordinator.
ln -sfn souls/coordinator/AGENTS.md AGENTS.md
```

If your harness expects a different instruction filename, add that adapter link
explicitly, for example:

```bash
ln -sfn AGENTS.md CLAUDE.md
```

## Developer worktree instance

```bash
cd /path/to/your/project
git worktree add instances/dev-task-123 -b dev-task-123
cd instances/dev-task-123

# Run the dashboard-generated aw init/connect command for alias dev-task-123.
ln -sfn ../../souls/developer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md
```

## Reviewer worktree instance

```bash
cd /path/to/your/project
git worktree add instances/review-task-123 -b review-task-123
cd instances/review-task-123

# Run the dashboard-generated aw init/connect command for alias review-task-123.
ln -sfn ../../souls/reviewer/AGENTS.md AGENTS.md
ln -sfn AGENTS.md CLAUDE.md
```

## Clean up

Before deleting an instance, preserve useful branch/soul changes and revoke or
remove the team membership through the dashboard or your team's chosen admin
flow. Then remove the explicit worktree:

```bash
git worktree remove instances/dev-task-123
git branch -D dev-task-123  # only if the branch is no longer needed
```
