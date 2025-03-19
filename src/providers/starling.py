from enum import Enum
from src.utils.homebank import HomeBankHeaders, HomeBankPaymentType


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
