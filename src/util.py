import secrets
import bibtexparser
from bibtexparser.bparser import BibTexParser
from repositories.citation_repository import unique_key
from entities.citation import Citation


class UserInputError(Exception):
    pass


def generate_cite_key(fields: dict):
    cite_key = ""
    for key, value in fields.items():
        if len(cite_key) > 6:
            break
        if key == "title":
            cite_key += value[:2]
        elif key == "year":
            cite_key += value[2:]
        elif key == "author":
            cite_key += value[:3]
        else:
            cite_key += value[:2]
    if len(cite_key) < 5:
        cite_key += secrets.token_hex(2)
    while not unique_key(cite_key):
        cite_key += secrets.token_hex(2)
    return cite_key


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
        invalid = False
        fields_in_correct_order = {}
        citation_key = citation["ID"]
        citation_type = citation["ENTRYTYPE"]
        citation.pop("ENTRYTYPE")
        citation.pop("ID")
        for key, value in reversed(citation.items()):
            if value == "":
                invalid = True
            fields_in_correct_order[key] = value
        if not invalid:
            if unique_key(citation_key) is False:
                citation_key = generate_cite_key(fields_in_correct_order)
            citation = Citation(citation_type, citation_key, fields_in_correct_order)
            list_of_citations.append(citation)
    return list_of_citations


def validate_bibtex(bibtex):
    if bibtex == "":
        raise UserInputError("Invalid input: empty")
    if bibtex[0] != "@":
        raise UserInputError("Invalid input: input should start with @")
