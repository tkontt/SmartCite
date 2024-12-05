import unittest
from unittest.mock import patch
from entities.citation import Citation
from util import (
    import_bibtex_citations,
    validate_bibtex,
    UserInputError,
)


class TestImportBibtex(unittest.TestCase):
    def setUp(self):
        self.bibtex = """@article{Jou20,
\tauthor = {Joulupukki},
\ttitle = {Toimitusketjujen optimointi},
\tyear = {2020},
\tjournal = {JouluTiedeJournal},
}

@article{Jou88,
\tauthor = {Joulumuori},
\ttitle = {Joulupuuron salainen ainesosa},
\tyear = {1888},
\tjournal = {JouluTiedeJournal},
}"""

    @patch("util.unique_key")
    @patch("util.generate_cite_key")
    def test_importing_valid_bibtex(self, mock_generate_cite_key, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou88"]

        mock_unique_key.side_effect = unique

        def generate(fields):
            author = fields.get("author", "")[:4]
            return author

        mock_generate_cite_key.side_effect = generate

        lista = import_bibtex_citations(self.bibtex)

        expected = [
            Citation(
                "article",
                "Jou20",
                {
                    "author": "Joulupukki",
                    "title": "Toimitusketjujen optimointi",
                    "year": "2020",
                    "journal": "JouluTiedeJournal",
                },
            ),
            Citation(
                "article",
                "Joul",
                {
                    "author": "Joulumuori",
                    "title": "Joulupuuron salainen ainesosa",
                    "year": "1888",
                    "journal": "JouluTiedeJournal",
                },
            ),
        ]

        self.assertEqual([e.to_dict() for e in expected], [l.to_dict() for l in lista])

    @patch("util.unique_key")
    @patch("util.generate_cite_key")
    def test_importing_invalid_bibtex(self, mock_generate_cite_key, mock_unique_key):
        def unique(key):
            return key not in ["Jou10", "Jou98"]

        mock_unique_key.side_effect = unique

        def generate(fields):
            author = fields.get("author", "")[:4]
            return author

        mock_generate_cite_key.side_effect = generate

        bibtex = """@article{Jou20,
\tauthor = {},
\ttitle = {Toimitusketjujen optimointi},
\tyear = {2020},
\tjournal = {JouluTiedeJournal},
}

@article{Jou88,
\tauthor = {Joulumuori},
\ttitle = {Joulupuuron salainen ainesosa},
\tyear = {1888},
\tjournal = {JouluTiedeJournal},
}"""

        lista = import_bibtex_citations(bibtex)

        expected = [
            Citation(
                "article",
                "Jou88",
                {
                    "author": "Joulumuori",
                    "title": "Joulupuuron salainen ainesosa",
                    "year": "1888",
                    "journal": "JouluTiedeJournal",
                },
            ),
        ]

        self.assertEqual([e.to_dict() for e in expected], [l.to_dict() for l in lista])

    def test_validate_bibtex(self):
        with self.assertRaises(UserInputError):
            validate_bibtex("")
        with self.assertRaises(UserInputError):
            validate_bibtex("moivaan!")
        validate_bibtex(self.bibtex)
