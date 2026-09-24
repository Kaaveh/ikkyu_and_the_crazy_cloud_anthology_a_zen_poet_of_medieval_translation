# 024 — The Introduction, read against the scan

**010's method, for the three files it ticked without reading.
`introduction-1/2/3`, PDF pp. 25–83, printed pp. 1–59.**

## Context

010's checklist marked `introduction-1/2/3` done for 005's CJK-bleed fix.
That fix was real. It removed 1,229 characters of Chinese column. But it
was not a read against the scan, and 010's session 12 found that out from
the endnote markers. The Introduction numbers its own notes 1–88, and the
sequence in `source/` is:

```
introduction-1: 1 2 3 4 5 8 19 12 13 16 17 18 19 21 22 29 24 2? 26 27 28 29 3° 31 33 …
introduction-2: 59 60 61
introduction-3: 63 65 66 97 68 69 70 72 3 74 76 7? 8 79 89 81 83
```

About thirty markers are wrong or missing, which is the Anthology's damage
before 010 read it. Checking them turned up two things that are bigger:

- **Every quoted poem is run together as prose.** The print sets each one
  as verse beside its Chinese original. `introduction-1/2/3` have no hard
  line break at all. Confirmed for *Ch’ang-men Spring Grass* (p. 13),
  Ikkyū's enlightenment poem (p. 18) and *Addressed to Reverend Yōsō*
  (p. 25). Seventeen pages have lines pairing English with CJK, and the
  pages where the OCR lost the CJK do not show up that way. Expect twenty to
  thirty poems. The fix is 010's: `VERSE_QUOTES`, one confirmed quote at a
  time, and `build_introduction()` must call `split_verse_quotes()`.
- **Local damage the Anthology's rules never reached**: `Gid` for *Giō*
  ×4, `kéan!>` (*kōan* with marker 15), `biwa hashi` for *biwa hōshi*,
  `Jodo Shinsht` for *Jōdo Shinshū*, `SGcho` and `Socho` for *Sōchō*,
  `Tofukuji`, `Daio`.

**The Persian carries all of it.** No checker sees any of it, because every
defect sits inside a block.

## Dependencies

010 (done but for its `just check`, which waits on 023). Nothing depends on
this except the edition.

## Requirements

1. **Read `introduction-1/2/3` against pp. 25–83.** The tooling is 010's:
   the page map, `pdftoppm -r 150 -gray`, 300–400 dpi for a doubtful digit.
2. **Markers first.** The sequence alone finds most of them. The table
   below is what session 12 of 010 confirmed on the page, so start there.
3. **Fix in the generator, never in `source/`.** Anchor every rule on its
   own text: `apply_typos` runs over the bibliography and glossary too, which
   stay verbatim.
4. **Verse quotes by 010 requirement 4**: confirmed text, not a heuristic.
   Each changes block count and turns `check_parity` red, which is expected.
5. **Record every changed file** and hand it to a re-translation spec.
   `introduction-1.md` is 67 K characters and shipped at 900. Budget it as
   the longest run in the book.

## What 010 session 12 already confirmed

Markers, each seen on its page (PDF numbers):

| marker | page | `source/` has | print |
|---|---|---|---|
| 6 | 29 | `anywhere.®` | `anywhere.6` |
| 7 | 31 | `fifteenth century.’` | `century.7` |
| 9 | 34 | `“Portrait of Ikkyū,9 is` | `Ikkyū,”9` |
| 10 | 34 | `historical sense. [19]` | 10 |
| 11 | 34 | `Reverend Ikkyū,”™` | `Ikkyū,”11` |
| 13 | 35 | `Southern Court. [13] a point of some importancce,` | `Court,13 … importancce.` |
| 14 | 37 | `neglect are deep.!4`, the poem's last line | 14 |
| 15 | 37 | `kéan!>` | `kōan15` |
| 41 | 49 | `interview. [4]!` | 41 |
| 43 | 50 | `leprosy43` | 43 |
| 50 | 52 | `Mori.“50` | `Mori.”50` |
| 51 | 53 | `Ikkyū. [5]!` | 51 |

Candidates located in the OCR, pages not yet looked at: 23 (`him in. [29]`,
p. 41), 25 (`Sings. [2]?`, p. 42), 30 (`himself. [3]°`, p. 44), 32 (`(no.
73)?`, p. 45), 39 (`(no. 84) [89]`, p. 48), 40 (`(no. 85) [4]°`, p. 49),
47 (`Sumiyoshi. [4]?`, p. 52), 57 (`existence.’”5?`, p. 59), 67
(`[97]`, p. 68), 71 (`hedge.”?!`, p. 73), 73 (`knew.”? [3]`, p. 74), 77
(`[7]?`, p. 76), 78 (`[8]`, p. 76), 80 (`Cloud.’’ [89]`, p. 79), 82
(`China).®?`, p. 80), 84 (`ruins,84`, p. 82). Not located: 20, 58, 62, 64,
75.

Local damage, confirmed:

- p. 26: `Jikaishi` → *Jikaishū*; `Jodo Shinsht` → *Jōdo Shinshū*;
  `Katsuroan、 “Blind Donkey Hermitage.` → `Katsuroan, “Blind Donkey
  Hermitage.”`.
- p. 28, 29: `Shuonan` ×2 → *Shūon’an*; `SGcho` → *Sōchō*.
- p. 4: the `、` after `heaven.` is a speck.
- p. 7: `Tofukuji` ×2 → *Tōfukuji*.

Carried from 010's *found in passing* lists:

- `introduction-1`: `interview. [4]!`, `leprosy43`, `Mori.“50` (above);
  `Shnonan`/`Shuonan` for *Shūon’an*, which 014 fixed in `131`; `Jikaishi`.
- `introduction-3`: `my ruins,84`, bare after a comma; `Ch Yüan` ×4 for
  *Ch’ü Yüan*, p. 71, which session 8 fixed in `071` only; the `、` after
  `“Rain`.

## Acceptance criteria

- [ ] `introduction-1/2/3` read against the scan, every defect fixed in the
      generator or recorded here as a deliberate exception.
- [ ] Markers 1–84 in sequence across the three files, with no gap and no
      wrong number.
- [ ] Every quoted poem in the Introduction is verse in `source/`.
- [ ] Every changed file listed in a re-translation spec.
- [ ] `just check` passes after that spec has run.

## Out of scope

Translating anything. `introduction-4`, which 010 read in session 12.
