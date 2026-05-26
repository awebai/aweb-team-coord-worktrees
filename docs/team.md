# Coordinator + worktree team

This team has one long-lived coordinator workspace and two code worktree agents.

## Shape

- `agents/coordinator/` is the persistent coordination home. It owns intake, planning, routing, status, and final integration decisions.
- `worktrees/<repo>-dev/` is the developer worktree agent for implementation changes.
- `worktrees/<repo>-review/` is the reviewer worktree agent for independent review.

The coordinator should not make routine code edits in the shared work directory. It should delegate code changes to the developer worktree and ask the reviewer worktree for review before merge/release decisions.

## Operating loop

At session start, every agent should run:

```bash
aw workspace status
aw mail inbox
aw chat pending
aw roles show
```

Use `aw mail` for handoffs, review requests, and status updates. Use `aw chat` only when someone is blocked on a near-term answer.

## Handoff pattern

1. Coordinator defines a small task and sends it to the developer.
2. Developer works in its own git worktree, keeps changes small, and reports evidence/tests.
3. Coordinator asks reviewer for an independent review.
4. Reviewer reports blocking findings or ACK.
5. Coordinator decides whether to merge, request amendments, or escalate.

## Ground rules

- Keep work small and reviewable.
- Prefer shared aweb state over private TODO lists.
- Do not overwrite another agent's workspace state or `.aw/` directory.
- Treat `worktrees/` as generated local output, not template source.
