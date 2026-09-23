# 016 — A note's closing paragraph, given back

**In 16 files the last paragraph of a note — commentary on the poem as a
whole — runs into the gloss on the note's last word. Giving it back adds a
block to each.**

## Context

Found by 010's fifth session; its *Session 5* notes have the detail. The
print ends some notes with a paragraph of its own, set off by a blank line
and not in italics: "As duplicated in the translation, the three rhyming
lines of this poem all end with the word 'Zen'" (poem 130, p. 114). It is
about the poem, not the last lemma. `source/049.md` appends it to the gloss
on *Sung-yüan*, and so does the Persian.

**Cause.** `build_translations()` builds each chunk as
`[lines[j] … if lines[j].strip()]`: every blank line goes before
`parse_prose()`, which would have split on it. The raw OCR has the blank
line. It cannot simply be kept, because a blank line is also where one page
ends and the next begins.

**Measured**: a blank line inside a Notes chunk with the same page-foot
number on both sides of it (`get_trans_lines()`' `foots`). 17 paragraphs in
16 files are joined:

| file | the paragraph begins |
|---|---|
| `001` | This poem has always been held up… |
| `004` | The intrusion of the first person pronoun… |
| `015` | This same theme is taken up by Ikkyū… |
| `021` | There are very few important female figures… |
| `024` | The opening of this set of poems invokes… |
| `024` | In the first line of this poem, it is no longer… |
| `026` | Overtly simple, this poem… |
| `030` | These poems occur within a group of poems… |
| `049` | As duplicated in the translation… |
| `075` | This poem is the seventh in the same series… |
| `086` | While the moral of the title is simple… |
| `091` | For the poet, the sound of the dry leaves… |
| `092` | Although considered to be doctrinally opposed… |
| `109` | These are the first poems in the Crazy Cloud Anthology… |
| `112` | This is one of the very few poems in the Crazy Cloud… |
| `118` | This poem and its afternote seem… |
| `131` | There is an entry in the Nempu which may refer… |

The same measurement also finds three already split some other way (`010`,
the second in `024`, and `139`'s *Moonlight Night*). Three hits are not
afterwords at all: `024`'s `(79` and `Pi` labels and a set title in
`073`–`075`.

**Not the same as 010's *Note entries run together*.** That is the lemmas
of one note joined into a paragraph, which the print sets as separate lines
without a blank one. It is the book-wide shape of every `## Notes` and is
kept. This is a real paragraph break, with a blank line, that the generator
throws away.

## Dependencies

010 session 5 (committed). Changes no file numbers, so it blocks nothing and
nothing blocks it. **015 touches `049` too**; whichever runs second
re-translates it again.

Nine of the 16 are in decades 010 has not read (`075` onward). Running this
first means those decades read a `source/` that already has the break.

## Requirements

1. **Keep the blank line in a Notes chunk where the page does not change**,
   and let `parse_prose()` split on it. Confirmed paragraphs, not a looser
   rule (010 requirement 4): the three non-afterword hits above must not
   move. `split_book.py`'s `EXPECTED_POEMS` guards the poem count, not
   this; diff `source/` before and after and expect exactly the 16.
2. **Read each on its page** before trusting the measurement. It found these
   17 from the OCR's blank lines. A break the OCR lost entirely is not in it.
3. **Re-translate the 16**, through the pipeline as `CLAUDE.md` describes.
   Each gains one block (`024` two), so `check_parity` fails all 16 until
   they are done.
4. **§1.4 markers and `parity: offset`**: check each of the 16 before
   restoring, and re-apply any after (`CLAUDE.md`'s first sanctioned edit).
   Not checked when this spec was written.
5. **§2 against the old files**, as 011–013 did.

## Acceptance criteria

- [x] `just split` changes exactly the 16 files, each by one paragraph break
      (`024` by two), and no text.
- [x] Each of the 17 paragraphs read on its page.
- [x] The 16 re-translated; `check_parity` 153/153.
- [x] The endnote-marker comparison in 010's *Tooling* shows no new
      disagreement.
- [x] `just check` green.

## Out of scope

010's *Note entries run together* and *Prose block quotes break mid-quote*:
both book-wide shapes it records and keeps. `139`'s flattened *Moonlight
Night*, for 010's decade `131`–`141`.

## Implementation notes

### The generator: matched on the text, not the blank line

`AFTERWORDS` in `generate_final_markdown.py` lists the 17 openings, each with
its page. A Notes chunk keeps a blank line only where the next line starts
with one of them, and `parse_prose()` splits there. The page-foot test found
them; it is not what the code runs on (010 requirement 4). The three
non-afterword hits — `024`'s `(79` and `Pi`, the *Congratulating Elder Ki*
set title — have no entry and do not move.

`just split` against a snapshot of `source/` changed exactly the 16 files,
each by one paragraph break (`024` by two), whitespace-identical otherwise.

**All 17 read on their pages** (pp. 67, 71, 82, 89, 91, 93, 96, 99, 114,
134, 142, 145, 146, 156, 158, 161, 169): each a roman paragraph after the
last italic lemma, set off by a blank line.

### Re-translation: one sitting

All 16 drafted at 4500, one at a time. 14 came back at block parity with
every marker and no space-joined verb prefix. The exceptions:

| file | shipped | why |
|---|---|---|
| `026` | 400 | Classic at 4500 (the stanza broken into four blocks). 900 kept the poem and the afterword Advanced and the notes block Classic («…را برای او به خانه می‌آورد»). 400 clean, 5/5. |
| `092` | 400 | 4500 was Advanced at parity but dated Hōnen «۱۱۳۳-۱۲۰۹»; the source says 1133-1212 (the old file had «۱۱۲۱», also wrong). 900 got the date and turned the tail Classic, inverting a sentence («بدون شک در رحمت او نیست») and dropping *and that alone*. 400 right on both. |
| `001` | 4500 | The Classic *fūryū* passage 011 recorded is back, the same text; 011 shipped it at 4500 after trying every rung. |

**A date is not something the block or marker counts see.** `092`'s was
found by a number comparison, `source/` against `fa/`, now run on all 16:
the only other differences are `131`'s «هفتاد و چهارمین» for *74th*,
`030`'s title «(۲)» for *(II)*, and `112`'s `offset +1`.

**Draft repairs in scratch, before `restore`**, as 011 did:

- `004`: line 1 broken in two; joined.
- `024`: Yün-men's verse, lines 3 and 4 run together — the same fault 011
  repaired. Split.
- `131`: the model joined the last two Nempu paragraphs. Split, nothing
  dropped.

**§1.4:** `112` is the only one of the 16 with a marker. Re-applied after
`restore`, header identical to the old file's.

**§2, conformed against the old files and the table:** ایکیو / ایککیو /
ایکّیو → ایک‌کیو in 13 files, and the recorded forms: `001` تز’و-مینگ (the
model gave two spellings), یانگ-چ’ی, یون-من, چ’یو یوآن, لان-تس’ان,
دایتوکوجی; `004` ته-شان, چ’ن; `015` تس’او-شان; `021` شی-شی چی-کو لیوئه;
`024` شیوئه-تو, یوآن-وو, وو-ت’ای, چیانگ-هو, یون-من; `030` دایتوکوجی and
«کریزی کلاود» → ابر دیوانه; `049` سونگ-یوآن, شیو-ت’انگ; `075` تز’و-مینگ;
`086` «شیو-ت’انگ لو», «چ’وآن تنگ لو», چوانگ چو, چوانگ تزو, and *Chien-ho*
«چین-هو» (new, `STYLE.md` §2); `091` یانگ-شان, وی-شان; `092` هونن; `109`
پای-چانگ; `131` ته-شان, شو-اون-آن. A scan of the 16 for every form §2's
"what the model gave" column records came back clean after.

**Left as the model gave it:** `030`'s «(۲)»: the book has both «(II)» and
«(۲)» in titles, and a title is the translator's. `024`'s *Blue Cliff
Record* twice in one paragraph, «سوابق صخره‌ی آبی» and «…کبود»: 013's case,
for 007. The ایکیو left in `071`, `introduction-1` and `notes.md` is outside
this spec.

**Result:** `just check` green, 153/153 on parity and anchors. The marker
comparison disagrees only on `064`, `070` and `introduction-1`, 010's known
three.

The typeset PDF was not read. This spec's criteria do not ask for it.
