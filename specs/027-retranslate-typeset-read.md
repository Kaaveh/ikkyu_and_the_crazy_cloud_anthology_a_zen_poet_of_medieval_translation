# 027 — Re-translate what 007's typeset read found

**Four files whose Persian is wrong in a way only the typeset page showed.
`source/` is clean for all four; the drafts are not.**

## Context

Spec 007's end-to-end read of the PDF (see its *The typeset read* notes)
fixed everything it found in the build. Four faults are in `fa/` itself, and
`CLAUDE.md` allows only two hand-edits there — the obscene-poem marker and a
§2 proper-noun conform. None of these is either, so they are re-translated.

**`just check` is green and stays blind to all four.** Quotation marks and a
word inside a heading change no block count and no anchor.

## Dependencies

007's read (committed). The `apparatus.py` fix for 107 is committed too.

## The files

| file | what is wrong |
|---|---|
| `014.md` | Poem 44's notes, lines 16 and 18: guillemets reversed — `»نان-چ’یوآن«` — and mixed with curly quotes, `”نان-چ’یوآن«`, `»نان-چ’یوآن“`. 44 wrong marks. The English uses plain `“…”` throughout. |
| `020.md` | Poem 66's notes: a verse quote opens with a straight `"` and closes `."»`. |
| `086.md` | Poem 293's notes, line 20: `»وو« و »یوئه«`, reversed. |
| `107.md` | The heading reads `درآمدِ منثور بر ۵۳۱ and ۵۳۲`. The model was never at fault: `apparatus.py` re-emits this label from `source/` and changed only the digits. Fixed in 007; the file needs `restore` to run again, and `restore` needs a draft. |

The sweep that found the three quote faults — a guillemet used as the wrong
end of a pair, and `"`/`“`/`”` touching Persian — found nothing else in `fa/`.
Run it again after the re-translation; it must come back empty:

```bash
python3 - <<'EOF'
import glob,re
for f in sorted(glob.glob('fa/*.md')):
    for i,l in enumerate(open(f),1):
        if (re.search(r'(?:^|[\s(\[])»(?=[^\s.,،؛:!?)\]»«])',l)
            or re.search(r'(?<=[^\s(\[«»])«(?=[\s.,،؛:!?)\]]|$)',l)
            or re.search(r'["“”](?=[^A-Za-z]*[؀-ۿ])|[؀-ۿ][^A-Za-z]*["“”]',l)):
            print(f, i)
EOF
```

`bibliography.md`, `glossary-index.md` and `notes.md` carry curly quotes
inside English entries; those are the book's, not faults. Skip them when
reading the output.

## Acceptance criteria

- [ ] All four re-translated through the `CLAUDE.md` pipeline (`-w --raw`,
      `strip` / `restore -o`), each read for Classic.
- [ ] The sweep above prints nothing outside the three back-matter files.
- [ ] `fa/107.md`'s heading is `درآمدِ منثور بر ۵۳۱ و ۵۳۲`.
- [ ] `just check` passes.
- [ ] The four pages read in the typeset PDF.

## Out of scope

The Ryōzen line in `introduction-2.md` (see 007): the Persian is right and
only the typesetting is wrong, in one place.
