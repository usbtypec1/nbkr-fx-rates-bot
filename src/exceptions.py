class BankAPIError(Exception):
    pass


class NationalBankAPIError(BankAPIError):
    pass


class CommercialBankAPIError(BankAPIError):
    pass


class FXRateNotFoundError(Exception):
    pass
