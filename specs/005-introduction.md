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

**And 008 requirement 2, for `introduction-1/2/3` — added during
implementation, where it blocked those three files.** The Chinese column bled
into them and the English wraps around it, so the text the translator is handed
is not yet the book. The other four files in this spec have none of it and did
not need to wait.

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

- [x] `plates.md`
- [x] `foreword.md`
- [x] `preface.md`
- [ ] `introduction-2.md` — **blocked on 008 requirement 2**
- [x] `introduction-4.md`
- [ ] `introduction-3.md` — **blocked on 008 requirement 2**
- [ ] `introduction-1.md` — **blocked on 008 requirement 2**

Ordered small to large on purpose: the two long files are last, so the short ones
have already shaken out any problem with prose under `--raw` before fifteen chunks
are committed to it.

## Acceptance criteria

- [~] All seven at `status: reviewed`. **Four of seven**; `introduction-1/2/3`
      are blocked on 008 requirement 2.
- [x] `just check` passes with all seven compared. Green with the four
      compared; the other three are still `untranslated` and are skipped.
- [x] The four image paths in `fa/plates.md` are byte-identical to `source/` and all
      four files exist in `images/`. Verified by diff, not assumed.
- [ ] The chunk seams in `introduction-1.md` and `introduction-3.md` were read, not
      just counted. **Not reached.** The seams in `preface.md` and
      `introduction-2.md` were read and are where the per-chunk fallback was
      found, so the requirement earned its place before the files it names.
- [x] ~~Dates and page references are still Latin-digit.~~ **Fails, and cannot
      be met by config.** The normalizer is clean; the model converts them
      first. See the implementation note — a decision is owed.
- [~] All seven read in the typeset PDF. **The four that exist, read at 201
      pages.** No bidi fault: `(Mori)`, `(Masaki Museum)`, `(Hsü-t’ang)`,
      `(Kyōunshū)`, `(Ikkyū)`, `(Chūsei Zenka no Shisō)`, `(Iwanami Shoten)`,
      `(René de Berval)`, `(Kato Shuichi)` all set left-to-right inside the
      Persian. §2.2's apostrophe survives typesetting (`شیو-ت’انگ`). Both poems
      under Plate 4 hold their line breaks — no reflow, no wrapped line.
- [x] **Added:** the PDF builds at all. It did not before this spec — see the
      `fa/images` note below.

## Out of scope

The Anthology. Back matter. Release.

## Implementation notes

### Four of seven done. The three Introduction files are blocked on 008.

`plates.md`, `foreword.md`, `preface.md` and `introduction-4.md` are at
`status: reviewed` and `just check` is green. `introduction-1/2/3` are not
translatable yet, and the reason is already written down in
**008 requirement 2** — the Chinese column bled into them, because
`build_introduction()` never runs lines through `clean_translation_line()`.
This spec does not list 002/008 as a dependency, and it should.

What the bleed looks like in `source/introduction-2.md`:

```
Po Chü-i asked Master Bird Nest, ““What is the broad FaJee5 it)BSBEAO
meaning of Buddhism?” Bird Nest answered, “Do ROP EEK. no evil, do much
good.”>8 Po Chü-i said, “But a Ay mE, RES three-year-old child could
understand a teaching like J AAL Smale that.””
```

The Chinese is interleaved *word by word* into the English sentence, together
with the OCR's failed attempts at it. Measured over the front matter:

| file | blocks | damaged | CJK chars | garbage runs |
|---|---:|---:|---:|---:|
| `plates.md` | 24 | 0 | 0 | 0 |
| `preface.md` | 9 | 0 | 0 | 0 |
| `introduction-4.md` | 7 | 0 | 0 | 0 |
| `foreword.md` | 10 | 1 | 1 | 0 |
| `introduction-2.md` | 16 | **2** | 43 | 4 |
| `introduction-1.md` | 104 | **13** | 161 | 9 |
| `introduction-3.md` | 61 | **9** | 141 | 8 |

12–14% of blocks in the three files. That is low enough to look survivable and
is not: the damage is *upstream of the translator*, and it produced three
distinct failures on `introduction-2.md` alone — a Classic fallback on the
damaged block, a dropped block, and dropped characters. Chasing them down the
chunk ladder trades one for another (see below). The four clean files went
through first time.

**`source/introduction-2.md` also carries a running page header**, `35
INTRODUCTION`, welded into the middle of a sentence that a page break split.
It is the only one in the book — worth a scan in 008 rather than a rule.

### The adapter was changed to protect the CJK, and the change was reverted

Reverted, not kept, for two reasons. The sentinel does not survive: 34 in, 20
out, and `restore` rightly refuses such a draft — the heading sentinels work
because a heading is its own line, and these sit inline in dense prose. And
the premise was wrong anyway. This CJK is not content to protect; it is
debris, and §2.8's Lan-t'san precedent — *the Persian does not follow OCR
damage* — says the model deleting it is the better outcome. Protecting it
would have laundered the bleed into the edition. The fix belongs in the
generator, which is exactly what 008 requirement 2 says.

### The Classic fallback happens **per chunk**, not per file

This contradicts `CLAUDE.md` ("the two do not mix inside a file") and it is
the spec-004 detectors' blind spot. `preface.md` at the default 4500:

| chunk | source paragraphs | ezafe per 1k chars |
|---|---|---|
| 1 (3,932 ch) | 1–2 | 6.3, 7.9 |
| 2 (2,111 ch) | 3–8 | **0.0, 0.0, 0.0, 0.0, 0.0, 0.0** |

Both of 004's tests pass this file. Whole-file `grep -c ِ` is 25; the verb
prefix test is 25 ZWNJ against 0 spaced. The prose is where it shows — "Good
fortune has blessed me with many fine teachers" came back as
«خوشبختانه در این مسیر معلمان خوب زیادی را به من عطا کرده است», subject
dropped. **Measure ezafe per paragraph, not per file**: a run of paragraphs at
exactly 0 over more than ~1,500 characters is the signal. A single 0 paragraph
between healthy ones is not — `foreword.md` has one and is fine, which is
004's `099.md` finding again.

`preface.md` at `--chunk 900` came back Advanced throughout, and that also
dissolved a merged block the 4500 run had produced.

**On damaged input the ladder stops helping.** `introduction-2.md`: 900 gives
good Persian but drops a block; 400 keeps all 16 blocks and turns seven
paragraphs Classic. There is no chunk size that fixes damaged source.

### Requirement 4 is half-met, and the half that fails is not the normalizer

The normalizer is innocent: `latin_digits = false` works and `normalize
--check` is clean on all 147 files. **The model converts the digits itself,
before any checker sees them** — `1960s` → «دههٔ ۱۹۶۰», `page 18` →
«صفحه ۱۸», `(Bellingham, 1973)` → «(بلینگهام، ۱۹۷۳)». So the acceptance
criterion "dates and page references are still Latin-digit" is **not met**,
and no config change would have met it.

Left as translated rather than patched, because the book is already mixed and
deliberately so: `apparatus.py` itself renders poem numbers through
`to_persian_digits`, so every Anthology heading is `# شعر ۱۳۰`, and
`fa/notes.md` carries 705 Latin digits beside 505 Persian. Reversing it in
`fa/preface.md` alone would be 126 hand-edits toward a consistency the rest of
the book does not have. **A decision is owed here** — either requirement 4 is
narrowed to say the normalizer must not convert, which is what it actually
tests, or the book picks one script for digits and that belongs in `STYLE.md`
and in a checker, not in one spec's acceptance list.

### Requirement 3: the cross-reference list

The citations read "poems nos. 639, 640, 641", not "poem 639", so a naive
scan under-reports them. Resolved against the numbered files:

- `introduction-1.md` cites **17**: 8, 33, 89, 90, 91, 93, 180, 210, 293, 531,
  532, 541, 542, 639, 640, 641, 647 → `003, 009, 029, 030, 031, 032, 061, 068,
  084, 104, 105, 112, 113, 122, 123, 124, 126`.
- `introduction-3.md` cites **3**: 639, 640, 641. It also cites 206 and 493,
  which are not in Arntzen's selection — expected, not a defect.
- `plates.md` cites poem 130, and its caption's «خودارزیابی» already matches
  `fa/047.md`'s heading. Checked and consistent.

Neither long file contains a single hard line break, so the quoted poems are
welded into the surrounding prose paragraph. Requirement 2's machinery is
therefore not load-bearing here, and requirement 3 is harder than it reads:
there is no line structure in the Introduction's copy of a poem to compare
against the Anthology's.

### §2

The pass was mechanical enough to script. `tools/`-external, in the session
scratchpad: reduce both the draft and STYLE.md's 98 canonical forms to a
skeleton — drop the §2.2 apostrophe, the separators and the harakat, fold
§2.3's `یو` onto `و`, `آ` onto `ا`, `ئ` onto `ی` — and anything matching a
canonical skeleton but not its text is a near-miss. It does not catch a
dropped letter, so `ایکیو` for `ایک‌کیو` is still handled by name; that one is
also the single commonest correction in this spec, 41 occurrences in the
foreword alone.

Applied: `Ikkyū`, `Hsü-t'ang`, `Po Chü-i`, `Niao K'o` (new, §2.2 →
`نیائو ک’و`), `Hōnen`, `Kyōunshū` (§2.8's `کیوئونشو`, first appearance in
`fa/`; the model spelled it two ways in one file), `Ichijoji`, `Jōdo Shinshū`,
and two stray U+200B.

**One whole-book sweep**, on 004's own precedent that the table has to be
swept over everything: `fa/085.md` had `تائو یوآن-مینگ`, and §2.2 cites that
exact `Tao`/`T'ao` collision as its worked example. Now `ت’ائو یوآن-مینگ`.

**The same sweep reports 53 more near-misses in 004's committed files** —
`کوان` for `کوآن` (12), `ویمالاکی‌رتی` (8), `مایتریا` (6), `چ’ینگ-سو` (5).
Left alone: they are a closed spec's files and the call is the book's owner's,
not this spec's.

### The PDF did not build, and nothing before this spec would have noticed

`plates.md` is the first chapter in the book with images. `_quarto.yml` lists
chapters as `fa/plates.md`, so Quarto resolves `images/plate_1_calligraphy.png`
relative to `fa/`, and lualatex stopped on `fa/images/plate_1_calligraphy.png`
not found. Fixed with a `fa/images` symlink rather than a rewritten path:
requirement 5 wants those four paths byte-identical to `source/`, and `restore`
would put them back regardless.

### Requirement 5 — verified, not assumed

All four image paths in `fa/plates.md` are byte-identical to `source/` and all
four PNGs exist in `images/`. `CLAUDE.md`'s measurement holds and the adapter
still needs no image machinery. `restore` took `plates.md` first try, verse
under Plate 4 included — the one hand repair it needed was `*شعر موری:*` glued
to the end of the last verse line, which is 004's category-2 repair.
