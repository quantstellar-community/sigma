---
name: karpathy-minimalism
description: 'Apply Karpathy-style minimalism and anti-dependency principles to code and system design. Use this skill when the user wants to reduce dependencies, avoid supply chain risks, rewrite something in pure Python or minimal code, audit a project for bloat, design agent-native CLI tools, or says "too many dependencies", "minimize deps", "pure python", "yoink this", "vibe code this", "no frameworks", "agent-native design". Based on 28k-like litellm attack post and 25k-like 243-line GPT post.'
disable-model-invocation: false
user-invocable: true
related_skills:
  - karpathy-agentic-engineering
  - karpathy-supply-chain-hygiene
  - karpathy-vibe-to-agentic
  - karpathy-education-first
---

# Skill 4: Minimalism & Agent-Native Design（极简主义 + 代理原生设计）

> Source: https://x.com/karpathy/status/2036487306585268612 | https://x.com/karpathy/status/2021694437152157847
> litellm supply chain attack (~28k likes) | 243-line pure Python GPT (~25k likes)

## Core Principle

**Every dependency is a liability. Every abstraction you don't understand is a risk.**

Karpathy's rule: if you can implement the core in 200 lines of pure Python — do it. Don't install a package that installs 47 transitive dependencies just to get 3 functions.

And: design everything so an LLM agent can use it without friction — CLI-first, markdown-structured, zero magic.

## The Minimalism Decision Tree

Before `pip install` or `npm install` anything:

```
Q1: Can I implement the core function in < 300 lines?
    → YES: Write it. Paste below as reference.
    → NO: Continue to Q2

Q2: Does this package have < 5 transitive dependencies?
    → YES: OK to use, but pin the version
    → NO: Continue to Q3

Q3: Is this a well-known, audited package (requests, numpy, etc.)?
    → YES: Use it, but still pin version
    → NO: STOP. Either find a simpler alternative or implement yourself.
```

## Dependency Audit Prompt

Run this before adding anything to a project:

```
Audit this dependency for supply chain risk:

Package: [PACKAGE_NAME] v[VERSION]

1. List ALL transitive dependencies (not just direct)
2. Check for recent security advisories
3. Identify any dependencies that are maintained by a single person with < 100 GitHub stars
4. Check if the package does any network calls on import
5. Check if install scripts run arbitrary code (setup.py, postinstall hooks)

Risk score: LOW / MEDIUM / HIGH
Recommendation: USE / AVOID / IMPLEMENT_YOURSELF
```

## The "Yoink" Pattern (Karpathy's term)

Instead of installing a package, copy the specific function you need:

```
Given this package: [PACKAGE_URL or PASTE CODE]

Extract ONLY the function(s) I need for: [SPECIFIC_USE_CASE]

Requirements:
- Pure Python (stdlib only, no imports except builtins + [ALLOWED_STDLIB])
- Under [N] lines
- Add a comment: "# yoinked from [source] on [date]"
- Include a docstring explaining what it does

I need: [SPECIFIC_FUNCTION_NAME or DESCRIPTION]
```

## Agent-Native Design Principles

Make everything legible to LLM agents:

| ❌ Agent-Hostile | ✅ Agent-Native |
|----------------|----------------|
| GUI-only tools | CLI with clear flags |
| JSON config with magic keys | Commented YAML or Markdown config |
| Monolithic functions | Small, named, single-purpose functions |
| Error: "something went wrong" | Error: "Step 3 failed: expected X, got Y. Try: [suggestion]" |
| Relative paths everywhere | Explicit absolute paths |
| Stateful side effects | Pure functions with explicit IO |

## Minimal Implementation Template

When "yoinking" or implementing from scratch:

```python
#!/usr/bin/env python3
"""
[FUNCTION_NAME] — minimal implementation
yoinked/inspired from: [SOURCE]
date: [DATE]
dependencies: none (stdlib only)

Usage:
    python3 [filename].py [args]
    
Or import:
    from [filename] import [function]
"""

# ---- core implementation ---- (~100 lines max for core logic)

def [function](input):
    """
    [One sentence description]
    
    Args:
        input: [type and description]
    Returns:
        [type and description]
    """
    # implementation
    pass


# ---- CLI entry point ----
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 [filename].py [input]")
        sys.exit(1)
    result = [function](sys.argv[1])
    print(result)
```

## The 243-Line GPT Lesson

Karpathy implemented a full GPT training + inference in 243 lines of pure Python to prove a point: understanding the core matters more than using the abstracted version.

**Apply this to any tool you regularly use:**

```
Implement a minimal version of [TOOL/CONCEPT] from scratch.

Requirements:
- Pure Python, stdlib only
- Under 300 lines
- Must demonstrate the core algorithm (not just wrap an API)
- Include inline comments explaining WHY each step works

This is for learning, not production.
Start with the simplest possible working version.
```

## Security Hygiene Checklist

```markdown
Before adding any dependency:
- [ ] Checked PyPI/npm for recent security advisories
- [ ] Verified maintainer is active (last commit < 6 months)
- [ ] Reviewed install scripts (setup.py, package.json scripts)
- [ ] Pinned exact version: package==1.2.3 (not ~=1.2)
- [ ] Checked transitive dep count (pip show --files or npm ls --all)
- [ ] Considered: can we implement this in < 200 lines instead?

For existing projects:
- [ ] Run: pip-audit or npm audit
- [ ] Check for packages not in requirements.txt (pip freeze vs requirements diff)
- [ ] Verify no packages make network calls on import
```

## Workflow

**属于工作流：想法到上线（第3步）**

| 位置 | 上游 | 下游 |
|------|------|------|
| 第3步（瘦身） | karpathy-agentic-engineering（实现后） | karpathy-supply-chain-hygiene（安全审查） |

完整链路：idea-files → agentic-engineering → minimalism → supply-chain-hygiene → vibe-to-agentic

## Prompt Contract

```text
Audit this project/code for dependency minimalism: <PASTE_CODE_OR_DESCRIBE>. For each dependency: 1) Is it needed? What specific feature does it provide? 2) Can it be replaced with < 200 lines of stdlib code? 3) How many transitive deps does it pull in? 4) Risk score (LOW/MED/HIGH). Then produce a minimized version plan: what to keep, what to yoink, what to rewrite. Output a dependency budget: max N packages, each justified.
```

## Verification Checklist

- [ ] 每个依赖都有存在理由（不是「方便」）
- [ ] 能用 < 200 行实现的已标记为「可 yoink」
- [ ] transitive dependency 总数在预算内
- [ ] 核心逻辑不依赖任何可能被删的包
- [ ] Agent 可以在只有 stdlib 的环境里跑核心功能
- [ ] CLI 入口简单明了（不需要额外工具就能用）
