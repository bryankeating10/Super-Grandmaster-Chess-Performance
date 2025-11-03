import pandas as pd
import numpy as np

# Opt in to Pandas’ future behavior (no warnings about downcasting)
pd.set_option('future.no_silent_downcasting', True)


class MetaDataCleaner:
    """Utility class for cleaning metadata DataFrames."""

    @staticmethod
    def clean_metadata(df: pd.DataFrame) -> pd.DataFrame:
        """Perform all metadata cleaning steps."""
        df = MetaDataCleaner.replace_with_nan(df)
        df = MetaDataCleaner.convert_to_datetime(df)
        # More cleaning steps can be added here later
        return df

    @staticmethod
    def replace_with_nan(df: pd.DataFrame) -> pd.DataFrame:
        """Replace placeholders with NaN and safely re-infer data types."""
        cleaned = df.replace(["", "?", "-"], np.nan)
        cleaned = cleaned.infer_objects(copy=False)
        return cleaned

    @staticmethod
    def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
        """Convert date and time columns to datetime objects safely. Unparseable values become NaN."""
        date_columns = ["Date", "UTCDate", "EndDate"]
        time_columns = ["UTCTime", "StartTime", "EndTime"]
        df = df.copy()

        # Convert date columns
        for date_col in date_columns:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="%Y.%m.%d")

        # Convert time columns
        for time_col in time_columns:
            if time_col in df.columns:
                df[time_col] = pd.to_datetime(df[time_col], errors="coerce", format="%H:%M:%S").dt.time

        return df

class MoveDataCleaner:
    '''Utility class for cleaning movedata lists'''

    @staticmethod
    def clean_movedata(mv_list: list):
        pass