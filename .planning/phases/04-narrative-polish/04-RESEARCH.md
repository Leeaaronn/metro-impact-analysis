# Phase 4: Narrative & Polish - Research

**Researched:** 2026-03-26
**Domain:** Jupyter notebook narrative writing, figure formatting, portfolio README
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Audience & Tone**
- D-01: Target reader is a hiring manager scanning portfolios — 10 minutes max reading time
- D-02: Tone is professional but not academic — write like a consulting analyst presenting to a client, not a PhD defending a thesis
- D-03: No jargon without a one-sentence plain English explanation immediately after
- D-04: Every section must answer "so what?" — interpret numbers, don't just report them
- D-05: Executive summary must be readable by someone who skips everything else

**Notebook Structure & Flow**
- D-06: Section order: Executive Summary (no code) → Data & Methodology → Exploratory Analysis → Statistical Tests → Robustness Checks → Limitations → Conclusion
- D-07: Executive summary at the very top — 5-6 sentences covering the answer to the central question, key numbers, and a one-line methodology description
- D-08: Methodology section explains DiD in 2-3 sentences with the formula, then defines treatment/control/pre/post windows
- D-09: Do NOT reorganize existing EDA and stats sections — add narrative markdown cells around them
- D-10: Conclusion should be 2-3 sentences that directly answer "did the extension cause ridership changes?"

**Figure Formatting**
- D-11: Keep current whitegrid + muted palette (already set in viz.py `set_default_theme()`)
- D-12: Figure sizes: `figsize=(12, 6)` for full-width, `(10, 5)` for half-width
- D-13: Font sizes: title 14, axis labels 12, tick labels 10
- D-14: Every figure gets a caption as a markdown cell immediately below it explaining the takeaway in one sentence
- D-15: No figure should require reading the code to understand what it shows

**README Scope & Format**
- D-16: Include: one-paragraph project summary, key finding (one sentence with DiD result), screenshot or badge showing tests passing, setup instructions (`make all`), project structure tree, tech stack list, contact info placeholder
- D-17: Don't duplicate the full analysis — point readers to the notebook
- D-18: Keep README under 100 lines — portfolio README, not documentation

### Claude's Discretion
- Exact wording of narrative sections (following tone/audience decisions above)
- Which existing markdown cells need rewriting vs which are already good enough
- Whether to add section divider cells between major notebook sections
- Specific figure caption wording

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

## Summary

Phase 4 is a writing and presentation phase. No new analysis or code will be written. The deliverable is a polished `notebooks/analysis.ipynb` that tells a complete story from research question through conclusion, plus a new `README.md` at the project root.

The notebook already has 48 cells covering EDA (cells 7–26) and statistical analysis (cells 27–47). The Phase 4 work inserts narrative markdown cells at the top (executive summary), between setup and EDA (methodology), and after the robustness checks (limitations + conclusion). Figure formatting updates land in `src/viz.py` plot functions and individual notebook code cells.

The actual DiD result that must appear in the executive summary and README is: the Foothill Extension increased Gold Line ridership by approximately **38,120 average daily boardings** (p < 0.001, 95% CI [28,686; 47,554]), representing a doubling of pre-extension ridership (pre mean: 27,363; post mean: 55,347; +102%). This number is confirmed by running the analysis against `data/clean/ridership_clean.csv`.

**Primary recommendation:** Add narrative cells around existing analysis structure — do not restructure cells. Draft each section with the consulting-analyst voice, then apply figure formatting patches as a second pass.

---

## Actual Analysis Numbers (Confirmed)

The planner and implementer MUST use these verified numbers, not placeholders:

| Metric | Value |
|--------|-------|
| DiD coefficient (Treatment x Post) | +38,120 avg daily boardings |
| DiD standard error | 4,813 |
| DiD p-value | < 0.001 (highly significant) |
| DiD 95% CI | [28,686 ; 47,554] |
| R-squared | 0.137 |
| N observations | 461 |
| Gold Line pre mean | 27,363 avg daily boardings |
| Gold Line post mean | 55,347 avg daily boardings |
| Gold Line % change | +102.3% |
| Paired t-test (Gold pre vs post) | p < 0.001, Cohen's d = 5.25 (large) |
| Independent t-test (Gold post vs control post) | p = 0.023, Cohen's d = -0.39 (small) |
| Parallel trends p-value | 0.038 (marginal; must be flagged in limitations) |
| No-Expo DiD coefficient | +43,811 (consistent with primary) |

**Source:** Direct execution against `data/clean/ridership_clean.csv` using `src/stats.py:did_regression()` — 2026-03-26.

---

## Standard Stack

This phase uses no new libraries. All tools are already installed in `requirements.txt`.

### Core (already installed)
| Library | Version | Purpose |
|---------|---------|---------|
| jupyter | 1.1.1 | Notebook editing environment |
| nbconvert | 7.16.6 | `make notebook` validation after edits |
| seaborn | 0.13.2 | Figure theme already applied in `set_default_theme()` |
| matplotlib | 3.9.3 | Font size and figsize parameters |

**No new `pip install` commands needed for this phase.**

---

## Architecture Patterns

### Notebook Cell Structure (existing pattern, must be preserved)
```
[markdown] ## Section Header + explanation of what and why
[code]     execution
[markdown] **Interpretation:** one-sentence takeaway (or caption for figures)
```
CLAUDE.md mandates: "Markdown cells must outnumber code cells or be roughly equal." The current notebook has 28 markdown cells and 20 code cells (ratio: 1.4:1). Phase 4 adds ~10 markdown cells (executive summary 2, methodology 3, limitations 2, conclusion 1, section dividers 2) — improving the ratio to ~1.8:1.

### Insertion Points (by existing cell index)
| New Content | Insert Position | Type |
|-------------|-----------------|------|
| Executive Summary (2 cells) | Before cell 0 (push existing cells down) | markdown |
| Methodology section (3 cells) | After cell 6 (after analysis window setup) | markdown |
| Figure captions (6 cells) | After each of cells 8, 10, 12, 18, 20, 25 | markdown |
| Limitations section (2 cells) | After cell 47 (after Phase 3 summary) | markdown |
| Conclusion (1 cell) | After limitations | markdown |

Note: After executive summary insertion, all existing cell indices shift by 2. The planner should specify insertions by content landmark, not raw index.

### Figure Formatting Pattern
All five plot functions in `src/viz.py` need tick label font size added. Current `set_default_theme()` sets title (14) and axis labels (12) but not tick labels (10). The fix is one `rcParams` line:

```python
# In src/viz.py:set_default_theme()
plt.rcParams.update({
    "figure.dpi": 120,
    "figure.figsize": (12, 6),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,   # ADD THIS
    "ytick.labelsize": 10,   # ADD THIS
})
```

The `plot_ridership_trends` and `plot_treatment_vs_control` functions already use `figsize=(14, 7)` and `(14, 6)` respectively — these override the rcParams default. Per D-12, full-width figures should be `(12, 6)`. Both functions should be updated to `(12, 6)`.

`plot_distributions` uses `figsize=(6 * n_groups, 5)` — for 4 groups this is (24, 5), which is oversized. Change to `(10, 5)` for the 2-group use case (pre/post Gold) or `(12, 5)` for 4-group (pre/post × treatment/control).

`plot_boxplot_comparison` uses `(10, 6)` — acceptable, matches D-12's half-width `(10, 5)` closely.

`plot_correlation_heatmap` uses `(8, 6)` — acceptable as a square-ish plot.

### Anti-Patterns to Avoid
- **Reorganizing existing cells:** D-09 is explicit — add around, never move existing EDA/stats cells.
- **Repeating numbers without interpretation:** Every number in a markdown cell must have a "so what?" sentence.
- **Academic hedging language:** Avoid "may suggest", "appears to indicate". Say "the data shows" or "the DiD estimate is."
- **Jargon without definition:** DiD, parallel trends, HC1, Cohen's d — each needs a one-sentence plain-English gloss on first use.
- **Captions that describe rather than conclude:** Bad: "This figure shows ridership over time." Good: "Ridership on the Gold Line roughly doubled after the extension opened in March 2016, while control lines declined modestly."

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| Displaying formatted numbers in markdown | Python f-string templates | Write static markdown with pre-computed values from verified numbers table above |
| Figure captions | Any code-based captioning | Plain markdown cell immediately below each figure code cell |
| README project tree | ASCII art generator | Write it by hand from known directory layout |
| Test badge in README | CI/CD badge service | Simple text line: "Tests: `make test` (pytest — all passing)" |

---

## Content Specifications Per Section

### Executive Summary (D-05, D-07)
Must function standalone. Skeleton:
1. Sentence 1: Research question in plain English.
2. Sentence 2: Data and method (one sentence).
3. Sentence 3: Key DiD finding with number and significance.
4. Sentence 4: Pre/post magnitude for context.
5. Sentence 5: Robustness note (consistent across checks).
6. Sentence 6: Limitation caveat (line-level data only; parallel trends marginal).

Key numbers to include: "+38,120 avg daily boardings", "p < 0.001", "Gold Line ridership doubled (+102%) after the extension".

### Methodology Section (D-08)
Structure:
1. Data markdown cell: Describe the Streets For All dataset — 944 rail-only rows, 6 lines, Jan 2012–Dec 2019 primary window. Note the 2018 data gap and line-level (not station-level) granularity.
2. DiD design markdown cell: Explain treatment (Gold Line), control (A/B/C/E lines), pre (Jan 2012–Feb 2016), post (Apr 2016–Dec 2019). Include the formula: `Y = β0 + β1(Treatment) + β2(Post) + β3(Treatment × Post) + ε`. Define β3 in plain English.
3. Assumptions cell: List parallel trends assumption. Note the marginal test result (p = 0.038) and what it means (marginal evidence of a pre-period trend difference; results should be interpreted with caution).

### Limitations Section (D-09 of specifics section)
Must reference prior decisions from STATE.md:
- **Line-level only (D-02):** Cannot attribute ridership gains to specific new stations (Arcadia, Monrovia, etc.); confounds network effect with new-station effect.
- **Business proximity dropped (D-01):** Cannot quantify economic impact on station neighborhoods.
- **2018 data gap (D-05):** Three months missing system-wide; slight undercounting of post-period observations.
- **Regional Connector discontinuity (D-03):** Gold Line was absorbed into A Line in June 2023; extended-window analysis accounts for this but adds interpretive complexity.
- **Parallel trends marginal (p = 0.038):** The pre-period trend test is marginally significant — the treatment and control groups were not perfectly parallel before the extension. This is the key internal validity caveat.
- **Generalizability:** Findings apply to one specific extension in one metro area; other transit expansions may differ.

### Conclusion (D-10)
2-3 sentences answering "did the extension cause ridership changes?":
- Sentence 1: Yes/no answer with the DiD number.
- Sentence 2: Robustness note.
- Sentence 3: Caveats on generalizability or the parallel trends assumption.

### README (D-16, D-17, D-18)
Target: under 100 lines. Required sections:
1. Project title + one-paragraph summary
2. Key finding (one sentence with DiD coefficient)
3. Setup instructions: `git clone`, `make all`
4. Project structure tree (from CLAUDE.md layout)
5. Tech stack table (pandas, scipy, statsmodels, seaborn, pytest, nbconvert)
6. Contact placeholder: `[Your Name] — [GitHub URL]`

Do NOT include: full results tables, code examples, methodology details — those live in the notebook.

---

## Common Pitfalls

### Pitfall 1: Numbers Without Context
**What goes wrong:** Writing "the DiD coefficient is 38,120" without explaining that this means roughly doubling the pre-extension ridership baseline of 27,363.
**How to avoid:** Always pair an absolute number with a relative or contextual frame. "38,120 additional average daily boardings — roughly matching the entire pre-extension ridership level."

### Pitfall 2: Hedging the Parallel Trends Issue Away
**What goes wrong:** Mentioning "parallel trends" was tested but burying the marginal p-value (0.038) as a minor footnote, overstating confidence in causal identification.
**How to avoid:** In the limitations section, name the specific p-value and explain what it means in plain English: "The pre-period trend test shows marginal evidence (p = 0.038) that Gold Line and control lines were not perfectly parallel before the extension — slightly weakening the causal claim."

### Pitfall 3: Breaking Notebook Execution
**What goes wrong:** Editing existing code cells while adding markdown, accidentally deleting or corrupting a code cell, causing `make notebook` to fail.
**How to avoid:** Only add new markdown cells via JSON-level notebook editing. Never modify existing code cell sources. Verify with `make notebook` after each task.

### Pitfall 4: Figure Caption Describes, Doesn't Conclude
**What goes wrong:** "Figure 2 shows the treatment and control groups over time."
**How to avoid:** Every caption answers "what does this tell us?": "The treatment group (Gold Line) accelerated above the control average after March 2016, consistent with the DiD estimate of +38,120 boardings."

### Pitfall 5: README Over 100 Lines
**What goes wrong:** Adding full methodology description, all test results, and output examples — README becomes a second notebook.
**How to avoid:** D-17 is explicit: point readers to the notebook. If a detail belongs in the analysis, it does not belong in the README.

### Pitfall 6: Tick Label Size Not Applied
**What goes wrong:** Adding `xtick.labelsize` / `ytick.labelsize` to `set_default_theme()` but `plot_ridership_trends` calls `set_default_theme()` then immediately sets `figsize` at `plt.subplots()` — the figsize in `plt.subplots()` overrides the rcParams default.
**How to avoid:** The figsize must be updated in the `plt.subplots(figsize=...)` call directly, not just in rcParams. `set_default_theme()` handles tick sizes (rcParams); individual plot functions handle figsize at subplots creation time.

---

## Environment Availability

Step 2.6: SKIPPED — this phase is purely notebook cell additions, `src/viz.py` edits, and `README.md` creation. All required tools (Python, jupyter, nbconvert, pytest) are confirmed present from prior phases.

---

## Validation Architecture

`workflow.nyquist_validation` is not set in `.planning/config.json` — treat as enabled.

This phase adds no new functions to `src/stats.py` or `src/viz.py` that require new unit tests. The existing `tests/test_data.py` suite remains the gate. The primary validation for Phase 4 is notebook execution (`make notebook`) rather than new pytest tests.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.3.4 |
| Config file | none (pytest discovers `tests/` by convention) |
| Quick run command | `python -m pytest tests/ -v` |
| Full suite command | `python -m pytest tests/ -v` |
| Notebook validation | `jupyter nbconvert --to notebook --execute notebooks/analysis.ipynb --output analysis_executed.ipynb` |

### Phase Requirements to Test Map
| Behavior | Test Type | Command | Notes |
|----------|-----------|---------|-------|
| Notebook executes top-to-bottom without errors | Smoke | `make notebook` | Required by CLAUDE.md |
| Figure formatting functions produce correct figsize | Manual inspection | Open executed notebook | Verify (12,6) dimensions |
| Markdown cell count >= code cell count | Manual inspection | Count cells in executed notebook | REQUIREMENTS.md non-negotiable |
| README under 100 lines | Automated | `wc -l README.md` | D-18 |

### Wave 0 Gaps
None — no new test files needed. Existing `tests/test_data.py` covers data validation. The phase gate is `make notebook` green.

---

## Project Constraints (from CLAUDE.md)

All directives below apply to any code touched in this phase:

| Directive | Applies In Phase 4 |
|-----------|-------------------|
| Black formatter, line length 88 | Yes — `src/viz.py` edits must pass Black |
| isort (Black-compatible profile) | Yes — `src/viz.py` imports |
| Type hints on all public functions | Yes — any new helper functions in viz.py |
| One logical operation per notebook cell | Yes — each new markdown cell covers one topic |
| Markdown cell before every code cell | Yes — already the pattern; new figure caption cells satisfy this |
| `sns.set_theme(style="whitegrid", palette="muted")` | Yes — do not change; D-11 locks this |
| Descriptive `snake_case` variable names | Yes — for any new variables |
| Allowed libraries only | Yes — no new libraries; all in requirements.txt |
| `make test` must pass | Yes — figure formatting changes must not break tests |
| `make notebook` must pass | Yes — this is the primary phase gate |

---

## Sources

### Primary (HIGH confidence)
- Direct notebook inspection (`notebooks/analysis.ipynb`, 48 cells) — cell structure, existing markdown, insertion points
- Direct code inspection (`src/viz.py`, `src/stats.py`) — current figsize values, theme settings, function signatures
- Direct data execution (`data/clean/ridership_clean.csv` + `src/stats.py:did_regression`) — verified DiD numbers
- `CLAUDE.md` — coding standards, allowed libraries, formatting requirements
- `.planning/phases/04-narrative-polish/04-CONTEXT.md` — all locked decisions D-01 through D-18
- `.planning/REQUIREMENTS.md` — non-negotiables: full stat reporting, markdown/code ratio, no p-hacking
- `.planning/STATE.md` — D-01 through D-05 decisions that must be cited in limitations

### Secondary (MEDIUM confidence)
- None required — this phase has no external library research needs

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Analysis numbers: HIGH — verified by running code against clean data on 2026-03-26
- Insertion points: HIGH — verified by reading all 48 notebook cells
- Figure formatting gaps: HIGH — verified by reading `src/viz.py` line by line
- Content specifications: HIGH — locked by CONTEXT.md decisions
- README structure: HIGH — D-16 through D-18 are explicit

**Research date:** 2026-03-26
**Valid until:** Stable indefinitely — internal project, no external dependencies change
