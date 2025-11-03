import chess.pgn as ch
import pandas as pd
import numpy as np
import re

class MoveData:
    def __init__(self, pgn_path):
        self.pgn_path = pgn_path # Path to pgn file
        self.moves_dict = self._extract_moves() # Extracts move data from pgn

    def _extract_moves(self):
        """Read PGN file and extract move data for each game safely."""
        moves_dict = {} # To store game:move_dataframe key-value pairs

        with open(self.pgn_path, encoding="utf-8") as pgn:
            game_id = 1 # Index of first game

            while True: # Testing game format validity
                try:
                    game = ch.read_game(pgn)
                except Exception:
                    continue
                if game is None:
                    break

                moves = self._parse_game_moves(game)
                if not moves.empty:
                    moves_dict[game_id] = moves
                    game_id += 1
        return moves_dict

    def _parse_game_moves(self, game):
        """Extract moves in wide format with white and black columns."""
        moves = []
        node = game
        move_number = 1
        white_move = np.nan
        white_time = np.nan
        white_eval = np.nan

        while node.variations:
            next_node = node.variation(0)
            move_san = next_node.san()
            comment = next_node.comment or ""

            time = self._extract_clock_time(comment)
            evaluation = self._extract_evaluation(comment)
            color = "white" if node.board().turn else "black"

            if color == "white":
                # Store white's move data
                white_move = move_san
                white_time = time
                white_eval = evaluation
            else:
                # Black's move - create row with both white and black data
                moves.append({
                    "move_number": move_number,
                    "white_move": white_move,
                    "white_time": white_time,
                    "white_eval": white_eval,
                    "black_move": move_san,
                    "black_time": time,
                    "black_eval": evaluation,
                })
                move_number += 1
                # Reset white data
                white_move = np.nan
                white_time = np.nan
                white_eval = np.nan

            node = next_node

        # Handle case where game ends on white's move (no black response)
        if white_move is not None:
            moves.append({
                "move_number": move_number,
                "white_move": white_move,
                "white_time": white_time,
                "white_eval": white_eval,
                "black_move": np.nan,
                "black_time": np.nan,
                "black_eval": np.nan,
            })

        df = pd.DataFrame(moves)
        if not df.empty:
            df.set_index("move_number", inplace=True)
        return df

    def _extract_clock_time(self, comment):
        """
        Extract clock time from a comment string like:
        { [%eval 0.17] [%clk 0:00:30] } or {[%clk 0:03:00]}
        Returns the time as a string or None if not found.
        """
        if not comment:
            return np.nan
        match = re.search(r"\[%clk\s*([0-9:\.]+)\]", comment)
        return match.group(1) if match else np.nan

    def _extract_evaluation(self, comment):
        """
        Extract engine evaluation value from comments like:
        { [%eval 0.17] } or { [%eval -3.15] } or { [%eval #5] }
        Returns a float (centipawn), 'M5' for mate, or None.
        """
        if not comment:
            return np.nan

        match = re.search(r"\[%eval\s*([#\-0-9\.]+)\]", comment)
        if not match:
            return np.nan

        eval_str = match.group(1)
        if eval_str.startswith("#"):
            # Mate score (e.g., #5 means mate in 5)
            return f"M{eval_str[1:]}"
        try:
            return float(eval_str)
        except ValueError:
            return np.nan

    def get_game_moves(self, game_id):
        """Return moves DataFrame for a specific game."""
        return self.moves_dict.get(game_id)

    def to_dict(self):
        """Return all move data as dictionary."""
        return self.moves_dict