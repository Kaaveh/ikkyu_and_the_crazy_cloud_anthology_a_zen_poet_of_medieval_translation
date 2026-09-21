# 006 — Back matter

**5 files · 35,665 chars · four of them entry lists kept verbatim**

## Context

The apparatus: abbreviations, the endnotes, the bibliography, an index of poems and a
glossary-index. Four of the five are entry lists whose content is Wade-Giles and
Japanese romanisation, CJK characters, publication data, and page references into the
1986 print edition. Machine-translating a bibliography entry does not produce a
Persian bibliography entry — it produces a damaged one, and the damage is invisible
to anyone who cannot check it against the original.

**The decision is: translate the headings and the prose, keep the entries verbatim.**
A reader who wants to find *Chūsei Zenka no Shisō* needs the string
`Chūsei Zenka no Shisō`, not a transliteration of it.

`notes.md` is the exception. It is 17.5 K of real prose — 88 notes to the
Introduction and 116 to the translations — and is translated like any other prose in
the book.

This spec is small and independent, which is why the roadmap puts it before the long
Introduction files: it unblocks a complete `just build` early.

## Goal

Five files at `status: reviewed`, `just check` green, and no file where a verbatim
entry has been silently rewritten by the normalizer.

## Dependencies

002 — `notes.md` is the worst OCR damage in the book and cannot be translated until
it is repaired. The other four depend on nothing.

## Requirements

1. **Treatment, file by file:**

   | file | blocks | treatment |
   |---|---:|---|
   | `abbreviations.md` | 2 | Heading only. The five entries are publication data — verbatim. |
   | `notes.md` | 207 | **Fully translated.** Prose. |
   | `bibliography.md` | 5 | Heading, `## Primary Sources`, `## Secondary Sources`. Entries verbatim. |
   | `index-of-poems.md` | 3 | Heading + the one-paragraph preamble. Entries verbatim, page numbers untouched. |
   | `glossary-index.md` | 3 | Heading + the one-paragraph preamble. Entries verbatim. |

2. **The h1 of every one of these comes from `pyproject.toml`, not the translator.**
   All five are in `[tool.book.titles]`, so `apparatus.py` re-emits
   `کوته‌نوشت‌ها`, `یادداشت‌ها`, `کتاب‌شناسی`, `نمایهٔ شعرها`,
   `واژه‌نامه و نمایه` whatever the model returns. To change one, edit
   `pyproject.toml`. The `## Primary Sources` / `## Secondary Sources` headings in
   `bibliography.md` are *not* structural labels — they are prose and the translator's.

3. **How to produce a part-translated file.** `restore -o` is still the only thing
   that writes `fa/`, and it takes whatever draft you hand it. So:

   ```bash
   tools/apparatus.py strip source/bibliography.md -o /tmp/bib.en.md
   cp /tmp/bib.en.md /tmp/bib.fa.md
   # translate only the heading/prose lines into /tmp/bib.fa.md by hand or by
   # running gtranslate.py on just that prose; leave every entry line untouched
   tools/apparatus.py restore source/bibliography.md /tmp/bib.fa.md -o fa/bibliography.md
   ```

   Two rules while editing the draft:
   - **Do not touch the `⟦1⟧` sentinel.** It is the h1 title placeholder; `restore`
     refuses the file if it is gone, and re-emits the Persian heading from config.
   - **Do not add or remove blank lines.** Parity counts blank-line-delimited blocks,
     and every entry list here is a single block of consecutive `- ` lines. Keep it
     that way and the counts match with no offset needed.

4. **Wrap every verbatim list in `<!-- normalize: off -->`.** `normalize`'s `quotes`
   rule is script-blind: it rewrites ASCII and curly quotes to `«»` anywhere,
   including inside an English book title, and `just fix` will do it without asking.
   The `tatweel`, `arabic_yeh` and `arabic_kaf` rules are equally happy to touch a
   transliteration.

   ```markdown
   <!-- normalize: off -->

   - Blue Cliff Record (Ch. Pi-yen Lu …), T 47 …
   - Ch’an-lin Lei-chü …

   <!-- normalize: on -->
   ```

   **This costs nothing in parity**: `iter_blocks` skips comment-only blocks
   (`_md.py:136`), so the two directives do not count as blocks and no
   `<!-- parity: offset -->` is needed. Verify that with `just check` rather than
   trusting this paragraph.

5. **Page references point at an edition the reader does not have.** Every number in
   `index-of-poems.md` and `glossary-index.md` is a page of the 1986 Shambhala
   printing. They are useless to a reader of the Persian HTML or EPUB and actively
   misleading in the Persian PDF, whose pagination is its own.

   Decide what to say about that and say it once — a sentence in the translated
   preamble of each file, or a line in `index.md`. Do not renumber them; there is no
   mapping to renumber them to.

6. **`notes.md` is 207 blocks and four chunks.** Ordinary prose translation, after
   002 has repaired it. Its two section headings (`## Notes to Introduction`,
   `## Notes to Translations`) are prose and the translator's. The notes reference
   poems by number and works by abbreviation (`T 47`, `SP`, `KZ`) — those
   abbreviations are the ones `abbreviations.md` defines and must not be translated
   or have their digits converted.

7. **Do not repair OCR here.** `bibliography.md` and `glossary-index.md` have
   garbled CJK that spec 002 deliberately deprioritised, on the grounds that a
   verbatim garbled entry is visible as garbage while a translated one is not. If
   002 left it, leave it and note it — do not start an audit inside a translation
   spec.

## Files

- [ ] `abbreviations.md` — 432 chars
- [ ] `bibliography.md` — 8,046 chars
- [ ] `index-of-poems.md` — 5,071 chars
- [ ] `glossary-index.md` — 4,598 chars
- [ ] `notes.md` — 17,518 chars, ~4 chunks · **depends on 002**

## Acceptance criteria

- [ ] All five at `status: reviewed`.
- [ ] `just check` passes with all five compared, and **no file declares a
      `parity: offset` or `parity: skip`**. If one turns out to need it, that is a
      sign the draft gained or lost a blank line — fix that instead.
- [ ] `just fix` followed by `just check` leaves every verbatim entry byte-identical
      to `source/`. This is the real test of requirement 4, and the only way to know
      the `normalize: off` regions are placed correctly.
- [ ] The four verbatim files' entry lists diff clean against `source/`.
- [ ] Something in the book tells the reader what the page numbers refer to.
- [ ] All five read in the typeset PDF — the mixed Persian/Latin/CJK lines in the
      index files are where bidi faults are most likely in the whole book.

## Out of scope

The Anthology, the Introduction, release. Repairing OCR — that is 002.

## Implementation notes

_(filled in during implementation)_
