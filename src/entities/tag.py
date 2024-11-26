
class Tag:
    def __init__(self, tag, tag_id: int = None):
        self.id = tag_id
        self.tag = tag

    def __str__(self):
        return f"{self.id}, {self.tag}"

    def to_dict(self):
        return {
            "id": self.id,
            "tag": self.tag,
        }
