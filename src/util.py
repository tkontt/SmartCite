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
        if len(cite_key) > 5:
            break
        if key == "title":
            part_title = value[:3]
            cite_key += part_title
        if key == "year":
            cite_key += value[2:]
        if key == "author":
            cite_key += value[:3]
        else:
            cite_key += value[:1]
    if len(cite_key) < 5:
        cite_key += secrets.token_hex(2)
    if unique_key(cite_key):
        return cite_key
    cite_key += secrets.token_hex(2)
    if unique_key(cite_key):
        return cite_key
    return generate_cite_key(fields)


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
        validate_fields(fields_in_correct_order)
        if unique_key(citation_key) is False:
            citation_key = generate_cite_key(fields_in_correct_order)
        citation = Citation(citation_type, citation_key, fields_in_correct_order)
        list_of_citations.append(citation)
    return list_of_citations


def validate_bibtex(bibtex):
    if bibtex == "":
        raise UserInputError("Not a valid input")
    if bibtex[0] != "@":
        raise UserInputError("The input should start with @")
    if bibtex[-1] != "}":
        raise UserInputError("The input should end with }")


def valid_inputs(bibtex, list_of_valid):
    amount_of_inputted_citations = bibtex.count("@")
    if amount_of_inputted_citations != len(list_of_valid):
        difference = amount_of_inputted_citations - len(list_of_valid)
        print(difference)
        raise UserInputError(
            f"""{difference} of the citation/s were not in valid form.
            {len(list_of_valid)} was/were added"""
        )
