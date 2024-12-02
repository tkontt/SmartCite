import unittest
from unittest.mock import patch
from util import generate_cite_key


class TestCiteKeyGeneration(unittest.TestCase):
    def setUp(self):
        self.fields = {
            "author": "Joulupukki",
            "title": "Toimitusketjujen optimointi",
            "year": "2020",
            "journal": "JouluTiedeJournal",
        }

    @patch("util.unique_key")
    def test_generate_cite_key(self, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou88"]

        mock_unique_key.side_effect = unique

        key = generate_cite_key(self.fields)
        expected = "JouTo20"
        self.assertEqual(expected, key)
