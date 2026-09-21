# 003 — Pilot: the first ten poems

**`fa/001.md` – `fa/010.md` · 10 files · 21,031 chars · 7 with notes**

## Context

The pipeline has been run end to end exactly once, on `002.md`, and never again. That
one file proves the mechanism works; it does not prove the *decisions* work, because
there were none when it was made.

This spec is ten files. It exists so that when a 001 decision turns out to be wrong
against real verse — and one of them will — revising costs ten files rather than 135.

Batch composition is deliberate: `001.md` is the only two-chunk poem in the batch and
exercises chunk rejoining; `005.md` carries a bold set header; `006.md` is one of the
few poems with no `## Notes`; `008.md` is a prose introduction, which is prose sitting
in a verse sequence and behaves differently under `--raw`.

## Goal

Ten files at `status: reviewed`, `just check` green, the PDF read, and a written
record of how often `restore` refused and why — so 004 can size itself.

## Dependencies

001 (the style decisions are what this tests), 002 (translating unrepaired source
wastes the run).

## Requirements

1. **Run the pipeline exactly as `000-overview.md` documents it**, one file at a
   time, sequentially. `-w` and `--raw` both mandatory; never `>` into `fa/`.

2. **Judge the output text, not the picker.** After the first file, read the Persian
   and confirm it carries the Advanced model's signature — ezafe diacritics
   (`استادِ`, `چشمِ حقیقی`) and restructured sentences rather than clause-by-clause
   word order. `fa/002.md` is the reference. If a file comes back reading like
   Classic, re-run it; if two in a row do, stop and check the UA warning on stderr
   before burning eight more runs.

3. **`STYLE.md` is provisional here and only here.** When the text contradicts a
   decision, change the decision, then revise what you already translated to match,
   and record the change in `STYLE.md` with a line of reasoning. After this spec the
   guide is binding.

4. **Re-translate `002.md`.** It is currently `status: draft` from a pre-decision
   run. Whatever 001 settled about proper nouns and register, this file predates it.
   Either re-run it through the pipeline or ratify it explicitly — do not leave it as
   the one file nobody checked against the style guide.

5. **Count the refusals.** For each file, record whether `restore` accepted the draft
   first time and, if not, what the refusal said and what fixed it. Ten files is a
   large enough sample to tell "the model drops a sentinel now and then" from "this
   book's headings systematically defeat the round-trip", and the two need completely
   different responses in 004.

6. **`just check` after each file**, not after the batch. A parity mismatch is far
   cheaper to attribute when one file changed.

7. **Read these ten in the typeset PDF before closing the spec.** `just pdf`. Verse
   that reflowed into prose, a stanza whose lines wrapped, a Latin-script name
   reversed by bidi — all obvious typeset and all invisible in a Markdown diff.

## Files

| file | chars | notes | why it is in the pilot |
|---|---:|:---:|---|
| `001.md` | 7,495 | ✓ | Two chunks — the only poem file here that splits |
| `002.md` | 1,194 | ✓ | Already translated; re-run or ratify (requirement 4) |
| `003.md` | 1,119 | ✓ | Ordinary quatrain + run-on note block |
| `004.md` | 1,311 | ✓ | |
| `005.md` |   365 |   | Bold set header above the heading (defect 5 in spec 002) |
| `006.md` |   320 |   | No `## Notes` — the minimal case |
| `007.md` | 1,694 | ✓ | Long interrogative title; tests heading-label restore |
| `008.md` | 2,062 |   | **Prose introduction** — prose under `--raw` |
| `009.md` | 3,054 | ✓ | Longest single-chunk file in the batch |
| `010.md` | 2,417 | ✓ | |

- [ ] `001.md`
- [ ] `002.md`
- [ ] `003.md`
- [ ] `004.md`
- [ ] `005.md`
- [ ] `006.md`
- [ ] `007.md`
- [ ] `008.md`
- [ ] `009.md`
- [ ] `010.md`

## Acceptance criteria

- [ ] All ten at `status: reviewed`.
- [ ] `just check` passes with ten files compared, not skipped — confirm the count in
      the `check_parity` and `apparatus` output lines.
- [ ] Every poem's stanza survives: `apparatus --check` reports no hard-line-break
      mismatch.
- [ ] All ten read in the typeset PDF.
- [ ] Every `STYLE.md` change made during this spec is applied consistently across
      all ten, including retroactively.
- [ ] The refusal tally is written into **Implementation notes** below.

## Out of scope

`011.md` onwards. Front matter, Introduction, back matter.

## Implementation notes

_(filled in during implementation — the refusal tally goes here)_
