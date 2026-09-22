# Working on this book

A Persian translation of *Ikkyū and the Crazy Cloud Anthology* (Sonja Arntzen).
135 poems and 12 surrounding sections, 147 files.

## The shape of the repo

- `…translation.md` — the English monolith, produced by
  `generate_final_markdown.py` from the PDF. Gitignored: it is the copyrighted
  source text.
- `split_book.py` — splits that monolith into `source/`. **`source/` is
  generated**; fix the script, never the files.
- `source/` — English, one file per poem or section. Gitignored, same reason.
- `fa/` — the Persian translation. This is the work, and it is committed.
- `STYLE.md` — the translation decisions: register, proper nouns, verse layout.
  Almost none of it is enforced by anything; read it before translating.
- `tools/apparatus.py` — this book's adapter over the shared checkers.
- `pyproject.toml` — config only. What makes general checkers run on this book.

## The checkers are not in this repo

They are the `bargardan-tools` package, shared with the other books in this
corpus and installed from `tools/requirements.txt`, pinned to a tag. There is
no vendored copy here to keep in sync.

It works because `bargardan_tools` reads its config relative to the *current
directory*, so running it from here picks up this project's `pyproject.toml`.
Nothing in it knows which book it is checking — which is why `just check` can
skip `check_linebreaks` for verse without patching anything.

`just venv` installs it. To work against a local checkout of the package
instead of the pinned tag, `pip install -e ../bargardan-tools`.

## Translating

- **Translate with `gTranslator`, one file at a time.** It lives at
  `~/Project/Backend/gTranslator`, is private, and nothing in `just check`
  depends on it — only producing a *new* draft does:

  ```bash
  GT=~/Project/Backend/gTranslator
  tools/apparatus.py strip source/002.md -o /tmp/002.en.md
  "$GT/.venv/bin/python" "$GT/gtranslate.py" \
      -f /tmp/002.en.md -t fa -w --raw -o /tmp/002.fa.md
  tools/apparatus.py restore source/002.md /tmp/002.fa.md -o fa/002.md
  ```

- **`-w` is mandatory.** Every other mode serves the Classic model, which
  translates clause by clause and is markedly worse here. The failure is
  silent: the model picker claims "Advanced" while Classic is served, so judge
  the output text, never the picker. Advanced gives ezafe diacritics
  (`چشمِ حقیقی`) and restructures sentences; Classic does neither.
  `grep -c ِ` on the draft separates them in one command — 0 is Classic.

- **The fallback is per *chunk*, so measure ezafe per paragraph, not per
  file.** Spec 005 found `preface.md` Advanced for its first two paragraphs and
  Classic for the remaining six, split exactly at the chunk boundary. A
  whole-file count cannot see that: this file scores 25, and the verb-prefix
  test below passes it clean. The signal is **a run of paragraphs at exactly 0
  ezafe totalling more than ~1,500 characters**; one 0 paragraph between
  healthy ones is normal (spec 004's `099.md`, spec 005's `foreword.md`).

  ```bash
  awk 'length>120' fa/preface.md | while IFS= read -r l; do
    printf '%5d %s\n' "$(printf '%s' "$l" | grep -o 'ِ' | wc -l)" "${l:0:40}"
  done
  ```

- **When a file comes back Classic, go down the ladder and re-run.** Re-running
  unchanged does nothing: the fallback is per-input and deterministic, and the
  same text at the same chunk size gives the same model every time. It is not
  the user agent, not a timing race and not quota — spec 003 ruled out all
  three. **Halving is the wrong ladder** (spec 004: `098.md` came back Classic
  at 4500, 2250, 1125, 562 *and* 281, and Advanced at 400). Use **4500, 900,
  400, 300**. `009.md` needed 300; `preface.md` needed 900.

- **A ladder step trades one failure for another once `source/` is damaged.**
  Spec 005: `introduction-2.md` at 900 gives good Persian and drops a block; at
  400 it keeps every block and turns seven paragraphs Classic. If no chunk size
  is clean, stop — the input is the problem, not the chunk. Check the file
  against the damage table in `specs/005-introduction.md` before spending
  another run on it.

- **`--raw` is mandatory too, and matters more here than in the prose books.**
  It stops the translator's line-unwrapping, which would run a stanza together
  before the model ever saw it.

- **Never concatenate files.** `fa/` must mirror `source/` file-for-file or
  `check_parity` cannot pair them.

- **Always through `tools/apparatus.py`.** `strip` before, `restore -o` after.
  Never `>` into `fa/` — a redirect truncates the file before the tool can
  refuse a bad draft.

- `introduction-1.md` is 67k characters, about fifteen chunks, and is by far
  the longest run. The rest are small; most poems are a single chunk.

## What the adapter does, and what it does not

Measured, twice, on a representative file: the Advanced model returns `#`/`##`
markers and `![alt](images/plate_1_calligraphy.png)` completely intact, path
and all. So unlike Lin-chi's, this book's adapter carries **no** image or link
machinery. It does two things:

1. Re-emits the structural heading labels — `Poem N:`, `Notes`, `Plate N:`,
   `Prose Introduction to …` — from `source/`, so `شعر ۷` cannot become
   `قطعهٔ هفتم` three chapters later. The *title* after the label is real prose
   and is left for the translator.

2. Puts back the hard line breaks that hold a stanza together. The model
   strips the two trailing spaces, and without them every poem reflows into a
   single paragraph.

**When `restore` refuses, it names the lines.** It aligns breaks run-by-run, so
it recovers on its own when the model re-breaks a quoted poem inside a prose
note — which it does, correctly, in 002.md. If it still refuses, end the named
draft lines in `/tmp` with two spaces and run it again. Edit the draft in
`/tmp`, never `fa/`: `restore` is the only thing that writes `fa/`, and it
validates first.

## Status values in `fa/` front matter

Two states. `untranslated` (what `make_stubs` writes) → `reviewed` (what
`restore` writes). **The machine draft is the edition**: there is no
hand-revision stage after the pipeline, so there is no later step to promote a
`draft` into place. `check_parity` and `apparatus --check` skip `untranslated`
and check the rest.

## The two sanctioned hand-edits to `fa/`

`restore` is the only thing that *creates* a file in `fa/`. Two edits are made
by hand afterwards, and only these two:

1. **The obscene-poem marker** (`STYLE.md` §1.4) — a `> [زبانِ این شعر عامدانه
   رکیک است.]` block under the heading, plus `<!-- parity: offset +1 -->`. It
   cannot be added before `restore`: it changes the run structure, so
   `align_hard_breaks_by_block` stops matching and `engine.restore` refuses the
   draft.
2. **Conforming a proper noun to `STYLE.md` §2** — the model transliterates by
   ear and nothing checks it.

Anything else that is wrong in `fa/` is re-translated, not patched. `just check`
must pass after either edit.

## `just check` has no `check_linebreaks`

That checker enforces one sentence per line, which is right for prose and
meaningless for verse. This book is mostly verse. The note is at the foot of
`pyproject.toml`.

Bidi overrides are reported but never auto-fixed, so `just fix` can still leave
`just check` failing. That is by design — a human has to look at those.
