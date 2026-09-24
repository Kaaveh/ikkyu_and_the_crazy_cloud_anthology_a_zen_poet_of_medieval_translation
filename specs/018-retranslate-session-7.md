# 018 — Re-translate what 010's seventh session repaired

**017 again, for the next batch. `source/` changed in 5 files; four need
re-translating.**

## Context

Spec 010's seventh session (poems 176–210, files `061`–`070`) fixed local
damage in `generate_final_markdown.py`. See 010's *Session 7* notes for what
and why. All five changed files are in the decade.

**`just check` stays green.** Every change is inside an existing block, so
neither parity nor anchors can see it. What shows it is the marker
comparison in 010's *Tooling*: `063`, `066` and `069` disagree with `source/`.
The two files that used to disagree, `064` and `070`, now agree. In both, the
Persian had the marker right and the source did not.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 7 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (4)

| file | what changed in the source |
|---|---|
| `063.md` | marker **[72]**, was `eating.”2`. **The Persian has [2]**, so it sends the reader to the wrong note. `“a day of no work` opened |
| `066.md` | marker **[75]**, was `Yü-lu®>`, which the Persian dropped; `Sung-yüan` ×2, was `Sung-ytian` and `Sung-yuan`; `(1025-72)` |
| `069.md` | marker **[77]**, was `Yü-lu.??`, which the Persian dropped |
| `070.md` | `Buddha-Devil`, was `BuddhaDevil`, in the poem and the note. **The Persian's third line leaves it out**: «آن معمای ذن (کوآن)». Also `Sung-dynasty`, `Ch’ing-su`, and five quote marks in the *Hsü Ch’uan Teng Lu* quote |

### B. No re-translation (1)

- `064.md` — marker [74], left bare by the OCR, is bracketed now; the
  quote opens `“...` and closes `‘…’”`. The Persian already has all of it:
  «…بودا خواهید شد!»» [74].

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** Check that no file in group A carries
   one or a `parity: offset` before running.
3. **§2 against the old files and the table.** *Ch’ing-su* is «چ’ینگ-سو»;
   the old `070` has it nine times and «چینگ-سو» five more. *Sung-yüan* and
   *Tz’u-ming* have rows.
4. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `063` carries [72], `066` [75], `069` [77] and
      [78].
- [ ] `070`'s poem names the Buddha-Devil kōan.
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `065`'s prose introduction set as one
paragraph where p. 125 has five: that is the book-wide shape in 010's
*Session 7* item 3, and it waits for a spec of its own. The break before
`070`'s *Ikkyū often refers…* and the breaks inside `069`'s and `070`'s
quotes belong to the *Prose block quotes* shape, which is left alone
book-wide.
