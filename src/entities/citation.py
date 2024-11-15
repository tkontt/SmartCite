class Citation:
    def __init__(self, id: int, citation_type: str, citation_key: str, fields: dict):
        self.id = id
        self.citation_type = citation_type
        self.citation_key = citation_key
        self.fields = fields
