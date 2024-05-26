class ORMException(Exception):
    pass


class FieldError(ORMException):
    pass


class StrictError(ORMException):
    pass


class NotFoundFieldError(ORMException):
    pass
