# 011 — Re-translate what 010's second session repaired

**009 again, for the next batch. `source/` changed in 40 files; the Persian of
most of them is now stale.**

## Context

Spec 010's second session (poems 011–020, plus a marker re-read of 001–010)
fixed six defect classes in `generate_final_markdown.py`. See 010's
*Session 2* notes for what and why. Three of those fixes are book-wide, so
the 40 changed files run from `001` to `introduction-3`, not just the decade
that was read.

**`just check` is red on three of them.** `apparatus --check` reports that
`010`, `011` and `020` now have a verse quote with more hard breaks than the
Persian. `check_parity` still passes 147/147: every other change is inside
an existing block, and that is exactly why none of this was caught.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 2 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files, in three groups

### A. Re-translate: words or verse restored (14)

| file | what changed in the source |
|---|---|
| `001.md` | **`know`**, **`cloud`** restored; markers [1], [2] |
| `004.md` | marker [5] |
| `007.md` | the `[26]`/`[27]` labels; marker **[6], was [9]**; `Yüeh Küang` ×5 |
| `009.md` | markers [7], [8] |
| `010.md` | four-line verse quote re-broken; marker [10] — **check fails** |
| `011.md` | Lotus Sūtra couplet re-broken; [11], [12]; **[13], was [18]** — **check fails** |
| `014.md` | **`When Nan-ch’üan saw them`**; `remorseful`; `Fo-yen`; [17], [18] |
| `015.md` | **`see notes to poem no. 71.`** (the Persian dropped the sentence); `Sōtō`, `a burning`; [20]; **[21], was 24** |
| `018.md` | **`fūryū`** in the poem's last line, was `tryu`; `Chao-chou`; [25] |
| `019.md` | `I’ll`; `. . . :`; [26], [27], [29]–[32] |
| `020.md` | love-song couplet re-broken; **`Yüan-wu said,`**; `Yüan-wu`, `Wu-tsu`, `Hui Yüan`; [33]; **[34], was [33]** — **check fails** |
| `024.md` | **`the reader`** restored |
| `038.md` | **`scrambled`**, **`the coffin,`** restored; [54] |
| `058.md` | **`as the first`** restored |

### B. Markers only (11) — needs a decision

The digits were already in `source/`, welded to a closing quote (`it."35`), and
are now bracketed. The Persian dropped most of them and left a few bare.

`025` [48] · `028` [35] · `037` [53] · `044` [61], [6], `Lan-ts’an` · `046` [64] ·
`061` [2] · `071` [82] · `080` [88] · `082` [89] ·
`introduction-1` [33], [45], plus `Tung-shan`, `Chao-yang`, `Sūtra` ·
`introduction-3` [68], [69], [89], [81], plus `Wu-tsu`, `Ta-mei`, `Lan-tsan`,
`Hui-chih`, `Kao-tang`, `Wu-shan`

**Nothing sanctions inserting a marker by hand**, so as the rules stand, all
eleven are re-translations. For nine short poem files that is cheap. For
`introduction-1.md` it is not: 67 K characters at a chunk size of 900 is about
73 chunks, and the two words of text in it that changed are name hyphens. The
open question is whether to add a third sanctioned hand-edit to `CLAUDE.md`
(put `[N]` back where the source has it, nothing else) or to re-run the file.
**Decide before starting group B.**

### C. No re-translation (15)

A name's Latin spelling changed and nothing else: `031` `036` `045` `057` `062`
`084` `094` `097` `101` `120` `121` `124` `133`. The Persian spells these
names in Persian script from `STYLE.md` §2, so a changed hyphen or macron in
the English does not reach it. Check each against §2. Conforming one is the
second sanctioned hand-edit.

`bibliography.md` (`Diamond Sūtra`) and `glossary-index.md` (`Yüeh Küang`) keep
their entries verbatim (spec 006), so each needs one word conformed by hand:
§2 again.

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in groups A or B carries one or a
   `parity: offset` (checked when this spec was written).
3. **Group B once the question above is settled.**
4. **Group C by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated; `just check` green.
- [ ] Group B decided, recorded here, and done.
- [ ] Group C checked against `STYLE.md` §2; the two back-matter words
      conformed.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any file in groups A and B. (It still shows `062` and `068`, where
      the Persian has a marker the source lacks. Those are source defects for
      a later decade of 010.)
- [ ] Typeset PDF read for the touched files.

## Out of scope

Anything 010 has not read yet. The marker comparison lists files outside this
spec, and they wait for their decade.
