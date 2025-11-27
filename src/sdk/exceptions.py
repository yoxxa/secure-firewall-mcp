# TODO - design exception
# Custom exception representing a request exceeding the default of 5 retries (or allocated amount)
class RetryError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# TODO - design exception
class FMCSDKError(Exception):
    """
        Custom exception repesenting an error whilst using the FMC SDK
        Args:
            message: The error message from the SDK.
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(message)