import csv
from enum import Enum

from src.display import display_rows_in_terminal


class HomeBankPaymentType(Enum):
    NONE = 0
    CREDIT_CARD = 1
    CHECK = 2
    CASH = 3
    BANK_TRANSFER = 4
    INTERNAL_TRANSFER = 5
    DEBIT_CARD = 6
    STANDING_ORDER = 7
    ELECTRONIC_PAYMENT = 8
    DEPOSIT = 9
    FINANCIAL_INSTITUTION_FEE = 10
    DIRECT_DEBIT = 11


class HomeBankHeaders(str, Enum):
    DATE = "date"
    PAYMENT = "payment"
    INFO = "info"
    PAYEE = "payee"
    MEMO = "memo"
    AMOUNT = "amount"
    CATEGORY = "category"
    TAGS = "tags"


class StarlingHeaders(str, Enum):
    DATE = "Date"
    COUNTER_PARTY = "Counter Party"
    REFERENCE = "Reference"
    TYPE = "Type"
    AMOUNT = "Amount (GBP)"
    BALANCE = "Balance (GBP)"
    CATEGORY = "Spending Category"
    NOTES = "Notes"


class StarlingPaymentType(Enum):
    DEPOSIT_INTEREST = 'DEPOSIT INTEREST'
    DIRECT_DEBIT = 'DIRECT DEBIT'
    FASTER_PAYMENT = 'FASTER PAYMENT'
    CICS_CHEQUE = 'CICS CHEQUE'


STARLING_TO_HOMEBANK_MAP = {
    StarlingPaymentType.DEPOSIT_INTEREST: HomeBankPaymentType.DEPOSIT,
    StarlingPaymentType.DIRECT_DEBIT: HomeBankPaymentType.DIRECT_DEBIT,
    StarlingPaymentType.FASTER_PAYMENT: HomeBankPaymentType.BANK_TRANSFER,
    StarlingPaymentType.CICS_CHEQUE: HomeBankPaymentType.CHECK
}


def parse_payment_type(payment_type):
    return STARLING_TO_HOMEBANK_MAP.get(StarlingPaymentType(payment_type), HomeBankPaymentType.NONE).value


def parse_line(line):
    result = {
        HomeBankHeaders.DATE: line[StarlingHeaders.DATE],  # No .value needed
        HomeBankHeaders.PAYMENT: parse_payment_type(line[StarlingHeaders.TYPE]),
        HomeBankHeaders.INFO: "",
        HomeBankHeaders.PAYEE: line[StarlingHeaders.COUNTER_PARTY],
        HomeBankHeaders.MEMO: line[StarlingHeaders.REFERENCE],
        HomeBankHeaders.AMOUNT: line[StarlingHeaders.AMOUNT],
        HomeBankHeaders.CATEGORY: "",
        HomeBankHeaders.TAGS: "",
    }

    return result


def read_starling_csv(input_file):
    """Read the Starling CSV file and return a list of parsed rows"""
    parsed_rows = []
    with open(input_file, newline='') as csvfile:
        dicReader = csv.DictReader(csvfile)
        for row in dicReader:
            parsed_data = {
                key.value: value for key,
                value in parse_line(row).items()
            }
            print(parsed_data)
            parsed_rows.append(parsed_data)
    return parsed_rows


def write_homebank_csv(output_file, rows):
    """Write the parsed rows to a new HomeBank CSV file"""
    if not rows:
        return

    fieldnames = list(rows[0].keys())  # Get headers from first row

    with open(output_file, 'w', newline='') as csvfile:
        dict_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(rows)

    # Display in terminal
    display_rows_in_terminal(rows)


def convert_starling_to_homebank(input_file, output_file):
    parsed_rows = read_starling_csv(input_file)
    write_homebank_csv(output_file, parsed_rows)


convert_starling_to_homebank('before.csv', 'after.csv')
