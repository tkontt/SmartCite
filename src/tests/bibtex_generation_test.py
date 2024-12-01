import unittest
from entities.citation import Citation
from util import generate_bibtex

class TestBibtexGeneration(unittest.TestCase):
    def setUp(self):
        pass

    def test_bibtex_generates_correctly(self):
        citations = []
        citations.append(Citation("article", "1",
        {
            "author": "1",
            "title": "1",
            "year": "1",
            "journal": "1"
        }))
        citations.append(Citation("article", "2",
        {
            "author": "2",
            "title": "2",
            "year": "2",
            "journal": "2"
        }))

        bibtex = generate_bibtex(citations)

        expected = """@article{1,
\tauthor = {1},
\ttitle = {1},
\tyear = {1},
\tjournal = {1},
}

@article{2,
\tauthor = {2},
\ttitle = {2},
\tyear = {2},
\tjournal = {2},
}

"""

        self.assertEqual(bibtex, expected)

    def test_empty_bibtex_generates_correctly(self):
        citations = []
        bibtex = generate_bibtex(citations)
        self.assertEqual(bibtex, "")
