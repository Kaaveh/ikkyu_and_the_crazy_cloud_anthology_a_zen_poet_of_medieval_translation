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
implementation, where it blocked those three files, and then done here.** The
Chinese column had bled into them, so the text the translator was handed was
not yet the book. The other four files have none of it and did not wait.

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
- [x] `introduction-2.md`
- [x] `introduction-4.md`
- [x] `introduction-3.md`
- [x] `introduction-1.md`

Ordered small to large on purpose: the two long files are last, so the short ones
have already shaken out any problem with prose under `--raw` before fifteen chunks
are committed to it.

## Acceptance criteria

- [x] All seven at `status: reviewed`.
- [x] `just check` passes with all seven compared — and with the whole book:
      **`parity: 147 file(s) match, 0 skipped`**.
- [x] The four image paths in `fa/plates.md` are byte-identical to `source/` and all
      four files exist in `images/`. Verified by diff, not assumed.
- [x] The chunk seams in `introduction-1.md` and `introduction-3.md` were read, not
      just counted. This is where the spec paid off: block *counts* alone would
      have passed the `introduction-3.md` runs at 900 and 400, and reading them
      is what found `کنایه` for `تلمیح`. Counting found the two dropped blocks
      at 4500; reading found the terminology.
- [x] ~~Dates and page references are still Latin-digit.~~ **Fails, and cannot
      be met by config.** The normalizer is clean; the model converts them
      first. See the implementation note — a decision is owed.
- [x] All seven read in the typeset PDF, at **231 pages** once the Introduction
      was in it. No bidi fault: `(Mori)`, `(Masaki Museum)`, `(Hsü-t’ang)`,
      `(Kyōunshū)`, `(Ikkyū)`, `(Chūsei Zenka no Shisō)`, `(Iwanami Shoten)`,
      `(René de Berval)`, `(Kato Shuichi)` all set left-to-right inside the
      Persian. §2.2's apostrophe survives typesetting (`شیو-ت’انگ`). Both poems
      under Plate 4 hold their line breaks — no reflow, no wrapped line.
- [x] **Added:** the PDF builds at all. It did not before this spec — see the
      `fa/images` note below.

## Out of scope

The Anthology. Back matter. Release.

## Implementation notes

### All seven done. Three of them needed 008 requirement 2 doing first.

`parity: 147 file(s) match, 0 skipped` — the book is fully translated.

Four files went straight through. `introduction-1/2/3` did not: the Chinese
column had bled into them, which is **008 requirement 2**, written down long
before this spec and unfixed. It is fixed now, in `drop_column()`; 008 carries
the detail, including the correction that the requirement's own diagnosis was
half wrong. This spec should have listed 002/008 as a dependency from the
start.

What the bleed looked like in `source/introduction-2.md`:

```
Po Chü-i asked Master Bird Nest, ““What is the broad FaJee5 it)BSBEAO
meaning of Buddhism?” Bird Nest answered, “Do ROP EEK. no evil, do much
good.”>8 Po Chü-i said, “But a Ay mE, RES three-year-old child could
understand a teaching like J AAL Smale that.””
```

and after `drop_column()`:

```
Po Chü-i asked Master Bird Nest, ““What is the broad meaning of Buddhism?”
Bird Nest answered, “Do no evil, do much good.” Po Chü-i said, “But a
three-year-old child could understand a teaching like that.””
```

Damaged blocks before and after, over the whole front matter:

| file | blocks | damaged before | after |
|---|---:|---:|---:|
| `plates.md` | 24 | 0 | 0 |
| `preface.md` | 9 | 0 | 0 |
| `introduction-4.md` | 7 | 0 | 0 |
| `foreword.md` | 10 | 1 | 1 |
| `introduction-2.md` | 16 → 21 | 2 | **0** |
| `introduction-1.md` | 104 → 106 | 13 | **0** |
| `introduction-3.md` | 61 → 62 | 9 | **0** |

The block counts rise because cutting the column lets paragraphs separate that
had been welded through it.

`source/introduction-2.md` also carried the book's only running page header,
`35 INTRODUCTION`, welded into a sentence a page break had split. It survived
because `build_introduction()` fetched that one page without
`strip_page_footer` — the only such call in the function. Also fixed.

### The adapter grew CJK protection, and the change was reverted

Worth recording because it was the wrong fix for a real symptom, and it took a
measurement to see that.

The model deletes the Chinese characters: 43 in, 32 out on `introduction-2.md`,
one block losing all six of its runs. Carrying them as `strip`/`restore` tokens
is what the adapter already does for headings, so that was tried. **It does not
work — 34 sentinels in, 20 out.** A heading sentinel survives because a heading
is its own line; these sit inline in dense prose and go the same way the
characters did.

It was reverted for the better reason too: the premise was wrong. That CJK is
not content to protect, it is column bleed, and §2.8's Lan-t'san precedent —
*the Persian does not follow OCR damage* — means the model deleting it was the
right outcome. Protecting it would have laundered the bleed into the edition
and hidden the generator bug. The fix belonged upstream, which is where it went.

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

**On damaged input the ladder stops helping.** Before the source was repaired,
`introduction-2.md` at 900 gave good Persian and dropped a block; at 400 it
kept all 16 and turned seven paragraphs Classic. No chunk size fixes damaged
source — that run is what sent this spec to 008.

**After the repair, every file still needed its own size, and for a different
reason each time.** Block parity is the gate, so the choice is made on it:

| file | chunk | blocks | what the other sizes did |
|---|---|---|---|
| `introduction-2.md` | 4500 | 20 → 21 | one split, merged by hand |
| `introduction-3.md` | 2250 | 62 → 63 | 4500 **dropped two blocks**; 900 and 400 kept the count but said `کنایه` for `تلمیح` 15 and 29 times |
| `introduction-1.md` | 900 | 106 → 106 | 2250 dropped one, 4500 dropped five |

**A split block is a better failure than a dropped one.** A split is merged by
hand in one edit; a dropped block would have to be written by hand, which
`CLAUDE.md` does not sanction. So where no size is perfect, take the one that
splits.

### The zero-ezafe threshold over-flags, and `introduction-1.md` is where it shows

The measure this spec added to `CLAUDE.md` called 23 paragraphs of
`introduction-1.md` suspect — 12,773 characters. **On reading them they are
fine**: ordinary declarative Persian with no ezafe construction to make.

```
ایک‌کیو خود را «ابر دیوانه» می‌نامید، لقبی که بار معنایی غنی دارد.
```

Accurate, idiomatic, and zero ezafe. That is spec 004's `099.md` finding at
scale, and it also came back **byte-identical from the 2250 and the 4500 run**,
which is `CLAUDE.md`'s "per-input and deterministic" confirmed at chunk level.

**Spec 004's verb-prefix test is the one that settles it**: 311 ZWNJ against 44
spaced. Genuine Classic — `preface.md`'s second chunk, `introduction-3.md` at
900 — looks quite different: dropped subjects, a doubled word
(«ابهامات و ابهامات»), Latin names left standing in the Persian, and the wrong
term for the chapter's own subject. `CLAUDE.md` now says the ezafe run is a
prompt to read, not a verdict.

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

### Requirement 3 has exactly one real case in the whole book

The citations read "poems nos. 639, 640, 641", not "poem 639", so a naive scan
under-reports them. `introduction-1.md` cites **17** poems that exist as
numbered files and `introduction-3.md` cites **3** — but all of them **by
number only**. A number is not a rendering, so there is nothing to diverge.

Checking every Anthology poem title against the Introduction turns up **one**
that appears in both: poem 494, *Spreading Horse Dung to Cultivate the Mottled
Bamboo*, in `101.md` and in `introduction-3.md` (which prints it over its
companion, poem 493, not in Arntzen's selection). **The two renderings had
diverged:**

| | |
|---|---|
| `fa/101.md` | پخش کردن **فضولات** اسب برای پرورش بامبوی **خال‌دار** |
| `fa/introduction-3.md` | پخش کردن **سرگین** اسب برای پرورش بامبوی **ابلق** |

Aligned to the Anthology's, which is what the requirement asks for and is also
the form in the book's table of contents. It turned out to be the internally
consistent choice as well: `introduction-3.md`'s own commentary already glosses
the phrase as `بامبوی خال‌دار (mottled bamboo)` further down the same page.

`plates.md` cites poem 130 and its caption's «خودارزیابی» already matched
`fa/047.md`'s heading.

**Neither long file contains a single hard line break** — the quoted poems sit
inside prose paragraphs — so requirement 2's break machinery was never
load-bearing here, contrary to what the spec expected.

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

Totals: **95 corrections in `introduction-3.md`** and **173 in
`introduction-1.md`**, nearly all found by the sweep rather than by eye.

**`آرهات` has overruled §2.7's `اَرهَت` in practice.** §2.7 marks Arhat
(suggested) and says a suggestion is cheap to overrule until it is in many
files. It is now in 22, all `آرهات`, none `اَرهَت`. `introduction-1.md` follows
the book rather than the table, and **§2.7 should be updated to record that** —
the table is meant to be where a translator looks before inventing a form, and
right now it would mislead.

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
