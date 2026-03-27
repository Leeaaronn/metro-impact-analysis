---
phase: 4
slug: narrative-polish
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-26
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `tests/` directory (existing) |
| **Quick run command** | `make test` |
| **Full suite command** | `make test && make notebook` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `make test`
- **After every plan wave:** Run `make test && make notebook`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | D-07 | notebook-exec | `make notebook` | ✅ | ⬜ pending |
| 04-01-02 | 01 | 1 | D-08 | notebook-exec | `make notebook` | ✅ | ⬜ pending |
| 04-01-03 | 01 | 1 | D-09 | notebook-exec | `make notebook` | ✅ | ⬜ pending |
| 04-01-04 | 01 | 1 | D-10 | notebook-exec | `make notebook` | ✅ | ⬜ pending |
| 04-02-01 | 02 | 1 | D-11–D-15 | unit+notebook | `make test && make notebook` | ✅ | ⬜ pending |
| 04-03-01 | 03 | 2 | D-16–D-18 | file-check | `test -f README.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* `make test` and `make notebook` are already configured. README.md is a new file created during execution.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Narrative reads well for 10-min scan | D-01 | Subjective quality | Read notebook top-to-bottom, check flow |
| Jargon has plain English explanation | D-03 | Semantic check | Search for DiD, p-value, CI — verify explanation follows |
| README under 100 lines | D-18 | Line count | `wc -l README.md` (automated fallback) |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
