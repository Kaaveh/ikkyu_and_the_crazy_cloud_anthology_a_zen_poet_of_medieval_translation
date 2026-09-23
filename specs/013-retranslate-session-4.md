# 013 — Re-translate what 010's fourth session repaired

**012 again, for the next batch. `source/` changed in 10 files; four need
re-translating, one needs a §2 conform, and `038` belongs to 014.**

## Context

Spec 010's fourth session (poems 091–115, files `031`–`040`) fixed local
damage in `generate_final_markdown.py`. See 010's *Session 4* notes for what
and why. Unlike sessions 2 and 3, nothing here is book-wide: every changed
file is in the decade.

**`just check` is red on three of them.** `apparatus --check` reports `031`,
`037` and `038` short of hard breaks: each gained a quoted poem set as verse.
`check_parity` reports `038` a block over. Every other change is inside an
existing block and fails nothing.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 4 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

**Before or after 014, not during.** 014 renumbers every file after `038`,
so `039` and `040` here are `041` and `042` once it has run. Nothing here
depends on 014; if 014 goes first, use the new names.

## The files

### A. Re-translate (4)

| file | what changed in the source |
|---|---|
| `031.md` | marker **[47], was [4]** — the Persian carries `[4]`; Tu Fu's couplet set as verse — **check fails**; *Hui*, `I’m`, `in a poem` |
| `034.md` | marker **[50]**, which the Persian dropped; the closing quote after `the hermitage,` |
| `037.md` | Ch'u Ssu-tsung's quatrain set as verse — **check fails**; `Ryōzen: Ryōzen’s style`, was `Rydzen: Ryozcens`; `opportunity` |
| `040.md` | marker **[60], was [6]°** — the Persian carries `[6]`; `Shōen` |

### B. §2 conform (1)

- `039.md` — «شوین» for *Shōen*, where `040.md` has «شوئن». §2.4 drops the
  macron and §2.8's «دایئو» spells the hiatus with ئ, so «شوئن» is the form.
  A sanctioned hand-edit (`CLAUDE.md`). If 040's re-translation comes back
  with something else, conform both to «شوئن».

### C. No re-translation (4)

- `032.md` — two stray quotes around *Katsu*. The Persian has «کاتسو» both
  times.
- `033.md` — a stray `’` after `charlatan.”`. The translator renders `«»`
  either way.
- `035.md` — `sufficient`, was `sufhcient`. The Persian read through it.
- `036.md` — `Ryōzen`, was `Ryozen`. §2.4: «ریوزن» either way, and that is
  what the Persian has.

### Not here

- `038.md` — marker [57], a quoted poem, five local repairs, **and poems 111
  and 113 inside it**. Re-translating it now would be thrown away when 014
  splits it into three files. 014 owns it.

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in group A carries one or a
   `parity: offset` (checked when this spec was written).
3. **Group B by hand, group C by reading.**

## Acceptance criteria

- [ ] Every group A file re-translated; `apparatus --check` green on `031`
      and `037`.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `031` carries [47], `034` [50], `040` [60].
- [ ] *Shōen* is «شوئن» in `039` and `040`.
- [ ] Group C checked.
- [ ] `just check` green except `038`, which stays red until 014.

## Out of scope

`038.md` — 014. Anything 010 has not read yet.
