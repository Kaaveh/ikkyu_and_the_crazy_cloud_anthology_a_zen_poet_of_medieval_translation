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

1. ~~**The checklist: 147 files read against the PDF.**~~ **Moved to
   [010](./010-source-audit.md)**, which owns the read now. It was started
   here — `001`–`010` are done, and what they turned up (the justified-spacing
   deletions across the whole Anthology, the `Daid` → `Daitō` rule that erased
   Daiō, and `split_poem7_death_verse` having been dead code) is recorded
   there, along with the 22 files it repaired. At 147 files this is weeks of
   work and a spec of its own, not a fold-in item on this one.

   The original text of the requirement follows, since 010 inherits it.

   002's own checklist
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

2. ~~**The Chinese column bled into `introduction-1/2/3`.**~~ **Done**, in spec
   005, where it blocked three of that spec's seven files.

   **The diagnosis above was wrong in its second half.** The English does not
   wrap around the column: the page is an ordinary two-column setting, English
   left and the original right. What produced the interleaving is that
   `build_introduction()` joined the lines into paragraphs without cutting the
   column off first, so the right-hand text landed *between* two English words
   — `they would ignore fF, DARRZ karma and the world…`.

   It did need its own logic, but a much smaller piece than "its own
   extraction". `clean_translation_line()` is genuinely wrong here — it reads
   any run of three spaces past column 45 as the gutter, and the Introduction
   is set justified, so it also eats stretched word spacing: 52 lines,
   including `his craziness` and `balancing act`. The fix is `drop_column()`,
   which measures the gutter with the existing `find_gutter()` instead of
   guessing at it. The measurement doubles as the test for whether to cut:
   a one-column page has no such blank run, so it raises and the page is
   returned untouched.

   **Result: 363 CJK characters and OCR garbage runs removed, 0 left, and no
   English word lost.** `just split` afterwards changed only
   `introduction-1/2/3` — none of the 144 translated files moved.

3. **`bibliography.md` and `glossary-index.md` are still half garbled CJK.**
   Deliberately deprioritized in 002 on the grounds that a verbatim garbled
   entry is visible as garbage to a reader, while a translated one would
   launder it into confident-looking Persian. Spec 006 keeps these entries
   verbatim regardless, so fix what's cheap here; don't hold this spec on it,
   and don't let 006 either.

## Files and acceptance criteria

**Moved to [010](./010-source-audit.md), which owns them now.** The copy that
used to sit here stayed unticked while 010 moved on, which made 008 look like
open work of its own. It has none:

- requirement 1 (the 147-file read) is 010's checklist;
- requirement 2 (the Introduction's CJK bleed) was done inside 005;
- requirement 3 (`bibliography.md` / `glossary-index.md`) is 010
  requirement 5.

**008 closes when 010 does.** It did, with 023.

## Out of scope

Translating anything. Same rule as 002: `fa/` is untouched here except that a
source change to an already-translated file (currently only `002.md`) means
that file needs re-translation — tracked in whichever spec owns that file's
translation, not here.

## Implementation notes

**Closed with 010, on 2026-09-24.** Nothing was done under this number after
the handover, so there is nothing to record beyond where each requirement
went:

- **Requirement 1, the 147-file read**, is 010's, and done, with one
  exception. 010 closed by handing `introduction-1/2/3` to
  [024](./024-introduction-read.md) unread. The Introduction's read is still
  owed, and 024 owns it.
- **Requirement 2, the Introduction's CJK bleed**, was done inside 005.
- **Requirement 3, `bibliography.md` and `glossary-index.md`**, was signed off
  by 010's twelfth session as out of reach at 006's priority. Both stay
  verbatim.
