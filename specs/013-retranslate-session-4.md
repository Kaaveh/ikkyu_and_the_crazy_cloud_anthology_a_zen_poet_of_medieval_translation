# 013 — Re-translate what 010's fourth session repaired

**012 again, for the next batch. `source/` changed in 10 files; four need
re-translating, one needs a §2 conform, and `038` went to 014.**

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

**014 has run**, and renumbered every file after `038`. The names below
are the new ones: what 010's session 4 read as `039` and `040` are `041`
and `042`.

## The files

### A. Re-translate (4)

| file | what changed in the source |
|---|---|
| `031.md` | marker **[47], was [4]** — the Persian carries `[4]`; Tu Fu's couplet set as verse — **check fails**; *Hui*, `I’m`, `in a poem` |
| `034.md` | marker **[50]**, which the Persian dropped; the closing quote after `the hermitage,` |
| `037.md` | Ch'u Ssu-tsung's quatrain set as verse — **check fails**; `Ryōzen: Ryōzen’s style`, was `Rydzen: Ryozcens`; `opportunity` |
| `042.md` | marker **[60], was [6]°** — the Persian carries `[6]`; `Shōen` |

### B. §2 conform (1)

- `041.md` — «شوین» for *Shōen*, where `042.md` has «شوئن». §2.4 drops the
  macron and §2.8's «دایئو» spells the hiatus with ئ, so «شوئن» is the form.
  A sanctioned hand-edit (`CLAUDE.md`). If 042's re-translation comes back
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

- `038.md` — split in three and re-translated by 014.

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in group A carries one or a
   `parity: offset` (checked when this spec was written).
3. **Group B by hand, group C by reading.**

## Acceptance criteria

- [x] Every group A file re-translated; `apparatus --check` green on `031`
      and `037`.
- [x] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `031` carries [47], `034` [50], `042` [60].
- [x] *Shōen* is «شوئن» in `041` and `042`.
- [x] Group C checked.
- [x] `just check` green.

## Out of scope

Anything 010 has not read yet.

## Implementation notes

### One sitting, three of four at 4500

**Every draft came back Advanced.** No space-joined verb prefix in any of them.
The 0-ezafe lines were all verse. `031` and `037` gained their quoted poems as
four lines of verse each; restore took all four drafts first time.

**`034` went to 400, for a typo, not for Classic.** At 4500 the note read
«باید با آن دست‌وپنج نرم کنیم», which is a dropped letter and not something
either sanctioned hand-edit covers. Re-running at 4500 gave the same output,
byte for byte. 900 did too: the file is 801 characters, so it is one chunk at
either size. 400 split it, came back Advanced with the same block count, and
reads «دست‌ و پنجه» (the ZWNJ was stripped by `just fix`). Same ladder, second
kind of failure: it moves the model off a bad reading as well as off Classic.

**§2, conformed against the old files and the table:**

- `031`: کوی-تسونگ → کوئی-تسونگ ×7, «وو تِنگ هویی یوان» → «وو تنگ هوی یوآن»,
  «دو فو» → «تو فو», one ویمالاکی‌رتی, بودی‌ساتوا ×2 → §2.7's بودیساتوا
- `034`: «شو-تانگ لو» → «شیو-ت’انگ لو»
- `037`: ایکیو → ایک‌کیو ×3, «چو سو-تسونگ» → «چ’و سو-تسونگ», «سان تی شی» →
  «سان ت’ی شی», and the model's own «تای‌شوآن‌جینگ» → «ت’ای شیوآن چینگ»
- `042`: شوئِن → شوئن, «سوما شیانگ‌جو» → «سو-ما شیانگ-جو», «وِن‌جون» →
  «ون-چیون», «وِن شوآن» → «ون شیوآن»
- `041` (group B): شوین → شوئن

The new forms are in `STYLE.md` §2 under spec 013.

**One edit made and taken back.** `037`'s draft glosses *The Great Mystery* as
`(یا *تای‌شوآن‌جینگ* / *Taixuanjing*)`. I first deleted the parenthetical
as Pinyin. §2.9 keeps the model's glosses and does not correct them. So it went
back in, with only the Persian half conformed to §2.1.

**Left as the model gave it:** `037`'s «بلو کلیف رکورد». The book has four
renderings of the *Blue Cliff Record* and §2 settles none of them. It is a
title, not a transliteration rule, and so it is for 007's read, not a conform
here.

**Result:** `just check` green, 153/153 on parity and anchors. The marker
comparison disagrees only on `064`, `070` and `introduction-1`, 010's known
three (`062` and `068` before 014 renumbered). `031` carries [47], `034` [50],
`042` [60].

### Group C

All four read. `032` has «کاتسو» both times. `033` closes the charlatan quote
cleanly: «…شیاد بوده‌ام.». `035` reads «همین امر برای ایجاد آشوبی بزرگ در
طریقت ما کافی بود.» `036` has «ریوزن». Nothing to conform.

The typeset PDF was not read. This spec's criteria do not ask for it, unlike
012's.
