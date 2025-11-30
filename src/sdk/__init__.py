from sdk.core import CoreFMC
from asyncio import Lock
from httpx import AsyncClient

class AsyncFMC(CoreFMC):
    """
    Async SDK for Firepower Management Center
    Args:
        host: FMC host to gather data from API
        username: FMC user who will call API
        password: Password of FMC user
    """
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host: str = host
        self.username: str = username
        self.password: str = password
        # Used for handling/updating API token header
        self._lock: Lock = Lock()
        self._token: str = None
        # TODO: Research - other potential parameters
        self.client: AsyncClient = AsyncClient(
            base_url = str(self.host),
            # Change to True for SSL - need cert
            verify = False
        )
        # TODO - refine HTTP headers
        self.headers: dict = {
            "accept": "*/*", 
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive", 
            "user-agent": "python-httpx/0.28.1",
        }
        self.params = {
            "limit": 1000, 
            "expanded": True
        }
        # Cache global domain
        self.global_domain_uuid = None

    # TODO - determine if this is all thats needed
    # Needed for testing, enables async context manager
    async def __aenter__(self):
        return self

    # TODO - determine if this is all thats needed
    # Needed for testing, enables async context manager
    async def __aexit__(self, exc_type, exc_value, traceback):
        del self