from httpx import AsyncClient, HTTPStatusError, ConnectTimeout, RequestError, Response
from requests.auth import HTTPBasicAuth
from asyncio import Lock

class AsyncFMC:
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
            base_url = self.host,
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

    async def _get_token(self) -> str:
        """
        Retrieves a fresh API token from FMC.
        Returns:
            A str for the API token required for subsequent requests.
        """
        response = await self.client.post(
            f"/api/fmc_platform/v1/auth/generatetoken",
            auth = HTTPBasicAuth(self.username, self.password)
        )
        response.raise_for_status()
        return response.headers["X-auth-access-token"]

    async def _invalidate_token(self) -> None:
        """
        Invalidate existing underlying stored API token.
        """
        async with self._lock:
            self._token = None

    # Depending on if we do the data structure with multiple FMCs, likely will need to revise auth strategy.
    async def _authenticate(self) -> None:
            """
            Retrieves a fresh API token from FMC.
            Returns:
                A str for the API token required for subsequent requests.
            """
            async with self._lock:
                # Deals with race condition where request 401's and token changed prior to request
                if self._token:
                    self.headers["X-auth-access-token"] = self._token
                self._token = await self._get_token()
                self.headers["X-auth-access-token"] = self._token