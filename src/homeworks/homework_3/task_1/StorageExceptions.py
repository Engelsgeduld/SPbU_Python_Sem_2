from abc import ABCMeta


class StorageException(Exception, metaclass=ABCMeta):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmptyActionListError(StorageException):
    def __init__(self) -> None:
        super().__init__("Actions list is empty. Nothing to redo")


class NotSupportedCollectionTypeError(StorageException):
    def __init__(self, collection_type: str) -> None:
        super().__init__(f"{collection_type} is not supported")
