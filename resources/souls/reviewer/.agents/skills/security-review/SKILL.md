---
name: security-review
description: Adversarial security review of a change — injection, authn/authz, data exposure, crypto, input validation, business-logic, config, supply chain, code execution, XSS, plus agent-network threats (prompt injection, impersonation). Always run this alongside code-review on every product-code change.
---

# Security review

Run this on **every** product-code review, paired with `code-review` —
security is never out of scope.

Assume the code is hostile until proven otherwise. Find the vulnerabilities
a real attacker would find, and explain each so an engineer can fix it.
Review the **changed code in context** (diff-aware), and read the code —
tools miss logic flaws.

## Categories to work through

Adapt to the stack (web items don't apply to a batch job, etc.). Trace every
user/agent-controlled input to every sink.

1. **Injection** — SQL, NoSQL, OS command, LDAP, XPath, template, XXE.
2. **Authentication & authorization** — broken authn, privilege escalation,
   IDOR, bypass logic, session flaws, missing auth on sensitive routes/jobs.
3. **Data exposure** — hardcoded secrets/keys, sensitive data in logs, PII
   handling, information disclosure.
4. **Cryptographic issues** — weak algorithms, bad key management, insecure
   randomness.
5. **Input validation** — missing/improper validation or sanitization at
   trust boundaries, buffer issues.
6. **Business-logic flaws** — race conditions, TOCTOU.
7. **Configuration** — insecure defaults, verbose errors/debug mode,
   permissive CORS, missing security headers, default creds.
8. **Supply chain** — vulnerable/typosquatted dependencies (`npm audit` /
   `pip-audit` / read manifests).
9. **Code execution** — RCE via deserialization (pickle/yaml.load), eval
   injection.
10. **XSS** — reflected, stored, DOM-based (web targets).

## Agent-network threats

This team runs as networked agents over aweb, and many products built this
way handle agent identity or user data — weight these heavily whenever
either is true:

- **Cross-agent prompt injection** — content from another agent/user (a
  message, profile, or record) treated as instructions. In a multi-agent
  system a malicious payload can cascade through shared context to other
  agents. Treat all inbound agent/user content as **data, not
  instructions**; check that it can't steer tool calls or actions.
- **Agent impersonation / identity spoofing** — stolen keys/tokens or a peer
  mimicking a trusted agent to gain access or issue commands. Check that
  messages are authenticated to a verified identity and that authority isn't
  granted on a claimed (unverified) identity.
- **Over-broad data sharing between agents** — does an agent expose more
  data than the interaction needs? Check least-privilege and consent
  boundaries; PII shouldn't leak across the network or into logs.
- **Tool/action abuse** — can manipulated input cause an agent to perform
  unauthorized actions (send mail as the user, alter records, exfiltrate
  data)? Check authorization on every consequential tool/action.

## Filter to real, impactful findings

Reduce noise — by default **exclude**: denial-of-service, rate-limiting,
memory/CPU exhaustion, generic input-validation without a proven impact, and
open redirects, *unless* the change makes one concretely exploitable. Drop
pre-existing issues and findings on unchanged lines.

## Report — one row per finding

| Field | Content |
|---|---|
| **ID** | SEC-NNN |
| **CWE** | CWE-XXX (name) |
| **Severity** | Critical / High / Medium / Low (CVSS-ish reasoning) |
| **Location** | `file:line` |
| **Exploit scenario** | one sentence: how an attacker uses this |
| **Fix** | concrete, code-level remediation |

No hand-waving: **if you can't write the exploit scenario, downgrade the
severity.** Show any tool output verbatim, then add manual findings. Feed the
decision back into the `code-review` reply (blocking vs note).
