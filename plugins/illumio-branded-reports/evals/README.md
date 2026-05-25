# Evals

Real-world inputs that broke earlier versions of this skill. Each case is
seeded from a production incident — a customer-facing deliverable that
shipped (or almost shipped) with a defect.

These cases serve three purposes:

1. **Regression checks.** When changing SKILL.md, `scripts/visual_verify.py`,
   or any reference file, run the relevant evals to confirm the change
   doesn't reintroduce a known failure.
2. **Trigger documentation.** Each case explains the *kind* of input that
   trips the bug — useful for spotting the same pattern in new work.
3. **Onboarding.** Reading the eval set is the fastest way to internalize
   what this skill is defending against.

## Format

`evals.json` is the canonical source. Each case has:

- `id` — `EVAL-NN`
- `title` — one-line description
- `severity` — P0 / P1 / P2
- `targets_check` — which programmatic check or workflow rule this exercises
- `input_fixture` — HTML, prompt, or scenario that triggers the bug
- `expected_detection` — how `scripts/visual_verify.py` (or workflow rule)
  catches it
- `expected_fix` — the canonical fix from SKILL.md
- `pass_criteria` — what counts as the case being resolved
- `anti_pattern` (optional) — the wrong output, kept for tripwire matching

## Running

There is no automated runner yet — these cases are checked manually during
skill review. A future enhancement would script each case end-to-end:
1. Materialize the input fixture into an HTML file.
2. Run `scripts/visual_verify.py` against it.
3. Assert the expected check fires with the right magnitude.
4. Apply the expected fix.
5. Re-run and assert clean.

For now, treat `evals.json` as documentation: read it before modifying the
skill, and add a new case when a real-world incident surfaces a category
the existing cases don't cover.

## Adding a case

When a new failure mode appears in a real document:

1. Sanitize the customer/partner-specific content (replace names with
   `<CUSTOMER>`, IPs with `10.0.0.0/24`, hostnames with `<HOST>`, per
   `references/personal-info-policy.md` §3).
2. Add a case to `evals.json` with the next `EVAL-NN` id.
3. If the case requires a new programmatic check, extend
   `scripts/visual_verify.py` and document it in
   `references/visual-verification.md`.
4. Commit with prefix `eval:` per the workshop's git convention.

## Coverage

| Category | EVAL IDs | Programmatic | Human-review |
|---|---|---|---|
| SVG text overflow | EVAL-02, EVAL-03 | Yes (check 1) | Backstop |
| Z-index intersection | EVAL-01 | Yes (check 4) | Backstop |
| Diagram label collisions | EVAL-04 | Not yet — candidate | Yes |
| Workflow: no sampling | EVAL-05 | No (workflow rule) | Yes |
| Tone: no creative analogies | EVAL-06 | Tripwire substring + LLM judge | Yes |
| Brand: logo rendering | EVAL-07 | Partial (check 3 catches missing) | Yes |
| Cleanup: render artifact bloat | EVAL-08 | No (workflow rule) | Yes |

Gaps to address in future cases:
- DOM horizontal overflow (check 2) has no representative eval yet
- Image load failure (check 3) has no representative eval yet
- Bilingual EN/ES parallel rendering — no eval covers the case of producing
  both language variants from the same source
