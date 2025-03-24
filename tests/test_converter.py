# tests/test_converter.py
import sys
from src.utils.display import display_rows_in_terminal
import pytest
from src.main import read_starling_csv, write_homebank_csv
from src.providers.starling import parse_line
import csv
import tempfile
import os


@pytest.fixture
def sample_csv_data():
    """Create a temporary CSV file with sample data"""
    sample_data = [
        {
            'Date': '01/01/2024',
            'Counter Party': 'TESCO',
            'Reference': 'Groceries',
            'Type': 'CARD_PAYMENT',
            'Amount (GBP)': '-50.00',
            'Balance (GBP)': '1000.00',
            'Spending Category': 'SHOPPING'
        },
        {
            'Date': '02/01/2024',
            'Counter Party': 'SALARY',
            'Reference': 'January Salary',
            'Type': 'DEPOSIT',
            'Amount (GBP)': '2000.00',
            'Balance (GBP)': '3000.00',
            'Spending Category': 'INCOME'
        }
    ]

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

    assert len(parsed_rows) == 2
    assert parsed_rows[0]['date'] == '01/01/2024'
    assert parsed_rows[0]['payee'] == 'TESCO'
    assert parsed_rows[0]['memo'] == 'Groceries'
    assert parsed_rows[0]['amount'] == '-50.00'

    assert parsed_rows[1]['date'] == '02/01/2024'
    assert parsed_rows[1]['payee'] == 'SALARY'
    assert parsed_rows[1]['amount'] == '2000.00'


def test_write_homebank_csv(sample_csv_data):
    """Test writing parsed data to HomeBank CSV format"""
    parsed_rows = read_starling_csv(sample_csv_data)

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_output:
        write_homebank_csv(temp_output.name, parsed_rows)

        # Read back the written file and verify contents
        with open(temp_output.name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            written_rows = list(reader)

            assert len(written_rows) == 2
            assert written_rows[0]['date'] == '01/01/2024'
            assert written_rows[0]['payee'] == 'TESCO'
            assert written_rows[0]['amount'] == '-50.00'

    os.unlink(temp_output.name)


def test_parse_line():
    """Test parsing individual lines"""
    input_row = {
        'Date': '01/01/2024',
        'Counter Party': 'TESCO',
        'Reference': 'Groceries',
        'Type': 'CARD_PAYMENT',
        'Amount (GBP)': '-50.00',
        'Balance (GBP)': '1000.00',
        'Spending Category': 'SHOPPING'
    }

    parsed_data = parse_line(input_row)

    assert parsed_data['date'] == '01/01/2024'
    assert parsed_data['payee'] == 'TESCO'
    assert parsed_data['memo'] == 'Groceries'
    assert parsed_data['amount'] == '-50.00'


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
