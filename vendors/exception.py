class AccessDenied(Exception):
    pass


class RowNotFound(Exception):
    pass


class PasswordNotCorrect(Exception):
    pass


class UsernameNotUnique(Exception):
    pass


class NegativeBalanceException(Exception):
    pass
