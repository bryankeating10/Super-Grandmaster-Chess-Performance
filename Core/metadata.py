# Core/metadata.py
import chess.pgn as ch
import pandas as pd

class MetaData:
    def __init__(self, pgn_path: str):
        self.pgn_path = pgn_path # Path to pgn file
        self.metadata_list = [] # To store game metadata dictionaries 
        self._extract_metadata() # Extracts metadata from pgn

    def _extract_metadata(self):
        """Read the PGN file and extract metadata for all games."""
        with open(self.pgn_path) as pgn:
            game_id = 1 # Index of first game
            while True:
                game = ch.read_game(pgn) # Read next game from file
                if game is None: # End of file
                    break

                headers = dict(game.headers) # Extract metadata categories
                headers["Game_ID"] = game_id # Add a game ID category
                self.metadata_list.append(headers) # List of all game metadata
                game_id += 1 # Next game index

    def to_dataframe(self):
        """Return a DataFrame of all game metadata."""
        df = pd.DataFrame(self.metadata_list) # Converts metadata list to dataframe
        if "Game_ID" in df.columns:
            df.set_index("Game_ID", inplace=True) # Sets game ID as index
        return df