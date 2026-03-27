# Phase 4: Narrative & Polish - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-26
**Phase:** 04-narrative-polish
**Areas discussed:** Narrative voice & audience, Notebook structure & flow, Figure formatting rules, README scope & format

---

## Narrative Voice & Audience

| Option | Description | Selected |
|--------|-------------|----------|
| Narrative voice & audience | Who is reading this? Academic tone vs conversational? How technical should prose be? | ✓ |

**User's choice:** User provided detailed free-text response covering all aspects
**Notes:** Target is hiring manager with 10 min max. Professional consulting tone, not academic. No unexplained jargon. Every section answers "so what?". Executive summary standalone-readable.

---

## Notebook Structure & Flow

| Option | Description | Selected |
|--------|-------------|----------|
| Notebook structure & flow | Section ordering, integration of narrative with existing code sections | ✓ |

**User's choice:** User provided detailed free-text response
**Notes:** Fixed order: Exec Summary → Data & Methodology → EDA → Stats → Robustness → Limitations → Conclusion. Don't reorganize existing sections — add narrative around them. Exec summary = 5-6 sentences at top. Conclusion = 2-3 sentences directly answering the central question.

---

## Figure Formatting Rules

| Option | Description | Selected |
|--------|-------------|----------|
| Figure formatting rules | Theme, palette, sizes, font sizes, captions | ✓ |

**User's choice:** User provided detailed free-text response
**Notes:** Keep whitegrid + muted. Full-width (12,6), half-width (10,5). Title 14pt, axis 12pt, ticks 10pt. Every figure gets a caption markdown cell below with one-sentence takeaway. No figure should require reading code.

---

## README Scope & Format

| Option | Description | Selected |
|--------|-------------|----------|
| README scope & format | What goes in README, how detailed, length | ✓ |

**User's choice:** User provided detailed free-text response
**Notes:** One-paragraph summary, key finding with DiD result, test badge/screenshot, `make all` setup, structure tree, tech stack, contact placeholder. Under 100 lines. Don't duplicate analysis — point to notebook.

---

## Claude's Discretion

- Exact wording of narrative sections
- Which existing markdown cells need rewriting vs are already sufficient
- Section divider cells between major sections
- Specific figure caption wording

## Deferred Ideas

None — discussion stayed within phase scope
