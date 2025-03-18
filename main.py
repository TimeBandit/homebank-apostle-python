import csv
from enum import Enum


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


StarlingToHomeBankMap = dict({
    'Date': 'date',
    'Counter Party': 'payee',
    'Reference': 'memo',
    'Amount (GBP)': 'amount'
})


class StarlingHeaders(Enum):
    DATE = 'Date'
    COUNTER_PARTY = 'Counter Party'
    REFERENCE = 'Reference	Type'
    TYPE = 'Type'
    AMOUNT = 'Amount (GBP)'
    BALANCE = 'Balance (GBP)'
    CATEGORY = 'Spending Category'
    NOTES = 'Notes'

# HomeBankHeaders = ('date',	'payment',	'info',	'payee',	'memo',	'amount',	'category',	'tags')


class HomeBankHeaders(Enum):
    DATE = 'date'
    PAYMENT = 'payment'
    INFO = 'info'
    PAYEE = 'payee'
    MEMO = 'memo'
    AMOUNT = 'amount'
    CATEGORY = 'category'
    TAGS = 'tags'


class StarlingPaymentType(Enum):
    DEPOSIT_INTEREST = 'DEPOSIT INTEREST'
    DIRECT_DEBIT = 'DIRECT DEBIT'
    FASTER_PAYMENT = 'FASTER PAYMENT'
    CICS_CHEQUE = 'CICS CHEQUE'


def parse_payment_type(type):
    match type:
        case StarlingPaymentType.DEPOSIT_INTEREST:
            return HomeBankPaymentType.DEPOSIT
        case StarlingPaymentType.DIRECT_DEBIT:
            return HomeBankPaymentType.DIRECT_DEBIT
        case StarlingPaymentType.FASTER_PAYMENT:
            return HomeBankPaymentType.BANK_TRANSFER
        case StarlingPaymentType.CICS_CHEQUE:
            return HomeBankPaymentType.CHECK
        case _:
            raise ValueError()


def parse_line(line):
    result = dict({
        HomeBankHeaders.DATE: line[StarlingHeaders.DATE],
        HomeBankHeaders.PAYMENT: parse_payment_type(line[StarlingHeaders.TYPE]),
        HomeBankHeaders.INFO: "",
        HomeBankHeaders.PAYEE: line[StarlingHeaders.COUNTER_PARTY],
        HomeBankHeaders.MEMO: line[StarlingHeaders.REFERENCE],
        HomeBankHeaders.AMOUNT: line[StarlingHeaders.AMOUNT],
        HomeBankHeaders.CATEGORY: "",
        HomeBankHeaders.TAGS: "",
    })
    return result


with open('before.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    dicReader = csv.DictReader(csvfile)

    for row in dicReader:
        parse = parse_line(row)
        print(parse)
