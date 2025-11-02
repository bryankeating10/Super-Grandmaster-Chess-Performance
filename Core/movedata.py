class MoveData:
    def __init__(self, game, game_id):
        self.game_id = game_id
        self.game = game
        self.moves_df = self._parse_moves()

    def _parse_moves(self):
        # parse game moves into DataFrame
        pass

    def move_count(self):
        return len(self.moves_df)
