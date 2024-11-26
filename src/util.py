import secrets
from repositories.citation_repository import unique_key

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
