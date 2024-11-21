import json

class Citation:
    def __init__(self, citation_type: str, citation_key: str, fields: dict, id: int = None):
        self.id = id
        self.citation_type = citation_type
        self.citation_key = citation_key
        self.fields = fields

    def __str__(self):
        data = {
            "id": self.id,
            "citation_type" : self.citation_type,
            "citation_key" : self.citation_key,
            "fields" : self.fields 
            }
    
        return json.dumps(data)
    
    def to_dict(self):
        """
        Converts the Citation object to a dictionary.
        """
        return {
            "id": self.id,
            "citation_type": self.citation_type,
            "citation_key": self.citation_key,
            "fields": self.fields,
        } 