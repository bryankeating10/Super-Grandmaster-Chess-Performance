import pandas as pd
import numpy as np

class MetaDataCleaner:
    '''Utility class for cleaning metadata Dataframes'''

    @staticmethod
    def clean_metadata(df: pd.DataFrame):
        df = df.copy() # Avoid modifying original

class MoveDataCleaner:
    '''Utility class for cleaning movedata lists'''

    @staticmethod
    def clean_movedata(mv_list: list):
        pass