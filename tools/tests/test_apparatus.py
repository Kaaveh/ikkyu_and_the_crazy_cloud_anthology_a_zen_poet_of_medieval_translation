#!/usr/bin/env python3
"""Checks for this book's adapter.

The engine is tested in bargardan_tools/tests; this covers only the half that
knows about this book -- which heading parts are structure, and whether the
stanza survives.

Run:  just test        (or: python3 -m unittest discover -s tools/tests)
"""

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO))

from tools import apparatus


def roundtrip(name, text):
    """strip, then restore with the identity 'translation'."""
    return apparatus.restore_text(name, text, apparatus.strip_text(name, text))


class HeadingRendering(unittest.TestCase):
    def test_poem_label_is_persian_and_title_is_left_alone(self):
        out = roundtrip("002.md", "# Poem 7: Praising Monk\n\nA line.\n")
        self.assertIn("# شعر ۷: Praising Monk", out)

    def test_notes_label_keeps_its_blank_line(self):
        # A \s*$ in the pattern once ate the newline and welded the heading to
        # the paragraph below, which check_parity then reports as a lost block.
        out = roundtrip("002.md", "# Poem 7: T\n\nLine.\n\n## Notes\n\nA note.\n")
        self.assertIn("## یادداشت‌ها\n\nA note.", out)

    def test_named_file_takes_its_title_from_pyproject(self):
        out = roundtrip("foreword.md", "# Foreword by Someone\n\nText.\n")
        self.assertIn("# پیش‌گفتار", out)
        self.assertNotIn("Foreword by Someone", out)

    def test_heading_with_no_configured_title_is_left_for_the_translator(self):
        # "Primary Sources" has no [tool.book.titles] entry, so the pattern
        # must not match it -- the engine reads a None render as "drop".
        out = roundtrip("bibliography.md", "# Bibliography\n\n## Primary Sources\n\nX.\n")
        self.assertIn("## Primary Sources", out)

    def test_prose_introduction_keeps_its_reference_numbers(self):
        out = roundtrip("129.md", "# Prose Introduction to Nos. 819, 820\n\nText.\n")
        self.assertIn("۸۱۹", out)
        self.assertIn("۸۲۰", out)


class HardBreaks(unittest.TestCase):
    def test_breaks_are_restored_run_by_run(self):
        source = "# Poem 7: T\n\nOne.  \nTwo.  \nThree.\n"
        draft = apparatus.strip_text("002.md", source).replace("  \n", "\n")
        out = apparatus.restore_text("002.md", source, draft)
        self.assertEqual(out.count("  \n"), 2)

    def test_a_run_the_model_rebroke_does_not_block_the_others(self):
        # The model reformats verse quoted inside a prose note into real lines
        # -- correctly. Whole-file positional alignment gives up at that point;
        # this must still repair the stanza above it.
        source = "# Poem 7: T\n\nOne.  \nTwo.\n\nA prose note quoting a poem.\n"
        draft = ("# ⟦1⟧ T\n\nOne.\nTwo.\n\n"
                 "A prose note\nquoting\na poem.\n")
        out = apparatus.restore_text("002.md", source, draft)
        self.assertEqual(out.count("  \n"), 1)


class Corpus(unittest.TestCase):
    """The whole of source/, if it has been generated."""

    def test_every_file_round_trips(self):
        source_dir = REPO / "source"
        files = [p for p in sorted(source_dir.glob("*.md"))
                 if p.name not in apparatus.EXCLUDE] if source_dir.is_dir() else []
        if not files:
            self.skipTest("source/ not generated; run `just split`")
        for path in files:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                out = roundtrip(path.name, text)
                self.assertNotIn("⟦", out, "sentinel leaked into the output")
                for label, want in (("hard breaks", lambda t: sum(
                        1 for l in t.split("\n") if l.endswith("  ") and l.strip())),
                        ("headings", lambda t: sum(
                            1 for l in t.split("\n") if l.startswith("#")))):
                    self.assertEqual(want(text), want(out), label)


if __name__ == "__main__":
    unittest.main()
