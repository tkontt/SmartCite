import secrets
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
    return bibtex
