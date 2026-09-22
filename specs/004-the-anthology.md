# 004 — The Anthology: `011` – `135`

**125 files · 131,940 chars · 14 prose introductions · 3 set headers · 86 with notes**

## Context

The bulk of the book, and the part that decides whether it reads as one voice.
Every file here is a single chunk — none of the 125 exceeds the translator's 4,500-
character limit — so this is 125 runs of about eleven seconds each, plus the
`strip`/`restore` round trip.

Sequential only. One Chrome profile, and `_cleanup_chrome_profile()` kills whatever
holds it at startup, so a second run started in parallel destroys the first.

The poems are not uniform. Ikkyū writes praise-verses for dead masters, mountain-
hermitage poems, savage attacks on named contemporaries, and a long sequence about
Lady Mori that is explicitly erotic. `STYLE.md` §1 settled how the register moves
between these; this spec is where that decision meets 125 files of it.

## Goal

125 files at `status: reviewed`, `just check` green, the PDF read part by part.

## Dependencies

003. The pilot's refusal tally is what tells you whether to expect a clean run or a
repair after every file.

## Requirements

1. **`STYLE.md` is binding from here.** If the text contradicts it, that is a
   terminology question to settle deliberately, not a decision to change mid-batch.
   A change made here costs revising everything already done in this spec.

2. **Sequential runs.** No parallelism, for the profile reason above. Budget roughly
   a decade of files per sitting.

3. **`just check` after each decade, not after each file.** The pilot is what
   established the per-file rhythm; at this volume, a decade is the right unit. If
   parity fails for a decade, bisect within it.

4. **Three set-header files need care: `029`, `048`, `076`.** Each opens with a bold
   line above its `# Poem N:` heading (`**Living in the Mountains   two poems**`).
   Spec 002 decided what these become; whatever that decision was, confirm the
   translated file follows it, because `apparatus.py` does not re-emit that line —
   it is prose, and the model translates it freely.

5. **Fourteen prose introductions behave differently.** `013`, `017`, `033`, `035`,
   `039`, `042`, `063`, `066`, `103`, `109`, `111`, `125`, `129`, `134`. They are
   prose paragraphs, not verse, sitting inside a verse sequence, and `--raw` is still
   mandatory for them — the flag is per-run and these run alone. Their heading label
   (`Prose Introduction to No. N`) is re-emitted by `apparatus.py` with the numbers
   converted to Persian digits; the rest of the heading is prose.

6. **Repair, not re-run, when `restore` refuses once.** The three rules from
   `000-overview.md`, repeated because this is where they will be needed:
   - Edit the draft in `/tmp`, never `fa/`.
   - Only ever insert or delete a bare `⟦n⟧`. Never write the label markup by hand.
   - **If most of a file's sentinels are missing, re-translate instead.** That is the
     silent Classic-model failure, and hand-placing a dozen markers into a bad draft
     only makes it look finished.

   Say in the commit body which markers were placed by hand.

7. **Watch for the register drifting at volume.** 125 files translated in sequence
   over weeks will drift, and the drift is invisible from inside any one file.
   Every few decades, read a poem from the first decade next to one just finished. If
   they no longer sound like the same translator, that is worth fixing while there
   are still files left to make consistent.

8. **Read the PDF part by part.** Not file by file — the point is the cumulative
   texture — but not once at the end either, because by then a systematic fault is
   125 files deep.

## Checklist

- [x] `011`–`020` · 16,866 chars · prose intros `013`, `017`
- [x] `021`–`030` · 17,699 chars · set header `029`
- [x] `031`–`040` · 12,173 chars · prose intros `033`, `035`, `039`
- [x] `041`–`050` · 8,464 chars · prose intro `042`; set header `048`
- [x] `051`–`060` · 9,850 chars
- [x] `061`–`070` · 11,189 chars · prose intros `063`, `066`
- [x] `071`–`080` · 9,117 chars · set header `076`
- [x] `081`–`090` · 10,986 chars
- [x] `091`–`100` · 5,855 chars
- [x] `101`–`110` · 7,579 chars · prose intros `103`, `109` · the Lady Mori sequence
      begins at `104`
- [x] `111`–`120` · 7,631 chars · prose intro `111`
- [x] `121`–`130` · 9,060 chars · prose intros `125`, `129`
- [x] `131`–`135` · 5,471 chars · prose intro `134`; `135` is the last poem

## Acceptance criteria

- [x] All 125 at `status: reviewed`.
- [x] `just check` passes with 135 Anthology files compared (125 here plus the
      pilot's 10), none skipped. The 12 skipped are the front matter, the
      Introduction and the back matter, all out of scope.
- [x] `apparatus --check` reports no hard-line-break mismatch anywhere — every
      stanza survived. 135 files match.
- [x] The whole Anthology read in the typeset PDF (173 pages, `_book/`).
- [x] The three set-header files match the spec 002 decision.
- [x] No `STYLE.md` **decision** was changed. §2.8 and §1.4 gained records of
      what the decisions produced; neither reverses anything.

## Out of scope

Front matter, Introduction, back matter, release.

## Implementation notes

### The refusal tally

**Six of 125 files needed a hand repair. Zero sentinels were placed by hand,
here or in the whole spec.** Spec 003's sizing was right: this book's headings
do not defeat the round-trip.

| file | what `restore` said | what fixed it |
|---|---|---|
| `019` | dropped 3 hard breaks, moved -2 | two spaces on the three named draft lines |
| `019` | *then* `check_parity`: 9 blocks against 10 | split the second Ta-sui speech out of the paragraph above it |
| `024` | dropped 3 hard breaks, moved -1 | `## ⟦2⟧` was glued to the last verse line — broken back out |
| `030` | dropped 3 hard breaks, moved -1 | the blank line between two note paragraphs had been swallowed |
| `038` | dropped 8 hard breaks, moved -2 | two note paragraphs run onto one line — split by hand |
| `085` | dropped 3 hard breaks, moved -2 | same as `038` |
| `098` | dropped 3 hard breaks, moved +2 | not a round-trip failure at all: the Classic model. Re-translated |

**Four of those seven rows are now automatic and will not recur.** The
`restore` error always names hard line breaks, because that is what it checks
last, but three distinct causes hide behind that one message and each has a
mechanical repair:

1. **The quatrain's trailing spaces are stripped.** Nearly every poem. The
   engine aligns breaks by position across the whole file, so one merged
   paragraph anywhere shifts every run after it; matching *block for block*
   against `source/` instead is immune to that.
2. **A heading sentinel glued to the end of the line above.** The marker is
   present and misplaced, so putting it on its own line is a position edit,
   not markup written by hand.
3. **A blank line between two paragraphs swallowed**, with the paragraphs
   themselves still on separate lines.

Only the fourth — two paragraphs run onto **one** line — is left for a human,
deliberately, because where the break goes is a reading and not a count. It
happened twice in 125 files.

### The Classic fallback happened twice, and neither signal the pilot left
### behind was sufficient

`098.md` and `128.md`. Both recovered at **`--chunk 400`**, which is one of the
two sizes spec 003 measured on `009.md`.

**Halving is the wrong ladder.** `098.md` came back Classic at 4500, 2250,
1125, 562 *and* 281, and Advanced at 400 — halving walks straight past the
sizes that work. The ladder used from the ninth decade on is **4500, 900, 400,
300**.

**`grep -c ِ` fails in both directions, and this spec has an example of each:**

- `099.md` scored **0 ezafe and was Advanced.** A 22-word quatrain with no
  ezafe construction in it. Re-running it at the top of the ladder gave a
  byte-identical draft, which is spec 003's "per-input and deterministic"
  again.
- `128.md` scored **above 0 and was Classic.** It also had the right block
  count, so the structural test added after `098` let it through too.

**The test that separates all 135 files cleanly is the verb prefix.** Advanced
joins it with a ZWNJ (`می‌ریزند`), Classic puts a space there (`می ریزند`), and
the two do not mix inside a file. Run over every file in the book — the
pilot's ten included — it flags exactly one, `128.md` itself:

```
for f in fa/*.md; do
  z=$(grep -o 'می‌' $f | wc -l); s=$(grep -o 'می [آ-ی]' $f | wc -l)
  [ "$s" -gt "$z" ] && echo "$f"
done
```

The other tell on `128.md` needed no counting: Classic left `Unryōin in
Sen’yūji` standing in Latin script inside a Persian heading. Advanced
translates both temple names and glosses them under §2.9.

### §2 is the cost, and the table is how it stopped growing

**The recurring-noun table reached 92 entries.** The per-decade passes applied
203 corrections and two whole-book sweeps another 8, on top of what was
applied inline as the table grew. Spec 003 projected of the order of 1,200
across the book and about nine per file; the rate here fell steeply — 32 in the
first decade, 5 in the seventh, 1 in the twelfth — because the table learns.

**The model's commonest error is not a spelling, it is a separator.** A ZWNJ
where `source/` has a hyphen, a hyphen where it has a space: `چوانگ‌تزو` for
`Chuang Tzu`, `شیو-ت’انگ‌لو` for `Hsü-t’ang Lu`, `نان‌چوآن` in one decade
against `نان-چوآن` in another. After that come the dropped §2.2 apostrophe and
the dropped §2.3 `ü`, and both do real damage: **`Hsüan-tsang` and
`Hsüan-tsung` are two different men, and without §2.3 the model's forms for
them collide.**

It is inconsistent inside a single file, exactly as the pilot found. `038.md`
spells P'u-hua two ways in one file, the very name §2.2 uses as its worked
example. `057.md` needed seven distinct corrections for a five-line poem
because its subject, Tz'u-en K'uei-chi, is two apostrophes in one name and the
model dropped both, nine times.

**The table has to be swept over everything, not just the current decade.** It
learns names as the Anthology goes, so `014.md` was still carrying a form the
sixth decade taught it about. Two whole-book sweeps caught eight of those, two
of them in the pilot's own files.

### §1.4: 28 candidates read, 2 marked

`107.md` and `108.md`, and that is the whole set — **a tenth of what §1.4
budgeted for.**

The other 26 are all the poem 6 case. `053.md` is titled "On a Brothel" and
its four lines are cloud-rain and love's deep river; `076.md` is an arhat
revelling in one; `119.md` is titled "Cause and Effect for a Lustful Monk" and
is four lines of doctrine. **Arntzen is frank far more often than she is
crude, and §1.4 marks the crude.** Reading 26 of them in a row is what makes
the line feel right rather than arbitrary.

The mechanism works as §1.4 predicted, now that it has finally been used: the
marker is a counted block, `<!-- parity: offset +1 -->` above the heading is
free because a block that is only an HTML comment does not count, and all
three checkers pass. The practical consequence is that `check_parity` needs
the companion directive in two files rather than thirty.

### §1.3 met both of its binding cases and survived them

§1.3 quotes two poems to justify the register and both are in this spec.

- **`080.md`** (poem 284) came back with روسپی‌خانه and زربفت — no euphemism,
  no abstraction. `076.md` gives روسپی‌خانه unprompted three more times.
- **`107.md`** (poem 535) is within a word of §1.3's own prediction:
  میان ران‌ها against §1.3's در میانِ ران‌ها.

That also closes a note left open in the second decade: `029.md` renders
"brothels" as the softer عشرت‌کده‌ها, and against 135 files it is one file's
variation and not a systematic softening. §1.3 is not re-opened and `029.md`
is not patched.

### Register (requirement 7)

Checked at the fourth, tenth and final decades, each time reading a
first-decade poem beside one just finished. No drift: the same compact
classical lexicon and the same ezafe density throughout, and the three
registers stay apart — the prose introductions are §1.1's scholarly Persian in
all fourteen, the verse is §1.2's in all 120.

### The PDF (requirement 8)

Read in five passes across the 173 pages, not once at the end. Everything the
pilot checked still holds at 135 files:

- **No verse reflowed** and **no stanza line wrapped** at this measure.
- **No bidi reversal.** Every §2.9 gloss sets left-to-right inside the
  Persian — `(Crazy Cloud)`, `(Po Chü-i)`, `(Sen’yūji)`, `(Blue Cliff
  Record)`. LuaLaTeX is doing what `tex/preamble.tex` chose it for.
- **The §2.2 apostrophe survives typesetting**: `نان-چ’یوآن`, `تس’او-شان`,
  `چ’انگ-لو` all set with the mark inside the word.
- **Structural labels intact**, including `درآمدِ منثور بر ۸۱۹، ۸۲۰، ۸۲۱، ۸۲۲`
   — a prose-introduction label carrying four numbers.
- **All three set headers** set bold in their own block above the stanza.
- **Both §1.4 markers** set as their own block between heading and verse.

### Defects found in `source/`, for spec 008

- **`source/084.md`: `Chienho`** — the hyphen of `Chien-ho` fused away by the
  extraction. The Persian follows it as «مارکیِ چیِن‌هو». §2.8's Lan-t'san
  precedent says the Persian does not follow OCR damage, but the undamaged
  form is a guess from here.
- **`source/030.md`: `(90`** — the same stray-open-paren class spec 003 found
  as `(26` and `(27` in `source/007.md`, still reaching the page.

One translation blemish left as translated, per "the machine draft is the
edition": `fa/011.md` has `ییین` for one of its several `یین`.
