# 020 — Re-translate what 010's ninth session repaired

**019 again, for the next batch. `source/` changed in 3 files; one needs
re-translating.**

## Context

Spec 010's ninth session (poems 280–344, files `081`–`090`) fixed local
damage in `generate_final_markdown.py` and added Lady Pan's fan poem to
`VERSE_QUOTES`. See 010's *Session 9* notes for what and why. All three
changed files are in the decade.

**`just check` is red on one file.** `086`'s fan poem is one block of ten
lines now, where it was the tail of a paragraph and two paragraphs more. So
`check_parity` reports `fa/086.md: 11 blocks, source has 10`, and
`apparatus --check` reports `3 hard line break(s), source has 12`. The
marker comparison in 010's *Tooling* disagrees on `086` too.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 9 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (1)

| file | what changed in the source |
|---|---|
| `086.md` | marker **[91]**, was `many. [9]`. **The Persian has [9]**. Marker **[92]**, left bare, which the Persian carries as a bare «۹۲». **Lady Pan's fan poem set as ten lines of verse**; the Persian runs it into three prose paragraphs. In the *Chuang Tzu* passage: `I’ll`, `I’m` and `you’d`, which were `Ill`, `Tm` and `youd`. Also three quotes made single, and `store.’”` closed. The Persian's quotes there are garbled: `»وو«`, `"من`, `.«»` |

### B. No re-translation (2)

- `084.md` — the *I Ching* quote gets back `,”` after *Great* and `“`
  before *What is it?*, and closes `”` for `’’`. The Persian already has
  «مهارِ نیروی عظیم» and «آن چیست؟ نیک‌بختیِ عظیمِ راهِ آسمان.» [89].
- `087.md` — `"objects to` becomes `“objects” to`. The Persian already
  has «موضوعات/پدیده‌ها» in guillemets.

## Requirements

1. **Group A through the pipeline**, as `CLAUDE.md` describes: `strip`,
   `gtranslate.py -w --raw`, `restore -o`. Check `pgrep -f gtranslate.py`
   first. Judge the draft on ezafe, not the picker.
2. **No §1.4 marker to re-apply.** Check that `086` carries none and no
   `parity: offset` before running.
3. **§2 against the old file and the table.** *Chien-ho* has a row, from
   this file (016): «چین-هو». So do *Chuang Chou* and *Chuang Tzu*,
   *Ch’uan Teng Lu* and *Hsü-t’ang Lu*. *Lady Pan* is «بانو پان», as in
   `073`.
4. **The fan poem is verse, and restore sets it.** STYLE.md §3.3 says a
   quoted poem is set the way `source/` sets it. If the model runs the lines
   together, `restore` refuses and names them. Break the draft in `/tmp`,
   as `CLAUDE.md` says, and do not touch `fa/`.
5. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] `086` re-translated.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no
      disagreement for `086`: [90] [91] [92] [93].
- [ ] `086`'s fan poem is ten lines of verse.
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `090`'s title (poem 344, `Untitled` where
the Index gives one) is 014's open question, for all three such files at
once.

## Implementation notes

_None yet._
