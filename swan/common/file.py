class File:
    def __init__(self, name, url, cid, created_at, updated_at):
        self.name = name
        self.url = url
        self.cid = cid
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "name": self.name,
            "cid": self.cid,
            "url": self.url,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
        }
