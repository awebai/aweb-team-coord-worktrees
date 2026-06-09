# Coordinator + worktree team

This operating pattern has one long-lived coordinator soul plus explicit developer and reviewer instances when work needs them.

## Shape

- `souls/coordinator/` is the durable coordination body. It owns intake, planning, routing, status, and final integration decisions.
- `souls/developer/` is the durable developer body. Concrete developer instances get explicit git worktrees.
- `souls/reviewer/` is the durable reviewer body. Concrete reviewer instances get explicit checkouts/worktrees and should review with fresh eyes.

Actual team aliases are chosen when each instance is connected to aweb and are not committed in this pattern.

The coordinator should not make routine code edits in the shared checkout. It should delegate code changes to an explicit developer instance and ask an explicit reviewer instance for review before merge/release decisions.

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
- Treat `instances/` and git worktrees as explicit local output, not pattern source.
