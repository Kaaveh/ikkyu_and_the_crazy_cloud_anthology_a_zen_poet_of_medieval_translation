# 015 — Re-translate what 010's fifth session repaired

**013 again, for the next batch. `source/` changed in 9 files; three need
re-translating, and two need a §2 conform for a row §2 had wrong.**

## Context

Spec 010's fifth session (poems 117–134, files `043`–`050`) fixed local
damage in `generate_final_markdown.py`. See 010's *Session 5* notes for what
and why. Seven changed files are in the decade. `001` and `introduction-3`
are not: they carry *Lan-ts'an*, whose §2 row the session corrected.

**`just check` is red on one of them.** `apparatus --check` reports `046`
short of a hard break: Lan-ts'an's couplet is now set as verse. Block parity
is unchanged — the couplet was two paragraphs and is now one, and the lemma
after it has become a paragraph of its own. Every other change is inside an
existing block and fails nothing.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 5 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

**016 touches `049` too.** Whichever runs second re-translates it again. It is
one short file; neither spec waits for the other.

## The files

### A. Re-translate (3)

| file | what changed in the source |
|---|---|
| `044.md` | `Daiki Kōjū Zenji`, was `Koja` — **the Persian has «دایکی کوجا زِنجی» (Daiki Koja Zenji)**; `Message.”` |
| `046.md` | markers **[62], [63], were [6], [68]** — the Persian carries both; Lan-ts'an's couplet set as verse — **check fails**; `Lan-ts’an` in the poem and the note; `Master Kasō: Kasō Sōdon`; `Yōsō`; `Ch’u’s`; three quotes |
| `049.md` | marker **[65]**, bare in the OCR, which the Persian dropped; `Kasō’s`, `“I know`, `Tettō` |

### B. §2 conform (2)

**`STYLE.md` §2 had *Lan-ts'an* wrong**, as `Lan-tsan` → «لان-تسان»: the OCR's
form, not the book's. The row now reads `Lan-ts’an` → «لان-تس’ان» (§2.2). A
sanctioned hand-edit (`CLAUDE.md`), every occurrence:

- `001.md` — «لان-تسان» ×2. The source now says `Lan-t’san` twice, as p. 66
  prints it; the Persian takes §2's form, not the page's slip.
- `introduction-3.md` — «لان-تسان» ×6. The source gained two apostrophes,
  `Lan-ts’an`, which is the only change and needs no re-translation.

`046` has the name six times; its re-translation is conformed with it.

### C. No re-translation (4)

- `045.md` — `is`, was `1s`, in the poem. The Persian read through it: «چه
  نوع ذنی است؟».
- `047.md` — `P’u-hua`, was `P’yu-hua`. The Persian has «پ’و-هوا» already.
- `048.md` — `severed?”`, was `severed?’`. The Persian renders `«»` either
  way: «…نشده است؟» [64]».
- `050.md` — `scriptures;`, was `scriptures ;`. Nothing to carry.

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in group A carries one or a
   `parity: offset` (checked when this spec was written).
3. **§2 against the old files and the table.** *Kōjū* is new: §2.4 gives
   «کوجو». *Lan-ts'an* is «لان-تس’ان», not the «لان-تسان» the old `046`
   has — group B.
4. **Group B by hand.**
5. **Group C by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated; `apparatus --check` green on `046`.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `046` carries [61]–[63], `049` [65].
- [ ] *Daiki Kōjū Zenji* is «دایکی کوجو زنجی» in `044`, whatever gloss the
      model adds beside it (§2.9).
- [ ] *Lan-ts'an* is «لان-تس’ان» everywhere in `fa/`: no «لان-تسان» left.
- [ ] Group C checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `049`'s closing paragraph, run into its last
note: that is 016's, and 015's draft will carry it joined, as `source/` does.
