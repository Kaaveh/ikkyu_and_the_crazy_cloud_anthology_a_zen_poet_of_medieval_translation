# 004 — The Anthology: `011` – `135`

**125 files · 131,940 chars · 14 prose introductions · 3 set headers · 86 with notes**

## Context

The bulk of the book, and the part that decides whether it reads as one voice.
Every file here is a single chunk — none of the 125 exceeds the translator's 4,500-
character limit — so this is 125 runs of about eleven seconds each, plus the
`strip`/`restore` round trip.

Sequential only. One Chrome profile, and `_cleanup_chrome_profile()` kills whatever
holds it at startup, so a second run started in parallel destroys the first.

The poems are not uniform. Ikkyū writes praise-verses for dead masters, mountain-
hermitage poems, savage attacks on named contemporaries, and a long sequence about
Lady Mori that is explicitly erotic. `STYLE.md` §1 settled how the register moves
between these; this spec is where that decision meets 125 files of it.

## Goal

125 files at `status: reviewed`, `just check` green, the PDF read part by part.

## Dependencies

003. The pilot's refusal tally is what tells you whether to expect a clean run or a
repair after every file.

## Requirements

1. **`STYLE.md` is binding from here.** If the text contradicts it, that is a
   terminology question to settle deliberately, not a decision to change mid-batch.
   A change made here costs revising everything already done in this spec.

2. **Sequential runs.** No parallelism, for the profile reason above. Budget roughly
   a decade of files per sitting.

3. **`just check` after each decade, not after each file.** The pilot is what
   established the per-file rhythm; at this volume, a decade is the right unit. If
   parity fails for a decade, bisect within it.

4. **Three set-header files need care: `029`, `048`, `076`.** Each opens with a bold
   line above its `# Poem N:` heading (`**Living in the Mountains   two poems**`).
   Spec 002 decided what these become; whatever that decision was, confirm the
   translated file follows it, because `apparatus.py` does not re-emit that line —
   it is prose, and the model translates it freely.

5. **Fourteen prose introductions behave differently.** `013`, `017`, `033`, `035`,
   `039`, `042`, `063`, `066`, `103`, `109`, `111`, `125`, `129`, `134`. They are
   prose paragraphs, not verse, sitting inside a verse sequence, and `--raw` is still
   mandatory for them — the flag is per-run and these run alone. Their heading label
   (`Prose Introduction to No. N`) is re-emitted by `apparatus.py` with the numbers
   converted to Persian digits; the rest of the heading is prose.

6. **Repair, not re-run, when `restore` refuses once.** The three rules from
   `000-overview.md`, repeated because this is where they will be needed:
   - Edit the draft in `/tmp`, never `fa/`.
   - Only ever insert or delete a bare `⟦n⟧`. Never write the label markup by hand.
   - **If most of a file's sentinels are missing, re-translate instead.** That is the
     silent Classic-model failure, and hand-placing a dozen markers into a bad draft
     only makes it look finished.

   Say in the commit body which markers were placed by hand.

7. **Watch for the register drifting at volume.** 125 files translated in sequence
   over weeks will drift, and the drift is invisible from inside any one file.
   Every few decades, read a poem from the first decade next to one just finished. If
   they no longer sound like the same translator, that is worth fixing while there
   are still files left to make consistent.

8. **Read the PDF part by part.** Not file by file — the point is the cumulative
   texture — but not once at the end either, because by then a systematic fault is
   125 files deep.

## Checklist

- [x] `011`–`020` · 16,866 chars · prose intros `013`, `017`
- [x] `021`–`030` · 17,699 chars · set header `029`
- [x] `031`–`040` · 12,173 chars · prose intros `033`, `035`, `039`
- [x] `041`–`050` · 8,464 chars · prose intro `042`; set header `048`
- [x] `051`–`060` · 9,850 chars
- [x] `061`–`070` · 11,189 chars · prose intros `063`, `066`
- [x] `071`–`080` · 9,117 chars · set header `076`
- [x] `081`–`090` · 10,986 chars
- [x] `091`–`100` · 5,855 chars
- [ ] `101`–`110` · 7,579 chars · prose intros `103`, `109` · the Lady Mori sequence
      begins at `104`
- [ ] `111`–`120` · 7,631 chars · prose intro `111`
- [ ] `121`–`130` · 9,060 chars · prose intros `125`, `129`
- [ ] `131`–`135` · 5,471 chars · prose intro `134`; `135` is the last poem

## Acceptance criteria

- [ ] All 125 at `status: reviewed`.
- [ ] `just check` passes with 135 Anthology files compared (125 here plus the
      pilot's 10), none skipped.
- [ ] `apparatus --check` reports no hard-line-break mismatch anywhere — every
      stanza survived.
- [ ] The whole Anthology read in the typeset PDF.
- [ ] The three set-header files match the spec 002 decision.
- [ ] No `STYLE.md` change was made during this spec, or if one was, it is applied
      across all 125 and recorded with its reasoning.

## Out of scope

Front matter, Introduction, back matter, release.

## Implementation notes

_(filled in during implementation)_
