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

- [x] `abbreviations.md` — 432 chars
- [x] `bibliography.md` — 8,046 chars
- [x] `index-of-poems.md` — 5,071 chars
- [x] `glossary-index.md` — 4,598 chars
- [x] `notes.md` — 17,518 chars, ~4 chunks · **depends on 002**

## Acceptance criteria

- [x] All five at `status: reviewed`.
- [x] `just check` passes with all five compared, and **no file declares a
      `parity: offset` or `parity: skip`**. If one turns out to need it, that is a
      sign the draft gained or lost a blank line — fix that instead.
- [x] `just fix` followed by `just check` leaves every verbatim entry byte-identical
      to `source/`. This is the real test of requirement 4, and the only way to know
      the `normalize: off` regions are placed correctly.
- [x] The four verbatim files' entry lists diff clean against `source/`.
- [x] Something in the book tells the reader what the page numbers refer to.
- [ ] All five read in the typeset PDF — the mixed Persian/Latin/CJK lines in the
      index files are where bidi faults are most likely in the whole book.
      **Not met, and not fixable inside this spec** — see "The PDF" below.

## Out of scope

The Anthology, the Introduction, release. Repairing OCR — that is 002.

## Implementation notes

### The four verbatim files went exactly as written

`strip`, wrap each `- ` list in `<!-- normalize: off -->`, translate the heading
and the one prose paragraph by hand, `restore`. Requirement 4's claim about
parity holds: `iter_blocks` skips the comment-only blocks, no file needed an
offset, and `just fix && just check` leaves all 302 entry lines byte-identical
to `source/`.

The `## Primary Sources` / `## Secondary Sources` headings are
`منابع دست‌اول` / `منابع دست‌دوم`. Requirement 5 is answered in the translated
preamble of both index files: "شماره‌ها به صفحه‌های چاپ اصلی انگلیسی (۱۹۸۶)
ارجاع می‌دهند، نه به صفحه‌شمار این ترجمه." — one added sentence, no renumbering.

### `notes.md` needed a harness, and the reason is worth recording

The spec calls it "17.5 K of real prose". It is not: **154 of its 204 notes are
under 60 characters** and are bare citations — `27. Ibid., T 47, p. 497a.` The
plain pipeline fails on those three ways, and each failure is silent:

1. **The model merges adjacent one-line citations**, losing a block. Two
   whole-file runs at `--chunk 4500` and `--chunk 2200` each lost one or two.
2. **A chunk that is nothing but citations is served Classic, every time.**
   Measured at four chunk sizes and at every split point tried, down to a single
   note. Classic produces exactly the damage requirement 6 forbids: `T 47` →
   `ت 47`, `KZ` → `کز`, `SP` → `اس پی`, `roll` → `رول`, and `p. 12bc` →
   `ص. ۱۲ قبل از میلاد`.
3. **Advanced sometimes hands a citation-only note straight back in English**,
   which leaves the file carrying two conventions for identical content.

**The fix for (2) is a prose primer.** Prepend one prose note to the same
citations and Advanced is served instead, keeping `T 47`/`ZZ`/`KZ` intact and
rendering `roll`/`v.` as `طومار`/`جلد`. So the file was translated in ~1,800
character pieces, each with note 3 prepended as a primer whose own translation
is thrown away, and each piece gated on three objective checks — block count,
every `CZS|KZ|SP|ZZ|T N` still present, and at least one Arabic-script *letter*
in the output. A piece that fails is split and retried; the fallback is
per-input and deterministic, so a different input is the only thing that can
change it. Then a mop-up pass re-translates whatever blocks still came back in
English, in batches behind the same primer. Two mop passes cleared all 23.

Two traps in the gates, both of which cost a run:

- `\bT\b` also matches **T.S. Eliot** and the T of **T'ao Yüan-ming**, so the
  abbreviation gate must be `\bT\s+\d+`.
- `\p{Arabic}` matches **Persian digits**, so an untouched citation whose only
  change was `62.` → `۶۲.` passes a "did it get translated" test. The gate needs
  a letter: `[\p{Arabic}&&\p{L}]` with `regex.V1`.

The harness is throwaway and lives in the scratchpad, not the repo: it exists
because `notes.md` is the one file in the book made of citations, and nothing
else here will need it. If the Introduction turns out to need the primer trick
too, that is the point to move it into `tools/`.

### `notes.md` hand-steps, both applied to the draft in `/tmp`, never to `fa/`

- **Entry numbers to Latin digits**, per STYLE §4.2 — the marker and the entry
  it points at change together. The model persianises them; 191 were converted
  back. Page references *inside* a note stay Persian, per §5.
- **One `<!-- normalize: off -->` region**, around note 71, whose English
  article title is in ASCII quotes that the script-blind `quotes` rule would
  turn into `«A Biographical Study of Tz'u-en»`.

### Source defects found, not repaired (requirement 7)

- `notes.md` note 99 is `roll 7, ZZ, v. roll 7, ZZ, v. 138` in `source/` — an
  OCR doubling. The model dropped the repeat and the Persian reads correctly;
  the abbreviation gate reports it as its one remaining mismatch. **The `fa/`
  file is right and `source/` is wrong.** Spec 008's.
- `glossary-index.md` is worse than "some garbled CJK": `Gozan frill, 7,8, 9,
  17422531`, `Muso Soseki 278684`, `Katada #16 katsu "%, 101`. Left verbatim,
  visibly broken, as requirement 7 asks.

### The PDF — the one criterion not met

`quarto render --to pdf` completes clean and all five files typeset. The Notes
and the Index of Poems read correctly: Latin runs inside Persian paragraphs are
not reversed, which is what LuaLaTeX + `bidi=basic` was chosen for.

**But every CJK character is invisible in the PDF.** The codepoints are in the
file — `pdftotext` on the bibliography page returns `Jikaisha 自戒 集,in Nakamoto
Tamaki 中 本 環` — and the rendered page has a blank gap where each one should
be. Vazirmatn has no CJK glyphs and no fallback font is declared, so LuaLaTeX
drops them without a "Missing character" warning. A second fault follows from
the first: the neutral comma between a CJK run and a page number then lands on
the wrong side, so a glossary entry reads `Gio ␣␣␣ ,13, 14`.

This is a build defect, not a translation one, and it is **book-wide, not back
matter's**: `introduction-1.md` carries 111 CJK characters and `introduction-3.md`
107. Fixing it means vendoring a CJK font into `fonts/` beside the Vazirmatn
pair — a licensing and repo-size decision for the maintainer, and one that
should not be smuggled in under a translation spec. Declaring a *system* font
instead would work on one machine and silently produce the same blank gaps
everywhere else, which is worse than the current state.

**Left for spec 007 (release), where the font stack belongs.** The HTML and
EPUB builds are unaffected: browsers and readers fall back on their own.
