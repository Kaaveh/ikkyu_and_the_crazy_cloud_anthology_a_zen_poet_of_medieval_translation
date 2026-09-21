# 008 — Source repair follow-up

**What 002 didn't finish, so it's tracked instead of dropped.**

## Context

002 fixed every defect class it found a corpus-wide rule for: the wrong-poem
title, `notes.md`'s marginal letters, the CJK column bleed in poem files, the
set-header position, the subject's own name, and — added in a second session
once spec 001 unblocked them — fused endnote digits and the one confirmed
flattened verse quotation (poem 7's death poem). `just check` passes and every
mechanical fix has been diffed against the pre-fix tree by hand.

What's left is not a mechanical rule. It's a read.

## Goal

The 147-file PDF audit closed out, and a decision recorded on the two
low-priority back-matter files.

## Dependencies

002 (this is its unfinished checklist, not new scope).

## Requirements

1. **The checklist: 147 files read against the PDF.** 002's own checklist
   (reproduced below) was never worked — 002's two sessions were driven by
   defect-class scans over the whole tree, not a file-by-file read. Reading
   the poem files first is the highest-value use of this: it's how the
   session-2 attempt at a general verse-detection rule found out it was
   wrong (it turned quoted kōans into fake verse in `007`, `010`, `011`,
   `014`, `015`, `019`, `020`, `024`, `028`, `030`, `037`, `038`, `044`,
   `052`, `057`, `065`, `067`, `068`, `070`, `071`, `075`, `084`, and more —
   see 002's implementation notes) — a targeted fix needs a confirmed
   instance, and confirming needs the PDF, not a heuristic over the text.
   Any other note hiding a flattened verse quotation the same way poem 7's
   did is found this way, not by trying the general rule again.

2. **The Chinese column bled into `introduction-1/2/3`.** `build_introduction()`
   never runs lines through `clean_translation_line()` — the poem-file fix
   from 002 requirement 4 doesn't apply here because the Introduction's
   English wraps *around* the column rather than stopping at it. Needs its
   own extraction logic, not a reuse of the poem-file one.

3. **`bibliography.md` and `glossary-index.md` are still half garbled CJK.**
   Deliberately deprioritized in 002 on the grounds that a verbatim garbled
   entry is visible as garbage to a reader, while a translated one would
   launder it into confident-looking Persian. Spec 006 keeps these entries
   verbatim regardless, so fix what's cheap here; don't hold this spec on it,
   and don't let 006 either.

## Files

The checklist from 002, unchanged and still all unread against the PDF:

### Anthology

- [ ] `001`–`010`
- [ ] `011`–`020`
- [ ] `021`–`030`
- [ ] `031`–`040`
- [ ] `041`–`050`
- [ ] `051`–`060`
- [ ] `061`–`070`
- [ ] `071`–`080`
- [ ] `081`–`090`
- [ ] `091`–`100`
- [ ] `101`–`110`
- [ ] `111`–`120`
- [ ] `121`–`130`
- [ ] `131`–`135`

### Front matter and Introduction

- [ ] `plates.md`
- [ ] `foreword.md`
- [ ] `preface.md`
- [ ] `introduction-1.md` — **CJK column bleed, requirement 2. Its own session.**
- [ ] `introduction-2.md`
- [ ] `introduction-3.md` — **CJK column bleed, requirement 2.**
- [ ] `introduction-4.md`

### Back matter

- [ ] `abbreviations.md`
- [ ] `notes.md` — already repaired in 002; re-read here since it's the
      audit's job to confirm, not assume
- [ ] `bibliography.md` — CJK garbling, requirement 3, low priority
- [ ] `index-of-poems.md`
- [ ] `glossary-index.md` — CJK garbling, requirement 3, low priority

### Finally

- [ ] `source/README.md` re-read once the above is done.

## Acceptance criteria

- [ ] Every file above read against the PDF, defects found either fixed in
      the generator or recorded here as a deliberate exception.
- [ ] The gibberish scan from 002 requirement 4 returns nothing outside
      `bibliography.md` / `glossary-index.md`, or those two are explicitly
      signed off as out of reach at 006's priority.
- [ ] Any new flattened-verse-quotation instance found is fixed the same way
      poem 7's was — a targeted match on confirmed text, not a general
      indentation heuristic (002 already tried the general version and
      reverted it).
- [ ] `just split` re-run after every generator fix; `just check` passes.

## Out of scope

Translating anything. Same rule as 002: `fa/` is untouched here except that a
source change to an already-translated file (currently only `002.md`) means
that file needs re-translation — tracked in whichever spec owns that file's
translation, not here.

## Implementation notes

_(filled in during implementation)_
