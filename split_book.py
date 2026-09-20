#!/usr/bin/env python3
"""
split_book.py
Splits the English monolith into source/, one file per translatable unit.

The unit is a level-3 block and everything under it. For the Translations that
is a poem together with its "#### Notes" -- kept in one file on purpose, the
way Record_of_Linji interleaves a discourse with its commentary, so the notes
are translated with the poem they gloss in view. Sections with no level-3
headings become one file each.

Files are numbered by position, not by poem number: the poem numbers are not
contiguous (6, 7, 8, 17, 25 ...) and several level-3 blocks are not poems at
all ("Hsii-t'ang's Three Pivot Phrases", "Prose Introduction to No. 33").
source/README.md maps every file back to its heading.

source/ is flat. check_parity and make_stubs pair source/ and fa/ by filename
with a non-recursive scan, so a nested tree would silently disable both.

Run:  python3 split_book.py
"""

import sys
import re
from pathlib import Path

MONOLITH = Path(
    "ikkyu_and_the_crazy_cloud_anthology_a_zen_poet_of_medieval_translation.md"
)
SOURCE_DIR = Path("source")

# (level-2 heading, output name, split at level 3?)
#
# "Contents" is dropped: it is a hand-written table of contents with anchor
# links into the monolith, and Quarto builds its own from _quarto.yml. Keeping
# it would mean translating a navigation aid that the book will not use, and
# its dead anchors would fail the link check.
SECTIONS = [
    ("Plates",                                     "plates",          False),
    ("Contents",                                   None,              False),
    ("Foreword by Shūichi Katō",                   "foreword",        False),
    ("Preface",                                    "preface",         False),
    ("Introduction",                               "introduction",    True),
    ("Translations from the Crazy Cloud Anthology", None,             True),
    ("Abbreviations",                              "abbreviations",   False),
    ("Notes",                                      "notes",           False),
    ("Bibliography",                               "bibliography",    False),
    ("Index of Poems",                             "index-of-poems",  False),
    ("Glossary-Index",                             "glossary-index",  False),
]

# Guards against a silent re-extraction change upstream. If
# generate_final_markdown.py is edited and the shape moves, this fails loudly
# here rather than producing a source/ that no longer matches fa/.
EXPECTED_POEMS = 135
EXPECTED_INTRO = 4


def split_level(lines, level):
    """Group lines into (heading_text, block_lines) at the given heading level.

    Anything before the first heading of that level is returned under a None
    heading, so no text is ever dropped on the floor.
    """
    marker = "#" * level + " "
    groups, heading, current = [], None, []
    for line in lines:
        if line.startswith(marker):
            if heading is not None or any(l.strip() for l in current):
                groups.append((heading, current))
            heading, current = line[len(marker):].strip(), [line]
        else:
            current.append(line)
    if heading is not None or any(l.strip() for l in current):
        groups.append((heading, current))
    return groups


def merge_bodyless(blocks):
    """Fold a heading-with-no-body into the block that follows it.

    Four level-3 headings introduce a run of poems rather than naming one --
    "Living in the Mountains  two poems", "Hsii-t'ang's Three Pivot Phrases".
    On their own they would become empty chapters; attached to the first poem
    of their group they read the way the page does.
    """
    out = []
    pending = []
    for heading, lines in blocks:
        body = [l for l in lines[1:] if l.strip()]
        if not body:
            # As a heading it would be a second level-1 in the file and so a
            # duplicate chapter in Quarto's table of contents. As a bold lead-in
            # it reads the way the page does and leaves the poem as the title.
            pending += [f"**{lines[0].lstrip('# ').strip()}**\n", "\n"]
            continue
        out.append((heading, pending + lines) if pending else (heading, lines))
        pending = []
    if pending:                       # a trailing group heading, nothing to join
        out.append((pending[0].strip("*\n"), pending))
    return out


def _is_verse_line(line):
    """A plain text line, i.e. not a heading, list item, quote, image or table."""
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith(("#", "-", "*", ">", "!", "|"))


def mark_verse(lines):
    """Give every line of a stanza a Markdown hard break.

    The extraction writes a prose paragraph as one long line and a stanza as a
    run of consecutive short ones, so "two plain lines in a row" identifies
    verse structurally rather than by guessing at length. Measured over the
    poem files: 366 lines across 120 files, and zero hits inside a "#### Notes"
    block, whose paragraphs are single lines.

    Without this every poem renders as one run-on paragraph, because Markdown
    reflows single newlines. The trailing two spaces also give check_parity's
    hard_breaks() something to count, so a translation that loses the stanza
    is caught instead of shipping as prose.
    """
    out = []
    for index, line in enumerate(lines):
        nxt = lines[index + 1] if index + 1 < len(lines) else ""
        if _is_verse_line(line) and _is_verse_line(nxt) and not line.rstrip("\n").endswith("  "):
            line = line.rstrip("\n") + "  \n"
        out.append(line)
    return out


def write(path, lines):
    """Write a block, trimming blank edges and ending with exactly one newline."""
    text = "".join(lines).strip()
    path.write_text(text + "\n", encoding="utf-8")
    return text


HEADING = re.compile(r"^(#{1,6}) ")


def normalize_headings(lines):
    """Shift a block's headings so its own title sits at level 1.

    Every file becomes a Quarto chapter, and Quarto takes a chapter's title
    from its first level-1 heading -- a file that opens at '###' renders with
    no title at all. The shift is relative, so a poem's '### Poem 7' / '####
    Notes' become '#' / '##' and a whole section's '##' / '###' become the
    same, without either having to know which case it is.
    """
    levels = [len(m.group(1)) for m in map(HEADING.match, lines) if m]
    if not levels:
        return lines
    shift = min(levels) - 1
    if not shift:
        return lines
    return [line[shift:] if HEADING.match(line) else line for line in lines]


def main():
    if not MONOLITH.exists():
        sys.exit(f"error: {MONOLITH} not found. Run generate_final_markdown.py first.")

    lines = MONOLITH.read_text(encoding="utf-8").splitlines(keepends=True)
    sections = {h: body for h, body in split_level(lines, 2) if h is not None}

    missing = [h for h, _, _ in SECTIONS if h not in sections]
    if missing:
        sys.exit(f"error: level-2 headings not found in {MONOLITH}: {missing}")

    SOURCE_DIR.mkdir(exist_ok=True)
    written = []          # (filename, heading) in reading order
    poem_index = 0

    for heading, name, split_h3 in SECTIONS:
        body = sections[heading]
        if name is None and not split_h3:
            continue                                   # dropped, e.g. Contents

        if not split_h3:
            path = SOURCE_DIR / f"{name}.md"
            write(path, normalize_headings(body))
            written.append((path.name, heading))
            continue

        blocks = merge_bodyless(
            [(h, b) for h, b in split_level(body, 3) if h is not None]
        )
        for offset, (h3, block) in enumerate(blocks, 1):
            if name is None:                           # the poems
                poem_index += 1
                path = SOURCE_DIR / f"{poem_index:03d}.md"
                block = mark_verse(block)
            else:
                path = SOURCE_DIR / f"{name}-{offset}.md"
            write(path, normalize_headings(block))
            written.append((path.name, h3))

    intro_count = sum(1 for n, _ in written if n.startswith("introduction-"))
    assert poem_index == EXPECTED_POEMS, \
        f"expected {EXPECTED_POEMS} poem blocks, got {poem_index}"
    assert intro_count == EXPECTED_INTRO, \
        f"expected {EXPECTED_INTRO} introduction blocks, got {intro_count}"

    generate_readme(written)
    print(f"Wrote {len(written)} files to {SOURCE_DIR}/ "
          f"({poem_index} poems, {intro_count} introduction, "
          f"{len(written) - poem_index - intro_count} named)")


def generate_readme(written):
    """An index of the split, so a filename can be traced back to its heading.

    Listed in [tool.book] exclude, so it is never translated or parity-checked.
    """
    rows = "\n".join(f"| `{name}` | {heading} |" for name, heading in written)
    (SOURCE_DIR / "README.md").write_text(
        "# source/\n\n"
        "The English text, split by `split_book.py`. Generated -- edit that\n"
        "script, not these files. Each file has one counterpart in `fa/` with\n"
        "the same name; `check_parity` pairs them by filename.\n\n"
        "| file | heading |\n|---|---|\n" + rows + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
