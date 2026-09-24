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

- [x] The 5 files of group A re-translated.
- [x] `preface.md` has the two paragraphs, and its poem list is the 43
      numbers from 6 to 567 and nothing else. (The spec said 44; the print
      has 43. See below.)
- [x] `foreword.md` names *Im Garten der schönen Shin*.
- [x] `notes.md`'s eight corrected references read as 010's table has them.
- [x] Group B re-copied, entries byte-identical to `source/`.
- [x] `just check` green. That closes 010.

## Out of scope

`introduction-1/2/3`, which are 024's. `bibliography.md` and
`glossary-index.md` beyond the one word above. 010 signed both off.

## Implementation notes

### Group A: four plain runs and one harness

**`plates` and `foreword` at 4500, `preface` at 900**, all Advanced and all
restored on the first try. `plates`' four image paths came back intact, and
the epigraph's second line has its hard break. The model ran `*Mori’s poem:*`
onto the stanza before it. One blank line put back in the scratch draft fixed
that, as in 022's `141`. `foreword` names *Im Garten der schönen Shin*.

**`preface`: the print has 43 poem numbers, not 44.** The spec's count was
wrong. On p. xv the list runs 16 + 11 + 11 + 5 = 43, from 6 to 567, and
`source/` and the Persian carry exactly those numbers in that order. The two
recovered paragraphs are the last two blocks, and parity is back to 10 on
10. At 900 the ezafe count falls from 17 in the first paragraph to 0–3 in
the rest, so all seven of those paragraphs were read. They are Advanced:
restructured, no Latin left standing, and nothing doubled.

**`introduction-4` at 4500.** *49 gō* is back as «۴۹ شعر از نوع «گو» (gō)»,
and markers [85]–[88] are right. **Left as the model gave it:** «مجموعه‌ی
سه‌شعریِ شماره‌های... شماره‌های ۶۹، ۷۰ و ۷۱», a stutter on *nos.* The
meaning is intact. 2250 does not stutter, but it serves the last three
paragraphs Classic («ترکیبی از ملاحظات عینی و ذهنی، انتخاب اشعار … را تعیین
کرده است»), which is the worse trade.

### `notes.md` needed 006's harness again, rebuilt

Both plain runs failed exactly as 006 recorded. At 4500 the draft had 205
blocks, with notes 65+66 and 18+19 merged. At 900 the count was 207, but in
both drafts the citation-only chunks came back Classic: 12–14 notes handed
back in English, `کز`, `ت 48`, `رول`. The harness was thrown away after 006,
so it was rebuilt in the scratchpad to 006's description. Pieces of about
1,800 characters, each behind note 3 as a primer whose translation is
discarded. Each piece is gated on block count, the `CZS|KZ|SP|ZZ|T N` set
per note, an Arabic-script letter, and no `رول`/`اس پی`/`کز،`. A failing
piece is halved and retried. **47 calls, and all 207 blocks passed**,
without the mop-up pass.

**What the old file carried is gone**: `Paar`, `Walsre`, `pe 7394`, `Daas`,
`pelo`, `joe`, and `yg` in Trans. 1. **The eight corrected references read
as 010's table has them**: Intro 59 roll ۴, Intro 73 *Ch’uan Teng Lu* roll
۱۱, T 51, 284a, Trans. 9 KZ ۱۱, Trans. 59 SP roll ۱۱۷ p. 2a, Trans. 78 KZ
۱۹۳, Trans. 99 ۱۱۵a, Trans. 100 roll ۱۳, Trans. 108 roll ۱. Intro 18 has its
294c and Intro 82 is Katō Shūichi.

006's two hand-steps were applied to the scratch draft again. The entry
numbers went back to Latin digits (§4.2), and `<!-- normalize: off -->`
went around note 106, the Sukey Hughes title in ASCII quotes, which was note
71 in 006's numbering.

**Left as the model gave it, as 006 left the old file:** titles are sometimes
transliterated and sometimes left in Latin script. The old file had 45 notes
with Latin standing and this one has 54. Page columns are sometimes Latin
(`ص 4b`) and sometimes Persian (`ص ۹الف`, `۲۵ الف و ب`): 6 notes in the old
file and 11 here. Hurvitz is «هوروویتس» here and «هورویتز» in the preface. Each
file keeps its old spelling, as requirement 5 says.

### §2, conformed against the table and the old files

- *Ikkyū*: «ایکیو», «ایکّیو» → «ایک‌کیو» in all five. The old `notes.md`
  had «ایکیو» ×20 unconformed. It now has none.
- *Kyōunshū*: «کی‌اون‌شو», «کیو-اون-شو» → «کیوئونشو», in `foreword`,
  `introduction-4` and `notes`.
- *Hsü-t’ang*: «شو-تانگ» → «شیو-ت’انگ», in `plates` and `notes` (×3).
- *T’ao Yüan-ming*: «تائو یوان‌مینگ» → «ت’ائو یوآن-مینگ», in `foreword` and
  `notes`.
- *Po Chü-i* «پو چیو-ای» and *Niao K’o* «نیائو ک’و» in `plates`, as the old
  file had them.
- *Shinran*: «شین‌ران» → «شینران», as the old `foreword` had it.
- *Lin-chi*: «لین‌چی» → «لین-چی», in `preface` and `notes`. *Ichijoji*
  «ایچیجوجی», as the old `preface` had it.
- In `notes`: *kōan* «کوان» → «کوآن», *Nempu* «نِمپو» → «نمپو», *Chuang Tzu*
  «چوانگ‌تزو» → «چوانگ تزو», *Ch’uan Teng Lu* → «چ’وآن تنگ لو», *Wu Teng Hui
  Yüan* «وو تِنگ هویی یوآن» → «وو تنگ هوی یوآن», *Wang Chang-ling*
  «چانگ‌لینگ» → «چانگ-لینگ», and *Vimalakīrti* → «ویمالاکیرتی».
- *Dōgen*, *Rennyo*, *Hōnen*, *Katō Shūichi*, *Yanagida Seizan* and *Iida
  Shōtarō* came back as the old files had them.

### Group B

Built by 006 requirement 3: the old file's Persian heading and preamble,
every entry as `strip` gave it, and `restore -o`. **All 210 entry lines are
byte-identical to `source/`.** That is 5 in `abbreviations`, 123 in
`index-of-poems` and 82 in `bibliography`. The diff is the ZZ entry, the
eleven index entries, and *Shisō* in `bibliography`.

### Result

`just fix` normalized two files: two stray ZWNJs in `notes`, and the ASCII
quotes the model put around «ایک‌کیو» inside `plates`' epigraph. **`just
check` is green**, with 153/153 on parity and anchors. That closes 010.
