# 011 — Re-translate what 010's second session repaired

**009 again, for the next batch. `source/` changed in 40 files; the Persian of
most of them is now stale.**

## Context

Spec 010's second session (poems 011–020, plus a marker re-read of 001–010)
fixed six defect classes in `generate_final_markdown.py`. See 010's
*Session 2* notes for what and why. Three of those fixes are book-wide, so
the 40 changed files run from `001` to `introduction-3`, not just the decade
that was read.

**`just check` is red on three of them.** `apparatus --check` reports that
`010`, `011` and `020` now have a verse quote with more hard breaks than the
Persian. `check_parity` still passes 147/147: every other change is inside
an existing block, and that is exactly why none of this was caught.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 2 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files, in three groups

### A. Re-translate: words or verse restored (14)

| file | what changed in the source |
|---|---|
| `001.md` | **`know`**, **`cloud`** restored; markers [1], [2] |
| `004.md` | marker [5] |
| `007.md` | the `[26]`/`[27]` labels; marker **[6], was [9]**; `Yüeh Küang` ×5 |
| `009.md` | markers [7], [8] |
| `010.md` | four-line verse quote re-broken; marker [10] — **check fails** |
| `011.md` | Lotus Sūtra couplet re-broken; [11], [12]; **[13], was [18]** — **check fails** |
| `014.md` | **`When Nan-ch’üan saw them`**; `remorseful`; `Fo-yen`; [17], [18] |
| `015.md` | **`see notes to poem no. 71.`** (the Persian dropped the sentence); `Sōtō`, `a burning`; [20]; **[21], was 24** |
| `018.md` | **`fūryū`** in the poem's last line, was `tryu`; `Chao-chou`; [25] |
| `019.md` | `I’ll`; `. . . :`; [26], [27], [29]–[32] |
| `020.md` | love-song couplet re-broken; **`Yüan-wu said,`**; `Yüan-wu`, `Wu-tsu`, `Hui Yüan`; [33]; **[34], was [33]** — **check fails** |
| `024.md` | **`the reader`** restored |
| `038.md` | **`scrambled`**, **`the coffin,`** restored; [54] |
| `058.md` | **`as the first`** restored |

### B. Markers only (11) — re-translate (decided)

The digits were already in `source/`, welded to a closing quote (`it."35`), and
are now bracketed. The Persian dropped most of them and left a few bare.

`025` [48] · `028` [35] · `037` [53] · `044` [61], [6], `Lan-ts’an` · `046` [64] ·
`061` [2] · `071` [82] · `080` [88] · `082` [89] ·
`introduction-1` [33], [45], plus `Tung-shan`, `Chao-yang`, `Sūtra` ·
`introduction-3` [68], [69], [89], [81], plus `Wu-tsu`, `Ta-mei`, `Lan-tsan`,
`Hui-chih`, `Kao-tang`, `Wu-shan`

**Decided 2026-09-23: re-run them.** Nothing sanctions inserting a marker by
hand, and the rules stay that way: no third hand-edit. All eleven go through
the pipeline like group A, `introduction-1.md` included, even though it is
67 K characters, about 73 chunks at 900, for two markers. Chunk sizes that
worked last time: `introduction-1.md` 900, `introduction-3.md` 2250
(`CLAUDE.md`). Run `introduction-1.md` with the Chrome profile to itself.

### C. No re-translation (15)

A name's Latin spelling changed and nothing else: `031` `036` `045` `057` `062`
`084` `094` `097` `101` `120` `121` `124` `133`. The Persian spells these
names in Persian script from `STYLE.md` §2, so a changed hyphen or macron in
the English does not reach it. Check each against §2. Conforming one is the
second sanctioned hand-edit.

`bibliography.md` (`Diamond Sūtra`) and `glossary-index.md` (`Yüeh Küang`) keep
their entries verbatim (spec 006), so each needs one word conformed by hand:
§2 again.

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** No file in groups A or B carries one or a
   `parity: offset` (checked when this spec was written).
3. **Group B through the same pipeline.** Short poem files first, then
   `introduction-3.md`, then `introduction-1.md` last and on its own.
4. **Group C by reading**, not by running anything.

## Acceptance criteria

- [x] Every group A file re-translated; `just check` green. `024` in session
      2, after its source was repaired.
- [x] Group B decided: re-translate, no new hand-edit.
- [x] Every group B file re-translated.
- [x] Group C checked against `STYLE.md` §2; the two back-matter words
      conformed.
- [x] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any file in groups A and B, **except `introduction-1`**, where the
      Persian has [43] and [50] and the source leaves them bare. Same class as
      `062` and `068`: a source defect, recorded in 010. (`024` agrees: its old
      Persian already carried its markers.)
- [x] Typeset PDF read for the touched files.

## Out of scope

Anything 010 has not read yet. The marker comparison lists files outside this
spec, and they wait for their decade.

## Implementation notes

### Session 1 — 39 of 40, one sitting

**Chunk sizes.** Most files at 4500. The exceptions, each chosen by reading
the drafts from each rung:

| file | shipped | why |
|---|---|---|
| `009` | 300 | Classic at 4500 and 900 (no ezafe, 7 blocks for 4); 400 went Classic in its last third. `CLAUDE.md` already said 300. |
| `014` | 900 | 4500 was Advanced but took the source's doubled `““When` as an opening quote and ran one «» from [15] to the end of the file, every inner quote turned into ”“. A quote cannot cross a chunk boundary. |
| `introduction-3` | 2250 | As last time. 62/62 blocks, every marker. |
| `introduction-1` | 900 | As last time. 106/106 blocks. Chrome profile to itself. |

**Two files have a Classic passage at every rung, and shipped anyway.** The
fallback is deterministic, so each one's Classic passage is the *same text*
the old file had. The re-translation restores what the source gained and
loses nothing:

- **`001`** — *taryn* through Tz'u-ming's students, at 4500, 900, 400 and 300.
  It is not the OCR damage in that passage (`taryn`, `fia`, `ryi#`): with
  those fixed in a scratch copy the model still fell back. Smaller rungs only
  added stray «...». Shipped 4500.
- **`037`** — the tail of the note at 4500 and 900 («بلو کلیف رکورد»); 400
  moved the Classic chunk next to `Rydzen: Ryozcens` instead, and 300 split
  blocks. Shipped 4500. «کیکان» looks like a tell and is not: it is *kikan*,
  the word the note is explaining.

`introduction-3`'s Eliot paragraphs, which render *allusion* «کنایه», are the
same case: word for word what spec 005 shipped.

### 024 — held back in session 1

No rung is clean. 4500: first chunk Classic, and `## ⟦2⟧` welded onto the
poem's last line. 2250 and 900: one Classic stretch each, and marker [38]
dropped. 400 and 300: Classic throughout, with «...» and a Hangul fragment in
the output. The damage (`’3? 69]`, `[4]°`, `Stitra`) sits exactly where [38]
is lost, so this is `CLAUDE.md`'s "stop — the input is the problem".

It is also the one file in this spec that 010 has not read: it is in decade
`021`–`030`, which is next. That decade will change `source/024.md` again, and
its re-translation spec should carry 024 — re-translating it now would be done
twice. The old `fa/024.md` stays: it lacks *the reader* and is Classic in
places, but its markers agree with the source.

### Paragraph joins

`038` joined *Rinzai had the steward…* to *P'u-hua put the coffin…*; `071` left
the *Chuang Tzu* quote on its own line with no blank line. Neither dropped
anything, so each was split back in scratch, as 009 did for `085`.

### §2

Every draft was conformed against its old file, as 009 did: ایکیو on almost
every file, and the usual ZWNJ-for-hyphen and dropped-apostrophe errors. The
count compares against the old file, so it cannot see a form both got wrong;
reading caught five that the old files had carried since 004 and 005 — P'ang and
Ch'üan in `028`, Ma Yüan in `025`, Tung-shan ×7 in `introduction-1`, and
Hsü-t'ang as «هسو-تانگ» in the same file. The first three are new rows in
`STYLE.md` §2. `introduction-3`'s T'ao Yüan-ming was matched to the rest of the
book («تائو»), not to §2.2, which wants «ت’ائو»: see *Left for other specs*.

**Group C** — `031`, `057`, `124`, `133` needed conforms; the other nine were
right. The PDF read found two that the name check had missed, in `031` and
`057`. `Yüeh Küang` stays «یوئه کوانگ» (`STYLE.md` §2): Wade-Giles has no
*küang* syllable, so there is no ü to carry.

**The PDF read found no typesetting fault.** It found source defects, which
are in 010 under *Found in passing by 011*.

### Left for other specs

- **T'ao is «تائو» in all 21 places the book names T'ao Yüan-ming**, never
  §2.2's «ت’ائو», though §2.2 cites that very name as its reason. A book-wide
  conform, not this spec's.
- **The model writes «...» before a poem number** — «شعر شماره‌ی... ۲۰۹»,
  «کوآن شماره... ۶۳» — in `001`, `014`, `019`, and in the old files too.
  Translator prose, so not a sanctioned hand-edit.

### Session 2 — 024, source first

Session 1's diagnosis held: the source was the problem. Read against the scan
(pp. 90–94), `024.md` had ten defects, not the three 011 listed, and one of them
was a wrong number: `dung ? [42]` is **41** in the print; the real 42 was the
`3` after *fragrant flowing water*. Also `(79` and `Pi` for the labels [70] and
[71], `Wu-tai`, `conJures`, `Fallen Hower`, and the three quoted poems (Hsüeh-tou's
tomb, kōan 96, Yün-men's verse) set a paragraph per line.

**Fixed in `generate_final_markdown.py`, isolated.** Ten typo rules, each
anchored on its own surrounding text and placed ahead of the general marker
rules, and three `VERSE_QUOTES` entries. `just split` against a snapshot of
`source/` changed `024.md` and no other file.

**The repaired source translated clean at 4500 on the first run**: 14/14 blocks,
all nine markers and labels, Advanced throughout. The rung that was hopeless
on the damaged text is the default on the repaired one. One draft repair: the
model ran lines 3 and 4 of Yün-men's verse onto one line, and it was broken
back in scratch before `restore`. §2 conformed as usual, plus Wu-t'ai →
«وو-ت’ای» (§2.2) and a Pinyin «جیانگ-هو» → «چیانگ-هو». PDF read: the three
verse blocks set as stanzas.
