# 026 — Re-translate `introduction-1`, piece by piece

**What is left of [025](./025-retranslate-introduction.md). `introduction-2`
and `-3` are done. `introduction-1` is the longest file in the book, and no
plain run of it is usable.**

## Context

025 re-translated `introduction-2` and `introduction-3` and found that the
plain pipeline cannot produce the two long files. Every chunk size either
drops a block, splits a quatrain into one-line blocks, or serves whole
chunks Classic. The fix for `introduction-3` was 006's prose-primer trick,
rebuilt as a piece harness (see 025's notes). It got through **with no
paragraph read as Classic**.

`introduction-1` passes the harness's structural gates. **It does not pass
reading.** Its Classic paragraphs carry none of the tells the gates look for,
and rejecting them by reading has been converging slowly. The session stopped
partway through the rejection passes. This spec finishes that work.

**`just check` is red on this one file:**

```
fa/introduction-1.md: 106 blocks, source has 119
fa/introduction-1.md: 0 hard line break(s), source has 31
```

`fa/introduction-1.md` is still the pre-024 translation. It is not touched
until a draft is accepted.

## What 025 established, and what this spec starts from

- **`source/introduction-1.md` is final.** 119 blocks, markers 1–57, 11
  verse quotes and 31 hard breaks. 025 added poem 538 as verse; see 025's
  notes, *The generator*.
- **Plain run at 900** (last time's size): *Come among the beasts to teach*
  (poem 73) **dropped**, two quatrains split into one-line blocks, about a
  dozen paragraphs Classic, and «ایککیو» ×17.
- **Harness at 2250**, which is 36 chunks: 119/119 blocks, markers 1–57, 31/31
  breaks, and no «ایککیو», on every pass.
- **The verb-prefix test does not settle it here.** `CLAUDE.md` says it does,
  following spec 004. In this session Classic joined «می‌» with a ZWNJ, like
  Advanced. Ezafe per paragraph, ZWNJ density, the rate of «یک», and
  guillemets were also measured on paragraphs already read and labelled.
  **None of them separates Classic from Advanced.** Reading is the only gate.
- **Classic here looks like this:** «یک بدنه سیاسی منحط» (*a degenerate body
  politic*), «اسقف‌های ذن» (*Zen prelates*), «وسایل نقلیه کوچک» (*Lesser
  Vehicle*), «مطمئناً، این یک گروه شعر غیرمعمول است که توسط…», a clause
  doubled («دیوانگی او را به جهانیان اعلام می‌کرد» twice), `unsui` left in
  Latin, and Latin digits in running prose («۱۴۷۰» as `1470`).

### Where the rejection passes stood

Paragraph numbers are lines of the stripped draft (`i1.v*.fa.md`).

| paragraphs | subject | best version seen |
|---|---|---|
| 3–7 | *Crazy Cloud*, the name | **v3** (halved, local primers). v4's fixed-primer version is Classic; v5's first paragraph is too, with its paragraphs 5–7 fine |
| 23 | *these were truly popular arts* | Classic in every version so far |
| 25, 27 | *degenerate body politic*; the Tōfukuji gate | **v4** |
| 29, 32 | *the Gozan was never*; *prelates* | **v5** |
| 44–48 | the Nempu; the Tokugawa tales; the sketch | **v3** |
| 127, 129 | *the Arhat*; *the enlightenment poem* | **v4** («ارابه‌ی کوچک») |
| 215–221 | Mori; *surely an unusual group of poems*; the Ōnin years | **v3/v4** for 215–217; **219 Classic in every version**; v5 regressed all four |

Every other paragraph read as Advanced in v2 and has not changed since.

## Requirements

1. **Build the draft with the piece harness**, not the plain pipeline.
   `strip`, then the harness, then `restore -o`. Check `pgrep -f
   "gtranslate.py|harness.py"` first. 006 said to move the harness into
   `tools/` the moment the Introduction needed it, which it now has.
   Decide that first. 025's notes describe it.
2. **Read every paragraph, not only the gate's failures.** Where a piece
   reads Classic, reject its cache key and rerun, and it moves to the next
   primer, then halves. Where a paragraph has been Classic behind every
   primer (23 and 219 so far), try more primers before giving up. If it
   stays Classic, record it here rather than patching it.
3. **Do not let a rejection regress a good neighbour.** Rejecting a whole
   piece re-translates all its paragraphs. v5 lost 215–217 that way. Halve
   first, then reject only the half that is Classic.
4. **Markers are Latin** (STYLE §4.2). The model persianises them sometimes,
   against what §4.2 records («[۳۲]»). The harness converts them back, as
   006 did for the notes' entry numbers. Correct §4.2's claim while you are
   there.
5. **Conform §2** (sanctioned edit 2). The draft spells these by ear:
   - *Ikkyū* «ایکیو» → «ایک‌کیو»;
   - *Shūon’an* «شوئون‌آن» → «شو-اون-آن», §2.5 and the table. **The old
     file had it wrong too.**
   - *Hsü-t’ang* «شو-تانگ» → «شیو-ت’انگ»;
   - *Daiō* → «دایئو», never «دایتو»;
   - *Yün-men* «یون‌من» → «یون-من»;
   - *Ken’ō* → «کن-او», by §2.5 (the old file had «کنو»);
   - *Arhat* «ارهات» → «آرهات», the book's form (26 occurrences);
   - *Giō*: the old file has «گیو», which the table does not cover. Pick one
     form and use it throughout.
   - Check *Wang Chang-ling*, *Chao-yang*, *Wei-shan*, *Tung-shan* and *Sōchō*
     against the table and the old file.
6. **Read the verse.** 11 quotes, poem 538 among them, each with its hard
   breaks. `restore` names any line that loses one.

## Acceptance criteria

- [x] `introduction-1` re-translated: 119 blocks, markers 1–57 in order, 31
      hard breaks.
- [x] Every paragraph read. None left Classic.
- [x] §2 conformed.
- [x] `just check` green: 153/153 on parity, normalize and anchors. That
      closes 025 and 024.

## Out of scope

`introduction-2` and `-3`, which 025 finished.

## Implementation notes

**Done in the session after 025's, from 025's scratchpad drafts.** Nothing was
re-run from scratch.

### Assembled paragraph by paragraph, not by more rejections

Rejecting a whole piece re-translates all its paragraphs, and v5 showed the
cost: a rejection aimed at one paragraph regressed its neighbours. But v2–v5
all pass the run-structure gate, so paragraph *i* is the same English
paragraph in every version. **The draft is built by picking, for each
paragraph, a version already read**, which is a selection among machine
outputs and not an edit. The picks, by 0-based paragraph index:

| paragraphs | version |
|---|---|
| 1–3 | v3 |
| 12, 13, 58, 59 | v4 |
| 14–16 | v5 |
| 21 | v2 |
| 22, 23, 96, 97 | v3 |
| every other paragraph | v2, which is identical in all four versions |

**Three paragraphs were Classic in every version**: 11 (*these were truly
popular arts*), 98 (*surely, this is an unusual group of poems*) and 99 (*the
time Ikkyū and Mori spent together*). Each was translated alone behind ten
primers: the four prose paragraphs before it, 025's fixed primer, and five
long paragraphs from `introduction-2` and `-3`. Each came back with at least
one Advanced candidate:
- **11:** 2 of 10 were Advanced. Candidate 3 was taken, with *without formally
  taking the tonsure* as «بی‌آنکه رسماً راهب شوند و موی سر بتراشند».
- **98:** 6 of 10 were Advanced. Candidate 4 was taken because it says *in his
  seventies* («هفتاد و چند سالگی»); candidate 7 read nicely but said «دههٔ هفتمِ
  عمر», his sixties.
- **99:** 8 of 10 were Advanced; candidate 7 was taken.

Then the whole file was read, all 273 lines. No Classic paragraph is left,
and no Latin digit stands outside a marker or a gloss.

### §2

- *Ikkyū* ×156.
- *Shūon’an* «شوئون‌آن» → «شو-اون-آن» ×10.
- *Hsü-t’ang* «شو-تانگ» → «شیو-ت’انگ».
- *Daiō* «دایو» → «دایئو».
- *Yün-men* → «یون-من».
- *Ken’ō* «کن‌ئو»/«کن‌او» → «کن-او».
- *Giō* «گی‌ئو» → «گیو», as the old file had it and by §2.4.
- *Tung-shan* «تونگ‌شان», and once «دونگ‌شان» from the Pinyin → «تونگ-شان»
  ×8.
- *Pai-chang* «پای‌چانگ», and «بای‌ژانگ» from the Pinyin → «پای-چانگ». That is
  8 against the source's 9: the model used a pronoun once.
- *Wei-shan* «وی-شان»; *Wang Chang-ling* «وانگ چانگ-لینگ».
- *Ch’ang-hsin* «چ’انگ-شین», *Ch’ang-men* «چ’انگ-من», *Ch’a-tu* «چ’ا-تو»,
  *Chiang-hsi* «چیانگ-شی», all by §2.1 and §2.2.
- *Zeami* «زآمی».
- *Nyoian*, *Yakushidō*, *Sumiyoshi* and *Katsuroan* as the old file had them.
- *Daitokuji* «دایتوکوجی» throughout.

### Also done

- STYLE §4.2 now records the persianised-marker exception.
- `CLAUDE.md` no longer says the verb-prefix test settles Advanced against
  Classic.

The harness is not in the repo. It lived in 025's scratchpad and served this
file only. **If a future long run needs it, 025's notes describe it**, and
006's advice stands: that is the point to put it in `tools/`.
