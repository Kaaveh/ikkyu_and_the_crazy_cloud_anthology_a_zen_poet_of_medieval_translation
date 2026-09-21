#!/usr/bin/env python3
"""This book's headings and verse, carried across gTranslator and verified.

The round-trip itself is general and lives in `bargardan_tools.anchors`, which
knows nothing about this book. This file is the half that does: which parts of
a heading are structure rather than prose, and the Persian form each takes.

What this book does NOT need, and why
-------------------------------------
Lin-chi strips its inline note anchors because the model deletes them --
measured, ten in and zero out. This book has none: its endnotes are referenced
by page number, not by an inline marker, so there is nothing inline to protect.
Measured on a representative file, twice, the Advanced model returns
`#`/`##` markers and `![alt](images/plate_1_calligraphy.png)` completely
intact, path and all. So there is no image or link machinery here.

What it does need
-----------------
1. **Structural heading parts.** "Poem 7:" and "Notes" are labels, not prose,
   and they occur 120 and 98 times. The model translates them well but not
   identically every time, and a book whose poems are headed `شعر ۷` in one
   chapter and `قطعهٔ هفتم` in the next looks broken. They are re-emitted from
   source/ so they cannot drift. The *title* after the label is real prose and
   is left for the translator.

2. **Hard line breaks.** This is a book of verse and the model strips the two
   trailing spaces that hold a stanza together; without them every poem
   reflows into one paragraph. `align_hard_breaks` puts them back by position
   when the model kept the line count, and says which lines to fix when it did
   not.

Pipeline -- note there is no `strip` step for files with no structural heading,
but running it is always safe:

    tools/apparatus.py strip   source/002.md                -o /tmp/002.en.md
    <gTranslator on /tmp/002.en.md>                          -o /tmp/002.fa.md
    tools/apparatus.py restore source/002.md /tmp/002.fa.md -o fa/002.md
    tools/apparatus.py --check
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import regex

from bargardan_tools import _md
from bargardan_tools import anchors as engine
from bargardan_tools._md import to_persian_digits

EXCLUDE = set(_md.config("book").get("exclude", []))
TITLES = _md.config("book").get("titles", {})

SOURCE = REPO / "source"
TARGET = REPO / "fa"

# The structural labels. Everything after them on the heading line is prose and
# is deliberately not matched, so the translator still sees it.
# [ \t]*$ rather than \s*$: under MULTILINE, \s also matches the newline, so
# \s*$ swallows the blank line after the heading and welds it to the paragraph
# below -- which check_parity then reports as a lost block.
LABELS = (
    r"(?P<poem>Poem[ ]+(?P<poem_n>\d+)[ ]*:)"
    r"|(?P<plate>Plate[ ]+(?P<plate_n>\d+)[ ]*:)"
    r"|(?P<notes>Notes)[ \t]*$"
    r"|(?P<prose>Prose[ ]+Introduction[ ]+to[ ]+(?:Nos?\.[ ]*)?(?P<prose_n>[^\n]+?))[ \t]*$"
)

# What restore writes into the front matter. Two states, not Lin-chi's three:
# the machine draft *is* the edition here. There is no hand-revision stage after
# the pipeline, so there is no later step to promote a "draft" into place and a
# third state would only ever record work that never happens. make_stubs writes
# "untranslated", which compare() skips; everything else is checked.
DRAFT_STATUS = "reviewed"

FA_NOTES = "یادداشت‌ها"
FA_POEM = "شعر"
FA_PLATE = "تصویر"
FA_PROSE = "درآمدِ منثور بر"


def token_re(name: str):
    """The heading pattern for one file.

    The file's own title is only matched when [tool.book.titles] has a Persian
    form for it. Headings with no entry -- "Primary Sources", "Epigraph" -- are
    left out of the pattern entirely rather than matched and rendered as None,
    because the engine reads None as "drop this token", not "leave it alone".
    """
    alternatives = LABELS
    if name in TITLES:
        # Anchored to the start of the file, which is the file's own title.
        # Every file in source/ opens with its level-1 heading; split_book.py
        # normalises the levels so that is always true. The "# " is held in a
        # lookbehind so the marker stays in the stripped text: a line that is
        # nothing but a sentinel is one the model may fold into the paragraph
        # below it, and a heading that stops being a heading is a lost chapter.
        alternatives = r"(?<=\A\#[ ])(?P<named>[^\n]+$)|" + alternatives
    return regex.compile(
        r"(?:" + alternatives + r")",
        regex.MULTILINE,
    )


def render_for(name: str):
    """The Persian form of each structural heading part, for one file."""

    def render(match):
        groups = match.groupdict()          # "named" is absent for most files
        if groups.get("named"):
            return TITLES[name]         # the "# " marker is left in place
        if match.group("notes"):
            return FA_NOTES
        if match.group("poem"):
            return f"{FA_POEM} {to_persian_digits(int(match.group('poem_n')))}:"
        if match.group("plate"):
            return f"{FA_PLATE} {to_persian_digits(int(match.group('plate_n')))}:"
        if match.group("prose"):
            # The numbers are cross-references into the Anthology and have to
            # survive exactly; only the digits change script.
            refs = regex.sub(r"\d+",
                             lambda d: to_persian_digits(int(d.group())),
                             match.group("prose_n"))
            return f"{FA_PROSE} {refs}"
        raise AssertionError(f"unhandled heading in {name}: {match.group()!r}")

    return render


def _runs(lines: list[str]) -> list[list[int]]:
    """Line indices of each run of consecutive non-blank lines."""
    runs, current = [], []
    for index, line in enumerate(lines):
        if line.strip():
            current.append(index)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def align_hard_breaks_by_block(source_text: str, draft: str) -> str:
    """Re-apply the source's hard line breaks run by run, not file by file.

    The engine aligns positionally across the whole file, which this book
    defeats: the model reformats verse *quoted inside a prose note* into real
    lines -- correctly, and Hsü-t'ang's death poem in 002.md is one -- so every
    line after that note shifts and the stanza at the top can no longer be
    matched by index, though it never moved.

    Matching run-of-lines against run-of-lines localises that. A run the model
    re-broke is skipped and the rest are still repaired; the engine's own
    whole-file check then runs as the safety net and reports anything left.
    """
    src_lines, draft_lines = source_text.split("\n"), draft.split("\n")
    src_runs, draft_runs = _runs(src_lines), _runs(draft_lines)
    if len(src_runs) != len(draft_runs):
        return draft                       # check_parity reports this properly
    for src_run, draft_run in zip(src_runs, draft_runs):
        if len(src_run) != len(draft_run):
            continue                       # the model re-broke this one
        for position, src_index in enumerate(src_run):
            target = draft_run[position]
            if src_lines[src_index].endswith("  ") and draft_lines[target].strip():
                draft_lines[target] = draft_lines[target].rstrip() + "  "
    return "\n".join(draft_lines)


def strip_text(name: str, text: str) -> str:
    return engine.strip(text, token_re(name), render_for(name))


def restore_text(name: str, source_text: str, draft: str) -> str:
    """Re-apply the stanza's hard line breaks, then put the headings back.

    Breaks first: engine.restore runs the whole-file alignment itself and
    refuses the draft if it cannot complete it, so a draft repaired only
    afterwards would never get that far. Stripping does not change the line
    structure, so the sentinel-bearing draft still lines up with source/.
    """
    aligned = align_hard_breaks_by_block(source_text, draft)
    body = engine.restore(name, source_text, aligned,
                          token_re(name), render_for(name))
    return f"---\nstatus: {DRAFT_STATUS}\n---\n\n{body.strip()}\n"


if __name__ == "__main__":
    raise SystemExit(engine.main(
        sys.argv[1:],
        strip_text=strip_text,
        restore_text=restore_text,
        source_default=SOURCE,
        target_default=TARGET,
        exclude=EXCLUDE,
        description=__doc__,
    ))
