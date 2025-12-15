# TODO - design exception
class FMCManagerError(Exception):
    """
        Custom exception repesenting an error for a FMCManager
        Args:
            message: The error message from the SDK.
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)