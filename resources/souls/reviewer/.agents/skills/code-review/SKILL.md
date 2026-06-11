---
name: code-review
description: Systematic, pragmatic review of a change for correctness, security, error handling, simplicity, naming, DRY, tests, and performance. Use when reviewing a developer's branch or commit.
---

# Code review

A thorough-yet-pragmatic review of a single change. Catch real issues;
respect the author's time. Review the **changed code in context** — not the
whole codebase.

## 1. Get the change

```bash
git fetch --all --prune
git diff main...<branch>        # the change set (named in the review request)
git log --oneline main..<branch>
```

Read surrounding code only as needed to understand the change. Note the
language, framework, and any `AGENTS.md`/project conventions that apply.

## 2. Understand the intent

Before critiquing, know what the change is for: read the request, commits,
and any acceptance criteria. Review against the intent, not your preference.

## 3. Review systematically

- **Correctness & logic** — does it do what it should? off-by-one, nil/null,
  race conditions, boundary/edge cases, control flow.
- **Security** — exposed secrets/credentials; unvalidated/unsanitized input;
  injection; broken authn/authz; unguarded sensitive ops. **Always run the
  `security-review` skill alongside this one** — every code review includes
  a security review; never skip it.
- **Error handling** — errors caught (not swallowed); informative but not
  leaky messages; cleanup on error paths; specific (not blanket) catches.
- **Simplicity & readability** — can another dev understand it quickly?
  needless complexity? self-documenting?
- **Naming** — names express purpose; consistent with surrounding code.
- **DRY** — duplicated logic or a missing abstraction.
- **Tests** — adequate coverage for new/changed behavior; tests assert real
  behavior (not just that mocks were called); edge/error paths covered.
- **Performance** — N+1 queries, needless loops, blocking ops that should be
  async, loading large datasets into memory.
- **Convention/contract** — matches project conventions and any contracts
  other agents publish and consume.

## 4. Verify before flagging (keep false positives low)

For each candidate issue, gut-check confidence and **drop the weak ones**:

- **Drop** pre-existing issues (not introduced by this change), pedantic
  nitpicks a senior engineer wouldn't raise, and anything a
  linter/typechecker/compiler/CI would catch — assume CI runs those.
- **Drop** issues on lines the change didn't touch.
- **Keep** only what you can justify: a real, likely-hit problem, or a real
  convention/contract violation. If you can't show why it's real, either
  downgrade it to a non-blocking nit or drop it.

Distinguish **"this is definitely wrong"** from **"this might be an issue."**
Say which. If unsure, say so.

## 5. Report

Lead with the decision, then concrete findings with exact `file:line`. Group
by severity:

- **🔴 Blocking** — security holes, exposed secrets, logic errors that will
  fail, missing essential error handling, data-corruption risks. For each:
  file:line, the problem, why it's dangerous, and a concrete fix.
- **🟡 Should-fix** — duplication, intent-obscuring names, missing
  validation, inadequate tests, perf concerns. For each: file:line, issue,
  suggestion.
- **🟢 Consider** — simplifications, minor refactors, docs.
- **✅ Done well** — call out genuinely good work.

Reply over chat with ACK, amendments, or needs-judgment. Be specific and
actionable; explain *why*, not just *what*; give fix examples where it
helps.
