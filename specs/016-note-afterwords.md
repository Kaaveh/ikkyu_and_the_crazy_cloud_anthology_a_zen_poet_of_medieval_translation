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

- [ ] `just split` changes exactly the 16 files, each by one paragraph break
      (`024` by two), and no text.
- [ ] Each of the 17 paragraphs read on its page.
- [ ] The 16 re-translated; `check_parity` 153/153.
- [ ] The endnote-marker comparison in 010's *Tooling* shows no new
      disagreement.
- [ ] `just check` green.

## Out of scope

010's *Note entries run together* and *Prose block quotes break mid-quote*:
both book-wide shapes it records and keeps. `139`'s flattened *Moonlight
Night*, for 010's decade `131`–`141`.
