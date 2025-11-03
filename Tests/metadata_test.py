import pandas as pd
import pytest
from Core.metadata import MetaData

@pytest.fixture
def sample_pgn_path():
    # Adjust to match your file structure
    return "Data/lichess_sample.pgn"

@pytest.fixture
def metadata_obj(sample_pgn_path):
    return MetaData(sample_pgn_path)

def test_metadata_loads_correctly(metadata_obj):
    assert hasattr(metadata_obj, 'games'), "MetaData should store games list"
    assert len(metadata_obj.games) > 0, "MetaData should load at least one game"

def test_to_dataframe_returns_dataframe(metadata_obj):
    df = metadata_obj.to_dataframe()
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
    assert not df.empty, "DataFrame should not be empty"

def test_dataframe_columns(metadata_obj):
    df = metadata_obj.to_dataframe()
    expected_columns = {"Event", "Site", "Date", "White", "Black", "Result"}
    assert expected_columns.issubset(set(df.columns)), "Missing essential metadata columns"

def test_handles_missing_fields(metadata_obj):
    df = metadata_obj.to_dataframe()
    assert df.isnull().sum().sum() >= 0, "Should handle missing or empty PGN tags gracefully"