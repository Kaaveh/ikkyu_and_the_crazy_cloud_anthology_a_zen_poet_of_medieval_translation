# ایک‌کیو و گلچین ابر دیوانه

A Persian translation of **_Ikkyū and the Crazy Cloud Anthology: A Zen Poet of
Medieval Japan_**, Sonja Arntzen's translation of and commentary on the
*Kyōunshū* — the Chinese-language poems of the Japanese Zen monk Ikkyū Sōjun
(1394–1481), who called himself Crazy Cloud.

126 poems and 15 prose introductions, plus front matter, a four-part
Introduction and five back-matter sections: 153 files, 238 typeset pages.

📄 **[Latest PDF and EPUB](../../releases/latest)**

Every page of the book carries an **«ویرایش این صفحه در گیت‌هاب»** link. If you
spot a typo, that is the whole workflow — no clone, no toolchain.

---

## The Persian is machine-translated

Say it up front, because it changes how you should read the book. Each file was
translated by Google Translate's Advanced model, one file at a time, and this
repository's own tools then put back what the model loses: the structural
headings (`شعر ۷`, `یادداشت‌ها`, `تصویر ۱`) and the hard line breaks that hold a
quatrain together. Automated checks catch a dropped paragraph and a stanza
reflowed into prose.

What they do not catch is whether the translation is any good. **There is no
hand-revision stage** — the machine draft is the edition. Exactly two hand-edits
are sanctioned afterwards: conforming a proper noun to [`STYLE.md`](STYLE.md),
and adding the warning note above the obscene poems.

## Rights

Read this before contributing or forking.

| | |
|---|---|
| **The Persian translation** | [CC BY-SA 4.0](LICENSE-TEXT) — share and adapt, keep it open |
| **The code and build** — `tools/`, `tex/`, `assets/`, `justfile`, the two generator scripts | [MIT](LICENSE-CODE) |
| **The English source text** | © Sonja Arntzen / Shambhala Publications, 1986. **Not redistributed here.** |
| **The plates** | Works held by Shinjuan (Daitokuji), Kyoto, reproduced from the English edition |
| **The underlying Chinese poems** | Public domain (Ikkyū died in 1481) |

The English source is licensed to the maintainer for the purpose of producing
this translation. It is **not** public domain, and it is **not** in this
repository: `source/`, the English monolith, the raw OCR and the scanned PDF are
all in `.gitignore` and must stay there.

One consequence worth knowing: the parity check, which catches dropped
paragraphs by comparing block counts between the two trees, cannot run without
`source/`. It reports "skipped" for anyone but the maintainer.

## Building from source

Needs [`just`](https://github.com/casey/just), Python 3, [Quarto](https://quarto.org)
and a TeX Live with LuaLaTeX.

```bash
git clone https://github.com/Kaaveh/ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation
cd ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation
just venv           # the Python environment and the checkers
just build          # HTML, PDF and EPUB into _book/, the mobile PDF into _book-mobile/
```

| | |
|---|---|
| `just check` | orthography, parity, hard line breaks, tests |
| `just fix` | correct what can be corrected automatically |
| `just build` | all three formats, plus the mobile PDF |
| `just pdf-mobile` | the phone edition only: a 90×160mm page, into `_book-mobile/` |
| `just pdf` / `just epub` / `just html` | one format |
| `just serve` | live preview on <http://localhost:4200> |
| `just --list` | everything |

The checkers are the **`bargardan-tools`** package, shared with the other books
in this corpus and installed from `tools/requirements.txt` at a pinned tag.
There is no vendored copy here. `tools/apparatus.py` is this book's adapter over
it.

### How the book is built

Pandoc-flavoured Markdown, one file per poem or section, rendered by Quarto into
HTML, EPUB and PDF from a single source tree.

The PDF uses **LuaLaTeX, not XeLaTeX**. Under XeLaTeX, Pandoc's template selects
babel with `bidi=default`, whose bidirectional handling is heuristic rather than
a real implementation of the Unicode Bidirectional Algorithm — it reverses the
word order of Latin-script runs embedded in Persian, so a citation like
`T 47, p. 497a` typesets backwards. This book's notes are full of such runs.
LuaLaTeX gets `bidi=basic`, which is a real UBA implementation. The reasoning
and the other approaches tried are in [`tex/preamble.tex`](tex/preamble.tex).

Fonts are vendored: [Vazirmatn](https://github.com/rastikerdar/vazirmatn) under
the SIL Open Font License, in `fonts/`. Vendoring rather than resolving from the
system font path is what makes the typeset output reproducible.

**Known limitation:** Vazirmatn has no CJK glyphs and no fallback font is
declared, so the handful of Chinese and Japanese characters in the book render
as blank gaps in the PDF. All but 26 of them are OCR garbage in
`bibliography.md` and `glossary-index.md`, deliberately left verbatim; the 26
real ones are Japanese book titles in `abbreviations.md`, each already given in
romanization beside the original. HTML and EPUB are unaffected — browsers and
readers fall back on their own.

A second fault follows from the first, and from the same files being
Latin-dominant lines inside a right-to-left paragraph: the neutral punctuation
that ends such a line lands at its other end, so an entry typesets as
`.Shoten, 1972`. Both are recorded in spec 007 and neither is fixed in v1.0.2.

Those two files are also the OCR's text, unrepaired: in the glossary, a run of
entries is often joined into one paragraph, and both carry stray symbols where
the scan had characters it could not read. Everything else in the book was
read against the scan (spec 010); these two were not.

## Versioning

Releases are tagged `vMAJOR.MINOR.PATCH`.

| | |
|---|---|
| **MAJOR** | A new edition, or a retranslation |
| **MINOR** | A new section, or a substantive revision to an existing one |
| **PATCH** | Typos, orthography, formatting, tooling |

## Repository layout

```
fa/            the translation — one file per poem or section, mirroring source/
source/        the English source (gitignored, never committed)
specs/         the work plan, one spec per stage
STYLE.md       register, proper nouns, verse layout
tex/           the LaTeX preamble for the PDF
fonts/         vendored Vazirmatn + OFL
images/        the four plates
assets/        RTL and EPUB stylesheets
tools/         the apparatus adapter, its tests, the checker pin
               (the general checkers are the bargardan-tools package)
_quarto.yml    the book: three formats, 153 sections in two parts
_language.yml  Persian UI strings — Quarto ships no fa locale
```

`CLAUDE.md` documents the translation pipeline itself, including why `-w` and
`--raw` are mandatory and how to tell a good draft from a bad one.
