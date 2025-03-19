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


class HomeBankHeaders(str, Enum):
    DATE = "date"
    PAYMENT = "payment"
    INFO = "info"
    PAYEE = "payee"
    MEMO = "memo"
    AMOUNT = "amount"
    CATEGORY = "category"
    TAGS = "tags"
