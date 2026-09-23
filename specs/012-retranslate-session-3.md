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

- [x] Every group A file re-translated; `just check` green.
- [x] The five heading-less notes (`021` `037` `050` `094` `121`) no longer
      end in the next set's title.
- [x] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file; `025` carries [43] and `028` [45].
- [x] Group C checked.
- [x] Typeset PDF read for the touched files.

## Out of scope

Anything 010 has not read yet. `031`'s `[4]`, `050`'s unclosed quote and
`124`'s `Kansho` are recorded in 010 for their decades.

## Implementation notes

### One sitting, all 13 at 4500

**Every file came back Advanced at the first rung.** No space-joined verb
prefix in any draft (the six hits in `038` are «نمی» and «تمامی», not
prefixes), and `030`'s zero-ezafe note paragraphs read as ordinary
declarative Persian, not Classic: subjects present, names transliterated,
nothing doubled. `037` is the file 011 found Classic at every rung in the
tail of its note; this time the tail reads Advanced.

**Two block joins, split back in scratch**, as 011 did for `038` and `071`:

- `028` — the kōan's first sentence and the rest joined by a single newline.
  That is the paragraph break 010 records as a source defect (*Prose block
  quotes break mid-quote*), so the model was right and parity wanted it back.
- `038` — «…ترک کنم.» and «پس از آنکه…» run into one paragraph.

**§2, conformed against the old files.** ایکیو → ایک‌کیو (`021` `030` `037`
`038` `050`); `028` lost P’ang ×6, Ch’üan ×3 and Hsüeh-tou, the three rows
spec 011 added to §2 for this very file; `038` P’u-hua ×8, Hsü-t’ang ×3,
Hui-neng, *Ch’uan Teng Lu*; `050` Hsü-t’ang; ZWNJ-for-hyphen in `021`
(*Shih-shih Chi-ku Lüeh*), `025` (Kung-sun), `051` (Shao-lin), `094`
(Chao-chou ×2), `095` (Shih-huang), `121` (Ch’ang-an); `037` Ch’u Ssu-tsung;
`030` «کریزی کلاود» → «ابر دیوانه» and «دایتوکو-جی» → «دایتوکوجی». `just fix`
took a tatweel out of `021` and an ASCII quote out of `038`.

**Result:** `check_parity` 147/147, `just check` green. The marker
comparison disagrees only on `062`, `068` and `introduction-1`, the three
010 already records.

**PDF read** (pp. 77–78, 86, 88, 96, 110, 159, 186 of the typeset book): the
five set headings set bold under their poem heading, the split paragraphs
hold, and the Latin glosses render in place. `038`'s `1 |` is set as a line
of poem 111: the source defect 010 has for decade `031`–`040`.

### Requirement 3 could not be met as written

The siblings disagree with each other, not only with the new headings:
`023` has «کلام مقدس، آلودگی را می‌زداید» against `022` and `024`'s «متون
مقدس آلودگی را می‌زدایند»; `096` has «به آتش کشید» against `095` and
`097`'s «سوزاند»; `052` has «بر فراز کوه ببر… سه دسته» against `051`'s «بر
کوه ببر… سه مرتبه»; and the set numbering is `(I)` in some and `(۱)` in
others. Each new set heading matches its own poem's title. Retitling a
sibling is translator prose, not one of the two sanctioned hand-edits, so it
is left, and recorded here for 007's read.

### Group C

`026` and `027` read: the Persian of each already carries what the source
gained. Nothing to conform.
