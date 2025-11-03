import pandas as pd
import numpy as np

class MetaDataCleaner:
    """Utility class for cleaning metadata DataFrames."""

    @staticmethod
    def clean_metadata(df: pd.DataFrame) -> pd.DataFrame:
        """Perform all metadata cleaning steps."""
        df = MetaDataCleaner.replace_with_nan(df)
        return df
    
    @staticmethod
    def replace_with_nan(df: pd.DataFrame) -> pd.DataFrame:
        """Replace placeholders with NaN, safely handling dtype conversion."""
        # Perform replacement and explicitly re-infer data types
        cleaned = df.replace(["", "?", "-"], np.nan)
        # Explicitly trigger Pandas to handle downcasting safely
        cleaned = cleaned.infer_objects(copy=False)
        return cleaned

class MoveDataCleaner:
    '''Utility class for cleaning movedata lists'''

    @staticmethod
    def clean_movedata(mv_list: list):
        pass