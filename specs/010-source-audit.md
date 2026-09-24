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
- [x] `043`–`050` — read. 9 files repaired, 2 of them outside the decade
  for *Lan-ts'an*; spec 015. Closing paragraphs of notes found joined book-wide; spec 016.
- [x] `051`–`060` — read. 9 files repaired, 1 outside the decade for its
  set's title; spec 017.
- [x] `061`–`070` — read. 5 files repaired, none outside the decade; spec 018.
  Settles two of the three standing marker disagreements, `064` and `070`.
- [x] `071`–`080` — read. 7 files repaired, none outside the decade; spec 019.
  One more set heading ran into a note; it was the last one missing.
- [x] `081`–`090` — read. 3 files repaired, none outside the decade; spec 020.
  Lady Pan's fan poem set back as verse.
- [x] `091`–`100` — read. 4 files repaired, none outside the decade; spec 021.
  A kōan's closing quote lost in a poem line, which the Persian misread.
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

### Session 5 — `043`–`050` (scan pp. 109–115)

Printed page numbers; the PDF page is 24 higher. Eight files, because 014's
renumbering moved the decade's first two to `041`/`042`, which session 4
had read. **9 files changed in `source/`**, all restorations: the decade's 7,
and `001` and `introduction-3` for one name. Three need re-translating:
[015](./015-retranslate-session-5.md).
One structural defect, book-wide: [016](./016-note-afterwords.md).

**1. A note's closing paragraph runs into its last entry.** Poem 130's note
ends with a paragraph of its own on p. 114, set off by a blank line: "As
duplicated in the translation, the three rhyming lines…". It is about the
poem as a whole, not the last lemma, and `source/049.md` appends it to
*Sung-yüan*'s gloss. The raw has the blank line; `build_translations()`
drops every blank line when it builds a chunk, so `parse_prose()` never sees
the break. It cannot simply keep them: a blank line is also a page break.

Measured book-wide: a blank line inside a Notes chunk, with the same page
foot on both sides. **17 such paragraphs in 16 files** — `001` `004` `015`
`021` `024`(×2) `026` `030` `049` `075` `086` `091` `092` `109` `112` `118`
`131`. Three more are already split some other way (`010`, `024`'s second,
`139`), and three hits are not afterwords: `024`'s `(79` and `Pi` labels,
and a set title in `073`–`075`. Fixing it moves block parity in all 16, most
of them read and re-translated already. Too big for a session: spec 016.

**2. Local damage, each checked on the page.**

- **Three markers.** `046` `you.”’6` is **62** and `dukes ?68` is **63**;
  `049` `future.’’6°` is **65**, left bare by the OCR and missing from the
  Persian. The decade runs 61 to 65 without a gap.
- **Lan-ts'an's couplet flattened**, now in `VERSE_QUOTES` (p. 111, `046`).
  Its first line was a paragraph of its own and its second ran into the next
  lemma. Turns `apparatus --check` red on the stale Persian.
- `044`: `Daiki Koja Zenji` → *Kōjū*; the Persian transliterates the OCR.
  `Message.’`.
- `045`: `1s` → *is*, in the poem.
- `046`: `Lan-tsan` in the poem and the legend; `Master as: Kasō Sddon` →
  *Master Kasō: Kasō Sōdon*; `YSso`; `Ch us`; `way.’`; the missing `”`
  after `messenger?`, with `Lan-ts an`; `activity’`.
- `047`: `P’yu-hua`. `048`: `severed?’`.
- `049`: `Kasé’s`, `"1 know`, `Tetto` → *Tettō*.
- `050`: `scriptures ;`.

**3. *Lan-ts'an*, and a §2 row built on the OCR.** p. 110 prints
**Lan-ts’an** where `046`'s poem had `Lan-tsan`. So do the glossary-index and
Introduction pp. 51–52; `introduction-3` had `Lan-tsan` and `Lan-ts an`
there, now fixed. p. 66, `001`'s note, prints **Lan-t’san** twice: a slip in
the book, and `source/` now follows it. `STYLE.md` §2 had settled
`Lan-tsan` → «لان-تسان» as «correct as given» and called `001`'s spelling OCR
damage — both backwards. The row is corrected to «لان-تس’ان», and 015 conforms
`001` and `introduction-3`. **2 more files changed in `source/`**, 9 in all.

**Left as the print has it:** `048`'s `in the the Sung-yüan Yü-lu`. `046`'s
`pp. 16-18` has a hyphen where the print sets an en dash, as 38 of the 40
page ranges in `source/` do. The prose after `046`'s block quote ("In his own
poem…") runs into the quote: the *Prose block quotes* shape session 3
records.

### Session 6 — `051`–`060` (scan pp. 115–122)

Printed page numbers; the PDF page is 24 higher. **9 files changed in
`source/`**, all restorations: the decade's 8, and `050` for its set's
title. Six need re-translating: [017](./017-retranslate-session-6.md). No
book-wide defect this time; two local ones in the generator's own tables.

**1. `POEM_TITLES` had the set 134–136 under a title the book never uses.**
*Three Poems to Show the Assembly (I)–(III)*; the set heading on p. 115 and
the book's Index both say *Three Poems to Show the Monks of My Circle*, and
`050`'s own bold set heading always did. The Persian followed the headings:
«سه شعر برای ارائه به جمع». Session 5 read `050` and did not catch it —
the heading label is the generator's, the page shows only the set heading.

**2. Two wrapped titles leaked a line into their verse.** The title-skip in
`build_translations()` is a hand count per title, and two were short:
*Praising the Dharma Master Tz’u-en / K’uei-chi* wraps to two lines on
p. 120 and was counted as one; *Congratulating Daiyūan’s … / … / Sōe
Daishō* wraps to three on p. 121 and was counted as two. `059` and `060`
each opened on a fifth verse line, `K’uei-chi` and `Soe Daisho`, and the
Persian carries both. Checked book-wide: a poem whose first verse line's last
words are in its own title. `084`, `090`, `112`, `118` also match, and all
four are real first lines.

**3. Local damage, each checked on the page.**

- **Three markers.** `054` `fabrications.66` and `mind.67` are **66** and
  **67**, and lost their closing quotes; `059` `day.”?!` is **71**, which the
  Persian dropped. The decade runs 66 to 71 without a gap.
- `052`: `Tozan` → *Tōzan* ×3, and `“sword mountain”` closed.
- `054`: `compassion.’`, `“far-out.`, `compassion .. .`, `Vimalakirti Sutra`
  → *Sūtra*.
- `055`: `Hames` → *flames* ×2, and the Hirano quote's ASCII `"` opened and
  closed.
- `057`: `1 am` → *I am*, in the poem.
- `058`: `madinan` → *madman*, in the poem. **The Persian has «دیوانه‌ای از
  اهل مدینه»**: a madman from Medina.
- `059`: `K'uei-chi's`, `K uei-chi`, `Kucichi` → *K’uei-chi*; `Hejust`;
  `Lotus Sutra` → *Sūtra*.
- `060`: `YsQ` → *Yōsō*; `“man from P’u-chou”’`.

**Left as the print has it:** `059`'s `aprocryphal`. `059`'s block quote
ends `women.”70` on p. 120 with no opening quote to close; `source/` has
`women. [70]`, which is the better reading of a typesetter's slip.

**Left, the ASCII-for-diacritics class** (session 2): `Sakyamuni` in `057`,
`Vimalakirti` and `Tathagata` in `054`, `Yogacara` and `samadhi` in `059` —
each without a macron everywhere in `source/`. `Sūtra` is not in that class:
`source/` has it with the macron 10 times to 4 without, and the decade's two
are fixed. `054`'s block quote breaks after its first line and `059`'s prose
after its quote runs into it: the *Prose block quotes* shape.

### Session 7 — `061`–`070` (scan pp. 123–130)

Printed page numbers; the PDF page is 24 higher. **5 files changed in
`source/`**, all restorations and all in the decade. Four need re-translating:
[018](./018-retranslate-session-7.md). No book-wide defect in the generator.
One book-wide shape is recorded for a decision (item 3).

**1. Five markers, and two old disagreements settled.**

- `063` `eating.”2` is **72**. The print sets `eating.72` with no quote to
  close. **The Persian carries [2]**, the wrong number, and it sends the
  reader to note 2.
- `064` `Buddhas!’ 74` is **74**, left bare by the OCR. The Persian had
  bracketed it already. This was one of the three standing disagreements in
  *Tooling*, and it was the source that was wrong.
- `066` `Yü-lu®>` is **75**, and the Persian dropped it.
- `069` `Yü-lu.??` is **77**, and the Persian dropped it.
- `070` `Devil.’ 79` is **79**, again bare. Here too the Persian had it
  right: the second standing disagreement.

The decade runs 72 to 80 without a gap. The marker comparison now disagrees
only on `introduction-1` among the old three, and on `063`, `066` and `069`,
which are 018's.

**2. Local damage, each checked on the page.**

- `063`: `‘a day of no work` opens with `“`.
- `064`: `“*...` becomes `“...`, and `“You shall all become Buddhas!’`
  becomes `‘…’”`, a quote inside a quote.
- `066`: `Sung-ytian` and `Sung-yuan` become *Sung-yüan*; `(1025- 72)`.
- `070`: `BuddhaDevil` ×2, one of them in the poem, becomes *Buddha-Devil*.
  Neither half is in `join_hyphen()`'s keep-list, and the print never sets
  the pair whole on one line. **The Persian's third line has no Buddha-Devil
  at all.** Also `Sungdynasty` becomes *Sung-dynasty*, and `Chingsu`
  becomes *Ch’ing-su*. In the *Hsü Ch’uan Teng Lu* quote, five quotes are
  restored as p. 129 sets them: `fruit.”`, `‘Tz’u-ming.`, `Path?’`,
  `“‘You have a go`, `‘You can enter`.

`061`, `062`, `067` and `068` read clean.

**3. The prose introductions are flattened to one paragraph, book-wide.**
p. 125 sets the *Prose Introduction to No. 187* as five paragraphs, each
indented. `source/065.md` has it as one. **All 15 prose-introduction files
in `source/` are a single paragraph.** `build_translations()` strips every
line of the chunk before handing it to `parse_prose()`, so the indent that
splits a paragraph is gone before it is looked for. Fixing it would move block parity in
every one of the 15 that the print breaks, and they have not been counted.
Like 016's afterwords, that is too big for a session and wants a spec of its
own. It is not opened here.

**Left as the print has it:** `063`'s `hid his tooks`, `065`'s
`distinguising`, and `070`'s `enbroiled`, each confirmed at 300 dpi. `063`'s
`Ta-chih: An honorific name for Pai-chang` has no full stop, and neither has
`067`'s `See notes to poem no. 33`. p. 130 starts a new paragraph at
*Ikkyū often refers*. The marker digit hid it from `parse_prose()`, the way
`059`'s did in session 6: the *Prose block quotes* shape. So is the break
inside `069`'s Hirano quote and `070`'s *Hsü Ch’uan Teng Lu* quote.

**Left, in the ASCII-for-diacritics class:** `Yamaraja` ×2 in `063`, one of
them in the poem. The print has *Yamarāja*. `source/` has no macron form
anywhere, and the Persian spells it «یاماراجا» either way.

### Session 8 — `071`–`080` (scan pp. 130–137)

Printed page numbers; the PDF page is 24 higher. **7 files changed in
`source/`**, all restorations and all in the decade. Six need re-translating:
[019](./019-retranslate-session-8.md). One defect of a book-wide class,
which turned out to have one member left.

**1. A tenth set heading ran into the note before it.** *Congratulating
Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after
His Leprosy* is set on p. 133 as a three-line heading over poems 240 and
244, with no "two poems" line under it. It was not in `KNOWN_SETS`, so it
became the last words of `073`'s note, and **the Persian translated it as
note text**: «تبریک به استاد «کی» (Ki) بابت ساخت صومعهٔ «دم عقاب»…». Session
5's blank-line measurement saw it as "a set title in `073`–`075`" and left
it. The map now has its first line, as it has *Three Poems to Show the Monks
of* for a wrapped heading; the rest of the heading falls into the set
chunk, which is dropped. `073` loses the stray text and `074` gains the
heading as a block, which is what turns `check_parity` red on `074`.

Checked book-wide: every poem titled `(I)` in `source/` now carries a bold
set heading except `036`, `045`, `108` and `136`. Those four sets open with a
prose introduction and the print gives them no heading. Nothing else is
missing.

**2. Four markers.**

- `072` `a cat.81` is **81**, and lost its closing quote. The Persian has
  both.
- `073` `returning home.’’82` is **82**; `Wu-men Kuan.8?` is **83**. **The
  Persian carries [8]**, the wrong number.
- `080` `marvelous.”’8?` is **87**, and the Persian dropped it.

The decade runs 81 to 87 without a gap.

**3. Local damage, each checked on the page.**

- `071`: the poem's last line ends `singing,` where p. 130 sets a full stop,
  and **the Persian ends the poem on a comma**. `Ch Yüan’s` is **Ch’ü
  Yüan’s** (p. 131); the Persian has «چو یوان» where §2 has «چ’یو یوآن».
- `072`: `Nan-ch’tian`, in the poem. The Persian has it right.
- `073`: `poetry ;` in the poem; `“a storm in a tea pot` closed;
  `“cnlightenment poem` is *“enlightenment” poem*, across the page break.
- `075`: `Soki` ×2 is **Sōki**, each anchored on its context, because the
  glossary-index has `Soki` too. `Jikaishi` is **Jikaishū**; **the Persian
  has «جیکایشی (Jikaishi)»**. `httle` is *little*, and four stray quotes:
  `beauty’`, `far out’’`, `song’:`, `song’?`.
- `079`: `Mafijusri` ×2 and `Majijusri` are **Mañjuśri**, as p. 136 sets
  it. `ch’ing/jo` and `jd` are **jō**; **the Persian has *jo* twice**.
  `Sutra` in the poem is *Sūtra*, and `Sarangama`, split across a line, is
  *Sūrangama*. `“circumstances”’`, `““Making`.
- `080`: `“no mind”’`.

`076`, `077` and `078` read clean.

**Left as the print has it:** `071`'s `on on the banks` (p. 131), `072`'s
`52.)One` with no space, `077`'s `“A lecture master asked, “The Twelvefold`
with two opening doubles and `plowed.86` closing neither, and `079`'s
`ch’ing/jō This` with no full stop.

**Left, in the ASCII-for-diacritics class:** `Ananda` ×4 in `079`, where the
print has *Ānanda*; `source/` has no macron form, and the Persian spells it
«آناندا» either way. `Sūrangama` for the print's *Śūraṅgama*: it is the form
`bibliography.md` has, twice.

### Session 9 — `081`–`090` (scan pp. 137–144)

Printed page numbers; the PDF page is 24 higher. **3 files changed in
`source/`**, all restorations and all in the decade. One needs
re-translating: [020](./020-retranslate-session-9.md). No book-wide defect.

**1. One marker with the wrong number, one left bare.** `086`'s
`too many.9` is **91**, and it lost its closing quote. The general rule made
it `[9]`, and **the Persian carries [9]**. `086`'s `store.’ 92` is **92**,
left bare, and the Persian has a bare «۹۲». The decade runs 88 to 96 without
a gap.

**2. Lady Pan's fan poem is verse again**, now in `VERSE_QUOTES`: ten lines
on pp. 141–142, in `086`'s note. 016 found it. Its first line was the end of
the lemma's paragraph and the rest ran together two paragraphs deep. This
turns `check_parity` and `apparatus --check` red on `086`.

**3. Local damage, each checked on the page.**

- `084`: the *I Ching* quote had lost two quote marks. The print has
  `“Taming Power of the Great,”` and `says, “What is it?`; the quote closes
  `Heaven.”89`, not `’’`. The Persian has the quote right already.
- `086`, in the *Chuang Tzu* passage: `Ill` and `Tm` are *I’ll* and
  *I’m*, and `youd` is *you’d*. `“Come, perch` and `“Why, of course! Tm`
  open with single quotes, since both are inside Chuang Chou's speech, and
  so does `right?” The perch`. The passage now closes `store.’”`.
- `087`: `"objects to` is *“objects” to*. The Persian has it right.

`081`, `083`, `085`, `088` and `089` read clean. `082` differs only in stray
quotes: `‘acceptable’` and `Dharma.’’ [88]`, where p. 138 has doubles. That
is the class this spec leaves alone, and nothing else in the file changes.

**Left as the print has it:** `Yueh` in `086`, with no ü. `086`'s first
*Will that be all right?* closes no quote. p. 141 breaks the *Chuang Tzu*
passage into two paragraphs, and `source/` has four: the *Prose block
quotes* shape. `089`'s *fūryū* lemma runs into the Rinzai quote before it:
the *note entries run together* shape.

**Left, in the ASCII-for-diacritics class:** `Mara` in `087` (×2) and
`090`, where the print has *Māra*. Those are the only four in `source/`, and
none has the macron. The Persian spells it «مارا» either way.

**Still open, from 014:** `090` is poem 344, `Untitled` in `POEM_TITLES`
where the Index says *Two Pieces of Skin and One Set of Bone*. That wants
one decision for all three files, not one per decade.

### Session 10 — `091`–`100` (scan pp. 145–150)

Printed page numbers; the PDF page is 24 higher. **4 files changed in
`source/`**, all restorations and all in the decade. One needs
re-translating: [021](./021-retranslate-session-10.md). No book-wide defect.

**1. A kōan's closing quote, lost in a poem line.** `091`'s second line read
`The kan “privately carriages pass confuses clear and cloudy.`; p. 145 sets
`The kōan “privately carriages pass” confuses`. With no closing quote, **the
Persian put the whole rest of the line inside the kōan**: «در خفا، کالسکه
عبور می‌کند و مرز میانِ صاف و ابری را درهم می‌آمیزد.» The poem says the
kōan confuses clear and cloudy, not that the carriages do.

**2. Local damage, each checked on the page.**

- `091`: `““No words`; `can get through.97` is **97**, which kept its
  number and lost its closing quote. The Persian has both.
- `092`: `Honen` ×3 and `Henen's` are **Hōnen**, two of them in the poem;
  `Jodoshi` is **Jōdoshū**. Each is anchored on `092`'s own text, because
  the glossary-index, the bibliography, `foreword.md` and `notes.md` spell
  it `Honen` too. Also `Butsu’’` and `alonc`, the latter at marker **98**.
  The Persian has «هونن» and «جودو-شو» already.
- `097`: `(803- 52)`, the same join as `066`'s in session 7.
- `100`: the poem's last line ends `belly.,`. At 400 dpi p. 150 has a full
  stop and a speck after it, not a comma.

The decade runs 97 to 98 without a gap; 99 and 100 are in `101`, poem 390's
notes, which cover the whole set. `093`, `094`, `095`, `096`, `098` and
`099` read clean.

**Left as the print has it:** `098`'s note has *sentient* where p. 149 sets
`senient`, the better reading of a typesetter's slip. `092`'s `Bliss... .` for
the print's `Bliss. . . .`. `091`'s kōan breaks after `enter;` and runs `In
principle` into the quote, and `092`'s Hōnen quote breaks at `It is nothing`
and `Those who believe`: the *Prose block quotes* shape. `097`'s
`(1037-101)` and `(1045-105)` are the print's own ranges, hyphens for en
dashes as everywhere.

**Poem 376 has no title on p. 147.** `094` is titled *Quietly Singing Beside
the Lamp* from `POEM_TITLES`, which is the Index's title for it. That is the
convention poems 44, 94 and 539 follow. `097` (poem 384) is `Untitled` where
the Index gives *Utterly Absorbed in the Dream of Wu-shan*: 014's open
question, unchanged.

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
- ~~`052.md` (was `050`) — `Tozan “sword mountain is a mountain in hell`: the quote never
  closes.~~ Session 6.
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

### Found in passing by session 5 — not yet confirmed against the scan

- `139.md` — a Tu Fu poem, "Moonlight Night", flattened in its note: title
  and lines run together two to a paragraph. The paragraph before it
  (`The sound of the bell of Ch’ang-lo…`) looks like verse run together too.
  Found by the blank-line measurement for 016, not read on the page.

### Found in passing by session 6 — not yet confirmed against the scan

- ~~`079.md` — `Sutra` once, beside `Sūtra` once in the same file.~~ Session 8.
- `112.md` (poem 536) — `resembless` and `IfI` in the poem.

### Found in passing by session 8 — not yet confirmed against the scan

- `introduction-3.md` — `Ch Yüan` ×4 for *Ch’ü Yüan*, the damage session 8
  fixed in `071`. The rule there is anchored on `071`'s context.
- `introduction-1.md` — `Jikaishi` once, probably *Jikaishū* as on p. 133.

### Found in passing by session 10

- `101.md` (poem 390, p. 151) — Po Chü-i's poem in the note, eight lines in
  print, is run together into four paragraphs, two lines to most of them.
  Also `Po Chit-i`, `Off.”’`, and `papiyan` for *pāpiyān*. `[388]` and
  `[390]` are the print's own labels.
- `foreword.md` — `Jodoshinsh@`, probably *Jōdoshinshū*; its page not
  checked. `glossary-index.md` has `Jodosht` and `Honen`, which 006 keeps
  verbatim.

### Found in passing by 016 — each seen on its page

- ~~`086.md` (poem 293, p. 142) — Lady Pan's fan poem, flattened.~~ Session 9.
- `109.md` (poems 531–532, p. 156) — *The poems concerning Mori are grouped
  together…* is an indented paragraph of its own in print, and runs into the
  afterword before it: that ends `(See p. 28.)`, and `parse_prose()` only
  splits an indent after `.` `!` `?` and quotes, not `)`.

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
