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

- [x] `001.md`
- [x] `002.md`
- [x] `003.md`
- [x] `004.md`
- [x] `005.md`
- [x] `006.md`
- [x] `007.md`
- [x] `008.md`
- [x] `009.md`
- [x] `010.md`

## Acceptance criteria

- [x] All ten at `status: reviewed`.
- [x] `just check` passes with ten files compared, not skipped — confirm the count in
      the `check_parity` and `apparatus` output lines.
- [x] Every poem's stanza survives: `apparatus --check` reports no hard-line-break
      mismatch.
- [x] All ten read in the typeset PDF.
- [x] Every `STYLE.md` change made during this spec is applied consistently across
      all ten, including retroactively.
- [x] The refusal tally is written into **Implementation notes** below.

## Out of scope

`011.md` onwards. Front matter, Introduction, back matter.

## Implementation notes

### The refusal tally (requirement 5)

**Nine of ten accepted on the first `restore`. One refused. Zero sentinels were
placed by hand.**

| file | `restore` | note |
|---|---|---|
| `001.md` | accepted | 3 chunks, not 2; both seams rejoined cleanly |
| `002.md` | accepted | re-run, see below |
| `003.md` | accepted | |
| `004.md` | accepted | |
| `005.md` | accepted | bold set header survived as a block of its own |
| `006.md` | accepted | |
| `007.md` | accepted | |
| `008.md` | accepted | prose under `--raw`, one paragraph in and out |
| `009.md` | **refused** | see below |
| `010.md` | accepted | |

The one refusal:

```
error: 009.md: the model dropped 3 hard line break(s) and moved +3 line(s), so
they cannot be put back by position. End the matching draft line(s) with two
spaces:
```

**It was not a round-trip failure and the documented fix would have been the
wrong one.** Ending those lines with two spaces would have made `restore` accept
a draft that was bad for an unrelated reason — the file had come back from the
Classic model, which sets each verse line as its own paragraph, so the quatrain
arrived as four blocks rather than one. The refusal was the checker catching the
Classic fallback, not a lost sentinel. Re-translating fixed it; `restore` then
accepted without an edit.

**This is the number 004 should size itself on: 0 dropped sentinels in 10 files,
across 22 structural headings.** `align_hard_breaks_by_block` did all the
recovery on its own. This book's headings do not defeat the round-trip, and no
`⟦n⟧` had to be placed by hand in the whole pilot. Budget the hand-editing for
§2 instead — see below.

### The `-w` failure is real, is not the UA, and has a fix

Requirement 2 sent us to check the stderr UA warning after two Classic runs.
**There was no warning, and the UA was not the cause.** `009.md` came back
Classic three times running, byte-identical each time, with `_select_advanced`
reporting success and `_assert_not_headless_ua` silent. Ruled out along the way:

- **Not the UA.** No warning on any run.
- **Not a settle race.** Patching `gtranslate.py`'s `_settle` to hold for 15 s
  instead of 2 changed nothing — it is not a Classic result being snapshotted
  before Gemini's replaces it.
- **Not quota or time of day.** `010.md`, re-translated immediately after the
  third failed `009` run, came back Advanced and byte-identical to its first run.
- **Not the file's subject matter.** The quatrain alone, in a file of its own,
  came back Advanced.

It is per-input and deterministic: the same text at the same chunk size gives
the same model every time. **The fix is `--chunk`.** Measured on `009.md`:

| `--chunk` | chunks | result |
|---:|---:|---|
| 4500 (default) | 1 | Classic throughout — 0 ezafe |
| 1500 | 3 | chunk 2 Advanced, 1 and 3 Classic |
| 900 | 4 | chunk 1 Classic |
| 600 | 6 | chunk 1 Classic |
| 400 | 10 | Advanced throughout — 36 ezafe, one garbled parenthesis |
| **300** | **13** | **Advanced throughout — 46 ezafe, clean** |

`fa/009.md` is the `--chunk 300` run. Nothing else in the batch needed the flag.

**For 004: judge every file, not just the first.** Counting ezafe diacritics
(`grep -c ِ`) separates the two models in one command and did so unambiguously
here — 0 for Classic against 11–36 for Advanced on comparable files. Prose files
score lower per character than verse (`008.md`: 3 in 3.5k) so read the text
before concluding, but a flat 0 means Classic every time. When it is Classic,
**halve `--chunk` and re-run** rather than re-running unchanged — three identical
re-runs at the default proved that re-running alone does nothing.

### `002.md`: re-run, then conformed (requirement 4)

Re-run rather than ratified. The new draft is better in one way that matters —
it kept the `[4]` endnote marker that the pre-decision draft had dropped — and
worse in the way §2 predicts: it gave `شو-تانگ` for Hsü-t’ang and `ایکیو` for
Ikkyū, losing exactly the forms `STYLE.md` §2.8 cites `fa/002.md` as the
authority for. Conforming it by hand under §2 restored them.

That is the pilot's argument for the §2 hand-edit in miniature: the file that
`STYLE.md` quotes as the model of correct proper nouns does not survive its own
re-translation without it.

### What `STYLE.md` got wrong (requirement 3)

Three changes, all recorded in `STYLE.md` with their reasoning. Two reverse a
decision outright; the third covers something no section had anticipated.

1. **§4.2 — endnote markers are `[4]`, not `[۴]`.** The model persianises every
   numeral in running prose and leaves every bracketed one alone: 5 of 5 across
   the ten files, no exception either way. `[۴]` could only be produced by hand,
   in ~70 files, on every re-run. **Spec 006 is affected**: `notes.md` entry
   numbers now stay Latin to match.
2. **§5 — numerals in prose are Persian.** The same measurement, read the other
   way. `(1185-1269)` → `(۱۱۸۵-۱۲۶۹)`, `pp. 16-17` → `صفحات ۱۶-۱۷`, `roll 43` →
   `طومار ۴۳`, every time. The old rule wanted page references kept Latin so a
   reader could find them in Arntzen's edition; it asked for something no part of
   the toolchain delivers, and `صفحات ۱۶-۱۷` costs a Persian reader nothing.
3. **§2.9 (new) — the model's parenthetical romanisations are kept.** It
   volunteers `(Ikkyū)`, `(kōan)`, `(Crazy Cloud Anthology)` after a name or term;
   29 in ten files, so ~350 across the book. They are not in `source/`. They are
   kept, because they serve §2.1's own argument — the reader has to be able to
   find the name again in Arntzen's index — and because stripping 350 of them is
   a hand-edit `CLAUDE.md` does not sanction.

Also updated: §1.4 records that **none of the first ten is an obscene-poem
candidate** (poem 6 is the near miss, and it settles that §1.4 marks a poem's
language, never its subject); §2.7 records that none of its four (suggested)
Sanskrit terms occurs in poems 6–35; §2.8 promotes five suggestions that did meet
verse and adds the eleven names the pilot settled.

### The §2 hand-edit is the real cost of this book

**89 proper-noun corrections in ten files** — about nine per file, so of the order
of 1,200 across the Anthology. The model transliterates by ear and is
inconsistent within a single file: `009.md` alone spelled Tetto three ways
(`تِتّو`, `تِتو`, `تِتّد`) and Ikkyū two. §2.2's aspiration mark is dropped
almost every time, and §2.1 is violated in the direction nobody would notice —
`Yüeh Kuang` came back as `یوئه گوانگ`, which is the Pinyin reading of the name.

004 should budget for this explicitly. It is not polish; it is the one thing in
the pipeline that no checker will ever catch.

### The PDF (requirement 7)

All ten read at `_book/…pdf`, pages 20–32. Nothing that a Markdown diff hides
went wrong:

- **No verse reflowed.** All nine quatrains set as four lines.
- **No stanza line wrapped** at this measure, long first lines included. §3.2's
  hanging indent is still wanted for spec 007, but it is not urgent for the
  Anthology's quatrains.
- **No bidi reversal.** Every §2.9 gloss, every `[N]`, and `«far out»` in
  `001.md` set left-to-right inside the Persian. LuaLaTeX is doing what
  `tex/preamble.tex` says it was chosen for; §2.9 is now a second reason not to
  switch engines.
- **Structural labels intact**, including `درآمدِ منثور بر ۳۳` on `008.md` and
  `شعر ۲۷:` in front of a title that wraps to three lines.
- **`005.md`'s bold set header** sets as bold above the stanza, in its own block.
- Poem 7's death poem still sets as prose. Known, and recorded in §3.3 — the
  defect is in `source/`, not `fa/`.

### Defects found in `source/`, for spec 008

None is fixable in `fa/`, and all three reach the page:

- **`source/007.md`: `(26` and `(27`** — print-edition note markers that the
  extraction turned into stray open-parens. They survive into `fa/007.md` and
  print as `(26)` `(27)` mid-sentence.
- **`source/009.md`: `’’8`** and **`source/010.md`: `s210`** — endnote digits
  still fused to the word before them, which spec 002's un-fusing rule missed.
  An unbracketed digit is prose to the model, so `’’8` reaches the page as
  `»۸`: persianised, unmarked, and pointing at nothing. This is exactly the
  failure the bracket in §4.2 exists to prevent.
- **`source/009.md`: `HsG-t’ang`** — OCR damage for `Hsü-t’ang`. The model
  recovered it unprompted at `--chunk 300` (`(Hsü-t’ang)`), but only by luck,
  and an earlier run rendered it as a bishop named `هاس-گونگ`.

One translation blemish that is not a source defect: `fa/001.md` renders
`poem no. 493 (p. 51)` with a stray ellipsis — `شعر شماره ... ۴۹۳`. Left as
translated; the machine draft is the edition.
