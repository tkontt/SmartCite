import secrets
from repositories.citation_repository import unique_key

def generate_cite_key():
    key = secrets.token_hex(6)
    if unique_key(key):
        return key
    return generate_cite_key()
