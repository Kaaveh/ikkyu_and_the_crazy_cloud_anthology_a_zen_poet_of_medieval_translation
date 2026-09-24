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

- [x] Every group A file re-translated.
- [x] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `063` carries [72], `066` [75], `069` [77] and
      [78].
- [x] `070`'s poem names the Buddha-Devil kōan.
- [x] Group B checked.
- [x] `just check` green.

## Out of scope

Anything 010 has not read yet. `065`'s prose introduction set as one
paragraph where p. 125 has five: that is the book-wide shape in 010's
*Session 7* item 3, and it waits for a spec of its own. The break before
`070`'s *Ikkyū often refers…* and the breaks inside `069`'s and `070`'s
quotes belong to the *Prose block quotes* shape, which is left alone
book-wide.

## Implementation notes

### One sitting, all four at 4500

**Every draft came back Advanced**, with 3, 3, 5 and 7 ezafe, and `restore`
took each one on the first try. Block counts match `source/` in all four. No
file in group A carried a §1.4 marker or a `parity: offset`.

**The markers are back.** `063` carries [72], where the old file had [2].
`066` carries [75] and `069` [77]. The model put [77] after the sentence's
full stop, which is where the source has it. `070` keeps [79] and [80]. The
marker comparison now disagrees only on `introduction-1`, the last of the
three that 010 has recorded since session 2.

**`070`'s third line names the kōan:** «آن «کوآنِ» (معمای ذن) مربوط به «بودا
و شیطان» را مطرح کرد». The note keeps «کوآنِ «بودا-شیطان»».

**§2, conformed against the table:**

- `063`: پای‌چانگ → پای-چانگ ×6.
- `066`: سونگ‌یوان → سونگ-یوآن ×7, ایکیو → ایک‌کیو ×2. *Po-yün* came
  back «بو-یون», as the old file had it; §2 lists it as correct as given.
- `069`: «چینگ-یوان» → «چ’ینگ-یوآن», ایکیو → ایک‌کیو.
- `070`: چینگ-سو → چ’ینگ-سو ×14, تزو-مینگ → تز’و-مینگ ×3, «شو چوان تنگ
  لو» → «شیو چ’وآن تنگ لو», ایکیو → ایک‌کیو ×5. *Tou-shuai* came back
  two ways; the four «تو-شوآی» are made «تو-شوای», as the old file and the
  draft's other three have it.

`just fix` turned `070`'s nested ASCII quotes into «طریقتِ».

**Left as the model gave it:** `066`'s «بطریقان» for *Patriarchs*, in the
poem and the note. The old file had the same word, and no §2 row covers it.

**Result:** `just check` is green, with 153/153 on parity and anchors.

### Group B

`064` read: «…بودا خواهید شد!»» [74], and the opening «... carries the
elision. Nothing to carry.

The typeset PDF was not read. This spec's criteria do not ask for it.
