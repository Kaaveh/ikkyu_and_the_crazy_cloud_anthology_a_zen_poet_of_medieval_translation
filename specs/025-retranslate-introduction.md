# 025 — Re-translate the Introduction

**What 024's read changed: `introduction-1`, `-2` and `-3`. Three files,
and the first of them is the longest run in the book.**

## Context

[024](./024-introduction-read.md) read the Introduction against the scan.
Its *Session 1* notes say what changed and why:

- about thirty endnote markers fixed;
- 25 quoted poems set back as verse;
- paragraph breaks recovered;
- four passages of lost words given back;
- some forty names restored with their diacritics.

**`just check` is red** on `check_parity`, and only for these three files:

```
fa/introduction-1.md: 106 blocks, source has 120
fa/introduction-2.md: 20 blocks, source has 19
fa/introduction-3.md: 62 blocks, source has 66
```

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

024 session 1, which is committed. `source/` is gitignored, so if it
predates that commit, rebuild it first:

```bash
.venv/bin/python generate_final_markdown.py && just split
```

`just split` alone does not rebuild the monolith.

## The files

| file | chunk size last time | what changed in the source |
|---|---|---|
| `introduction-1.md` | 900 | markers 1–57, most of the 25 verse quotes, Giō, Shūon’an, Sōchō, Daiō (not *Daitō*), and `IKkyu` ×6, which [023](./023-retranslate-session-12.md) group C deferred to this spec |
| `introduction-2.md` | 4500 | markers 58–62, the words given back on p. 62 (`as we read, “It must have been`), and its verse quotes |
| `introduction-3.md` | 2250 | markers 63–84, Ch’ü Yüan ×4, Kao-t’ang, Yang-t’ai, Sung Yü, and its verse quotes, among them Yün-men’s two sayings |

## Requirements

1. **Use the pipeline in `CLAUDE.md`, one file at a time**: `strip`, then
   `gtranslate.py -w --raw`, then `restore -o`. Run `pgrep -f gtranslate.py`
   first. Judge Advanced against Classic on ezafe per paragraph, then by the
   verb-prefix test, never by the picker.
2. **Start at last time's chunk size** (table above), then go down the
   ladder: 4500, 900, 400, 300. Choose on block parity, and prefer a split
   to a drop.
3. **Every verse quote keeps its hard breaks.** `restore` names any line
   that lost its break. Fix those in the scratch draft, never in `fa/`.
4. **Check the markers.** For each file, the `[N]` sequence in `fa/` must
   equal the one in `source/`.
5. **Read before accepting.** 005 found `introduction-3` rendering
   *allusion* as `کنایه` rather than `تلمیح`, the chapter's own title.
6. **Conform proper nouns to `STYLE.md` §2** (sanctioned edit 2). Where the
   table is silent, keep the old file's spelling.

## Acceptance criteria

- [ ] All three files re-translated, and their block counts match
      `source/`. **Two of three:** `introduction-2` 19/19 and `-3` 67/67.
      `introduction-1` moved to [026](./026-retranslate-introduction-1.md).
- [ ] Markers 1–84 in the Persian, in the same order as `source/`.
      **58–84 done.** 1–57 are 026's.
- [x] All 25 verse quotes set as verse. In `source/` that took a generator
      fix, since 024 had set 23. Both files done here carry theirs (2 + 12);
      `introduction-1`'s 11 are 026's.
- [ ] `just check` is green. Red on `introduction-1` alone, which 026 closes,
      and that also closes 024.

## Out of scope

`introduction-4`, which 023 re-translated.

## Implementation notes

**Stopped with `introduction-1` unfinished. The rest is
[026](./026-retranslate-introduction-1.md).**

### `introduction-2`: plain run at 2250

| size | result |
|---|---|
| 4500 | parity and markers clean, and verb prefix clean, but the last four paragraphs are Classic: «موشکافی دقیق و موشکافانه‌ای انجام دهند», *Self-Consuming Artifacts* as «مصنوعات خودمصرف‌کننده» |
| 900 | worse: «بیانیه لانه پرنده در تضاد با آن موضع ارتدکس»; the last paragraph Classic |
| 400 | Classic throughout |
| **2250** | **taken.** 19/19 blocks, markers 58–62, verb prefix 61:2, every paragraph read as Advanced |

**Left as the model gave it:** Niao K’o's dates, *(741-824)*, dropped at 2250
and at 4500. *It must have been something the Elder sang* is back
(«باید سخنی بوده باشد که آن پیرمرد در حال مستی سروده است»).

### `introduction-3`: no plain run is usable, so a piece harness

| size | structure | «کنایه» | «ایککیو» |
|---|---|---|---|
| 4500 | a paragraph **dropped**, one quatrain split into four blocks | 21 | 2 |
| 2250 | one quatrain split, two verse lines run together | 12 | 4 |
| 900 | three quatrains split, one of them missing a line | 16 | 6 |

At 2250 the Classic output was two whole chunks. **Chunk 3 opens with Li Yi's
quatrain**, and chunk 22 is the short tail. A chunk that starts with verse is
served Classic, as a chunk of bare citations was in 006. **006's prose primer
fixes it:** behind the prose paragraph before it, chunk 3 came back Advanced,
with the quatrain one block and *allusion* «تلمیح».

**The harness**, in the session scratchpad and not in the repo (026 decides
that):
- `split_chunks(text, 2250)`. Each chunk goes behind a primer, the last prose
  paragraph before it, and the primer's translation is dropped.
- One browser session for the whole run, reusing `gtranslate`'s own helpers.
  Every call is cached by the SHA-1 of its input.
- Each piece is gated on:
  - run structure equal to the English;
  - the `[N]` sequence;
  - no «ایککیو»;
  - no more «کنایه» than the English has *euphemism*/*irony*;
  - no paragraph with space-joined «می» dominating;
  - at most two Latin words outside glosses;
  - some Persian.
- A failing piece tries the next of three local primers, then a fixed primer
  (Po Chü-i's paragraph from `introduction-2`, Advanced in every run), then
  plain, then is halved at a paragraph boundary.
- Two gate bugs cost a run each:
  - `می [آ-ی]` matches words that end in «ی» («قدیمی به»); the pattern is
    `(?<![آ-ی])ن?می [آ-ی]`.
  - The model sometimes persianises a bracketed marker («[۳۲]»), which STYLE
    §4.2 says it never does. The harness converts them back, as 006 did for
    `notes.md`'s entry numbers.

**Result:** 67/67 blocks, markers 63–84, 30/30 breaks. «تلمیح» ×44, «کنایه»
×1 (*euphemism*, correct), «ایککیو» 0. Read in full. Every paragraph is
Advanced. **Left as the model gave it:** *Blue Cliff Record* as
«بلو کلیف رکورد», as in `037` and `notes`.

### The generator: two poems and a title 024 missed

024 records 25 verse quotes set; `source/` had 23. **Poems 538 and 107 were
silent no-ops in `INTRO_VERSE`**: `split_verse_quotes()` joined lines with
`\s+` but matched spaces *inside* a line literally, and the OCR had put
each poem's `(no. N)` in a paragraph of its own. A space inside a line now
matches any whitespace too.
The title of poem 57, *The Plum Ripened*, was fused onto the end of the
paragraph before it. There is now an `INTRO_TYPOS` rule on p. 68.

`source/` changed in those two files only. `introduction-1` went from 120 to
119 blocks and gained 3 breaks; `introduction-3` went from 66 to 67 blocks
and gained 3 breaks.

### §2, conformed

- `introduction-2`: *Po Chü-i* «بو/پو چو-یی» → «پو چیو-ای» (×11); *Ikkyū*
  (×9); *Niao K’o* «نیائو ک’و»; *Ch’uan Teng Lu* «چ’وآن تنگ لو»;
  *Vimalakīrti* «ویمالاکیرتی».
- `introduction-3`:
  - *Ikkyū* ×42;
  - *Ch’ü Yüan* «چو یوان» → «چ’یو یوآن» ×15;
  - *T’ao Yüan-ming* «تائو یوان‌مینگ» → «ت’ائو یوآن-مینگ» ×17. **The old
    file had «تائو» too.**
  - *Kao-t’ang* «کائو-ت’انگ», *Kao-ch’iu* «کائو-چ’یو», *Yang-t’ai*
    «یانگ-ت’ای», which 024 restored and §2.2 applies to;
  - *P’eng* «پ’نگ» (the old file had «پِنگ»);
  - *T’ien-t’ai* «تین-تای», the table's form (the old file had «تی‌ین-تای» ×7);
  - *Yün-men* «یون-من», *Lan-ts’an* «لان-تس’ان», *Hsiang-nan* «شیانگ-نان»,
    *Yüan-wu* «یوآن-وو», *kōan* «کوآن», *Ta-mei* «تا-می», *Daitokuji*
    «دایتوکوجی»;
  - *Hui-ssu* «هوی-سو» and *Wu Teng Hui Yüan*, as the old file had them;
  - *Arhat* «آرهات», the book's form, 26 occurrences, never the table's
    suggested «اَرهَت».

`just fix` normalised both files (ASCII quotes and stray ZWNJs).
