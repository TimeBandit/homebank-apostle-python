# tests/test_converter.py
import sys
from src.utils.display import display_rows_in_terminal
import pytest
from src.main import read_starling_csv, write_homebank_csv
from src.providers.starling import parse_line
import csv
import tempfile
import os

sample_data = [
    {
        'Date': '01/01/2024',
        'Counter Party': 'Starling Bank',
        'Reference': 'December Interest Earned',
        'Type': 'DEPOSIT INTEREST',
        'Amount (GBP)': '13.58',
        'Balance (GBP)': '8620.01',
        'Spending Category': 'INCOME',
        'Notes': ''
    },
    {
        'Date': '02/01/2024',
        'Counter Party': 'Affinity Water',
        'Reference': '44060495',
        'Type': 'DIRECT DEBIT',
        'Amount (GBP)': '-44.00',
        'Balance (GBP)': '8576.01',
        'Spending Category': 'GENERAL',
        'Notes': ''
    },
    {
        'Date': '25/01/2024',
        'Counter Party': 'BABATA S',
        'Reference': 'Rent January',
        'Type': 'FASTER PAYMENT',
        'Amount (GBP)': '350.00',
        'Balance (GBP)': '8715.50',
        'Spending Category': 'INCOME',
        'Notes': ''
    },
    {
        'Date': '14/11/2024',
        'Counter Party': 'Cheque',
        'Reference': 'Cheque',
        'Type': 'CICS CHEQUE',
        'Amount (GBP)': '1597.56',
        'Balance (GBP)': '12183.58',
        'Spending Category': 'INCOME',
        'Notes': ''
    }
]


@pytest.fixture
def sample_csv_data():
    """Create a temporary CSV file with sample data"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='') as temp_file:
        writer = csv.DictWriter(temp_file, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
        temp_name = temp_file.name

    yield temp_name
    os.unlink(temp_name)


def test_read_starling_csv(sample_csv_data):
    """Test reading and parsing Starling CSV file"""
    parsed_rows = read_starling_csv(sample_csv_data)

    assert len(parsed_rows) == 4
    assert parsed_rows[0]['date'] == '01/01/2024'
    assert parsed_rows[0]['payee'] == 'Starling Bank'
    assert parsed_rows[0]['memo'] == 'December Interest Earned'
    assert parsed_rows[0]['amount'] == '13.58'

    assert parsed_rows[1]['date'] == '02/01/2024'
    assert parsed_rows[1]['payee'] == 'Affinity Water'
    assert parsed_rows[1]['memo'] == '44060495'
    assert parsed_rows[1]['amount'] == '-44.00'

    assert parsed_rows[2]['date'] == '25/01/2024'
    assert parsed_rows[2]['payee'] == 'BABATA S'
    assert parsed_rows[2]['memo'] == 'Rent January'
    assert parsed_rows[2]['amount'] == '350.00'

    assert parsed_rows[3]['date'] == '14/11/2024'
    assert parsed_rows[3]['payee'] == 'Cheque'
    assert parsed_rows[3]['memo'] == 'Cheque'
    assert parsed_rows[3]['amount'] == '1597.56'


def test_write_homebank_csv(sample_csv_data):
    """Test writing parsed data to HomeBank CSV format"""
    parsed_rows = read_starling_csv(sample_csv_data)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_output:
        write_homebank_csv(temp_output.name, parsed_rows)

        # Read back the written file and verify contents
        with open(temp_output.name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            written_rows = list(reader)

            assert len(written_rows) == 4
            assert written_rows[0]['date'] == '01/01/2024'
            assert written_rows[0]['payee'] == 'Starling Bank'
            assert parsed_rows[0]['memo'] == 'December Interest Earned'
            assert written_rows[0]['amount'] == '13.58'

    os.unlink(temp_output.name)


def test_parse_line():
    """Test parsing individual lines"""

    parsed_data = parse_line(sample_data[0])
    assert parsed_data['date'] == '01/01/2024'
    assert parsed_data['payment'] == 9
    assert parsed_data['payee'] == 'Starling Bank'
    assert parsed_data['memo'] == 'December Interest Earned'
    assert parsed_data['amount'] == '13.58'

    parsed_data = parse_line(sample_data[1])
    assert parsed_data['date'] == '02/01/2024'
    assert parsed_data['payment'] == 11
    assert parsed_data['payee'] == 'Affinity Water'
    assert parsed_data['memo'] == '44060495'
    assert parsed_data['amount'] == '-44.00'

    parsed_data = parse_line(sample_data[2])
    assert parsed_data['date'] == '25/01/2024'
    assert parsed_data['payment'] == 4
    assert parsed_data['payee'] == 'BABATA S'
    assert parsed_data['memo'] == 'Rent January'
    assert parsed_data['amount'] == '350.00'

    parsed_data = parse_line(sample_data[3])
    assert parsed_data['date'] == '14/11/2024'
    assert parsed_data['payment'] == 2
    assert parsed_data['payee'] == 'Cheque'
    assert parsed_data['memo'] == 'Cheque'
    assert parsed_data['amount'] == '1597.56'


def test_invalid_csv_format():
    """Test handling of invalid CSV format"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write('invalid,csv,format\n1,2,3')
        temp_name = temp_file.name

    with pytest.raises(KeyError):
        read_starling_csv(temp_name)

    os.unlink(temp_name)


def test_empty_csv():
    """Test handling of empty CSV file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_name = temp_file.name

    parsed_rows = read_starling_csv(temp_name)
    assert len(parsed_rows) == 0

    os.unlink(temp_name)
