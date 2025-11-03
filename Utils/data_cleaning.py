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
        # More cleaning steps can be added here later
        return df

    @staticmethod
    def replace_with_nan(df: pd.DataFrame) -> pd.DataFrame:
        """Replace placeholders with NaN and safely re-infer data types."""
        cleaned = df.replace(["", "?", "-"], np.nan)
        cleaned = cleaned.infer_objects(copy=False)
        return cleaned

class MoveDataCleaner:
    '''Utility class for cleaning movedata lists'''

    @staticmethod
    def clean_movedata(mv_list: list):
        pass