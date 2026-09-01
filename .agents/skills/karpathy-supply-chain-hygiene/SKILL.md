---
name: karpathy-supply-chain-hygiene
description: 'Apply rigorous supply chain security hygiene to software projects — audit dependencies, detect risks, minimize attack surface. Use this skill when the user wants to audit project dependencies, is concerned about supply chain attacks, wants to set up secure dependency management, needs to review a requirements.txt or package.json, or says "dependency audit", "supply chain risk", "check packages", "secure dependencies", "pin versions", "check pypi". Based on Karpathy 28k-like litellm supply chain post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-minimalism
  - karpathy-agentic-engineering
  - karpathy-vibe-to-agentic
  - karpathy-understanding-first
---

# Skill 11: Supply Chain & Security Hygiene（供应链安全卫生）

> Source: https://x.com/karpathy/status/2036487306585268612
> "Software horror: litellm PyPI supply chain attack" — ~28k likes

## Core Principle

**Every dependency is a door you didn't build, maintained by someone you don't know.**

The litellm incident Karpathy flagged: a widely-used LLM library got compromised via its transitive dependencies. If your project pulled litellm, you were exposed — and you probably didn't even know litellm was in your stack until it was too late.

Karpathy's response: minimize deps, prefer simple implementations, audit everything.

## The Full Dependency Audit

Run this for any project before deployment or after any dependency update:

```
Perform a full supply chain security audit for this project.

Dependency file contents:
[PASTE requirements.txt / package.json / Gemfile / go.mod]

For each direct dependency, analyze:
1. Maintainer health: single maintainer? Last commit? GitHub stars?
2. Transitive depth: how many packages does it pull in?
3. Install-time code execution: does it run arbitrary code on install?
4. Network calls on import: does importing trigger outbound connections?
5. Version pinning: are we using exact versions or ranges?

Risk assessment per package:
- HIGH RISK: (list criteria)
- MEDIUM RISK: (list criteria)  
- LOW RISK: (list criteria)

Priority actions: [what to fix first]
```

## The 5-Minute Pre-Install Check

Before adding any new package:

```
Security pre-check for: [PACKAGE NAME] v[VERSION]

1. PyPI/npm stats: weekly downloads? Known? Established?
2. GitHub: https://github.com/[owner/repo] — stars, last commit, open issues?
3. Transitive deps: run `pip show [package]` or `npm ls [package]` — how deep does it go?
4. setup.py / postinstall: does it run code on install?
5. Import-time behavior: what does `import [package]` actually do?

Risk verdict: SAFE / VERIFY_FURTHER / AVOID
Alternative: if risky, what can I use instead or implement myself?
```

## Requirements File Hardening

Transform a loose requirements file to a pinned, audited one:

```
Harden this requirements.txt / package.json for production security.

Current file:
[PASTE FILE]

Output a new version that:
1. Pins all packages to exact versions (== not ~=)
2. Adds a comment for each package: what it's used for, why we need it
3. Flags any packages that could be eliminated with minimal effort
4. Groups by category: core / dev / testing
5. Adds a header comment with: last audited date, total dep count, audit command to run

Also: what command should I run to check for known vulnerabilities?
```

## The Minimal Dependency Philosophy

For each feature you're about to add via a package:

```
I'm about to add [PACKAGE] to solve [PROBLEM].

Before I do: help me evaluate if I should implement this myself instead.

The function I need: [SPECIFIC FUNCTION/CAPABILITY]

Can this be implemented with:
- Python stdlib only (in < 50 lines)?  YES/NO
- One simple function I can paste inline?  YES/NO

If yes to either: write the minimal implementation I need.
If no: confirm the package is the right choice and suggest the safest way to import it.
```

## Containerization + Isolation Template

For any project that pulls external dependencies:

```dockerfile
# Dockerfile template — minimal, audited, isolated
FROM python:3.11-slim  # pin exact base image

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy ONLY requirements first (layer caching)
COPY requirements.txt .

# Install with hash verification
RUN pip install --no-cache-dir --require-hashes -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "app.py"]
```

```
# requirements.txt with hashes (generate with pip-compile --generate-hashes)
requests==2.31.0 \
    --hash=sha256:58cd2187423839823... \
    --hash=sha256:942c5a758f98d79...
```

## Incident Response Checklist

If you discover a supply chain compromise:

```markdown
IMMEDIATE (within 1 hour):
- [ ] Identify: which version of which package is compromised?
- [ ] Check: is this version in our requirements.txt / lock file?
- [ ] Check: is this version installed in any running service?
- [ ] Isolate: take affected services offline if credentials could be exposed

SHORT-TERM (within 24 hours):
- [ ] Rotate: any credentials, tokens, API keys that ran in the affected environment
- [ ] Audit: what data could have been accessed/exfiltrated?
- [ ] Update: pin to a safe version or remove the package
- [ ] Scan: check all other packages for similar issues

LONG-TERM:
- [ ] Add automated scanning (pip-audit, npm audit, Dependabot)
- [ ] Implement hash pinning for critical projects
- [ ] Consider: can we eliminate this dependency entirely?
```

## Scanning Commands Reference

```bash
# Python
pip-audit                           # check for known vulns
pip freeze | pip-audit --stdin      # audit installed packages
safety check                        # alternative scanner

# Node.js  
npm audit
npm audit fix                       # auto-fix where safe

# Check transitive deps
pip show [package]                  # see direct deps
pip-tree [package]                  # see full tree

# Generate hashed requirements
pip-compile --generate-hashes requirements.in
```

## Workflow

**属于工作流：想法到上线（第4步）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第4步（安全检查） | karpathy-minimalism（瘦身后） | karpathy-vibe-to-agentic（最终收尾） |

完整链路：idea-files → agentic-engineering → minimalism → supply-chain-hygiene → vibe-to-agentic

## Prompt Contract

```text
Audit this dependency before I install it: <PACKAGE_NAME> v<VERSION>. Produce: 1) Transitive dependency count and tree, 2) Maintainer activity (last commit, bus factor), 3) Known CVEs or security advisories, 4) Any postinstall hooks or network calls on import, 5) Safer minimal alternative (or "implement yourself in N lines"), 6) Pinned install command if approved. Risk score: LOW/MEDIUM/HIGH. Recommendation: USE/AVOID/IMPLEMENT_YOURSELF.
```

## Verification Checklist

- [ ] 所有依赖都有 pinned version（==，不是 >=）
- [ ] 已检查 transitive dependency 数量
- [ ] 无 postinstall hook 或已审查其内容
- [ ] 单一维护者的包已标记风险
- [ ] 对高风险依赖提供了自实现替代方案
- [ ] lockfile（requirements.txt / package-lock.json）已提交到 repo
