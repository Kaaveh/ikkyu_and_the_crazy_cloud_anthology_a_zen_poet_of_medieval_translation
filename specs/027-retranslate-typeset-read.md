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

## Session 1 (2026-09-25): re-translation does not fix the quotes

**107 is done.** Re-translated at the default chunk, restored; only the heading
changed, to `درآمدِ منثور بر ۵۳۱ و ۵۳۲`. `just check` green.

**014, 020 and 086 were re-translated and came back with the same faults.**
All three came back Advanced (ezafe 25 / 7 / 46, read). Put through
`normalize --fix` in scratch, as `just fix` would, the sweep flags 014 line 12
~35 times and line 14 once, 020 lines 16–17, and 086 line 14 — the very
`»وو« و »یوئه«` 007 found. None was restored; `fa/` still holds the old three.

**The model is not the cause; nested quotation is.** The English nests quotes
in all three (014 line 12 runs `“”““”“…””“`; 086 line 14 `“‘‘`). The model
keeps the nesting: an outer `«…»` with an inner `"…"` or `”…“`. Then
`normalize`'s `quotes` rule — two regexes, `"([^"\n]*)"` and `“([^”\n]*)”`,
in `bargardan_tools` — pairs by position, not by nesting:

- Inside `«…»` the inner marks are an odd run once the model closes a quote
  with `."»` (020, 086), so every pair after it is paired across the gap
  between two quotes, and turns out `»…«`.
- The model writes the curly pair RTL-reversed, `”…“` (014). The curly regex
  opens at a `“` that is really a close, and every span it rewrites is the gap
  between two quotes.

No chunk size changes this: the nesting is in the English. **STYLE.md §6's
`<<<TBD>>>` — "nested quotation inside a `«»` span. Has not come up" — is
exactly this, and it has come up.**

### What closes it, and it is not a re-translation

A decision, then work in whichever place it lands:

1. **Fix the `quotes` rule in `bargardan-tools`** to know nesting and the
   reversed curly pair, tag it, bump the pin here, and settle §6 on what an
   inner quote becomes. Then re-run this spec as written. Shared package:
   the other books take the change too.
2. **Sanction a third hand-edit** in `CLAUDE.md` — repairing quote marks — and
   fix the three by hand. Leaves the rule to break the next nested quote.
3. **Exempt the three spans** with `<!-- normalize: off -->` and hand-write
   the inner marks. Same objection, plus a hand-edit that isn't sanctioned
   either.

Recommended: 1. It is the root cause, and the only one that also stops the
fault recurring.

## Acceptance criteria

- [ ] All four re-translated through the `CLAUDE.md` pipeline (`-w --raw`,
      `strip` / `restore -o`), each read for Classic.
- [ ] The sweep above prints nothing outside the three back-matter files.
- [x] `fa/107.md`'s heading is `درآمدِ منثور بر ۵۳۱ و ۵۳۲`.
- [ ] `just check` passes.
- [ ] The four pages read in the typeset PDF.

## Out of scope

The Ryōzen line in `introduction-2.md` (see 007): the Persian is right and
only the typesetting is wrong, in one place.
