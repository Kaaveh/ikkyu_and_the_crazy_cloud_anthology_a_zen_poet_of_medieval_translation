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

- [ ] All 22 files re-translated and written by `restore -o`.
- [ ] `just check` passes: `check_parity` 147/147, `normalize` clean,
      `apparatus --check` 147/147, no bidi findings.
- [ ] Every restored word is present in the Persian — spot-check the table
      above, which names what to look for in each file.
- [ ] `Daiō` has a `STYLE.md` §2 row and all three files use it.
- [ ] The typeset PDF was read for the 22 files.

## Out of scope

Reading the rest of the scan — that is 010, and it will produce more files for
a spec like this one. Revising translation that the source change did not
touch.

## Implementation notes

_(filled in during implementation)_
