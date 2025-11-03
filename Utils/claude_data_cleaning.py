# Utils/data_cleaning.py
import pandas as pd
import numpy as np
from typing import Optional, List


class MetaDataCleaner:
    """Utility class for cleaning chess game metadata DataFrames."""
    
    @staticmethod
    def clean_metadata(df: pd.DataFrame, 
                       drop_cols: Optional[List[str]] = None,
                       required_cols: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Clean metadata DataFrame with standard transformations.
        
        Args:
            df: Raw metadata DataFrame from MetaData.to_dataframe()
            drop_cols: List of columns to drop (optional)
            required_cols: Keep only rows that have these columns non-null (optional)
            
        Returns:
            Cleaned DataFrame
        """
        df = df.copy()  # Don't modify original
        
        # 1. Convert common columns to appropriate types
        df = MetaDataCleaner._convert_types(df)
        
        # 2. Handle missing values
        df = MetaDataCleaner._handle_missing(df)
        
        # 3. Standardize Result column
        if 'Result' in df.columns:
            df = MetaDataCleaner._standardize_result(df)
        
        # 4. Drop specified columns
        if drop_cols:
            df = df.drop(columns=[col for col in drop_cols if col in df.columns])
        
        # 5. Filter by required columns
        if required_cols:
            mask = df[required_cols].notna().all(axis=1)
            df = df[mask]
        
        return df
    
    @staticmethod
    def _convert_types(df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types."""
        # Convert Elo ratings to numeric
        for col in ['WhiteElo', 'BlackElo']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert Date to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d', errors='coerce')
        
        # Convert UTCDate and UTCTime if available
        if 'UTCDate' in df.columns:
            df['UTCDate'] = pd.to_datetime(df['UTCDate'], format='%Y.%m.%d', errors='coerce')
        
        if 'UTCTime' in df.columns:
            df['UTCTime'] = pd.to_datetime(df['UTCTime'], format='%H:%M:%S', errors='coerce').dt.time
        
        return df
    
    @staticmethod
    def _handle_missing(df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in common columns."""
        # Replace '?' with NaN (common in PGN files)
        df = df.replace('?', np.nan)
        df = df.replace('', np.nan)
        
        return df
    
    @staticmethod
    def _standardize_result(df: pd.DataFrame) -> pd.DataFrame:
        """Standardize Result column values."""
        result_map = {
            '1-0': 'White',
            '0-1': 'Black',
            '1/2-1/2': 'Draw',
            '*': 'Unknown'
        }
        
        if 'Result' in df.columns:
            df['Result_Category'] = df['Result'].map(result_map)
        
        return df
    
    @staticmethod
    def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Add useful derived columns."""
        df = df.copy()
        
        # Elo difference
        if 'WhiteElo' in df.columns and 'BlackElo' in df.columns:
            df['Elo_Diff'] = df['WhiteElo'] - df['BlackElo']
        
        # Average Elo
        if 'WhiteElo' in df.columns and 'BlackElo' in df.columns:
            df['Avg_Elo'] = (df['WhiteElo'] + df['BlackElo']) / 2
        
        # Extract year, month from Date
        if 'Date' in df.columns and pd.api.types.is_datetime64_any_dtype(df['Date']):
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            df['YearMonth'] = df['Date'].dt.to_period('M')
        
        # Time control category
        if 'TimeControl' in df.columns:
            df['Time_Category'] = df['TimeControl'].apply(MetaDataCleaner._categorize_time_control)
        
        return df
    
    @staticmethod
    def _categorize_time_control(tc: str) -> str:
        """Categorize time control into Bullet, Blitz, Rapid, Classical."""
        if pd.isna(tc) or tc == '-':
            return 'Unknown'
        
        try:
            # Parse formats like "180+0" or "600+5"
            if '+' in str(tc):
                base_time = int(tc.split('+')[0])
            else:
                base_time = int(tc)
            
            if base_time < 180:
                return 'Bullet'
            elif base_time < 600:
                return 'Blitz'
            elif base_time < 1500:
                return 'Rapid'
            else:
                return 'Classical'
        except:
            return 'Unknown'
    
    @staticmethod
    def filter_by_criteria(df: pd.DataFrame, 
                          min_elo: Optional[int] = None,
                          max_elo: Optional[int] = None,
                          result: Optional[str] = None,
                          player_name: Optional[str] = None) -> pd.DataFrame:
        """
        Filter DataFrame by common criteria.
        
        Args:
            df: Cleaned metadata DataFrame
            min_elo: Minimum average Elo rating
            max_elo: Maximum average Elo rating
            result: Filter by result ('White', 'Black', 'Draw')
            player_name: Filter games where this player participated
            
        Returns:
            Filtered DataFrame
        """
        df = df.copy()
        
        # Filter by Elo
        if min_elo and 'Avg_Elo' in df.columns:
            df = df[df['Avg_Elo'] >= min_elo]
        
        if max_elo and 'Avg_Elo' in df.columns:
            df = df[df['Avg_Elo'] <= max_elo]
        
        # Filter by result
        if result and 'Result_Category' in df.columns:
            df = df[df['Result_Category'] == result]
        
        # Filter by player name
        if player_name:
            if 'White' in df.columns and 'Black' in df.columns:
                df = df[(df['White'].str.contains(player_name, case=False, na=False)) | 
                       (df['Black'].str.contains(player_name, case=False, na=False))]
        
        return df


class MoveDataCleaner:
    """Utility class for cleaning chess move data DataFrames."""
    
    @staticmethod
    def clean_moves(df: pd.DataFrame, 
                    drop_mate_scores: bool = False,
                    convert_time_to_seconds: bool = True) -> pd.DataFrame:
        """
        Clean move data DataFrame.
        
        Args:
            df: Raw moves DataFrame from MoveData.get_game_moves()
            drop_mate_scores: Whether to drop rows with mate scores (M+/M-)
            convert_time_to_seconds: Convert time strings to seconds
            
        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        
        # Convert time to seconds if requested
        if convert_time_to_seconds:
            for col in ['white_time', 'black_time']:
                if col in df.columns:
                    df[col] = df[col].apply(MoveDataCleaner._time_to_seconds)
        
        # Handle mate scores
        if drop_mate_scores:
            for col in ['white_eval', 'black_eval']:
                if col in df.columns:
                    df = df[~df[col].astype(str).str.startswith('M', na=False)]
        
        return df
    
    @staticmethod
    def _time_to_seconds(time_str: str) -> Optional[float]:
        """Convert time string like '0:05:30' to seconds."""
        if pd.isna(time_str):
            return np.nan
        
        try:
            parts = str(time_str).split(':')
            if len(parts) == 3:
                hours, minutes, seconds = map(float, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                minutes, seconds = map(float, parts)
                return minutes * 60 + seconds
            else:
                return float(time_str)
        except:
            return np.nan
    
    @staticmethod
    def add_move_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Add derived metrics from move data."""
        df = df.copy()
        
        # Eval changes (how much position changed after each move)
        if 'white_eval' in df.columns:
            df['white_eval_numeric'] = pd.to_numeric(df['white_eval'], errors='coerce')
            df['white_eval_change'] = df['white_eval_numeric'].diff()
        
        if 'black_eval' in df.columns:
            df['black_eval_numeric'] = pd.to_numeric(df['black_eval'], errors='coerce')
            df['black_eval_change'] = df['black_eval_numeric'].diff()
        
        # Time spent per move
        if 'white_time' in df.columns:
            df['white_time_spent'] = -df['white_time'].diff()
        
        if 'black_time' in df.columns:
            df['black_time_spent'] = -df['black_time'].diff()
        
        return df