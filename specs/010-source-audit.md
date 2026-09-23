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
- [x] `021`–`030` — read. 15 files repaired across the book; spec 012.
- [x] `031`–`042` — read as `031`–`040`. 10 files repaired; spec 013. Six
  poems found swallowed book-wide; spec 014 gave them back and renumbered,
  so this decade is now `031`–`042`: `039`, `040` are poems 111 and 113,
  from the same pages, and `041`, `042` were `039`, `040`.
- [ ] `043`–`050`
- [ ] `051`–`060`
- [ ] `061`–`070`
- [ ] `071`–`080`
- [ ] `081`–`090`
- [ ] `091`–`100`
- [ ] `101`–`110`
- [ ] `111`–`120`
- [ ] `121`–`130`
- [ ] `131`–`141` — `132` (poem 690) and `131`'s note were read and repaired
  in 014.

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

### Session 3 — `021`–`030` (scan pp. 89–100)

Page numbers here are the printed ones; the PDF page is 24 higher. Two
defect classes, one of them book-wide. **15 files changed in `source/`**, all
restorations, and they are [012](./012-retranslate-session-3.md)'s.

**1. Five set headings ran into the note before them.** `KNOWN_SETS` listed
six headings and matched them by prefix. Four were missing outright —
*The Scriptures Wipe Away Filth*, *Wind Bell*, *On Tiger Mount, the Snow
Falls on Three Grades of Monks*, *The Second Year of Kanshō—Starvation* — and
*Addressed to a Monk Who Burned Books* was listed but never matched, because
the OCR spaces its words out across the gutter. Each became the last words of
the previous poem's note: "…the miraculous and the ordinary. The Scriptures
Wipe Away Filth three poems". **The Persian translated all five as note
text.** Poem 68's note ends `[مجموعه‌ی] «متون مقدس آلودگی را می‌زدایند» (سه
شعر).`

It is now a map from the OCR'd line, whitespace collapsed, to the printed
heading, and it matches the whole line. Prefix matching was a trap in waiting:
the note lemma "The Scriptures Wipe Away Filth: An allusion…" starts with a
heading too. All nine headings checked on the page (pp. 90, 99, 105, 116,
150, 167). The four that already worked come out byte-identical.

Ten files: `021` `037` `050` `094` `121` lose the stray heading, and `022`
`038` `051` `095` `122` gain it as a block, which is what turns
`check_parity` red on those five.

**2. Local damage, each checked on the page.**

- **Two wrong marker numbers**, both in files 011 re-translated for their
  markers: `025` had [48] for **43** (p. 95), `028` [35] for **45** (p. 98).
  The sequence runs 42, 43, 44, 45, 46 through the decade now.
- `030`: `(90 Daité:` is the label **[90]** and **Daitō** (p. 99). The Persian
  carries `(90 دایتو` verbatim.
- `028`: a closing quote lost after `go yet.`, doubled `““At`, `it."`, and
  `poem no, 54` (p. 98).
- `027`: `T ien-pao` in the poem's last line (p. 97).
- `026`: `everbeleaguered` → `ever-beleaguered`, a line-end hyphen that is
  the word's own (p. 96).
- `122`: `In the years of Kansho` → **Kanshō** (p. 167), confirmed while
  checking the Starvation heading, a decade early.
- Stray quotes normalised where the file changes anyway, as 018's was in
  session 2: `layman.”’`, `well.’’`, `“‘lesser vehicle”`, `““Arhat”’`,
  `“Mountain Road”’`, and `Nanko` → `Nankō`.

`022`, `023` and `029` read clean. `024`'s pages 91–94, which 011 left
owing, match its repaired source.

### Session 4 — `031`–`040` (scan pp. 100–108)

Printed page numbers, as in session 3. One structural defect, book-wide and
too big for this spec, and local damage in every file of the decade. **10
files changed in `source/`**, all restorations, and nothing outside the
decade; they are [013](./013-retranslate-session-4.md)'s, except `038`.

**1. Six poems are not in `source/` at all.** Poem 113, *Half a Cloud*, is
the last paragraph of `038.md`'s notes: its display number OCRs as `NIS`,
`get_num()` rejects it, so the poem, its title and its verse ran into the
note before it, and its own `Notes:` became a second `## Notes` in `038`.
Poem 111, the second *Wind Bell*, is the same fault inside a set: its number
OCRs as `1 |` and it sits in 110's verse as a fifth line and four more.

Checked book-wide two ways — a page-foot number with no `# Poem` heading
(111, 113, 332, 690), and a left-margin token under five characters that
`get_num()` rejects (adds `Bild;`, `Boe`, `537,`). Every one confirmed on
its page:

| poem | page | OCR'd number | swallowed into |
|---|---|---|---|
| 111 *Wind Bell (II)* | 105 | `1 \|` | `038` (110) |
| 113 *Half a Cloud* | 107 | `NIS` | `038` (110) |
| 315 *The Gentleman's Wealth* | 143 | `Bild;` | `085` (308) |
| 332 *The Last Chrysanthemum in the South Garden* | 143 | `Boe` | `085` (308) |
| 537 *Promise to Be Born in the Time of Maitreya* | 158 | `537,` | `108` (536) |
| 690 *Sea Cloud* | 170 | `690,` | `126` (647) |

All six are in the book's own *Index of Poems*. **The Anthology has 126
poems, not 120**, and 009's PDF read had it backwards: the "two quoted
poems" it recorded in `085.md` are poems 315 and 332. Fixing it adds six
files and renumbers every file after `038`, which moves `fa/`, `_quarto.yml`
and every file number in this spec's checklist. That is
[014](./014-swallowed-poems.md). It must run before `041`–`050` is read, or
the next decade is read under numbers that are about to change.

**2. Local damage, each checked on the page.**

- **Four markers.** `031` `[4]?` is **47**; `034` `women.”5?` is **50**, and
  the Persian dropped it; `038` `[5]?` is **57**; `040` `[6]°` is **60**.
  The decade runs 46 to 60 without a gap.
- **Three quoted poems flattened**, now in `VERSE_QUOTES`: Tu Fu's couplet
  in `031` (p. 101), Ch'u Ssu-tsung's quatrain in `037` (p. 104), Hsü
  Chung-ya's in `038` (p. 107). Each turns `apparatus --check` red on the
  stale Persian.
- `031`: `Aui` → *Hui*, `I’m:`, `flavors.”’`, `ina poem`, `flavors ?`.
- `032`: `‘‘Katsu,”’` in the poem, and the unclosed `“Katsu.` in the note.
- `033`: `charlatan.”’`. `034`: the unclosed `“the old woman burned the
  hermitage,`.
- `035`: `sufhcient`. The old `sufh-\s*cient` rule never fired, because
  `dehyphenate()` joins the halves first; it now matches both.
- `036`, `037`: `Ryozen`, `Rydzen: Ryozcens` → *Ryōzen*, *Ryōzen’s*. Each
  anchored on its context: `Ryozen` stands in `introduction-2.md` and the
  glossary too.
- `037`: `oppor- _ tunity`. `038`: `““The banner`, the unclosed `“The wind
  moves.`, `noon.”`, `stancc` → *distance*, `HalfaCloud`.
- `039`, `040`: `Shoen` → *Shōen*.

**Left as the print has it:** `038`'s `balustrade. [57]` closes no quote,
and neither does the page. `034`'s title *Old Woman Kōan* is `POEM_TITLES`'
own, for an untitled poem.

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

Session 3 adds two more:

- **`024`'s six stray quotes** — `cloud-rain.””`, `clear’’`, `(“‘cloud`,
  `water’;`, `“‘lascivious`, `fragrant’`. 024 was re-translated in 011 and
  the Persian renders every one of them correctly, so they are not worth a
  third run.
- **Prose block quotes break mid-quote.** `parse_prose()` starts a paragraph
  at any indented line after one that ends in punctuation, and every line of
  an indented block quote is indented. The *Blue Cliff Record* kōan in `028`
  splits after its first sentence, the *Nempu* entry in `030` after
  "Dharma.". Book-wide and structural, like the note entries above: fixing
  it moves block parity in every file with a quoted passage.

### Found in passing by 009's PDF read — not yet confirmed against the scan

For the decades that will reach them. Each is a `source/` defect the Persian
faithfully carries.

- ~~`018.md` — a note marker OCR'd as a bare `’’25`, no brackets.~~ Fixed in
  session 2 by the closing-quote marker rule.
- `085.md` — ~~two quoted poems ("The Gentleman's Wealth", "The Last
  Chrysanthemum in the South Garden") flattened into the note's prose, with
  `Bild;`, `Boe` and `%` as OCR garbage around them~~ — **not quotes:
  poems 315 and 332**, swallowed; session 4, spec 014. ~~T'ao Yüan-ming's
  poem in the second note has its lines run together in pairs.~~ Set as
  verse in 014, in what is now `089.md`.
- `125.md` (was `120`) — `Sdseian`.
- `134.md` (was `128`) — `Unryoin`, `Sen’yuji`, `Sen’yiji` in the note
  against `Unryōin` / `Sen’yūji` in the title.

### Found in passing by session 3 — not yet confirmed against the scan

- ~~`031.md` — marker `[4]` where the sequence wants **47**.~~ Session 4.
- `052.md` (was `050`) — `Tozan “sword mountain is a mountain in hell`: the quote never
  closes.
- `129.md` (was `124`) — `The Second Year of Kansho: 1461.` Probably *Kanshō*, as in the
  heading and poem 639 on p. 167; its own page not checked.

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
- ~~`031.md` — `Wu Teng Aui Yüan`, *Hui*.~~ Session 4.
- ~~`037.md` — `doctrine of Rydzen: Ryozcens style of Zen`.~~ Session 4. ~~The note ends
  `Wind Bell two poems`~~ — fixed in session 3 with the other set headings.
- ~~`038.md` — `1 |` as a line of the poem: poem 111's number. **Poem 111
  swallowed**, session 4.~~ Spec 014: now `039.md`.
- `introduction-1.md` — two markers left bare, so the marker comparison
  shows the Persian with two the source lacks: `leprosy43` (no punctuation
  before the digit) and `Mori.“50` (an opening quote where the closing-quote
  rule expects a closing one). The model brackets both, correctly. Also
  `interview. [4]!`.
- `introduction-3.md` — `my ruins,84`, bare, after a comma.
- `001.md` — `taryn`, `fia`, `ryi#` for *fūryū*, *fū*, *ryū*. Session 1's
  decade, read twice and left. Not what makes that passage Classic: 011 fixed
  them in a scratch copy and the model still fell back.

### Found in passing by 014 — each confirmed on its page

For the decades that will reach them. 014 checked every *Index of Poems*
entry on an Anthology page against the poem the generator starts there.
That is how it found these; none is a missing poem.

- ~~`014.md` (poem 44, p. 80) — titled from the wrong poem.~~ Untitled in
  print; `POEM_TITLES` gave it *Two Pieces of Skin and One Set of Bone*, the
  Index's title for poem 344 on p. 144. The Index calls poem 44 *Yen-t'ou's
  Old Sail Kōan*. **Fixed and re-translated in 014**, with poem 539, which
  had 537's title — 014 is in a decade already read, so nothing else would
  have reached it.
- `090.md`, `097.md`, `126.md` (poems 344, 384, 605) are `Untitled [first
  line]` in `POEM_TITLES` where the Index gives a title — *Two Pieces of
  Skin and One Set of Bone*, *Utterly Absorbed in the Dream of Wu-shan*,
  *Tu-ling's Flowers Sprinkling Tears*. Poems 44, 94 and 539 follow the
  Index. Either convention is defensible and the book has both. Decide once,
  not per decade.
- `introduction-1.md` — `Shnonan` and `Shuonan` for *Shūon’an*, the same
  OCR 014 fixed in `131.md`'s Nempu entry.

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
