import pandas as pd
import numpy as np

class MetaDataCleaner:
    '''Utility class for cleaning metadata Dataframes'''

    @staticmethod
    def clean_metadata(df: pd.DataFrame) -> pd.DataFrame:
        '''Perform all metadata cleaning operations'''
        df = df.copy() # Avoid modifying original
        df = MetaDataCleaner.replace_with_nan(df) # Replace placeholder values with np.nan

        # More cleaning steps here

        return df
    
    @staticmethod
    def replace_with_nan(df: pd.DataFrame) -> pd.DataFrame:
        """Replace placeholders with NaN, safely handling dtype conversion."""
        cleaned = df.replace(["", "?", "-"], np.nan)
        return cleaned.infer_objects(copy=False)


class MoveDataCleaner:
    '''Utility class for cleaning movedata lists'''

    @staticmethod
    def clean_movedata(mv_list: list):
        pass