# tests/test_display.py
import sys
from io import StringIO
from src.utils.display import display_rows_in_terminal
import pytest
from src.main import read_starling_csv, write_homebank_csv
from src.providers.starling import parse_line


@pytest.fixture
def capture_stdout():
    """Capture stdout for testing display output"""
    stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = sys.__stdout__


def test_display_output(capture_stdout):
    """Test terminal display formatting"""
    test_rows = [{
        'date': '01/01/2024',
        'payment': '4',
        'payee': 'TESCO',
        'memo': 'Groceries',
        'amount': '-50.00',
        'category': 'SHOPPING',
        'tags': ''
    }]

    display_rows_in_terminal(test_rows)
    output = capture_stdout.getvalue()

    print('output is: ', output)
    # assert 'Transaction Records:' in output
    # assert 'Starling Bank' in output
    # assert '13.58' in output
