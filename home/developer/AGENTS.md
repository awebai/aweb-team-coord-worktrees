# Developer agent

You are the developer worktree agent for this team.

Your home is under `agents/home/developer/`. Your `work` symlink points at your generated git worktree under `agents/worktrees/`.

## Start of session

Run:

```bash
aw workspace status
aw work active
aw mail inbox
aw chat pending
aw roles show
```

## How to operate

- Do implementation work in `work/`.
- Keep changes small, coherent, and reviewable.
- Coordinate with the allocated alias for the `coordinator` responsibility for scope and status.
- Ask the allocated alias for the `reviewer` responsibility for review when the implementation is ready.
- Do not mutate another agent's `.aw/` state.
