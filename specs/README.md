# Specs Roadmap — ایک‌کیو و گلچین ابر دیوانه

How to work on this project: see `CLAUDE.md` at the repo root. Shared context for
every spec: [`000-overview.md`](./000-overview.md).

Unlike a code project, **one spec here is not one session.** The body specs cover
weeks of work and carry a per-file checklist. Update the **Status** column when you
start (🟨 In progress) and when you finish (✅ Done).

## Status table

| #   | Spec                                                       | Depends on | Status         |
|-----|------------------------------------------------------------|------------|----------------|
| 000 | [Overview & shared context](./000-overview.md)             | —          | 📖 Reference   |
| 001 | [Conventions & style](./001-conventions-and-style.md)      | —          | ✅ Done        |
| 002 | [Source repair](./002-source-repair.md)                    | —          | ✅ Done        |
| 003 | [Pilot — the first ten poems](./003-pilot-poems.md)        | 001, 002   | ✅ Done        |
| 004 | [The Anthology — 011–135](./004-the-anthology.md)          | 003        | ✅ Done        |
| 005 | [Introduction & front matter](./005-introduction.md)       | 003, 008§2 | ✅ Done        |
| 006 | [Back matter](./006-back-matter.md)                        | 002        | ✅ Done        |
| 007 | [Release & publication](./007-release.md)                  | 004–006    | 🟨 In progress |
| 008 | [Source repair follow-up](./008-source-repair-followup.md) | 002        | 🟨 In progress |
| 009 | [Re-translate the repaired files](./009-retranslate-repaired-files.md) | 010 | ✅ Done        |
| 010 | [The 147-file source audit](./010-source-audit.md)         | 002        | 🟨 In progress |
| 011 | [Re-translate what 010's second session repaired](./011-retranslate-session-2.md) | 010 | ✅ Done        |
| 012 | [Re-translate what 010's third session repaired](./012-retranslate-session-3.md) | 010 | ✅ Done        |
| 013 | [Re-translate what 010's fourth session repaired](./013-retranslate-session-4.md) | 010 | ✅ Done        |
| 014 | [The six swallowed poems](./014-swallowed-poems.md)        | 010        | ✅ Done        |
| 015 | [Re-translate what 010's fifth session repaired](./015-retranslate-session-5.md) | 010 | ✅ Done        |
| 016 | [A note's closing paragraph, given back](./016-note-afterwords.md) | 010 | ✅ Done        |
| 017 | [Re-translate what 010's sixth session repaired](./017-retranslate-session-6.md) | 010 | ✅ Done        |
| 018 | [Re-translate what 010's seventh session repaired](./018-retranslate-session-7.md) | 010 | ✅ Done        |
| 019 | [Re-translate what 010's eighth session repaired](./019-retranslate-session-8.md) | 010 | ✅ Done        |
| 020 | [Re-translate what 010's ninth session repaired](./020-retranslate-session-9.md) | 010 | ✅ Done        |

## Next up

**Pick the first unfinished line. Update this list when a spec closes.**

1. **[010](./010-source-audit.md)**, next decade: `091`–`100`. Then a new
   re-translation spec for whatever it repairs, before the next decade.
   Repeat through `131`–`141`, then the front and back matter,
   `bibliography`/`glossary-index` (low priority), and `source/README.md`.
2. **[008](./008-source-repair-followup.md)** closes when 010 does. It has no
   work of its own left.
3. **[007](./007-release.md)** last: the end-to-end read of the typeset
   Persian PDF, once no re-translation spec is open.

**All 153 files are translated** — `check_parity` reports `153 file(s) match, 0
skipped`, and the book typesets at 236 pages.

**007 is part-done and tagged `v0.1.0`.** Every `TBD`/`TODO` is settled,
`README.md` and the two licence files exist, and `just build` produces all three
formats clean. What is left in it is one criterion: **the end-to-end read of the
typeset Persian PDF**, and that is what keeps the tag at `v0.1.0`.

**It is not the same read as 010.** 010 reads `source/` against the 228-page
English scan and asks whether the English says what the book says; 007 reads
the Persian output and asks whether it typesets. Different document, different
question, different eyes. An earlier version of this page implied they were one
pass; they are not.

### Why 010 needs its re-translation specs

010's first session fixed three generator faults and changed 22 files in
`source/`; [009](./009-retranslate-repaired-files.md) re-translated them. Its
second session (poems 011–020) changed 40 more, three fixes of it book-wide,
and [011](./011-retranslate-session-2.md) re-translated 39 of them. Its
third (poems 068–090) changed 15, among them five set headings that had run
into the note before them and two markers carrying the wrong number — both in
files 011 had just re-translated for their markers;
[012](./012-retranslate-session-3.md) owns them. Its fourth (poems
091–115) changed 10, [013](./013-retranslate-session-4.md)'s — and found six
poems the generator had never started, each run into the file before it.
The Anthology has 126 poems, not 120; [014](./014-swallowed-poems.md) gave
them back, and with them fixed two poems' titles and two poems' fourth lines.
Its fifth (poems 117–134) changed 9, [015](./015-retranslate-session-5.md)'s,
found a §2 row built on the OCR's spelling rather than the book's, and found
a note's closing paragraph joined to its last gloss in 16 files —
[016](./016-note-afterwords.md). Its sixth (poems 135–175) changed 9,
[017](./017-retranslate-session-6.md)'s, two of them for title lines the
generator miscounted. Its seventh (poems 176–210) changed 5,
[018](./018-retranslate-session-7.md)'s, and found every prose introduction
set as a single paragraph. Its eighth (poems 216–264) changed 7,
[019](./019-retranslate-session-8.md)'s, among them the last set heading
still running into a note. Its ninth (poems 280–344) changed 3,
[020](./020-retranslate-session-9.md)'s, one of them for a quoted poem
flattened into prose. Three of
011's 40 turned `apparatus --check` red, on re-broken verse quotes. **Most of
the 40 fail nothing**: `check_parity` counts blocks, and
a restored word or endnote marker does not change the count. That is the
argument for 010 — and for the marker comparison in its *Tooling* notes.

008 is part-done: **requirement 2 (the Introduction's CJK bleed) was completed
inside 005**, which it was blocking. Its requirement 1 (the 147-file PDF read)
and requirement 3 (`bibliography.md` / `glossary-index.md`) are untouched.

## Recommended order

Not top to bottom. The numbering follows the book; the work should not.

```
002  →  001  →  003  →  004  →  006  →  008§2  →  005  →  007  →  010  →  009  →  010  →  011  →  010  →  012  →  010  →  014  →  013  →  010  →  015  →  016  →  010  →  017  →  010  →  018  →  010  →  019  →  010  →  020
repair  style   pilot   bulk    back   bleed     intro   ship     audit   redo    audit   redo    audit   redo    audit   poems   redo    audit   redo    notes   audit   redo    audit   redo    audit   redo    audit   redo
```

**010 and its re-translation specs (009, 011, 012, 013, 015, 017, 018, 019, 020, …) alternate rather than run in
sequence.** Each decade of the audit
that repairs a file makes that file's Persian stale, so the tail of the roadmap
is a loop: read a chunk, fix the generator, list what broke, re-translate it,
green the checkers, read the next chunk.

**This is the order the work actually ran in, with one correction.** `008§2` is
not where the roadmap put it — see the 008 note below.

- **002 (source repair) first.** `source/` is generated from an OCR of the print
  edition and carries real damage — one poem is filed under the wrong title and
  `notes.md` has marginal letters interleaved into every note. Translating a
  damaged file wastes a translator run and, worse, produces a Persian file that
  looks finished. Repair is cheap now and expensive after 147 files exist.
- **001 (style) before any text.** Register and proper-noun policy are decided
  once and revised never; changing your mind at poem 80 means revising 79 files.
- **003 (pilot) is ten files.** It exists to test the 001 decisions against real
  verse while revising still costs ten files rather than 135.
- **004 (the Anthology) is the bulk** — 125 files, almost all a single chunk.
  Momentum work, and the place the voice actually settles.
- **006 (back matter) early-ish.** Four of its five files are entry lists kept
  verbatim, so it is small and independent, and it unblocks a full `just build`.
- **005 (Introduction) late.** `introduction-1.md` is 66 K characters, about
  fifteen chunks, and the single longest run in the book — the worst possible
  place to discover a style decision does not hold. Its register is modern
  scholarly English, different from the verse, so it wants a settled voice to
  push against rather than to define.

  **This paid off: no `STYLE.md` decision was reversed in 005.** The §2 table
  built over 003 and 004 absorbed the Introduction's much denser proper-noun
  load — 173 corrections in `introduction-1.md` alone — without a single new
  judgement call. The one thing it did surface is that §2.7's Arhat entry,
  marked (suggested), has been overruled in practice 22 files to 0.
- **007 (release) last.** Nothing reaches a reader until the book builds.
- **008 (source repair follow-up) — its requirement 2 is a hard dependency of
  005, not optional alongside it.** This page used to say 008 was "not on the
  critical path" and could be folded in rather than blocked on. That is right
  for its requirement 1 and requirement 3; it was **wrong for requirement 2**.
  The Chinese column had bled into `introduction-1/2/3`, so 12–14% of their
  blocks were damaged before a translator ever saw them, and 005 had to stop
  three files in and go fix the generator. Damaged source does not announce
  itself as a blocker — it looks like a translator problem, and costs a round of
  chunk-ladder runs before you work out that no chunk size helps.

  **Check the source before translating a file group, not after:**

  ```bash
  for f in source/*.md; do
    n=$(grep -o '[぀-ヿ一-鿿]' "$f" | wc -l)
    if [ "$n" -gt 0 ]; then printf '%6d  %s\n' "$n" "$f"; fi
  done
  ```

  Read the count against this table, because **CJK in `source/` is not by itself
  a defect** — some of it is the book:

  | file | now | meaning |
  |---|---:|---|
  | `bibliography.md` | 261 | garbled — 008 requirement 3, deliberately deferred |
  | `glossary-index.md` | 241 | same |
  | `abbreviations.md` | 26 | **correct.** Japanese titles, kept verbatim by 006 |
  | `notes.md` | 2 | correct |
  | `foreword.md` | 1 | the `が` in an OCR-mangled German book title |
  | `introduction-1/2/3` | **0** | was 161 / 43 / 141 before `drop_column()` |

  Three stray ideographic commas (`、`) survive in `introduction-1/3` and
  `preface.md`. They are CJK *punctuation*, outside the range above and outside
  the column bleed — leftovers for requirement 1's file-by-file read, not
  evidence the bleed is back.

  **Requirement 1 was not fold-in work either, and has moved to
  [010](./010-source-audit.md).** Ten files into it, it had found the same
  justified-spacing deletion running on every poem page, a typo rule that
  replaced Daiō with his own student throughout, and a verse-restoring fix that
  two specs recorded as done while it was dead code. 22 files repaired, and a
  re-translation spec ([009](./009-retranslate-repaired-files.md)) behind them.
  That is not something to fold into a follow-up. Requirement 3 genuinely is,
  and nothing is waiting on it.

## Scale

| Group                                              | Files | Chars   | Chunks |
|----------------------------------------------------|------:|--------:|-------:|
| Anthology (`001`–`141`): 126 poems, 15 prose intros |   141 | 153,504 |    143 |
| Introduction (`introduction-1` … `-4`)              |     4 | 118,094 |     28 |
| Front matter (`plates`, `foreword`, `preface`)      |     3 |  15,773 |      5 |
| Back matter (`abbreviations`, `notes`, `bibliography`, `index-of-poems`, `glossary-index`) | 5 | 35,523 | 11 |
| **Total**                                           | **153** | **322,894** | **187** |

Counts are from `source/` after 008's `drop_column()`, which removed 1,229
characters of Chinese column from the Introduction, re-measured after 014. Only **twelve files exceed
one chunk**, and only two of those are poems (`001.md`, `024.md`); the other 139
poem files are a single chunk apiece.

**4,500 is the translator's default, not the right size.** Spec 005 found the
Advanced/Classic fallback happens per *chunk*, so the size is chosen per file on
block parity: `introduction-2.md` wanted 4500, `introduction-3.md` 2250,
`introduction-1.md` 900, `preface.md` 900, `009.md` 300. Budget long files by
the ladder, not by dividing chars by 4,500 — `introduction-1.md` shipped at 900,
about 73 chunks, not the 15 this table implies.

97 of the 141 Anthology files carry a `## Notes` section.

## Definition of done (every spec)

- [ ] Every item in the spec's **Acceptance criteria** is checked and true.
- [ ] `just check` passes.
- [ ] The typeset PDF was read for the files touched — not just the Markdown.
      Bidi, ZWNJ and line-break faults are obvious typeset and invisible in a diff.
- [ ] Status table above updated; work committed.
