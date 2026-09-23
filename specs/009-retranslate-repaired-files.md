# 009 — Re-translate the files the source audit repaired

**The other half of a generator fix. `source/` is right again; `fa/` is not.**

## Context

Spec 010's first pass through the scan found that `clean_translation_line()`
had been deleting English from the Anthology the whole time — the same
justified-spacing fault spec 008 requirement 2 fixed in the Introduction, still
running on the poem pages. Fixing it, plus two others it turned up, changed
**22 files in `source/`**. Every one of them was translated months ago from the
damaged text.

`fa/` does not mirror them any more. One file fails `check_parity`; the other
21 changed words without changing block counts, which is precisely why nothing
caught this and why it needed a read.

**The generator fixes are already committed.** This spec is only the
re-translation they imply. 008's out-of-scope rule is what puts it here rather
than there: a source change to an already-translated file is owned by a
translation spec, not by the audit that found it.

## Goal

`fa/` mirroring the repaired `source/` for all 22 files, and `just check` green
again.

## Dependencies

The generator fixes in `generate_final_markdown.py` (committed). Run
`just split` first if `source/` predates them — `source/` is gitignored and
generated, so a fresh clone has to rebuild it before any of this means anything.

## The 22 files

All small. The largest is 3,142 characters and the smallest 287, so **every one
is a single chunk at the 4,500 default** — no ladder expected, though the rule
still applies if a file comes back Classic.

**None of them carries either sanctioned hand-edit**: no obscene-poem marker,
no `<!-- parity: offset -->`. So each is a plain strip → translate → restore,
with nothing to re-apply afterwards.

| file | source chars | what changed in the source |
|---|---:|---|
| `002.md` | 1,235 | `Daitō` → **`Daiō`**; death poem re-broken into four lines |
| `003.md` | 1,171 | `phrase describing`, `long a`, **`Daiō told`** restored |
| `008.md` | 2,064 | OCR garbage `RX` cut |
| `014.md` | 3,142 | `Daitō` → **`Daiō`** |
| `016.md` | 1,399 | `understood,` restored |
| `018.md` | 970 | `kōan, no. 64` restored (and its `、` normalised) |
| `031.md` | 1,828 | `Teng` restored |
| `035.md` | 823 | `about it.` restored |
| `040.md` | 706 | `as a cave in` restored, and de-capitalised |
| `057.md` | 2,822 | `behavior` — a broken hyphen-join repaired |
| `061.md` | 1,207 | `Pai-chang` restored |
| `066.md` | 435 | OCR garbage `exo` cut |
| `067.md` | 1,604 | `Ch’ing-yüan: The`, `honey, the man` restored |
| `085.md` | 2,190 | `among the` restored; garbage cut |
| `087.md` | 877 | `about the` restored |
| `094.md` | 1,342 | `Books` restored to a poem title |
| `099.md` | 501 | `Kuan, kōan` restored |
| `120.md` | 1,490 | `The` restored to a poem title |
| `128.md` | 666 | `under`, `is correct, the`, `a private retreat` restored |
| `129.md` | 815 | `that is, the` restored |
| `132.md` | 287 | `poetic` restored |
| `133.md` | 2,561 | `a`, `who`, `of which`, `in the` restored |

## Requirements

1. **Re-translate each file through the pipeline**, one at a time, exactly as
   `CLAUDE.md` describes — `strip`, `gtranslate.py -w --raw`, `restore -o`.
   Never `>` into `fa/`. Runs are sequential: check `pgrep -f gtranslate.py`
   before starting.

2. **Judge each draft by its text, not the model picker.** `grep -c ِ` on the
   draft; 0 is Classic and means going down the ladder (4500, 900, 400, 300).
   These files are one chunk each, so a Classic result is a whole-file result —
   the per-paragraph measurement that `preface.md` needed does not apply.

3. **`002.md` is the reference file, and it changes.** `STYLE.md` §2 cites
   `fa/002.md` as the argued source for «دایتو» and «دایتوکوجی». Re-read §2.4
   after the new draft lands and make sure the citation still says what it
   claims — the sentence it was citing now names a different monk.

4. **Settle `Daiō` in `STYLE.md` §2.** It is a new proper noun in this book's
   Persian: Daiō Kokushi (Nampo Jōmyō), Hsü-t'ang's student and Daitō's master.
   It appears in `002.md`, `003.md` and `014.md`, and it must not drift into
   «دایتو» — that is the exact error the source audit just removed. Decide the
   rendering once, add the row, and conform all three files to it under the
   §2 hand-edit exception.

5. **`002.md`'s death poem is now verse.** Four lines with hard breaks inside
   the note, per `STYLE.md` §3.3. `apparatus --check` enforces the breaks;
   check the Persian reads as a stanza and not as a sentence that happens to
   be broken.

## Acceptance criteria

- [x] All 22 files re-translated and written by `restore -o`.
- [x] `just check` passes: `check_parity` 147/147, `normalize` clean,
      `apparatus --check` 147/147, no bidi findings.
- [x] Every restored word is present in the Persian — spot-check the table
      above, which names what to look for in each file.
- [x] `Daiō` has a `STYLE.md` §2 row and all three files use it.
- [x] The typeset PDF was read for the 22 files.

## Out of scope

Reading the rest of the scan — that is 010, and it will produce more files for
a spec like this one. Revising translation that the source change did not
touch.

## Implementation notes

### Session 1 — all 22, one sitting

**20 of 22 went through at 4500 as the spec expected.** Two did not:

- **`128.md` came back Classic at 4500 and at 900** — the stanza split in
  two, «می‌کنید» for a line with no addressee. Advanced at 400 and 300; 300
  shipped, because 400 carried a doubled zero-width space and 300 renders
  *the mountains deepen* closer. This is spec 004's `098.md` again: a
  sub-900-character file that only a sub-chunk rung fixes.
- **`129.md` was Advanced at 4500 and still wrong.** «اتاقِ خواب» for *Dream
  Chamber* reads as "bedroom", and Mumu "No Dream" became «بی‌خوابی» —
  insomnia. Neither is a proper noun, so the §2 hand-edit could not cover it;
  re-translated at 400 and 300, and 300 shipped: «حجره‌ی رویا», «بی‌رویا», and
  *in the past and recently* rendered rather than smoothed. **An ezafe count
  cannot see this.** The draft scored 15 and was the worst of the three.

**`085.md` needed both `restore` repairs.** It refused on three stanza lines
the model had kept but lost the trailing spaces on — ended with two spaces in
the draft, as `CLAUDE.md` says. Then parity failed 12/13: the model had joined
"…Rinzai's teachings." to "The Master further said…". Nothing was dropped, so
the draft was split back at that sentence in scratch and restored again.

**The §2 conform was the bulk of the hand work — 16 of the 22 files.** A
fresh draft loses every correction the old file carried, so each file's
canonical §2 forms were counted old-against-new and every shortfall traced to
the model's variant: ایکیو ×7 files, شو-تانگ, نان-چوآن, کوی-تسونگ, the
*Tz'u-en K'uei-chi* cluster in `057`, and so on. Three differences are
correct and stay: `002` and `014` each lose a «دایتو» that was really Daiō,
and `003` gains one where the model supplied a dropped subject. `067`'s
«چینگ-یوان» was in the old file too and was caught only in the PDF read — the
count compares against the old file, so it cannot see a form both got wrong.

**The model told Daiō from Daitō unaided,** every time, in all three files. It
rendered Daiō «دایو»; §2 now fixes it as «دایئو».

**`STYLE.md`:** the Daitō row cited `fa/002.md`, whose «دایتو» was the OCR
error; it now cites `fa/003.md`, the poem on Daitō himself. §2.6's example
likewise. The Daiō row is new.

**The PDF read found no typesetting fault in the 22.** It found source defects,
which are 010's and are recorded there under the decade that will reach them.

### Left for other specs

- **ایکیو / ایکّیو survives in seven files 009 did not touch** — `044`, `046`,
  `069`, `110`, `124`, `introduction-1`, `notes`. A §2 conform, cheap and
  sanctioned, but out of this spec's scope.
- **`fa/130.md`'s heading reads «(I)»** where 131–133 have «(۲)», «(۳)», «(۴)».
  The source is `(I)`–`(IV)` throughout, so this is the model localising three
  numerals out of four, not OCR. A heading title is translator prose, not a
  sanctioned hand-edit, so it wants a re-translation of `130.md`.
