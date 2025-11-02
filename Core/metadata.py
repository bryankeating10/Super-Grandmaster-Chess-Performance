class MetaData:
    def __init__(self, headers, game_id):
        self.game_id = game_id
        self.headers = headers

    def to_dict(self):
        return {"Game_ID": self.game_id, **self.headers}

    def players(self):
        return self.headers.get("White"), self.headers.get("Black")