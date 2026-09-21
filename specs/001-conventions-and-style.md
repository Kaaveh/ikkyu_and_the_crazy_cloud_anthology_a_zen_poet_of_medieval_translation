# 001 — Conventions & Style

## Context

This repo has no `STYLE.md`. Lin-chi had one and it was binding; here the only
written conventions are scattered through `CLAUDE.md` and `pyproject.toml` comments,
and none of them is a *translation* decision.

Every sentence of the book is written in one register or another, and every page
carries proper nouns in three romanisation systems at once. Deciding these at poem 80
means revising 79 files. Deciding them now costs one session.

This is a decision session, not a translation session. It produces prose in
`STYLE.md`, two small code/doc edits, and **nothing under `fa/`**.

## Goal

`STYLE.md` exists with §1–§6 written, no `<<<TBD>>>` left in §1, §2 or §3. The status
model in the code matches the decision that the machine draft is the edition.

## Dependencies

None. Can run before or after 002; the recommended order puts 002 first only because
repair is cheapest before anything is translated.

## Requirements

1. **§1 Register.** The load-bearing one. Decide the Introduction's scholarly prose,
   the poems' compact formal verse, and the blunt/erotic poems separately, and decide
   whether the shift between them is signalled to the reader or left implicit.

   Test the decision against `source/107.md` ("A Beautiful Woman's Dark Place Has the
   Fragrance of a Narcissus") and `source/080.md` ("With a Poem About a Brothel,
   Putting to Shame Those Brothers Who…"). **If the Persian cannot be blunt, the
   decision is wrong** — a large part of the Anthology is deliberately obscene, and a
   translation that softens it is translating a different book.

2. **§2 Proper nouns.** The source mixes three systems on the same page:

   - **Wade-Giles Chinese** — `Hsü-t'ang`, `Ta-sui`, `P'u-hua`, `Yüan-wu`,
     `Po Lo-t'ien`. Not Pinyin. Decide whether the Persian transliterates from
     Wade-Giles or from the modern reading, and **decide what happens to the
     Wade-Giles apostrophe** (`t'ang`): it is a phonemic mark, not punctuation, and
     dropping it silently merges distinct names.
   - **Japanese macron romanisation** — `Ikkyū`, `Sōjun`, `Daitō`, `Yōsō`, `Kōan`,
     `Gojō`. Decide how the macron is carried into Persian.
   - **Sanskrit / Buddhist vocabulary** — `Bodhisattva`, `Arhat`, `Dharma`,
     `Vimalakīrti`, `Maitreya`, `Nirvana`. Some of these have settled Persian forms;
     some do not.

   `fa/002.md` already commits to `«شو-تانگ»` for Hsü-t'ang and `«یی-وانگ»` for
   Yü-wang, inside guillemets. Either ratify that as the rule or change it and
   re-translate that one file.

3. **§3 Verse layout.** The hard line breaks *are* the poem. `apparatus.py` restores
   them mechanically and `apparatus --check` fails if a file loses one, so the
   mechanism is not the question. The style rule is: **may a translator re-break a
   line, and if so when?** A Persian line is typically longer than Arntzen's English
   line, and a four-line quatrain that wraps to eight in the PDF reads as eight.

   Also decide how a poem *quoted inside a prose note* is set — `002.md` has one, the
   model re-broke it correctly, and the adapter tolerates that by design.

4. **§4 Notes.** 93 of the 135 Anthology files carry a `## Notes` section of
   run-together glosses — headword, colon, explanation, then the next headword, all
   in one paragraph (see `source/003.md`). Decide whether Persian keeps the run-on
   form or breaks to one gloss per line.

   **If it breaks, the block count changes** and every affected file needs a
   `<!-- parity: offset +N -->`. Prefer keeping the run-on form for that reason
   alone: an offset per file across 93 files is a checker turned off by attrition.

5. **§5 Digits.** Record the existing configuration and why, so nobody "fixes" it:
   `latin_digits = false` in `pyproject.toml` because poem numbers, the dates in the
   Introduction and the page references throughout the Notes are Latin-digit and
   should stay that way; but `[tool.book.titles]` headings and the `شعر N:` labels
   `apparatus.py` emits use Persian digits, because they are the book's own
   structure rather than a reference into someone else's edition.

6. **§6 Quotes.** `normalize`'s `quotes` rule is on and rewrites ASCII and curly
   quotes to `«»` **anywhere in the file, including inside verbatim English**. If the
   style decision goes the other way, turn the toggle off in `pyproject.toml` in the
   same commit. Note here that spec 006 depends on this rule's blindness and solves it
   with `<!-- normalize: off -->` regions rather than by disabling the rule.

7. **Change the status model in code.** The decision is that the machine draft is the
   edition — there is no hand-revision stage, so there is no later step to promote a
   `draft` into place.

   - `tools/apparatus.py`: `DRAFT_STATUS = "draft"` → `"reviewed"`, and rewrite the
     comment above it, which currently explains the three-state model.
   - `CLAUDE.md`: replace the "Status values in `fa/` front matter" section with the
     two-state one.
   - `fa/002.md` already says `status: draft`. Update it in the same commit.

   No test in `tools/tests/` asserts on the literal `"draft"` — checked — so the
   suite should stay green without changes. Confirm rather than assume.

8. **Say plainly that nothing enforces terminology.** There is no `check_glossary` in
   `bargardan-tools v0.1.0` and there will not be one for this book. `STYLE.md` §2 is
   the record of the recurring renderings, and it is a discipline, not a gate. A
   rendering that has not been argued out is a suggestion and must be labelled as one.

9. **Do not decide in advance what the book has not asked.** A section exists so that
   when the question arrives there is a place to put the answer. A guess written now
   is worse than a `<<<TBD>>>`, because it looks settled.

## Acceptance criteria

- [x] `STYLE.md` exists; §1–§6 written, each decision carrying a sentence of reasoning.
- [x] The §1 decision was tested against at least one deliberately obscene poem and
      survives it. Both `107.md` (Poem 535) and `080.md` (Poem 284), in §1.3.
- [x] §2 either ratifies `fa/002.md`'s renderings or changes them, and `fa/002.md`
      matches whichever was chosen. Guillemets ratified (§2.6); the aspiration mark
      and `ایک‌کیو` changed, and the file conformed.
- [x] §4 records whether note blocks stay run-on, and if not, that the parity-offset
      cost was accepted knowingly. Run-on kept. The offsets are spent on §1.4
      instead, ~30 of them, knowingly.
- [x] `pyproject.toml` matches the §6 decision on quotes. `quotes = true` stays;
      no change needed.
- [x] `tools/apparatus.py` writes `status: reviewed`; `CLAUDE.md` says so; `fa/002.md`
      says so.
- [x] No `<<<TBD>>>` remains in §1–§3. Three left in §4–§6, each deliberate:
      headword emphasis (§4.1), endnote cross-reference links (§4.2 — spec 006's),
      and nested quotation (§6). The Sanskrit vocabulary is in §2, so it could not
      be a TBD: it is given as renderings, four of them labelled (suggested) under
      requirement 8 rather than left as a gap.
- [x] `just check` passes.

## Out of scope

Translating anything. Repairing `source/` — that is 002.

## Implementation notes

Done in one session, as the spec expected. `STYLE.md` is the deliverable;
`tools/apparatus.py`, `CLAUDE.md` and `fa/002.md` are the three small edits
requirement 7 asks for. Nothing new under `fa/` — `002.md` was edited, not
translated.

**Decisions that were the maintainer's, not mine.** §1.2 (classical lexicon),
§1.4 (marked at each poem), §2.2 (carry the aspiration mark into the Persian
word) and §2.6 (ratify `fa/002.md`'s guillemets) were put to the maintainer with
the trade-offs. §1.4 and §2.2 were chosen *against* the recommendation, and the
arguments against are recorded in `STYLE.md` next to each so they are not
re-litigated.

**Three things were measured rather than asserted**, because each would have
been wrong in the file otherwise:

1. **`normalize`'s `quotes` rule pairs double quotes only.** Singles and a
   word-internal `’` pass through untouched, even inside a span the rule
   rewrites. This is what makes §2.2's aspiration mark viable at all. `ʼ`
   (U+02BC) was rejected on the way: it is Unicode bidi class L and would break
   the RTL run; `’` (U+2019) is class ON and takes the surrounding direction.
2. **The §1.4 marker costs exactly one parity offset per marked file.** A block
   that is nothing but HTML comments does not count toward parity
   (`_md.COMMENT_ONLY`), so `<!-- parity: offset +1 -->` is free and only the
   blockquote is charged. Verified end to end with `107.md`:
   `check_parity`, `normalize` and `apparatus --check` all pass.
3. **The marker has to be added *after* `restore`.** It changes the run
   structure, so `align_hard_breaks_by_block` stops matching and
   `engine.restore` refuses the draft. This breaks `CLAUDE.md`'s "restore is the
   only thing that writes `fa/`", so `CLAUDE.md` now names the two sanctioned
   hand-edits instead.

**The PDF was rendered and read**, per the roadmap's definition of done, and it
earned its keep twice:

- `شیو-ت’انگ` typesets correctly under LuaLaTeX — the mark holds its position
  inside the word and the run does not reverse. §2.2 is safe on the page, not
  just in the file.
- It caught §3.3, which I had written from the Markdown and had backwards. The
  model's re-break of Hsü-t'ang's death poem produces *soft* newlines, so the
  PDF reflows it into one prose paragraph; the re-break is invisible on the
  page. It cannot be fixed in `fa/` either — `apparatus --check` requires
  `hard_breaks(fa) == hard_breaks(source)`. §3.3 now says the defect is in
  `source/` and hands it back to 002.

**Scope taken on deliberately.** §4.2 (endnote markers) is not in this spec's
requirement list, but spec 002's implementation notes deferred the decision here
by name and left 155 fused digits waiting on it. The form is now fixed —
`[N]`, Persian digits in `fa/` — which unblocks 002 and constrains 006.

**§2.7 is renderings, not a gap.** Requirement 9 argues for deferring the
Sanskrit vocabulary to the 003 pilot, but the acceptance criteria forbid a
`<<<TBD>>>` anywhere in §2. Requirement 8 is the way out and is what §2.7 uses:
the five words with settled Persian forms are given as **argued**, and Arhat,
Maitreya, Bodhisattva and Vimalakīrti as **(suggested)** — a first reading,
explicitly not binding, cheap to overrule until it is in many files.

**`fa/002.md` changed in three ways**, all by hand, all conformance rather than
translation: `status: draft` → `reviewed`; `شو-تانگ` → `شیو-ت’انگ` (×7, §2.2 and
§2.3); `ایکیو` → `ایک‌کیو` (×4, §2.8 — the ZWNJ form is what
`[tool.book.titles]` already commits to, so the body now matches the book's own
table of contents). Its guillemets were ratified and left alone.

No test asserts on the literal `"draft"` — confirmed, not assumed; the
occurrences in `tools/tests/` are local variable names. The suite stayed green
without changes.

### Still to do

Nothing in this spec. Two obligations were handed to others:

1. **Spec 002** — un-fuse the 155 endnote digits to `[N]` (§4.2), and repair the
   flattened verse quotations in `notes.md` (§3.3).
2. **Spec 007** — a hanging indent for verse in `tex/preamble.tex` (§3.2). The
   preamble has no verse handling at all today, so a Persian line that overruns
   the measure wraps and reads as a new line.
