# 005 — Introduction & front matter

**7 files · 134,947 chars · ~33 chunks · 42% of the book**

## Context

Arntzen's apparatus: a foreword by Shūichi Katō, her preface, and a four-part
introduction that is a piece of scholarship in its own right — Ikkyū's life and the
Muromachi period, the dialectic of non-duality, the workings of allusion in his
verse, and a note on the text.

Two files dominate. `introduction-1.md` is 66 K characters, about fifteen chunks, and
is by far the longest run in the project; `introduction-3.md` is 40 K and about nine.
Everything else in the book is one or two chunks. These two are the only places where
the translator's chunk-rejoining is genuinely load-bearing.

This comes late deliberately. The register is modern scholarly English — dates,
citations, institutional history — and differs from the verse it introduces. A
settled voice from 003 and 004 gives it something to push against. Discovering a
style decision does not hold, fifteen chunks into the longest file in the book, is
the failure this ordering exists to prevent.

## Goal

Seven files at `status: reviewed`, `just check` green, the PDF read.

## Dependencies

003 at minimum, so `STYLE.md` is settled. Best after 004, so the poems the
Introduction quotes are already rendered.

## Requirements

1. **Budget `introduction-1.md` as a single long run** — about fifteen chunks, six to
   eight minutes of browser time, and nothing else touching the Chrome profile while
   it runs. Same for `introduction-3.md` at nine.

2. **Check the chunk seams.** `split_chunks` is lossless and `_rejoin` re-appends
   each chunk's own separator, so the paragraph structure should survive — but the
   failure mode this machinery exists to fix (two paragraphs silently welded at every
   seam) *only shows on inputs long enough to split*, and these are the only two such
   files in the book. `check_parity` catches a lost block by count; look at the
   Persian around each seam anyway, because a *merged* pair of paragraphs and a
   *dropped* one are the same count delta in opposite directions.

3. **The Introduction quotes poems that also appear in the Anthology.** Where a poem
   is cited both here and as a numbered file, the two renderings should not diverge.
   This is the strongest argument for running this spec after 004: the Anthology
   rendering exists and can be reused. Nothing enforces it — see the "no glossary
   checker" note in `000-overview.md`.

4. **Page references stay Latin-digit.** `latin_digits = false` in `pyproject.toml`
   exists for this file group above all: the Introduction is dense with dates
   (1394–1481, 1467, 1338-1568) and page references into the print edition. Confirm
   the normalizer left them alone rather than assuming it did.

5. **`plates.md` carries the only four image links in the book.**

   ```
   ![Plate 1: Calligraphy: "Do No Evil, Do Much Good"](images/plate_1_calligraphy.png)
   ```

   `CLAUDE.md` records that the Advanced model returns these intact, path and all,
   measured twice — which is why this book's adapter carries no image machinery at
   all, unlike Lin-chi's. **Verify rather than assume**: after `restore`, confirm all
   four paths are byte-identical to `source/plates.md` and that each names a file that
   exists in `images/`. If they do not survive, that is a finding that changes the
   adapter, not a file to patch by hand.

   `plates.md` also contains verse — Ikkyū's poem and Mori's poem under Plate 4 —
   with hard line breaks, inside what is otherwise a caption file.

6. **The h1 titles of all seven files come from `pyproject.toml`, not the
   translator.** `[tool.book.titles]` maps each named file to its Persian heading and
   `apparatus.py` re-emits it, so `introduction-2.md` will be headed
   `دیالکتیکِ نادوگانگی` whatever the model returns. To change one of these, edit
   `pyproject.toml` — editing `fa/` is undone by the next `restore`.

   The `Plate N:` labels in `plates.md` are re-emitted the same way (`تصویر ۱:`);
   the caption title after the label is prose and is the translator's.

## Files

| file | chars | chunks | notes |
|---|---:|---:|---|
| `plates.md` | 2,204 | 1 | Four image links; verse under Plate 4; `Plate N:` labels |
| `foreword.md` | 7,521 | 2 | By Shūichi Katō, not Arntzen — a third voice |
| `preface.md` | 6,047 | 2 | |
| `introduction-1.md` | 65,929 | ~15 | **The longest run in the project.** Its own session |
| `introduction-2.md` | 7,862 | 2 | "Dialectic of Non-Duality" — the most abstract prose in the book |
| `introduction-3.md` | 39,712 | ~9 | "Allusion". Quotes many poems; see requirement 3 |
| `introduction-4.md` | 5,672 | 2 | "A Note on the Text and Its Organization" |

- [ ] `plates.md`
- [ ] `foreword.md`
- [ ] `preface.md`
- [ ] `introduction-2.md`
- [ ] `introduction-4.md`
- [ ] `introduction-3.md`
- [ ] `introduction-1.md`

Ordered small to large on purpose: the two long files are last, so the short ones
have already shaken out any problem with prose under `--raw` before fifteen chunks
are committed to it.

## Acceptance criteria

- [ ] All seven at `status: reviewed`.
- [ ] `just check` passes with all seven compared.
- [ ] The four image paths in `fa/plates.md` are byte-identical to `source/` and all
      four files exist in `images/`.
- [ ] The chunk seams in `introduction-1.md` and `introduction-3.md` were read, not
      just counted.
- [ ] Dates and page references are still Latin-digit.
- [ ] All seven read in the typeset PDF — especially `introduction-1.md`, where a
      bidi fault around an embedded Latin citation is both likely and invisible in
      the Markdown.

## Out of scope

The Anthology. Back matter. Release.

## Implementation notes

_(filled in during implementation)_
