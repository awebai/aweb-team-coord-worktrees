---
name: get-code-reviewed
description: How a developer instance gets each commit reviewed without blocking. Use after EVERY commit on your branch — it launches a FRESH reviewer instance to review that commit asynchronously while you keep coding, you fold its findings in at a natural break, and you retire that reviewer once it returns its verdict. This is the sanctioned workflow that lets a developer spawn a reviewer.
---

# Get your code reviewed (a fresh reviewer per commit)

Review shouldn't stall your flow, and it should be **genuinely independent**.
So after each commit you launch a **brand-new reviewer instance** to review
that commit while you move on to the next piece of work — then you retire it
once it reports back. A *fresh* reviewer each time (never a reused, live one)
is the whole point: each review starts from the code with no memory or bias
from your previous commits, which is exactly what makes review worth
anything.

This is the **documented workflow** that sanctions a developer spawning a
reviewer (see the spawn rule in your AGENTS.md). Follow it **after every
commit** on your branch — including the commits where you fix earlier
findings.

## The cycle (per commit)

```
commit ──▶ launch a FRESH reviewer ──▶ chat it the request (non-blocking) ──▶ keep working
                                                          │
   reviewer reviews main…<branch> fresh ──▶ chats back ACK or amendments
                                                          │
   at a natural break: read it, retire that reviewer, and if amendments,
   fix them in your next commit (which gets its own fresh reviewer)
```

## 1. After a commit — launch a fresh reviewer for it

You committed in your **`work/`** tree (on your branch). You now spawn and
message the reviewer **from your home** — that's where your `aw` identity
lives — while reading the commit info from `work/` (`git -C work …`).

Use the **`spawn-instance`** skill — it has the full how-to. Run it from your
home and pass it the specifics:

- **role:** `reviewer`
- **name:** `reviewer-$(git -C work rev-parse --short HEAD)` — the short SHA
  of the commit you just made in `work/`; unique to THIS commit, never
  reused
- **launch with the reviewer soul's runtime, in tmux** (spawn-instance's
  auto-launch path). Reviewing on a different runtime than the author also
  keeps review independent — this blueprint's reviewer soul defaults to Pi.

Then tell it what to review over **chat** — the request and the verdict are
one short conversation, and chat keeps them in a single thread you can poll
at your next break. Run this from your home:

```bash
sha="$(git -C work rev-parse --short HEAD)"      # the commit to review (your branch HEAD, in work/)
br="$(git -C work branch --show-current)"        # your branch (= your instance name)
name="reviewer-$sha"
aw chat send-and-leave "$name" \
"Please review branch $br at commit $sha — diff against main (git diff main...$br).
Reply ACK if clean, or amendments with file:line. One-shot review for this commit." \
--start-conversation
```

`send-and-leave … --start-conversation` is **fire-and-forget**: it hands the
message off and returns immediately, so you don't block. Then carry on with
your next piece of work.

> **Use the non-blocking primitive.** Do **not** use `aw chat send-and-wait`
> — it holds your shell until the reviewer replies, which is *minutes* (a
> fresh session booting then running code-review + security-review over the
> diff). Mail would also wake a channel-connected reviewer, but the verdict
> exchange is conversational: chat keeps request and reply in one thread
> with waiting semantics, and `send-and-leave` stays async.

## 2. Fold in findings at a natural break

Check `aw chat pending` between steps (not mid-thought) — the reviewer's
reply lands there; read it with `aw chat history "$name"`. When that reviewer
replies:

- **ACK** → that commit is clean. Retire the reviewer (step 3).
- **Amendments** → retire the reviewer (step 3), then address every finding.
  Your fix is a **new commit**, so it gets its own fresh reviewer (back to
  step 1).

Don't let findings pile up across commits — clear them at the next break.

## 3. Retire the reviewer (every time)

A reviewer reviews exactly one commit. It closes its own session once it has
sent its verdict over chat; once you've read that verdict, run the
**`spawn-instance`** skill's tear-down to finish retiring it — delete its
workspace + identity and remove its instance dir — so reviewers don't pile
up on the network.

## Done

Your work is **done** when your **latest** commit comes back **ACK with no
remaining issues** and you've retired that reviewer. Then report done to the
coordinator and hand off your branch. You never merge.

## Notes

- This cycle is for your own **build** work. If you were handed a task to
  **fix specific review findings** on a branch, you do not run this — just
  fix them and report back; whoever asked you re-checks the fix.
- A fresh reviewer **per commit** — never keep one alive across commits, and
  never reuse one. Independence comes from the fresh start.
- This is the *only* routine reason to spawn an agent. Spawning anything
  else still needs a human's explicit say-so.
- The reviewer uses its own `code-review` + `security-review` skills; you
  only tell it *what* to review (branch + commit), never *how*.
