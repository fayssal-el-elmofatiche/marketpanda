import pytest
from marketpanda import MarketPanda
import pandas as pd

db_path = "/Users/fayssalelmofatiche/dev/dnbf/data/marketvault.db"

@pytest.fixture
def mp():
    return MarketPanda(db_path=db_path)

def test_symbols(mp):
    assert mp.symbols is not None

def test_symbols_type(mp):
    assert type(mp.symbols) == pd.core.frame.DataFrame

def test_symbols_columns(mp):
    print(mp.symbols.columns)

    assert sorted(mp.symbols.columns) == sorted(['id', 'exchange_id', 'ticker', 'instrument', 'name', 'sector',
       'currency', 'created_date', 'last_updated_date'])
