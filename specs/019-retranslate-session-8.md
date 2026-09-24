# 019 — Re-translate what 010's eighth session repaired

**018 again, for the next batch. `source/` changed in 7 files; six need
re-translating.**

## Context

Spec 010's eighth session (poems 216–264, files `071`–`080`) fixed local
damage in `generate_final_markdown.py` and added one set heading to
`KNOWN_SETS`. See 010's *Session 8* notes for what and why. All seven changed
files are in the decade.

**`just check` is red on one file.** `074` gains the *Elder Ki* set heading
as a block, so `check_parity` reports `fa/074.md: 2 blocks, source has 3`.
Everything else is inside an existing block. What shows it is the marker
comparison in 010's *Tooling*: `073` and `080` disagree with `source/`.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 8 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (6)

| file | what changed in the source |
|---|---|
| `071.md` | the poem's last line ends in a full stop, was `singing,`. **The Persian ends the poem on a comma.** `Ch’ü Yüan’s`, was `Ch Yüan’s`; the Persian has «چو یوان» |
| `073.md` | marker **[83]**, was `Wu-men Kuan.8?`. **The Persian has [8]**. The *Elder Ki* set heading is gone from the note's end, **which the Persian translates as note text**. `poetry;`, `“a storm in a tea pot”`, `“enlightenment” poem`, `home.” [82]` |
| `074.md` | gains the set heading **Congratulating Elder Ki on the New Construction of Eagle Tail Monastery and Inquiring after His Leprosy** as a block |
| `075.md` | `Sōki` ×2, was `Soki`; **`Jikaishū`, was `Jikaishi`, which the Persian carries** in Latin and in «جیکایشی»; `little`, was `httle`; four quote marks |
| `079.md` | **`jō` ×2, was `jo` and `jd`; the Persian has *jo* twice.** `Mañjuśri` ×3, `Sūtra` in the poem, `Sūrangama`, two quote marks |
| `080.md` | marker **[87]**, was `marvelous.”’8?`, **which the Persian dropped**; `“no mind”` |

### B. No re-translation (1)

- `072.md` — `Nan-ch’üan` in the poem, was `Nan-ch’tian`; marker [81] gets
  its closing quote. The Persian already has both: «نان-چ’یوآنِ کوچک» and
  «…گربه‌ای خفته است.» [81].

## Requirements

1. **Group A through the pipeline**, one file at a time, as `CLAUDE.md`
   describes: `strip`, `gtranslate.py -w --raw`, `restore -o`. Check
   `pgrep -f gtranslate.py` first. Judge each draft on ezafe, not the picker.
2. **No §1.4 markers to re-apply.** Check that no file in group A carries
   one or a `parity: offset` before running.
3. **§2 against the old files and the table.** *Ch’ü Yüan* is «چ’یو یوآن».
   `074`'s and `075`'s titles should agree with each other and with the new
   set heading: the old two already disagree («ایگل‌تیل» and «دم عقاب»).
4. **Group B by reading**, not by running anything.

## Acceptance criteria

- [x] Every group A file re-translated.
- [x] The endnote-marker comparison in 010's *Tooling* shows no disagreement
      for any group A file: `073` carries [82] [83] [84], `080` [87].
- [x] `071`'s poem ends on a full stop.
- [x] `073`'s note ends at *(See p. 13.)*; `074` opens the set with its
      heading.
- [x] Group B checked.
- [x] `just check` green.

## Out of scope

Anything 010 has not read yet. `introduction-3`'s `Ch Yüan` and
`introduction-1`'s `Jikaishi` are recorded in 010 as found in passing, for
the decade that reaches them.

## Implementation notes

### One sitting, all six at 4500

**Every draft came back Advanced**, with 9, 8, 3, 5, 5 and 13 ezafe, and
`restore` took each one on the first try. Block counts match `source/` in all
six. No file in group A carried a §1.4 marker or a `parity: offset`.

**The markers are right.** `073` carries [82] [83] [84], where the old file had
[8] for [83]. `080` carries [87]. The marker comparison now disagrees only on
`introduction-1`, as it did after 018.

**`071`'s poem ends on a full stop**: «…شب‌به‌شب نغمه‌سرایی می‌کند.»

**`073`'s note ends at** «(ص. ۱۳ را ببینید.)», and the *Elder Ki* heading is
gone from it. **`074` opens the set with its heading**, in bold, before the
first line: «تبریک به استاد «کی» بابت ساخت صومعه‌ی «دمِ عقاب» و جویا شدن از
وضعیت بیماری جذام او».

**`075` carries** «جیکایشو» (Jikaishū) and سوکی (Sōki). **`079` has *jō*
twice**, where the old file had *jo*.

**§2, conformed against the table:**

- `071`: «چو یوان» → «چ’یو یوآن»; «چو» → «چ’و» ×2, the clouds of Ch’u;
  ایکیو → ایک‌کیو.
- `073`: چانگ‌شین → چ’انگ-شین ×4, چوانگ‌تزو → چوانگ تزو, ایکیو → ایک‌کیو ×3.
- `075`: تسو-مینگ → تز’و-مینگ ×4, ایکیو → ایک‌کیو ×2, and «ایگل‌تیل» →
  «دمِ عقاب» ×2, in the title and the note.

**Eagle Tail is translated, not transliterated.** The new `074` came back
«دمِ عقاب» in both its title and the set heading, and every file already has
*Eagle Peak* as «قله‌ی عقاب». `075` was the odd one out, so it was conformed,
and §2.8 has a row for it now. The three titles still word the rest of the
heading differently («جویا شدن از وضعیت» against «پرس‌وجو درباره»). That is
prose, not a proper noun, and is left as the model gave it.

`just fix` turned the nested ASCII quotes in `073` («بوفه», «مال») and `079`
(«بودای شیطانی») into guillemets.

**Left as the model gave it:** `079`'s «آرهات» for *Arhat*. §2.7 suggests
«اَرهَت», but the book has «آرهات» in five files and the other nowhere, and the
old `079` had it too.

**Result:** `just check` is green, with 153/153 on parity and anchors.

### Group B

`072` read: «نان-چ’یوآنِ کوچک» in the poem, and «…گربه‌ای خفته است.» [81].
Nothing to carry.
