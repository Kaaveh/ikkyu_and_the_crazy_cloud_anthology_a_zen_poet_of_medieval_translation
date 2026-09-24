# 019 — Re-translate what 010's eighth session repaired

**018 again, for the next batch. `source/` changed in 7 files; six need
re-translating.**

## Context

Spec 010's eighth session (poems 216–264, files `071`–`080`) fixed local
damage in `generate_final_markdown.py` and added one set heading to
`KNOWN_SETS`. See 010's *Session 8* notes for what and why. All seven changed
files are in the decade.

**`just check` is red on one file.** `074` gains the *Elder Ki* set heading
as a block, so `check_parity` reports `fa/074.md: 2 blocks, source has 3`.
Everything else is inside an existing block. What shows it is the marker
comparison in 010's *Tooling*: `073` and `080` disagree with `source/`.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 8 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (6)

| file | what changed in the source |
|---|---|
| `071.md` | the poem's last line ends in a full stop, was `singing,`. **The Persian ends the poem on a comma.** `Ch’ü Yüan’s`, was `Ch Yüan’s`; the Persian has «چو یوان» |
| `073.md` | marker **[83]**, was `Wu-men Kuan.8?`. **The Persian has [8]**. The *Elder Ki* set heading is gone from the note's end, **which the Persian translates as note text**. `poetry;`, `“a storm in a tea pot”`, `“enlightenment” poem`, `home.” [82]` |
| `074.md` | gains the set heading **Congratulating Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after His Leprosy** as a block |
| `075.md` | `Sōki` ×2, was `Soki`; **`Jikaishū`, was `Jikaishi`, which the Persian carries** in Latin and in «جیکایشی»; `little`, was `httle`; four quote marks |
| `079.md` | **`jō` ×2, was `jo` and `jd`; the Persian has *jo* twice.** `Mañjuśri` ×3, `Sūtra` in the poem, `Sūrangama`, two quote marks |
| `080.md` | marker **[87]**, was `marvelous.”’8?`, **which the Persian dropped**; `“no mind”` |

### B. No re-translation (1)

- `072.md` — `Nan-ch’üan` in the poem, was `Nan-ch’tian`; marker [81] gets
  its closing quote. The Persian already has both: «نان-چ’یوآنِ کوچک» and
  «…گربه‌ای خفته است.» [81].

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** Check that no file in group A carries
   one or a `parity: offset` before running.
3. **§2 against the old files and the table.** *Ch’ü Yüan* is «چ’یو یوآن».
   `074`'s and `075`'s titles should agree with each other and with the new
   set heading: the old two already disagree («ایگل‌تیل» and «دم عقاب»).
4. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `073` carries [82] [83] [84], `080` [87].
- [ ] `071`'s poem ends on a full stop.
- [ ] `073`'s note ends at *(See p. 13.)*; `074` opens the set with its
      heading.
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `introduction-3`'s `Ch Yüan` and
`introduction-1`'s `Jikaishi` are recorded in 010 as found in passing, for
the decade that reaches them.

## Implementation notes

_None yet._
