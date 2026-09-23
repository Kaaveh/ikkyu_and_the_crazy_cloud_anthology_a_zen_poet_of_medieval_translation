# 017 — Re-translate what 010's sixth session repaired

**015 again, for the next batch. `source/` changed in 9 files; six need
re-translating.**

## Context

Spec 010's sixth session (poems 135–175, files `051`–`060`) fixed local
damage in `generate_final_markdown.py`. See 010's *Session 6* notes for what
and why. Eight changed files are in the decade. `050` is not: it is the
first poem of the set whose title the session corrected.

**`just check` is red on two of them.** `apparatus --check` reports `059`
and `060` one hard break over: the second line of each wrapped title had
become the poem's first verse line, and the Persian translated it as one.
Block parity is unchanged. Every other change is inside an existing block
and fails nothing.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 6 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (6)

| file | what changed in the source |
|---|---|
| `050.md` | title *Three Poems to Show the Monks of My Circle (I)*, was *…the Assembly* — **the Persian heading has «سه شعر برای ارائه به جمع»**; its own set heading already says «راهبانِ حلقهٔ من» |
| `051.md` | the same title, (II) — «…در جمع (۲)» |
| `052.md` | the same title, (III) — «…در جمع (III)», a Latin numeral besides; `Tōzan` ×3, `“sword mountain”` closed |
| `058.md` | `madman`, was `madinan` — **the Persian has «دیوانه‌ای از اهل مدینه», a madman from Medina** |
| `059.md` | the title's `K’uei-chi` gone from the verse — **check fails**; marker **[71]**, was `?!`, which the Persian dropped; `K’uei-chi` ×3 (`K'uei-chi's`, `K uei-chi`, `Kucichi`); `He just`; `Lotus Sūtra` |
| `060.md` | the title's `Soe Daisho` gone from the verse — **check fails**; `Yōsō`, was `YsQ`; `“man from P’u-chou”` |

### B. No re-translation (3)

- `054.md` — markers [66] and [67] gain their closing quotes, as do
  `compassion.”` and `“far-out.”`; `Vimalakirti Sūtra`; `compassion...`.
  The Persian closes every quote already: «…خیال نیست.» [66]», «…آرام
  کردم.» [67]».
- `055.md` — `flames`, was `Hames` ×2, and the quote closed. The Persian has
  «افکندنِ تن به کام شعله‌ها» in quotes, and «شعله‌ها» for both.
- `057.md` — `I am`, was `1 am`, in the poem. The Persian read through it:
  «یقین دارم».

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in group A carries one or a
   `parity: offset` (checked when this spec was written).
3. **§2 against the old files and the table.** *K’uei-chi* is «ک’وئی-چی»
   and *Yōsō* «یوسو»; the old `059` and `060` have both right. *Tōzan*
   has no row: the old `052` gives «توزان».
4. **The three titles read as one set.** `050`–`052` are one set heading
   translated three times; the old files gave it «به جمع» once and «در جمع»
   twice. Take one rendering of *the Monks of My Circle* and hold it, and
   keep it to what `050`'s bold set heading says.
5. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] Every group A file re-translated; `apparatus --check` green on `059`
      and `060`.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `059` carries [70] and [71].
- [ ] No «مدینه» in `058`.
- [ ] `050`–`052`'s headings name the monks of the circle, not an assembly,
      in one wording.
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet. `059`'s prose after its block quote
(*Hence, he became known…*) and `054`'s block quote broken after its first
line: 010's *Prose block quotes* shape, left alone book-wide.
