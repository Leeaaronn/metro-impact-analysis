# Phase 4: Narrative & Polish - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Transform the existing technical analysis notebook into a polished, readable deliverable by adding narrative markdown sections (executive summary, methodology, findings, limitations, conclusion), formatting all figures for consistency, and creating a portfolio-ready README.md. No new analysis or code — this is writing and presentation.

</domain>

<decisions>
## Implementation Decisions

### Audience & Tone
- **D-01:** Target reader is a hiring manager scanning portfolios — 10 minutes max reading time
- **D-02:** Tone is professional but not academic — write like a consulting analyst presenting to a client, not a PhD defending a thesis
- **D-03:** No jargon without a one-sentence plain English explanation immediately after
- **D-04:** Every section must answer "so what?" — interpret numbers, don't just report them
- **D-05:** Executive summary must be readable by someone who skips everything else

### Notebook Structure & Flow
- **D-06:** Section order: Executive Summary (no code) → Data & Methodology → Exploratory Analysis → Statistical Tests → Robustness Checks → Limitations → Conclusion
- **D-07:** Executive summary at the very top — 5-6 sentences covering the answer to the central question, key numbers, and a one-line methodology description
- **D-08:** Methodology section explains DiD in 2-3 sentences with the formula, then defines treatment/control/pre/post windows
- **D-09:** Do NOT reorganize existing EDA and stats sections — add narrative markdown cells around them
- **D-10:** Conclusion should be 2-3 sentences that directly answer "did the extension cause ridership changes?"

### Figure Formatting
- **D-11:** Keep current whitegrid + muted palette (already set in viz.py `set_default_theme()`)
- **D-12:** Figure sizes: `figsize=(12, 6)` for full-width, `(10, 5)` for half-width
- **D-13:** Font sizes: title 14, axis labels 12, tick labels 10
- **D-14:** Every figure gets a caption as a markdown cell immediately below it explaining the takeaway in one sentence
- **D-15:** No figure should require reading the code to understand what it shows

### README Scope & Format
- **D-16:** Include: one-paragraph project summary, key finding (one sentence with DiD result), screenshot or badge showing tests passing, setup instructions (`make all`), project structure tree, tech stack list, contact info placeholder
- **D-17:** Don't duplicate the full analysis — point readers to the notebook
- **D-18:** Keep README under 100 lines — portfolio README, not documentation

### Claude's Discretion
- Exact wording of narrative sections (following tone/audience decisions above)
- Which existing markdown cells need rewriting vs which are already good enough
- Whether to add section divider cells between major notebook sections
- Specific figure caption wording

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

No external specs — requirements fully captured in decisions above. Key internal references:

### Notebook & Code
- `notebooks/analysis.ipynb` — The deliverable notebook; all narrative additions go here
- `src/viz.py` — Contains `set_default_theme()` and all plot functions; figure formatting changes go here
- `src/stats.py` — Statistical functions producing results that narrative sections must interpret

### Project Context
- `.planning/REQUIREMENTS.md` — Non-negotiables for statistical reporting and notebook structure
- `.planning/STATE.md` — Decisions D-01 through D-05 (data gaps, dropped analyses, line-level fallback)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/viz.py:set_default_theme()` — Already sets `sns.set_theme(style="whitegrid", palette="muted")`. Figure size and font size updates go here or in individual plot functions.
- `src/viz.py` plot functions — `plot_ridership_trends`, `plot_treatment_vs_control`, `plot_distributions`, `plot_boxplot_comparison`, `plot_correlation_heatmap` — each needs figsize and font size standardization
- `src/stats.py` — `TestResult.to_dict()`, `DiDResult.to_dict()` — structured results that narrative cells can reference

### Established Patterns
- Every code cell has a markdown cell above it explaining what and why (CLAUDE.md rule)
- Figures use seaborn with matplotlib customization underneath
- Stats functions return structured dataclass results with test name, statistic, p-value, CI, effect size

### Integration Points
- Executive summary inserted as first cell(s) in notebook
- Methodology section inserted after setup/data loading, before existing EDA
- Findings narrative woven around existing Phase 2 (EDA) and Phase 3 (stats) sections
- Limitations and conclusion appended after robustness checks
- README.md created at project root

</code_context>

<specifics>
## Specific Ideas

- Executive summary should function as a standalone — someone who reads only that section understands the project, method, and answer
- "Consulting analyst presenting to a client" is the voice model
- Prior decisions to reference in limitations: business proximity dropped (D-01), line-level only (D-02), Regional Connector discontinuity (D-03), 2018 data gap (D-05)
- README key finding sentence should include the actual DiD coefficient and its interpretation

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-narrative-polish*
*Context gathered: 2026-03-26*
