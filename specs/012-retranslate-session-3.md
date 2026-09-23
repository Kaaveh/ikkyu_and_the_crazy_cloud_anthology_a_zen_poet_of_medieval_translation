# 012 — Re-translate what 010's third session repaired

**011 again, for the next batch. `source/` changed in 15 files; the Persian of
13 of them is now stale.**

## Context

Spec 010's third session (poems 068–090, files `021`–`030`) fixed two defect
classes in `generate_final_markdown.py`. See 010's *Session 3* notes for what
and why. The set-heading fix is book-wide, so the changed files run from `021`
to `122`, not just the decade that was read.

**`just check` is red on five of them.** `check_parity` reports `022`, `038`,
`051`, `095` and `122` one block short: each gained its set heading as a block
of its own. Every other change is inside an existing block and fails nothing.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 3 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (13)

| file | what changed in the source |
|---|---|
| `021.md` | the heading *The Scriptures Wipe Away Filth* taken out of the note — **the Persian translated it**; `layman.”` |
| `022.md` | gains **The Scriptures Wipe Away Filth: three poems** — **check fails** |
| `025.md` | marker **[43], was [48]**; `well.”` |
| `028.md` | marker **[45], was [35]**; the closing quote after `go yet.`; `“At`; `poem no. 54` |
| `030.md` | **[90] Daitō**, was `(90 Daité` — the Persian carries `(90 دایتو`; `Nankō`; `“Mountain Road”` |
| `037.md` | the heading *Wind Bell* taken out of the note |
| `038.md` | gains **Wind Bell: two poems** — **check fails** |
| `050.md` | the heading *On Tiger Mount…* taken out of the note |
| `051.md` | gains **On Tiger Mount, the Snow Falls on Three Grades of Monks: two poems** — **check fails** |
| `094.md` | the heading *Addressed to a Monk Who Burned Books* taken out of the note |
| `095.md` | gains **Addressed to a Monk Who Burned Books: three poems** — **check fails** |
| `121.md` | the heading *The Second Year of Kanshō—Starvation* taken out of the note |
| `122.md` | gains **The Second Year of Kanshō—Starvation: three poems**; `Kanshō` in the poem's first line — **check fails** |

### C. No re-translation (2)

- `026.md` — `everbeleaguered` → `ever-beleaguered`. The Persian already reads
  it right: «همواره در معرضِ تهدید».
- `027.md` — `T’ien-pao` in the poem's last line, and two stray quotes. The
  Persian already has «ت’ین-پائو», taken from the note.

(Group B, markers only, is 011's shape; this batch has none.)

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in group A carries one or a
   `parity: offset` (checked when this spec was written).
3. **Check each heading's Persian against its siblings.** The five new
   headings are the set's own title, bold, under the first poem's heading.
   `029.md` and `076.md` already have the shape; the new ones should match
   them, and the title should match what the poems' `### شعر` headings in
   the same set already say.
4. **Group C by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated; `just check` green.
- [ ] The five heading-less notes (`021` `037` `050` `094` `121`) no longer
      end in the next set's title.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file; `025` carries [43] and `028` [45].
- [ ] Group C checked.
- [ ] Typeset PDF read for the touched files.

## Out of scope

Anything 010 has not read yet. `031`'s `[4]`, `050`'s unclosed quote and
`124`'s `Kansho` are recorded in 010 for their decades.
