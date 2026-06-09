# Coordinator + worktree team

This team was created from the `coordinator-with-dev-review` blueprint: one
long-lived coordinator, developer instances in explicit git worktrees, and
ephemeral fresh-eyes reviewers. The full model is in
`agents/docs/team-architecture.md`.

## Shape

- `agents/souls/<role>/` are the durable, committed agent bodies. They grow
  with the team (docs, decisions, memory) and are reviewed like code.
- `agents/instances/<name>/` are runnable, gitignored copies of souls, each
  with its own aweb identity. One soul can back many instances; aliases are
  `<role>` for standing singletons and `<role>-<purpose>` for work-specific
  instances.
- The coordinator routes; developers implement in their own worktrees;
  reviewers verify independently. The coordinator does not make routine code
  edits and nothing merges without independent review.

## Operating loop

At session start, every agent runs:

```bash
aw workspace status
aw mail inbox
aw chat pending
aw roles show
```

Use `aw mail` for handoffs, review requests, and status updates. Use
`aw chat` only when someone is blocked on a near-term answer.

## Handoff pattern

1. Coordinator defines a small task with acceptance criteria and sends it to
   a developer instance.
2. The developer works in its own git worktree, keeps changes small, and
   reports evidence/tests.
3. Independent review comes from a reviewer instance with fresh eyes.
4. The reviewer reports blocking findings or ACK.
5. The coordinator decides: merge, request amendments, or escalate to the
   human.

## Ground rules

- Keep work small and reviewable.
- Prefer shared aweb state over private TODO lists.
- Spawn instances only on explicit human request or a documented workflow
  step (see the `spawn-instance` skill); retire one-shot instances when
  their job is done.
- Grow your soul per the `self-maintenance` skill; never edit your own
  AGENTS.md or role.
- Do not overwrite another agent's workspace state or `.aw/` directory.
