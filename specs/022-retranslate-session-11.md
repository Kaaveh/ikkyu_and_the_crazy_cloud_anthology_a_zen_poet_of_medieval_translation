# 022 — Re-translate what 010's eleventh session repaired

**021 again, for the last of the Anthology. `source/` changed in 26 files;
14 need re-translating.**

## Context

Spec 010's eleventh session (poems 390–839, files `101`–`141`) fixed local
damage in `generate_final_markdown.py`. It added seven verse quotes to
`VERSE_QUOTES` and one paragraph opening to `PARA_STARTS`, and it gave
poems 344, 384 and 605 the Index's titles. See 010's *Session 11* notes for
what and why. Twenty-four changed files are in the range; `090` and `097`
changed for their titles.

**`just check` is red.** `check_parity` reports six files:

```
fa/101.md: 8 blocks, source has 6
fa/109.md: 5 blocks, source has 6
fa/113.md: 7 blocks, source has 6
fa/126.md: 12 blocks, source has 5
fa/139.md: 9 blocks, source has 8
fa/141.md: 5 blocks, source has 6
```

`apparatus --check` will report hard breaks on those with a verse quote,
`117` among them. The marker comparison in 010's *Tooling* disagrees on
`103`, `125` and `139`.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 11 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (14)

| file | what changed in the source |
|---|---|
| `090.md` | title: *Two Pieces of Skin and One Set of Bone*, was `Untitled [Two pieces of skin and one set of bone]` |
| `097.md` | title: *Utterly Absorbed in the Dream of Wu-shan*, was `Untitled [Utterly absorbed…]` |
| `101.md` | **Po Chü-i's grass poem set as eight lines of verse**, which had run two lines to a paragraph. `Po Chü-i` was `Po Chit-i`; `pāpiyān` was `papiyan`; `Off.”` was `Off.”’` |
| `103.md` | marker **[101]**, left bare as `“Yes, yes. 101`. **The Persian dropped it.** `“Here, Master?”:` was `”’:` |
| `105.md` | `on pp. 51-53`, was `On ppab1=53`. **The Persian carries it**: «در صفحه ۵۳ (ppab1=53)». Also `I want`, `generations,”`, curly quotes on *Be that as it may, you’ve*, and `ease`, was `casc` |
| `109.md` | the afterword is **two paragraphs**, split at *The poems concerning Mori*. `Ch’u’s Pavilion` was `Cs Pavilion`; `objective fact` was `objective. fact` |
| `113.md` | three lines of "Everlasting Sorrow" set as one verse block, which had been a paragraph per line |
| `117.md` | the cowherd's couplet set as verse; `Yakushidō` ×2, was `Yakushido`; `human being.” But`, which had lost its closing quote |
| `125.md` | marker **[109]**, was a bare `109`. **The Persian has a bare «۱۰۹».** `Sōseian` was `Sdseian`, and **the Persian carries «سادِسی‌آن» (Sdseian)** |
| `126.md` | title: *Tu-ling’s Flowers Sprinkling Tears*, was `Untitled [Would that it were…]`. **Tu Fu's "Spring View" set as eight lines of verse**, which had been a paragraph per line. The poem's second line ends `passable.`, was `passable. ;`. `“Spring View,”` was `,”’` |
| `130.md` | `and instructed`, was `and «instructed`. **The Persian carries the stray mark**: «و «آنها را با آن راهنمایی کردم و گفتم:», with an opening that never closes. `Bunshō` was `Bunsho` |
| `135.md` | `Musō` and `Musū`, were `Muso` and `Musi`. **The Persian has «موسی» for *Musi***, which reads as Moses. `“Dream”;`, `“Dream Window,”` and `“Dream Chamber”` were `’’`, `,’` and `”’` |
| `139.md` | marker **[114]**, was `[113]`. **The Persian has [113] twice.** The *Wakan Rōei Shū* couplet and **Tu Fu's "Moonlight Night"** are set as verse, and the poem's title is a paragraph of its own. The three Dream monks as in `135`, plus `Musū Ryōshin`, `Tōfukuji` ×2 and `Tenryūji`. The old Persian has «موسو» for both Musō and Musū. Also `fifth-watch` (was `Sifth-watch`), `Ch’ang-lo` (was `Cl’ang-lo`), `Wakan Rōei Shū:` (was `Wakan Roei Shi: ;`), `5:00 A.M.` and `moonlight? [115]` |
| `141.md` | the couplet from "Sending Ink to a Friend" set as verse. `T’ien-t’ai` was `Tien-tai`; `“ten-thousand-times` was `‘‘` |

### B. No re-translation (12)

- `106.md` — `and “moon.”`, which had lost its quote marks.
- `108.md` — `Ch’u’s` in the poem, where the apostrophes were straight.
- `112.md` — `If I` in the poem, was `IfI`. This file carries the §1.4
  marker; it is not re-run.
- `116.md` — `Yakushidō`, was `Yakushido`. The Persian spells it
  «یاکوشی‌دو» either way.
- `118.md` — `Li Po’s poem “The Jeweled`, was `Li Pos poem ‘The Jeweled`.
- `119.md` — `if I ever forget`, was `if lever forget`, in the poem. The
  Persian already has «اگر هرگز … از یاد ببرم».
- `120.md` — `Chou.” [108]`, and `She’s`. The Persian closes the quote
  already.
- `121.md` — `Ikkyū’s`, was `IKkyu's`. The Persian has «ایک‌کیو».
- `129.md` — `Kanshō`, `“Burning house”`, `“Triple Sphere”`, `In Buddhist`.
- `131.md` — `Bunshō`, was `Bunsho`. The Persian glosses «بونشو» as
  `(Bunsho)`, without the macron, which is not worth a run.
- `134.md` — `Unryōin` ×2 and `Sen’yūji` ×2. The Persian has «اونریو-این»
  and «سن-یو-جی».
- `140.md` — `said, “It is`, where the opening quote was straight.

## Requirements

1. **Group A through the pipeline**, as `CLAUDE.md` describes: `strip`,
   `gtranslate.py -w --raw`, `restore -o`, one file at a time. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the
   picker.
2. **No §1.4 marker to re-apply.** Check that none of the 14 carries one or a
   `parity: offset` before running. (`111` and `112` do; neither is in
   group A.)
3. **§2 against the old file and the table.** The rows that matter here are
   *Po Chü-i* «پو چیو-ای», *Tu Fu* «تو فو», *Te-shan* «ته-شان», *Ch’u*
   «چ’و», *Ch’ang-an* and *Ch’ang-lo* «چ’انگ-آن», «چ’انگ-لو», *Fu-chou*
   «فو-چو», *Chuang Chou* «چوانگ چو», *Hsüan-tsung* «شیوآن-تسونگ»,
   *Maitreya* «مایتریا», *Mori* «موری» and *Rinzai* «رینزای». *Jui-yen*,
   *Wu-men* and *Tu-ling* are correct as given.
4. **The verse quotes are verse, and restore sets them.** STYLE.md §3.3 says a
   quoted poem is set the way `source/` sets it. If the model runs the lines
   together, `restore` refuses and names them. Break the draft in `/tmp`,
   as `CLAUDE.md` says, and do not touch `fa/`.
5. **Read the markers**: [101] in `103`, [109] in `125`, and [113] [114]
   [115] in `139`.
6. **Group B by reading**, not by running anything.

## Acceptance criteria

- [ ] The 14 files of group A re-translated.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no
      disagreement for any file in the range.
- [ ] `135` and `139` distinguish Musō from Musū.
- [ ] Every verse quote in `101`, `113`, `117`, `126`, `139` and `141` is
      verse in `fa/`.
- [ ] Group B checked.
- [ ] `just check` green.

## Out of scope

Anything 010 has not read yet: the front matter, `introduction-4` and the
back matter.
