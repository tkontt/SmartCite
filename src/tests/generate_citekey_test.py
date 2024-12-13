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

    @patch("util.unique_key")
    @patch("secrets.token_hex")
    def test_generate_cite_key_with_few_fields(self, mock_token_hex, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou88"]

        mock_unique_key.side_effect = unique
        mock_token_hex.return_value = "abcd"
        fields = {"author": "Jo", "year": "2020"}
        cite_key = generate_cite_key(fields)
        expected = "Jo20abcd"
        self.assertEqual(expected, cite_key)

    @patch("util.unique_key")
    @patch("secrets.token_hex")
    def test_generate_cite_key_with_short_fields(self, mock_token_hex, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou88"]

        mock_unique_key.side_effect = unique
        mock_token_hex.return_value = "abcd"
        fields = {"author": "J", "edition": "5"}
        cite_key = generate_cite_key(fields)
        self.assertEqual(cite_key, "J5abcd")

    @patch("util.unique_key")
    @patch("secrets.token_hex")
    def test_generate_cite_key_with_empty_fields(self, mock_token_hex, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou88"]

        mock_unique_key.side_effect = unique
        mock_token_hex.return_value = "abcd"
        fields = {}
        cite_key = generate_cite_key(fields)
        self.assertEqual(cite_key, "abcd")

    @patch("util.unique_key")
    @patch("secrets.token_hex")
    def test_generate_cite_key_not_unique_after_generating(
        self, mock_token_hex, mock_unique_key
    ):
        def unique(key):
            return key not in ["JouTo20", "Jou88"]

        mock_unique_key.side_effect = unique
        mock_token_hex.return_value = "abcd"
        cite_key = generate_cite_key(self.fields)
        self.assertEqual(cite_key, "JouTo20abcd")
