# 010 — The 147-file source audit

**Reading `source/` against the scan, one file at a time. Taken out of 008,
which was too small a box for it.**

## Context

This is spec 002's original checklist, carried into 008 as its requirement 1
and never worked: 002's two sessions were defect-class scans over the whole
tree, not a file-by-file read. It gets its own spec because the first decade of
it produced a generator fix, a factual correction and a re-translation spec,
and because at 147 files it is weeks of work, not a fold-in item.

**"The PDF" here is the 228-page English scan**, not the typeset Persian one.
This is a source-fidelity audit: does `source/` say what the print says. The
Persian PDF read is spec 007 requirement 5 and is a different pass with
different eyes.

Two things make the read worth doing rather than automating:

- **The OCR layer is not evidence.** The scan is images with an invisible
  OCR layer, and that layer is the same OCR `source/` was built from. Diffing
  the two compares OCR against itself and finds nothing. Only the page image
  shows what the book says.
- **The defects do not announce themselves.** A deleted word leaves fluent
  prose behind. `check_parity` counts blocks, so it sees a dropped paragraph
  and nothing smaller. Twenty-one of the 22 files 009 has to re-translate
  passed every checker in the repo.

## Goal

Every file in `source/` read against the scan; every defect either fixed in a
generator or recorded here as a deliberate exception.

## Dependencies

002 (this is its unfinished checklist). Not blocked by anything; nothing is
blocked by it except the quality of the edition.

## How to run a chunk

Locate first, then read. A helper that maps every `source/` file to its scan
pages, by anchoring on rare word 4-grams from the file body rather than its
heading (headings are the worst-OCR'd lines on a page):

```bash
pdftotext "$PDF" - | ...   # see the implementation notes below
pdftoppm -f 89 -l 101 -r 150 -png -gray "$PDF" out/p
```

150 dpi greyscale is enough to read the type and small enough to page through
quickly. Then read the rendered pages against the `source/` files.

**Work in chunks of ten and report per chunk.** Fix what is confirmed, in the
generator, then `just split` and diff `source/` against a copy taken before the
fix — that diff is the list of files whose Persian is now stale.

## Requirements

1. **The checklist below, read against the scan.** Poem files first: they are
   most of the book and the place a flattened verse quotation hides.

2. **Fix in the generator, never in `source/`.** `just split` reverts anything
   edited by hand. After each generator fix, re-split and diff.

3. **Record every changed file.** A source change to an already-translated file
   means that file needs re-translation, which is owned by a spec of its own —
   009 is the first of those. Do not re-translate here.

4. **A confirmed instance, not a heuristic.** 002 tried a general
   verse-detection rule and it turned quoted kōans into fake verse in `007`,
   `010`, `011`, `014`, `015`, `019`, `020`, `024`, `028`, `030`, `037`, `038`,
   `044`, `052`, `057`, `065`, `067`, `068`, `070`, `071`, `075`, `084` and
   more. Match on the confirmed text instead, the way poem 7's death poem now
   is.

5. **`bibliography.md` and `glossary-index.md`** — 008 requirement 3, still
   open, still low priority. 006 keeps their entries verbatim regardless, and
   a garbled entry is visibly garbage to a reader while a laundered one is not.
   Fix what is cheap; do not hold this spec on them.

## Files

### Anthology

- [x] `001`–`010` — read. Findings below; 22 files repaired across the book.
  Re-read for endnote markers in session 2, which session 1 had not checked.
- [x] `011`–`020` — read. 40 files repaired across the book; spec 011.
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
- [x] `introduction-1.md` — CJK column bleed fixed in 005 (`drop_column`).
- [x] `introduction-2.md` — same fix.
- [x] `introduction-3.md` — same fix.
- [ ] `introduction-4.md`

### Back matter

- [ ] `abbreviations.md`
- [ ] `notes.md` — repaired in 002; re-read here, since the audit's job is to
      confirm rather than assume
- [ ] `bibliography.md` — CJK garbling, requirement 5, low priority
- [ ] `index-of-poems.md`
- [ ] `glossary-index.md` — same

### Finally

- [ ] `source/README.md` re-read once the above is done.

## Acceptance criteria

- [ ] Every file above read against the scan, defects fixed in a generator or
      recorded here as a deliberate exception.
- [ ] Every file whose source changed is listed in a re-translation spec.
- [ ] The gibberish scan from 002 requirement 4 returns nothing outside
      `bibliography.md` / `glossary-index.md`, or those two are signed off as
      out of reach at 006's priority.
- [ ] `just split` re-run after every generator fix.
- [ ] `just check` passes — which, because a repair breaks parity against the
      stale Persian, means after the matching re-translation spec has run.

## Out of scope

Translating anything. Reading the typeset Persian PDF — 007 requirement 5.

## Implementation notes

### Session 1 — `001`–`010` (scan pp. 89–101)

Three defects, all fixed in `generate_final_markdown.py`, all book-wide rather
than local to the decade that surfaced them.

**1. `clean_translation_line()` was deleting English across the whole
Anthology.** Exactly the fault 008 requirement 2 recorded: the function guesses
the Chinese gutter at "a run of ≥3 spaces past column 45", and the pages are
set justified, so stretched word spacing trips it. 008 fixed the Introduction
with `drop_column()` — which measures the gutter instead — and left the poem
path on the guess. Confirmed against the scan:

| page | print | `source/` had |
|---|---|---|
| 94 | conventional **phrase de**scribing | "conventional scribing" |
| 94 | Fifth Avenue Bridge in Kyoto, **long a** haven | "Kyoto, haven" |
| 94 | enlightenment, **Daiō told** him not to | "enlightenment, him not to" |
| 187 | Night Conversation in the Dream **Chamber** | title cut short |
| 132 | as warm **as a cave in** winter | "as warm winter" |

The p. 132 line needed a second, one-line fix on top: the OCR capitalises
`Cave`, which in a poem line reads as a proper noun. Its pattern has to be
whitespace-tolerant and must not reach past `in` — typo rules run per line,
before the justified spacing is collapsed, and the verse breaks between `in`
and `winter`. Three attempts to write that rule failed for exactly those
three reasons in turn.

`get_trans_lines()` now routes each page through `drop_column()` and falls back
to `clean_translation_line()` only where no gutter is measurable — 21 of the
113 pages, which are genuinely one-column.

**A landmine came out with it.** `get_num()` read
`if idx == 1714 or s == '2'` — a hard-coded line index for poem 121, whose
display number OCRs to a bare "2". Restoring the deleted words shifted the
numbering by one line, at which point 1714 became the poem's first line, took
121 a second time and tripped the monotonic-number assertion. The text arm
alone is sufficient; the index arm is gone.

**2. `Daid` → `Daitō` was wrong three times in four.** The rule assumed every
OCR'd `Daid` is a mangled `Daitō`. Three of the four are **Daiō** — Daiō
Kokushi, Hsü-t'ang's student and Daitō's own master — so the book had
Hsü-t'ang instructing his own grand-successor. Checked on pp. 93, 94 and 104.
The Daitokuji founder is the one real `Daitō`, and it is now matched by its
context (`, founder`) ahead of the general rule.

**3. `split_poem7_death_verse()` was dead code through two specs that each
recorded it as done.** Hsü-t'ang's death poem is four indented lines on p. 93
and was flat prose in `source/002.md`. Two independent bugs kept the fix from
firing: its regex required a `(?P<pre>.*admired:) ` prefix that `parse_prose`
had already split into its own paragraph, and its call site was guarded by
`if num == '7'` when `num` is `None` on a Notes chunk — the number belongs to
the poem item, not to its notes. The guard is gone; the pattern is the poem's
whole text, which is guard enough.

**Result: 22 files changed in `source/`, every diff a restoration.** About 40
words back; the only removals are OCR garbage (`RX`, `exo`, `fitsHER`) and two
broken hyphen-joins repaired (`scribing` → `phrase describing`, `havior` →
`behavior`). They are spec 009's.

**Only `002.md` trips `check_parity`** — the death poem became a sixth block.
The other 21 changed words inside existing blocks, where no checker in this
repo can see them. That is the argument for the rest of this spec.

### Session 2 — `011`–`020` (scan pp. 102–112), and `001`–`010` again

Six defects. Two are book-wide generator faults; the rest are OCR damage
matched on confirmed text. **40 files changed in `source/`**, all of them
restorations, and they are [011](./011-retranslate-session-2.md)'s.

**1. The fallback cut was still deleting English on the one-column pages.**
Session 1 limited `clean_translation_line()` to the 21 pages where
`drop_column()` measures no gutter. On those pages it cut 8 times, and all 8
were English: "When **Nan-ch'üan** saw them" (p. 105), "Yüan-wu **said**"
(p. 112), "would **know**" and "Yün-men, **cloud**" (pp. 90, 92 — session 1's
own decade), "**the reader**", "**scrambled**", "**the coffin,**", "**as the
first**". It never cut a CJK character there. A one-column page has no column,
so the function is gone, `is_column_junk()` with it.

**2. Endnote markers are the least reliable thing in the OCR.** In the
Anthology they run 1, 2, 3 … without a restart, which makes a gap cheap to
see. It took this read to look, and the first twenty poems alone had:

- digits lost outright — `meaning.”`, `response.”`, `world.”`, `answer 5`;
- digits welded to a closing quote, which the endnote rule did not cover —
  `object.”29`, `it."35`. A new rule brackets them. It needs punctuation before
  the quote, so `“1 know` (an opening quote and a misread *I*) is left alone;
- digits misread as punctuation — `!2`, `?°`, `2?`, `3®`, `3!`, `*8`, `.!`;
- **the wrong number** — `18` for 13 (p. 103), `24` for 21 (p. 106), `9` for 6
  (p. 97), and `33` for 34 (p. 112). These are the dangerous ones: they look
  right and send the reader to the wrong note;
- `(26`, `(27` for the print's own bracketed poem-number labels on p. 97.

Poems 001–020 now carry 1–34 without a gap. **The Persian dropped most of the
damaged ones**: of 25 files whose markers disagree between `source/` and `fa/`,
most are this class. The comparison is in *Tooling* below.

**3. Dehyphenation fused names that break across a line.** `Master Fo-/yen`
became `Foyen`, `Chao-/chou` `Chaochou`, `Yüan-/wu` `YGanwu`. `join_hyphen()`
now keeps the hyphen when the hyphenated form is printed whole on a line
somewhere in the book. That restored 18 names across 14 files.

**4. Verse quoted in notes, flattened.** `split_poem7_death_verse()` is now
`split_verse_quotes()` over a table of confirmed quotes, matched across
paragraph breaks, because the OCR split one of them in two. Three were added:
the *Blue Cliff Record* verse in poem 35 (p. 101, session 1's decade), the
*Lotus Sūtra* couplet in poem 37 (p. 103), and the love song in poem 66
(p. 112). Requirement 4 still holds: each is matched on its own text.

**5. `Küang` → `Kuang` was wrong.** The print has **Yüeh Küang** on p. 97 and in
the glossary. The OCR gave five spellings of him, now one rule.

**6. Local OCR damage, each checked on the page.** `poem no. Tk` → `71.` (the
Persian had dropped the whole sentence), `tryu` → `fūryū` in poem 52's last
line, `rennorseful`, `SGto`, `Iam`, `Ts ao-shan`, `...@ burning`, `then ll`,
`burn, |`, `Wuc-tsu`, `Hui Yian`, `Sitra` (seven of them, book-wide).

### Left alone, on purpose

Five stray ideographic commas (`、`) sit in English prose — one each in
`preface.md` and `introduction-3.md`, two in `introduction-1.md`, and one in
`018.md`. The 018 one was normalised because that file is being re-translated
anyway. The other four are not worth a re-translation of `introduction-1.md`,
which is 67 K characters, for a comma. A general `、` → `,` rule is not the
answer either: `apply_typos` also runs over `bibliography.md` and
`glossary-index.md`, whose entries 006 keeps verbatim.

Session 2 adds these, the same kind of loss, none of which touches meaning:

- **ASCII for diacritics in some names** — `Sakyamuni` (14 of 14), `Kasyapa`,
  `Acarya`. Consistent, and the Persian spells the name from `STYLE.md` §2.
- **Stray and doubled quotes** — `’’` for `”`, `fish.’`, `““When`, a missing
  opening quote on `“Ears`, a missing closing one after `“Pivot`. The
  translator renders `«»` either way.
- **Note entries run together.** The print starts each lemma on a new line
  in italics; `parse_prose()` joins them into one paragraph. That is the
  book-wide shape of every `## Notes` section, and changing it would break
  block parity across 93 files.

### Found in passing by 009's PDF read — not yet confirmed against the scan

For the decades that will reach them. Each is a `source/` defect the Persian
faithfully carries.

- ~~`018.md` — a note marker OCR'd as a bare `’’25`, no brackets.~~ Fixed in
  session 2 by the closing-quote marker rule.
- `085.md` — two quoted poems ("The Gentleman's Wealth", "The Last
  Chrysanthemum in the South Garden") flattened into the note's prose, with
  `Bild;`, `Boe` and `%` as OCR garbage around them; and T'ao Yüan-ming's
  poem in the second note has its lines run together in pairs.
- `120.md` — `Sdseian`.
- `128.md` — `Unryoin`, `Sen’yuji`, `Sen’yiji` in the note against
  `Unryōin` / `Sen’yūji` in the title.

### Found in passing by 011 — not yet confirmed against the scan

Same terms. 011 re-translated these files and the Persian carries the damage
(or, where noted, quietly corrects it).

- ~~`024.md` (poems 69–71's notes)~~ — **confirmed on pp. 90–94 and fixed**,
  ahead of its decade, in 011's session 2: `filth.’3? 69]` is marker 37 and
  the label [69]; `(79` the label [70]; `Pi` the label [71]; `[4]°` is 40;
  **`dung ? [42]` is 41 in the print**, and `water.’ 3` is the real 42;
  `Stitra`, `Wu-tai`, `conJures`, `Fallen Hower`. Three quoted poems set back
  as verse. Every rule is anchored on its own text: `just split` changed
  `024.md` and nothing else. The decade's read still owes the rest of 024's
  pages and the stray quotes 010 leaves alone (`cloud-rain.””`).
- `031.md` — `Wu Teng Aui Yüan`, *Hui*.
- `037.md` — `doctrine of Rydzen: Ryozcens style of Zen`; and the note ends
  `Wind Bell two poems`, which is the next poem's heading run into it.
- `038.md` — `1 |` as a line of the poem: poem 111's number.
- `introduction-1.md` — two markers left bare, so the marker comparison
  shows the Persian with two the source lacks: `leprosy43` (no punctuation
  before the digit) and `Mori.“50` (an opening quote where the closing-quote
  rule expects a closing one). The model brackets both, correctly. Also
  `interview. [4]!`.
- `introduction-3.md` — `my ruins,84`, bare, after a comma.
- `001.md` — `taryn`, `fia`, `ryi#` for *fūryū*, *fū*, *ryū*. Session 1's
  decade, read twice and left. Not what makes that passage Classic: 011 fixed
  them in a scratch copy and the model still fell back.

### Tooling

The file-to-page index is worth rebuilding rather than storing — it takes
seconds and it moves whenever the generator changes. Anchor on word 4-grams
that appear on at most three pages, take the pages sharing the most of them.
Every one of the 147 files resolved on the first run with no manual help.

**Endnote markers, `source/` against `fa/`.** A cheap check that `just check`
does not run. It is how session 2 found out the Persian had dropped markers:

```bash
python3 - <<'PY'
import re, glob, os
tr = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
for f in sorted(glob.glob('source/[0-9i]*.md')):
    g = 'fa/' + os.path.basename(f)
    s = re.findall(r'\[(\d{1,3})\]', open(f).read())
    p = re.findall(r'\[(\d{1,3})\]', open(g).read().translate(tr))
    if s != p: print(os.path.basename(f), s, p)
PY
```

In the Anthology the sequence alone finds gaps: markers run 1, 2, 3 … and a
bracketed number that breaks the run is either a misread marker or a
reference to the full *Anthology*'s numbering (`[101]`, `[640]`).
