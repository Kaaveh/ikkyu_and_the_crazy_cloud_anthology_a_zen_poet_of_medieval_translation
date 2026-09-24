# 020 — Re-translate what 010's ninth session repaired

**019 again, for the next batch. `source/` changed in 3 files; one needs
re-translating.**

## Context

Spec 010's ninth session (poems 280–344, files `081`–`090`) fixed local
damage in `generate_final_markdown.py` and added Lady Pan's fan poem to
`VERSE_QUOTES`. See 010's *Session 9* notes for what and why. All three
changed files are in the decade.

**`just check` is red on one file.** `086`'s fan poem is one block of ten
lines now, where it was the tail of a paragraph and two paragraphs more. So
`check_parity` reports `fa/086.md: 11 blocks, source has 10`, and
`apparatus --check` reports `3 hard line break(s), source has 12`. The
marker comparison in 010's *Tooling* disagrees on `086` too.

**The generator fixes are committed.** This spec is only the Persian side.

## Dependencies

010 session 9 (committed). Run the generator and `just split` first if
`source/` predates it: `source/` is gitignored.

## The files

### A. Re-translate (1)

| file | what changed in the source |
|---|---|
| `086.md` | marker **[91]**, was `many. [9]`. **The Persian has [9]**. Marker **[92]**, left bare, which the Persian carries as a bare «۹۲». **Lady Pan's fan poem set as ten lines of verse**; the Persian runs it into three prose paragraphs. In the *Chuang Tzu* passage: `I’ll`, `I’m` and `you’d`, which were `Ill`, `Tm` and `youd`. Also three quotes made single, and `store.’”` closed. The Persian's quotes there are garbled: `»وو«`, `"من`, `.«»` |

### B. No re-translation (2)

- `084.md` — the *I Ching* quote gets back `,”` after *Great* and `“`
  before *What is it?*, and closes `”` for `’’`. The Persian already has
  «مهارِ نیروی عظیم» and «آن چیست؟ نیک‌بختیِ عظیمِ راهِ آسمان.» [89].
- `087.md` — `"objects to` becomes `“objects” to`. The Persian already
  has «موضوعات/پدیده‌ها» in guillemets.

## Requirements

1. **Group A through the pipeline**, as `CLAUDE.md` describes: `strip`,
   `gtranslate.py -w --raw`, `restore -o`. Check `pgrep -f gtranslate.py`
   first. Judge the draft on ezafe, not the picker.
2. **No §1.4 marker to re-apply.** Check that `086` carries none and no
   `parity: offset` before running.
3. **§2 against the old file and the table.** *Chien-ho* has a row, from
   this file (016): «چین-هو». So do *Chuang Chou* and *Chuang Tzu*,
   *Ch’uan Teng Lu* and *Hsü-t’ang Lu*. *Lady Pan* is «بانو پان», as in
   `073`.
4. **The fan poem is verse, and restore sets it.** STYLE.md §3.3 says a
   quoted poem is set the way `source/` sets it. If the model runs the lines
   together, `restore` refuses and names them. Break the draft in `/tmp`,
   as `CLAUDE.md` says, and do not touch `fa/`.
5. **Group B by reading**, not by running anything.

## Acceptance criteria

- [x] `086` re-translated.
- [x] The endnote-marker comparison in 010's *Tooling* shows no
      disagreement for `086`: [90] [91] [92] [93].
- [x] `086`'s fan poem is ten lines of verse.
- [x] Group B checked.
- [x] `just check` green.

## Out of scope

Anything 010 has not read yet. `090`'s title (poem 344, `Untitled` where
the Index gives one) is 014's open question, for all three such files at
once.

## Implementation notes

### One run, at 4500

**The draft came back Advanced**, with 16 ezafe. `086` carried no §1.4 marker
and no `parity: offset`.

**The fan poem came back as ten lines**, one per line of the English. What
`restore` refused was elsewhere: the model had joined the four *Chuang Tzu*
paragraphs with single newlines, three lines more than `source/` has, so
`restore` could not align the breaks by position and named the poem's lines.
Putting the three blank lines back in the `/tmp` draft was enough; no text
changed. Block count matches `source/`: 10.

**The markers are right**: [90] [91] [92] [93], where the old file had [9] and
a bare «۹۲».

**§2, conformed against the table:** «چوآن‌تِنگ‌لو» → «چ’وآن تنگ لو»,
«شو-تانگ‌لو» → «شیو-ت’انگ لو», «چوانگ‌تزو» → «چوانگ تزو», «چوانگ‌چو» →
«چوانگ چو» ×2, «چیِن-هو» → «چین-هو». *Lady Pan* came back «بانو پان».

**Left as the model gave it:** «دکان ماهی‌فروشی» for *dried fish store*; the
word *dried* is gone.

### The quotes in the *Chuang Tzu* passage are still wrong

The model quotes the story's inner speech with ASCII `"`, inside and around
`"وو"` and `"یوئه"`, and `just fix` turned them into guillemets one after the
other. The paragraph that begins «به او گفتم» now reads `»وو«` and `»یوئه«`,
and a `"من` opens in it that closes only in the next paragraph, as
`بمانم."» «اما`. These are the same faults the old file had. The English
causes part of it: the perch's speech opens in one paragraph and closes in the
next, and nothing opens it again in between.

**Re-running changes nothing:** a second run at 4500 gave the same text,
character for character. `CLAUDE.md` sanctions no hand-edit for quote marks,
so the faults stay in `fa/`. They are left for 007's typeset read, or for a
spec that decides whether quote marks become a third sanctioned edit.

**Result:** `just check` is green, with 153/153 on parity and anchors.

### Group B

`084` read: «مهارِ نیروی عظیم» and «آن چیست؟ نیک‌بختیِ عظیمِ راهِ آسمان.»
[89]. `087` read: «موضوعات/پدیده‌ها» in guillemets. Nothing to carry.
