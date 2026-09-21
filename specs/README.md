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
| 004 | [The Anthology — 011–135](./004-the-anthology.md)          | 003        | ⬜ Not started |
| 005 | [Introduction & front matter](./005-introduction.md)       | 003        | ⬜ Not started |
| 006 | [Back matter](./006-back-matter.md)                        | 002        | ⬜ Not started |
| 007 | [Release & publication](./007-release.md)                  | 004–006    | ⬜ Not started |
| 008 | [Source repair follow-up](./008-source-repair-followup.md) | 002        | ⬜ Not started |

## Recommended order

Not top to bottom. The numbering follows the book; the work should not.

```
002  →  001  →  003  →  004  →  006  →  005  →  007
repair  style   pilot   bulk    back   intro   ship
```

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
- **007 (release) last.** Nothing reaches a reader until the book builds.
- **008 (source repair follow-up) whenever there's room.** 002's leftover
  checklist — the 147-file PDF read, the Introduction's CJK bleed, and the two
  low-priority back-matter files. Not on the critical path to 003 or 004;
  fold it in alongside 005/006 rather than blocking on it.

## Scale

| Group                                              | Files | Chars   | Chunks |
|----------------------------------------------------|------:|--------:|-------:|
| Anthology (`001`–`135`): 120 poems, 15 prose intros |   135 | 152,971 |    137 |
| Introduction (`introduction-1` … `-4`)              |     4 | 119,175 |     28 |
| Front matter (`plates`, `foreword`, `preface`)      |     3 |  15,772 |      5 |
| Back matter (`abbreviations`, `notes`, `bibliography`, `index-of-poems`, `glossary-index`) | 5 | 35,665 | 11 |
| **Total**                                           | **147** | **323,583** | **181** |

Chunks at the translator's 4,500-character limit, ~11 s each. Only **twelve files
exceed one chunk**, and only two of those are poems (`001.md`, `024.md`). The other
133 poem files are a single chunk apiece.

93 of the 135 Anthology files carry a `## Notes` section.

## Definition of done (every spec)

- [ ] Every item in the spec's **Acceptance criteria** is checked and true.
- [ ] `just check` passes.
- [ ] The typeset PDF was read for the files touched — not just the Markdown.
      Bidi, ZWNJ and line-break faults are obvious typeset and invisible in a diff.
- [ ] Status table above updated; work committed.
