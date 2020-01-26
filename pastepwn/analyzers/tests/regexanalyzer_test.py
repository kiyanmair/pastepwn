# -*- coding: utf-8 -*-
import unittest
from unittest import mock
import re

from pastepwn.analyzers.regexanalyzer import RegexAnalyzer


class TestRegexAnalyzer(unittest.TestCase):

    def setUp(self):
        """Set's up a paste mock object"""
        self.paste = mock.Mock()

    def test_matchWord(self):
        analyzer = RegexAnalyzer(None, regex="word")
        self.paste.body = "This text contains the word 'word'!"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match, although it should!")
        self.assertEqual("word", analyzer.match(self.paste)[0])
        self.assertEqual("word", analyzer.match(self.paste)[1])
        self.assertEqual(2, len(analyzer.match(self.paste)))

    def test_matchPattern(self):
        analyzer = RegexAnalyzer(None, regex=r"\d{4}-123-\d{2}")
        self.paste.body = "This text contains 4444-123-55 a nice pattern!"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match, although it should!")
        self.assertEqual("4444-123-55", analyzer.match(self.paste)[0])

        self.paste.body = "This text contains 4657-123-57 a nice pattern!"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match, although it should!")
        self.assertEqual("4657-123-57", analyzer.match(self.paste)[0])

        self.paste.body = "This text contains 465-123-57 a bad pattern!"
        self.assertFalse(analyzer.match(self.paste), "The regex does match, although it shouldn't!")
        self.assertEqual([], analyzer.match(self.paste))

    def test_multiple(self):
        analyzer = RegexAnalyzer(None, regex=r"\d{4}-123-\d{2}")
        self.paste.body = "This text contains 4444-123-55 and 1864-123-11 and 1649-123-00 which in total are three nice patterns!"
        self.assertEqual(3, len(analyzer.match(self.paste)))
        self.assertEqual("4444-123-55", analyzer.match(self.paste)[0])
        self.assertEqual("1864-123-11", analyzer.match(self.paste)[1])
        self.assertEqual("1649-123-00", analyzer.match(self.paste)[2])

    def test_flags(self):
        """We only test a few flags, because as long as we use regex this should work fine"""
        analyzer = RegexAnalyzer(None, regex=r"ThIs iS mIxEd")
        self.paste.body = "this is mixed case (not)"
        self.assertFalse(analyzer.match(self.paste), "The regex does match, although it shouldn't!")

        # Test case independend flag / ignorecase
        analyzer = RegexAnalyzer(None, regex=r"ThIs iS mIxEd", flags=re.IGNORECASE)
        self.paste.body = "this is mixed case (not)"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match, although it should!")

        # Test multiline
        analyzer = RegexAnalyzer(None, regex=r"^regexiscool", flags=re.MULTILINE)
        self.paste.body = "this is a multiline string\nregexiscool is right at the start of the line\nand another line!"
        self.assertTrue(analyzer.match(self.paste), "The regex does not match in multiline strings, although it should!")

    def test_negativeMatch(self):
        """Test a case where the regex should not match"""
        analyzer = RegexAnalyzer(None, regex=r"[a-zA-Z]{15}")
        self.paste.body = "abcdef1ghijklmn and a lot more characters"
        self.assertFalse(analyzer.match(self.paste), "The regex does match, although it shouldn't!")

    def test_emptyBody(self):
        """Empty bodies should not match"""
        analyzer = RegexAnalyzer(None, regex=r"[0-9]", flags=re.MULTILINE)
        self.paste.body = ""
        self.assertFalse(analyzer.match(self.paste), "The regex does match, although it shouldn't!")
        self.assertEqual([], analyzer.match(self.paste))


if __name__ == '__main__':
    unittest.main()
