# 014 — The six swallowed poems

**Six poems of the Anthology are not in `source/` as poems. Each ran into the
file before it. Giving them back renumbers every file after `038`.**

## Context

Found by 010's fourth session; its *Session 4* notes have the detail. A
poem's display number is the only thing `build_translations()` starts a
poem on, and where the OCR garbles it past what `get_num()` and `OCR_MAP`
accept, the poem — title, verse, notes — becomes more lines of whatever came
before it. Six did, each confirmed on its page (printed page numbers; the
PDF page is 24 higher):

| poem | page | OCR'd number | now inside |
|---|---|---|---|
| 111 *Wind Bell (II)* | 105 | `1 \|` | `038` (110) — as more verse |
| 113 *Half a Cloud* | 107 | `NIS` | `038` (110) — as note text |
| 315 *The Gentleman's Wealth* | 143 | `Bild;` | `085` (308) — as note text |
| 332 *The Last Chrysanthemum in the South Garden* | 143 | `Boe` | `085` (308) — as note text |
| 537 *Promise to Be Born in the Time of Maitreya* | 158 | `537,` | `108` (536) |
| 690 *Sea Cloud* | 170 | `690,` | `126` (647) |

All six are in the book's *Index of Poems*. **The Anthology has 126 poems,
not 120**; `source/` goes from 147 files to 153. The Persian translated all
six, as parts of their hosts — as note prose in four of them.

## Dependencies

010 session 4 (committed). **Blocks 010's next decade**: `041`–`050` is read
under the file numbers this spec changes. Independent of 013, which lists
the two names it would move.

## Requirements

1. **Start the six poems in the generator.** `OCR_MAP` entries for the
   OCR'd numbers (`1 |` needs care: `get_num()` sees the stripped line),
   `POEM_TITLES` for all six, their title lines in the `t_lines` skip lists,
   and 110 renamed *Wind Bell (I)* to match the set's other poems. Confirmed
   text, not a looser number rule (010 requirement 4) — a looser `get_num()`
   will start poems on page numbers and note labels.
2. **`EXPECTED_POEMS` in `split_book.py`**: 135 → 141. It is the guard that
   stops exactly this change landing silently.
3. **Renumber `fa/` to match**, with `git mv`, highest number first so no
   move lands on a file not yet moved. `038` → `038`–`040`; old `039`–`085`
   shift by 2; `085` → `087`–`089`; old `086`–`108` by 4; `108` → `112`–`113`;
   old `109`–`126` by 5; `126` → `131`–`132`; old `127`–`135` by 6. Work the
   map out from the new `source/README.md`, not from this paragraph, and
   diff the headings of each pair before trusting it.
4. **`_quarto.yml`**, and every count that says 135 / 147 / 120: `CLAUDE.md`,
   `STYLE.md` §1.2 and §4.1, `specs/000-overview.md`, `specs/README.md`, 010's
   file checklist (which becomes `001`–`141`).
5. **Translate the six new files and re-translate the four hosts**, through
   the pipeline as `CLAUDE.md` describes. `038` also carries 010 session 4's
   local repairs (marker [57], Hsü Chung-ya's quatrain) — 013 left it here.
6. **`108`'s §1.4 marker.** It carries `> [زبانِ این شعر عامدانه رکیک است.]`
   and `<!-- parity: offset +1 -->`. Re-apply it after `restore`, to 536's
   file. Read 537 against §1.4 on its own terms: the marker belongs to the
   poem, not to the file it used to share.
7. **Look for a seventh.** The two checks that found these — a page-foot
   number with no `# Poem` heading, a rejected short left-margin token —
   see neither a poem whose number sits mid-page nor one whose number line
   OCRs as something long. `113.md` (542) also has two `## Notes`; the
   generator's `trailing_notes` case for 542 probably explains it, but it
   was not read.

## Acceptance criteria

- [x] `just split` writes 153 files, 141 of them Anthology.
- [x] Every page-foot poem number has a `# Poem` heading — 126 headings, no
      page foot without one.
- [x] `038`, `085`, `108`, `126` (old numbers) carry one `## Notes` each —
      as `087`, `112`, `131`. `038` now carries none, which is the print:
      the *Wind Bell* set's notes, labelled `[110]` and `[111]`, follow
      poem 111 on p. 105 and so sit in `039`, the way the *Scriptures Wipe
      Away Filth* set's all sit in `024`.
- [x] `fa/` mirrors `source/` file-for-file: `check_parity` 153 of 153,
      `normalize` clean. **`just check` is not green**, and was not before
      this spec: `apparatus --check` fails `031` and `037`, 013's stale
      verse quotes. 013 is what turns it green.
- [x] Counts updated everywhere requirement 4 names, and `README.md`.

## What was done

**The six poems** start in the generator on their confirmed OCR strings;
`EXPECTED_POEMS` is 141. `fa/` was renumbered with `git mv` from the top
down, and the map checked by diffing every moved pair: all byte-identical
except the files below.

**Four more generator faults, found by requirement 7's read** and fixed
because each put wrong text in a file this spec was re-translating anyway,
or in one no later decade would reach:

- **Poem 539 had 537's title.** `POEM_TITLES` called it *Promise to Be Born
  in the Time of Maitreya*, so once 537 existed two poems shared it. 539 is
  untitled in print; the Index calls it *Paper Sleeves* (p. 159), and so
  does the generator now.
- **Poem 44 had 344's title**, *Two Pieces of Skin and One Set of Bone*.
  The Index calls 44 *Yen-t'ou's Old Sail Kōan* (p. 80). `014.md` is in a
  decade 010 has already read, so nothing else would have caught it.
- **Poems 541 and 542 each lost their fourth line.** `trailing_notes` cut
  after four *raw* lines, and each poem wraps one verse, so line 4 went into
  a `## Notes` — which is also why `118.md` (542) had two. Now cut after four
  verses. 542's text after the verse is an afternote, not notes (its own
  `Notes:` follows on p. 161), and is set as plain prose.

**Requirement 7: no seventh poem.** Every *Index of Poems* entry on an
Anthology page resolves to a poem the generator starts, a set heading or a
prose introduction. Three looked like misses and are not: *Tu-ling's Flowers
Sprinkling Tears* (p. 166) is the Index's title for 605, *Yen-t'ou's Old
Sail Kōan* for 44, and the OCR's `Oca?` is *Ox, 21*, an Introduction page.
The Index also shows the book titling untitled poems two ways; that is in
010's notes, not decided here.

**The hosts' local damage**, confirmed on pp. 143–144 and 169–170 and fixed
in the same run, since they were being re-translated: markers **[96]**,
**[111]**, **[112]**; T'ao Yüan-ming's poem set as verse; `“‘clerics’’`,
`Essentials,’`, `late.’`, `the gd “‘sobriquets’”’`, `pupils.*Most` (a smudge
in the print, not a marker), `Kokyuan`, and `the Shnonan` → *Shūon’an*.

**Fourteen files through the pipeline:** the six new ones, the four hosts,
`115` (539, retitled), `117` and `118` (541, 542), and `014` (44). All at
4500 except `039` and `131`, which each merged two blocks there. `039` came
back clean at 900. `131` at 900 was Classic in its first note — *men of the
cloth* as «مردان پارچه» — and took 400. §2 conformed by hand in ten of
them (Ikkyū, P'u-hua, Hsü-t'ang, T'ao Yüan-ming, Po Chü-i, Maitreya,
Takigi and the rest); `just fix` for quotes in three.

**§1.4:** the marker is back on 536 (`112.md`). 537 (`113.md`) read on its
own terms and left unmarked — `STYLE.md` §1.4 records it.

The book typesets at 236 pages.

## Out of scope

010's other findings in these files — `085`'s T'ao Yüan-ming lines run
together in pairs, `126`'s stray quotes — belong to 010's decades. Fix them in
the same generator run if they are cheap and confirmed, and say so.
