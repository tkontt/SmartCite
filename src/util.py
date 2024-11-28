import secrets
import bibtexparser
from bibtexparser.bparser import BibTexParser
from repositories.citation_repository import unique_key
from entities.citation import Citation


class UserInputError(Exception):
    pass


def generate_cite_key():
    key = secrets.token_hex(6)
    if unique_key(key):
        return key
    return generate_cite_key()


def validate_fields(fields):
    if "" in fields.values():
        raise UserInputError("Missing required fields")


def generate_bibtex(citations: list[Citation]):
    bibtex = ""
    for citation in citations:
        bibtex += f"@{citation.citation_type}{{{citation.citation_key},\n"
        for field_name, field_value in citation.fields.items():
            bibtex += f"\t{field_name} = {{{field_value}}},\n"
        bibtex += "}\n\n"

    return bibtex


def import_bibtex_citations(bibtex):
    list_of_citations = []
    parser = BibTexParser()
    citations = bibtexparser.loads(bibtex, parser)
    for citation in citations.entries:
        fields_in_correct_order = {}
        citation_key = citation["ID"]
        citation_type = citation["ENTRYTYPE"]
        citation.pop("ENTRYTYPE")
        citation.pop("ID")
        for key, value in reversed(citation.items()):
            fields_in_correct_order[key] = value
        if unique_key(citation_key) is False:
            citation_key = generate_cite_key()
        validate_fields(fields_in_correct_order)
        citation = Citation(citation_type, citation_key, fields_in_correct_order)
        list_of_citations.append(citation)
    return list_of_citations
