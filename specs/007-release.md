# 007 — Release & publication

## Context

147 files translated is not a book. This spec turns the tree into HTML, PDF and EPUB
that someone can read, settles the decisions that were deliberately left as `TBD`
because they are translation calls rather than defaults, and tags the first version.

The build has never been run against a full `fa/`. Everything below is expected to
surface problems that only appear at book scale — a 135-chapter sidebar, a table of
contents in Persian, bidi faults in files nobody read side by side.

## Goal

`just build` producing three formats from a complete `fa/`, the PDF read end to end,
and a tagged release.

## Dependencies

004, 005, 006. Every file at `status: reviewed`.

## Requirements

1. **Settle the three `TBD` markers in `_quarto.yml`.** They are marked TBD because
   they are translation decisions, not defaults to keep:

   ```yaml
   title:    "ایک‌کیو و گلچین ابر دیوانه"   # TBD
   subtitle: "شاعری ذن از ژاپن سدهٔ میانه"   # TBD
   author:   "کاوه"                          # TBD: how you want to be credited
   ```

   The title is the same decision as any recurring term and should be argued the same
   way. Note that `index.md` currently gives the English original and Arntzen's
   credit; whatever the title becomes, the two must agree.

   Also settle the two `part:` titles — `درآمد` and
   `برگردان‌هایی از گلچین ابر دیوانه` — which are not marked TBD but were written
   before any translation existed.

2. **Fill the `<!-- TODO -->` in `index.md`.** A short note on the book, the source
   text, and the method — including, plainly, that the Persian was produced with
   machine translation and what that means. The reader is entitled to know how the
   book they are reading was made.

   `index.md` is also where the "what the page numbers refer to" note from spec 006
   may end up.

3. **Credit and licence.** This repo has no `README.md` and no licence files, unlike
   Lin-chi (`LICENSE-CODE`, `LICENSE-TEXT`, `CONTRIBUTING.md`). Decide whether it
   needs them before anything is published. The constraint from `000-overview.md`
   still holds absolutely: **the English source is licensed to the maintainer for
   producing this translation and nothing else**, and `source/`, the monolith, the
   raw OCR and the PDF stay gitignored. A release must not carry them — check the
   tarball, not just `.gitignore`.

4. **Build all three formats.** `just build`. Then, specifically:

   - **PDF.** Confirm LuaLaTeX actually ran. Under XeLaTeX, pandoc picks babel with
     `bidi=default`, which reverses Latin-script runs embedded in Persian — and this
     book's notes are full of them. The reasoning is in `tex/preamble.tex`; the
     symptom is a citation like `T 47, p. 497a` rendering backwards.
   - **EPUB.** `page-progression-direction: rtl` is set explicitly because pandoc
     does not derive it from `dir`. Open the file in a reader and confirm the spine
     goes right to left.
   - **HTML.** 135 chapters under one part. `collapse-level: 1` is set for this;
     check the sidebar is actually usable rather than merely configured.

5. **Read the typeset PDF end to end.** This is the acceptance test the Markdown
   cannot substitute for. Looking specifically for:
   - verse that reflowed into prose, or a quatrain whose lines wrap to eight;
   - bidi damage around Latin and CJK runs — worst in `notes.md`,
     `glossary-index.md`, `index-of-poems.md` and `introduction-1.md`;
   - ZWNJ faults, which are invisible in a diff and obvious in a typeset line;
   - the four plate images: present, right side up, captioned in Persian.

6. **`just check` green, including the bidi report.** `normalize` reports bidi
   override characters and never auto-fixes them, by design — so `just fix` can leave
   `just check` failing and a human has to look at each one. None should reach a
   release.

7. **Bump `book-version`** in `_quarto.yml` (currently `نسخهٔ ۰.۰.۱`) and tag.

## Acceptance criteria

- [x] No `TBD` or `TODO` marker left in `_quarto.yml` or `index.md`.
- [x] `just check` passes: 147 files compared by `check_parity` and
      `apparatus --check`, none skipped, no bidi findings.
- [x] `just build` produces HTML, PDF and EPUB with no errors.
- [x] The PDF was built by LuaLaTeX and a Latin citation inside a Persian sentence
      reads forwards.
- [x] The EPUB spine is right-to-left — `page-progression-direction="rtl"` on
      `<spine>` in `content.opf` — every chapter is `dir="rtl"`, EPUBCheck
      3.3 reports nothing, and the book was opened in epub.js. See *Closing*
      below.
- [x] The whole PDF read end to end — every page, 2026-09-25. See *The
      typeset read* below. Four files it found go to
      [027](./027-retranslate-typeset-read.md), which the `v1.0.0` tag waits on.
- [x] The release artifact contains no `source/`, no monolith, no raw OCR, no PDF of
      the original.
- [x] `book-version` bumped; tag pushed — `v0.1.0`, then `v1.0.0` once 027
      closed.

## Out of scope

Translating or revising text. A second edition.

## Implementation notes

### The three `TBD`s were not really three decisions (requirement 1)

The title argued itself. **`گلچین ابر دیوانه` is what the translation already
says, 165 times**, so the only live option was to change 165 files to match a
new cover. `STYLE.md` §2.8 settles `Crazy Cloud` → `ابر دیوانه` on its own
grounds; the cover follows the book, not the other way round. The subtitle
tracks the English one and needed nothing. Both part titles — `درآمد` and
`برگردان‌هایی از گلچین ابر دیوانه` — were written before any translation existed
and turn out to agree with it; kept.

The one real call was the credit, and the old value was wrong in kind rather
than in spelling: **the English book is Arntzen's.** `author` is now a list —
`سونیا آرنتزن` and `برگردان: کاوه` — which Quarto renders side by side on the
title page and pandoc emits as two `dc:creator` entries in the EPUB.

**A build warning nobody had looked at:** `repo-actions: [edit, issue]` with no
`repo-url`. Quarto warns and silently drops the links, so the
«ویرایش این صفحه در گیت‌هاب» affordance the README advertises did not exist.
One line.

### The PDF's CJK is a smaller problem than 006 handed over

Spec 006 left the blank-CJK-glyph fault to this spec as "book-wide, not back
matter's", citing 111 CJK characters in `introduction-1.md` and 107 in
`introduction-3.md`. **That was measured before 008 §2's `drop_column()`**,
which removed the Chinese column bleed from all three Introduction files. The
count today:

| file | CJK chars | what they are |
|---|---:|---|
| `bibliography.md` | 267 | OCR garbage, kept verbatim by 006 |
| `glossary-index.md` | 245 | same |
| `abbreviations.md` | 26 | real — five Japanese book titles |
| everything else | 0 | |

So vendoring a multi-megabyte CJK font buys 26 characters, every one of which
already appears in romanization immediately to its left:
`*Kyōunshū Zenshaku* (狂雲集全釈)` typesets as `Kyōunshū Zenshaku ( )`. **Not
done, deliberately.** The upgrade path is unchanged if it ever becomes worth it
— a font under a redistributable licence into `fonts/`, never a system font,
which would work on one machine and produce the same gaps everywhere else.

Page 209 rendered to PNG is the evidence, and it shows a **second fault** that
006 predicted in the glossary and that also hits `abbreviations.md`: these
entries are Latin-dominant lines inside an RTL paragraph, so the neutral full
stop that ends one lands at the other end — `.Shoten, 1972`, `.KZ:`. Fixing it
means putting the entry lists in an LTR context, which in Markdown is a `:::`
div, which changes the block count and breaks `check_parity` for those files.
Not a v0.1.0 change. Both faults are recorded in `README.md` under *Known
limitation* so a reader meets them as documented rather than as damage.

### What was verified, and what a human still has to do

`just check`: 147/147 on all three checkers, no bidi findings. `just build`:
exit 0, no warnings, three formats. The PDF is 230 pages, `Producer:
LuaTeX-1.24.0` — LuaLaTeX ran, and `pdftotext` returns `p. 117`, `pp. 207-9`,
`Blue Cliff Record` forwards, which is what that engine choice was for. All
four plates are embedded (pages 12, 14, 15, 16). `git archive HEAD` is 189
entries with zero matches for `source/`, `*.raw.md` or `*.pdf`.

**Requirement 5 is not met and cannot be met by any of the above.** Four pages
were rendered and read — the title page, a plate, a poem with notes (52, page
80: four verse lines intact, `Ch’uan Teng Lu` and `fūryū` forwards), and the
abbreviations page. That is a spot check, not the read. **This is why the
release is `v0.1.0`**: the end-to-end read stays open, along with 008
requirement 1, which is the same read from the other side.

### The typeset read (requirement 5)

Every page, read as rendered: the front matter, the Introduction and the
back matter one page at a time, the Anthology two pages to an image. Before
that, three sweeps over the whole book, which point the eye rather than
replace it:

- **Missing glyphs** from the LuaLaTeX log: CJK only, the known limitation.
  No Persian or Latin glyph is missing.
- **Reversed Latin**: every Latin word in `pdftotext` output checked against
  `fa/`. None reversed; the only unknowns were words hyphenated across a line.
- **Quotation marks** in `fa/`: see 027.

**Fixed in the build, so `fa/` is untouched.** Each one is commented at its
fix.

| fault | where | fix |
|---|---|---|
| Plate 1 ran off its page, lost its caption and left page 3 blank | plates | `\pandocbounded` capped at 60% of the page |
| `Figure 1: تصویر ۱: …` — the label doubled | plates | caption label off |
| `(-Tung` / `shan's`: a line broken at a hyphen puts the hyphen on the wrong side of the Latin run | Introduction, book-wide | no line break at a hyphen |
| A kasra or damma pushed its line down: poem 640's quatrain opened a stanza gap in its middle | book-wide | `\lineskiplimit` |
| `(T 14 ،Vimalakirti Sūtra)` — a Persian comma between Latin runs welded them and broke the brackets | `notes.md`, 17 places | `tex/rlm-before-comma.lua` |
| A wrapped verse line read as a line of its own: poem 115's quatrain as six lines | ~10 poems | `tex/verse-hang.lua`, continuations hang |
| `درآمدِ منثور بر ۵۳۱ and ۵۳۲` | `107.md` | `apparatus.py`; the file itself is 027's |
| `۱۲۰ شعر`, `۱۴۷ بخش` in the reader's note | `index.md` | 126 and 153 |

**Left as it is**, with the reason:

- `(Ryōzen) (۱۲۹۵-۱۳۶۹)` in `introduction-2.md` typesets as `((Ryōzen` at a
  line end. Two parentheticals side by side with the line broken between them
  — once in the book. The Persian is right.
- The bibliography and glossary are the OCR's text: joined entries, stray
  symbols, blank CJK, full stops at the wrong end. 008 requirement 3,
  deliberately deferred; `README.md` now says so.
- `notes.md` renders a Taishō column letter sometimes as `a`, sometimes as
  `الف`. Both read correctly; a style inconsistency, not a typesetting fault.

**Still not done:** the EPUB opened in a real reader. It builds, and its
spine is RTL. (Done at the close, below.)

### Closing: the EPUB validated and opened, and `v1.0.0`

The first time EPUBCheck 3.3 ran on the book, it found two faults. Nothing
built before had caught either one:

- **A fatal XML error in the reader's note.** `index.md`'s opening HTML comment
  had a `--` in it. Pandoc copies comments into the EPUB, and in XHTML a
  double hyphen inside a comment is not well-formed, so a strict reader
  refuses `ch001.xhtml`. That is the page that tells the reader the book is
  machine-translated. The comment is reworded, and it now says why.
- **No chapter was `dir="rtl"`.** Only the title page was. Pandoc gives chapter
  files its *variables* but not the document metadata, so the top-level
  `dir: rtl` never reached them. They were right-to-left only because
  `epub.css` set `direction: rtl`, and EPUB forbids that property in a style
  sheet (`CSS-001`) and lets a reader ignore it. Now `dir: rtl` is also set
  under `epub: variables:`, and the CSS rule is gone. A two-chapter test book
  confirmed the variable is what does it: without it, only the title page
  gets the attribute.

After the fix: `0 fatals / 0 errors / 0 warnings`, all 155 chapter files
`dir="rtl"`, and the spine still `page-progression-direction="rtl"`.

**Opened in epub.js** (Chromium, paginated two-page spread), the rendering
engine behind many web and app readers. The package direction reads `rtl`,
the first page of a spread is on the right and the text continues on the
left, and `next()` goes from the title page to the next spine item.
Vazirmatn is embedded and shapes correctly. Poem 52 keeps its four verse
lines, and `Ch’uan Teng Lu`, `fūryū` and `Blue Cliff Record` read forwards.
Pages checked: the title page, the reader's note, «تلمیح» in the
Introduction, and poem 52 with its notes. **It has still not been opened on a
dedicated device or in Apple Books.** Those are the strictest readers, and
the fatal error above is exactly what they reject. What is left there is a
person with a device, not a known fault.

**The PDF was not rebuilt in this session.** The container's TeX Live is
Debian's 2023 (LuaTeX 1.17), where `\babelprovide[import]{persian}` collides
with babel-persian (`\persiandate already defined`), and CTAN was not
reachable to install a current one. The book is built with LuaTeX 1.24. None
of this session's changes reaches the LaTeX output: two of them are
EPUB-only keys, LaTeX drops the HTML comment (checked with `pandoc -t
latex`), and `book-version` is printed only inside index.md's `unless-format="pdf"`
div. So the PDF at `v1.0.0` is the one 027 rebuilt and read.

`book-version` is now `نسخهٔ ۱.۰.۰`, and the tag is `v1.0.0`. Under
`README.md`'s versioning, MAJOR is "a new edition". This is the first edition
that has been read end to end, and every file the read found has been
re-translated.
