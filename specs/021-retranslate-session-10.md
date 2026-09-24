# 021 — Re-translate what 010's tenth session repaired

**020 again, for the next batch. `source/` changed in 4 files; one needs
re-translating.**

## Context

Spec 010's tenth session (poems 352–389, files `091`–`100`) fixed local
damage in `generate_final_markdown.py`. See 010's *Session 10* notes for what
and why. All four changed files are in the decade.

**`just check` is green.** Every fix is inside an existing block, and no
marker moved. What shows the damage is reading: `091`'s poem.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 10 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (1)

| file | what changed in the source |
|---|---|
| `091.md` | the poem's second line: `The kōan “privately carriages pass” confuses clear and cloudy.`, was `The kan “privately carriages pass confuses`. **The Persian puts the rest of the line inside the kōan**: «در خفا، کالسکه عبور می‌کند و مرز میانِ صاف و ابری را درهم می‌آمیزد.» Also `“No words`, was `““No`, and `through.” [97]`, which the Persian already has |

### B. No re-translation (3)

- `092.md` — `Hōnen` ×4 and `Jōdoshū`, where the source had `Honen`,
  `Henen` and `Jodoshi`. The Persian already has «هونن», as §2 does, and
  «جودو-شو». `Butsu”` and `alone` are inside text the Persian renders right.
- `097.md` — `(803-52)`, was `(803- 52)`. The Persian has «۸۰۳-۸۵۲».
- `100.md` — the poem ends `belly.`, was `belly.,`. The Persian ends on a
  full stop.

## Requirements

1. **Group A through the pipeline**, as `CLAUDE.md` describes: `strip`,
   `gtranslate.py -w --raw`, `restore -o`. Check `pgrep -f gtranslate.py`
   first. Judge the draft on ezafe, not the picker.
2. **No §1.4 marker to re-apply.** Check that `091` carries none and no
   `parity: offset` before running.
3. **§2 against the old file and the table.** *Wei-shan*, *Yang-shan* and
   *Rinzai* are in the old file as «وی-شان», «یانگ-شان» and «رینزای».
   *kōan* is «کوآن».
4. **Read the poem's second line.** The kōan is the quoted phrase alone, and
   it is the kōan that confuses clear and cloudy.
5. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] `091` re-translated.
- [ ] `091`'s second line quotes only *privately carriages pass*.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no
      disagreement for `091`: [97].
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `101`'s flattened Po Chü-i poem is recorded
in 010 for the next decade. `097`'s title (poem 384, `Untitled` where the
Index gives one) is 014's open question.

## Implementation notes

_None yet._
