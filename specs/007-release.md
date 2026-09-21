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

- [ ] No `TBD` or `TODO` marker left in `_quarto.yml` or `index.md`.
- [ ] `just check` passes: 147 files compared by `check_parity` and
      `apparatus --check`, none skipped, no bidi findings.
- [ ] `just build` produces HTML, PDF and EPUB with no errors.
- [ ] The PDF was built by LuaLaTeX and a Latin citation inside a Persian sentence
      reads forwards.
- [ ] The EPUB spine is right-to-left in a real reader.
- [ ] The whole PDF read end to end.
- [ ] The release artifact contains no `source/`, no monolith, no raw OCR, no PDF of
      the original.
- [ ] `book-version` bumped; tag pushed.

## Out of scope

Translating or revising text. A second edition.

## Implementation notes

_(filled in during implementation)_
