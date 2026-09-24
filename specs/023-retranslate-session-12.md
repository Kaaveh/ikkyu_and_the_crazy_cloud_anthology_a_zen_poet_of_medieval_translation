# 023 — Re-translate what 010's twelfth session repaired

**022 again, for the front matter, `introduction-4` and the back matter.
`source/` changed in 9 files: 5 need re-translating, 3 need an entry list
re-copied, and 1 belongs to 024.**

## Context

Spec 010's twelfth session read everything outside the Anthology and the
Introduction. See 010's *Session 12* notes for what and why. It fixed a page
range in `build_preface()`, eight wrong page references in `NOTE_FIXES`, the
hard-coded *ZZ* abbreviation and the epigraph, and it added `NOTE_TYPOS` and
`INDEX_TYPOS`.

**`just check` is red.** `check_parity` reports one file:

```
fa/preface.md: 9 blocks, source has 10
```

Every other change is inside existing blocks, where no checker can see it.
The Persian carries the damage all the same: the preface ends mid-word, the
reprinted-poems list has `TA` in it, the foreword has no title for the
German translation, and the notes send the reader to the wrong roll and page
eight times.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 12 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (5)

| file | what changed in the source |
|---|---|
| `plates.md` | the epigraph gains its source, *“Ikkyū no Shisō to Sono Shōgai”*, as a second line under Yanagida's name |
| `foreword.md` | *(Ikkyū: Im Garten der schönen Shin)*, was `(yg: Im Garten der sc が ez Shin)`. **The Persian dropped it.** *Nō* ×2, *Jōdoshinshū*, *Hōnen*, *Dōgen* ×4, *Sōtō*, *Shōbō Genzō*, *François*, *poètes maudits*, and the signature *Katō Shūichi* |
| `preface.md` | **two paragraphs back**, from p. xvi: the romanization and citation conventions. The old file ends «رومی‌سازی هپبورن-». **The reprinted-poems list** is the print's 44 numbers, where the Persian carries the OCR noise digit for digit. Also *Ikkyū*, *Katō Shūichi*, *Iida Shōtarō*, `U.B.C.,` |
| `introduction-4.md` | *49 gō*, was `49 gd,`, and **the Persian dropped the term**. *shi shū*, was `shi sha`; *Shisō* ×2; `“religious odes.”` and `three, two, one”` closed; `an order`, was `¢n order` |
| `notes.md` | **eight page references corrected** (010's table), eleven more rebuilt from garbage, and some thirty names, terms and quotes. **The Persian carries all of it**, `yg`, `Paar`, `Walsre`, `7394`, `Daas` and `pelo` included |

### B. Re-copy an entry list (3)

Entries are verbatim English, so these are not translation runs. Produce them
by 006 requirement 3: `strip` the source, keep the old file's Persian heading
and preamble, leave every entry line as `strip` gave it, `restore -o`.

- `abbreviations.md` — *ZZ*: **1946 (photo reprint of the original
  *Dainihon Zoku Zōkyō*)**, was 1968.
- `index-of-poems.md` — eleven entries, four of them with the page
  number back: *Ox, 21* (was `Oca?`), *…Pulled Out, 137*, *…City, 101*,
  *…Same Vase, 97*.
- `bibliography.md` — one word, *Chūsei Zenka no Shisō* in the second
  of its two entries.

### C. Not this spec's (1)

- `introduction-1.md` — `IKkyu` ×6 → *Ikkyū*. It is re-translated after
  [024](./024-introduction-read.md) has read it, and running it twice would
  mean two 900-chunk runs of the longest file in the book.

## Requirements

1. **Group A through the pipeline**, as `CLAUDE.md` describes: `strip`,
   `gtranslate.py -w --raw`, `restore -o`, one file at a time. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe per paragraph,
   not on the picker.
2. **`preface.md` wanted 900 in 005**, where it came back Classic at 4500
   after two paragraphs. Start there, and measure per paragraph, not per
   file.
3. **`notes.md` is four chunks and 207 blocks.** Count blocks before
   reading. A dropped note is a dropped block. Then check the eight
   corrected references by hand against 010's table, digits and all: the
   abbreviations (`T`, `SP`, `KZ`, `ZZ`, `CZS`) stay Latin.
4. **`plates.md`'s image lines come back intact**, as `CLAUDE.md` records.
   Check the paths anyway. The epigraph's second line needs its hard break,
   and `restore` will name it if the model drops it.
5. **§2 against the old file and the table.** *Dōgen*, *Rennyo*, *Shinran*,
   *Hōnen*, *Katō Shūichi*, *Yanagida Seizan*, *Iida Shōtarō*, *Leon
   Hurvitz*. Where the old file has a spelling and the table has none, keep the old
   file's.
6. **Group B by 006's procedure**, not by running the translator.

## Acceptance criteria

- [ ] The 5 files of group A re-translated.
- [ ] `preface.md` has the two paragraphs, and its poem list is the 44
      numbers from 6 to 567 and nothing else.
- [ ] `foreword.md` names *Im Garten der schönen Shin*.
- [ ] `notes.md`'s eight corrected references read as 010's table has them.
- [ ] Group B re-copied, entries byte-identical to `source/`.
- [ ] `just check` green. That closes 010.

## Out of scope

`introduction-1/2/3`, which are 024's. `bibliography.md` and
`glossary-index.md` beyond the one word above. 010 signed both off.
