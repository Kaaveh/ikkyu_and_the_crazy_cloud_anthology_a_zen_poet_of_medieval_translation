# 025 — Re-translate the Introduction

**What 024's read changed: `introduction-1`, `-2` and `-3`. Three files,
and the first of them is the longest run in the book.**

## Context

[024](./024-introduction-read.md) read the Introduction against the scan.
Its *Session 1* notes say what changed and why:

- about thirty endnote markers fixed;
- 25 quoted poems set back as verse;
- paragraph breaks recovered;
- four passages of lost words given back;
- some forty names restored with their diacritics.

**`just check` is red** on `check_parity`, and only for these three files:

```
fa/introduction-1.md: 106 blocks, source has 120
fa/introduction-2.md: 20 blocks, source has 19
fa/introduction-3.md: 62 blocks, source has 66
```

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

024 session 1, which is committed. `source/` is gitignored, so if it
predates that commit, rebuild it first:

```bash
.venv/bin/python generate_final_markdown.py && just split
```

`just split` alone does not rebuild the monolith.

## The files

| file | chunk size last time | what changed in the source |
|---|---|---|
| `introduction-1.md` | 900 | markers 1–57, most of the 25 verse quotes, Giō, Shūon’an, Sōchō, Daiō (not *Daitō*), and `IKkyu` ×6, which [023](./023-retranslate-session-12.md) group C deferred to this spec |
| `introduction-2.md` | 4500 | markers 58–62, the words given back on p. 62 (`as we read, “It must have been`), and its verse quotes |
| `introduction-3.md` | 2250 | markers 63–84, Ch’ü Yüan ×4, Kao-t’ang, Yang-t’ai, Sung Yü, and its verse quotes, among them Yün-men’s two sayings |

## Requirements

1. **Use the pipeline in `CLAUDE.md`, one file at a time**: `strip`, then
   `gtranslate.py -w --raw`, then `restore -o`. Run `pgrep -f gtranslate.py`
   first. Judge Advanced against Classic on ezafe per paragraph, then by the
   verb-prefix test, never by the picker.
2. **Start at last time's chunk size** (table above), then go down the
   ladder: 4500, 900, 400, 300. Choose on block parity, and prefer a split
   to a drop.
3. **Every verse quote keeps its hard breaks.** `restore` names any line
   that lost its break. Fix those in the scratch draft, never in `fa/`.
4. **Check the markers.** For each file, the `[N]` sequence in `fa/` must
   equal the one in `source/`.
5. **Read before accepting.** 005 found `introduction-3` rendering
   *allusion* as `کنایه` rather than `تلمیح`, the chapter's own title.
6. **Conform proper nouns to `STYLE.md` §2** (sanctioned edit 2). Where the
   table is silent, keep the old file's spelling.

## Acceptance criteria

- [ ] All three files re-translated, and their block counts match
      `source/`.
- [ ] Markers 1–84 in the Persian, in the same order as `source/`.
- [ ] All 25 verse quotes set as verse in `fa/`.
- [ ] `just check` is green. That closes 024.

## Out of scope

`introduction-4`, which 023 re-translated.
