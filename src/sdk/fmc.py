from sdk.exceptions import RetryError, AsyncFMCError
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
    
    # TODO - add pagination
    async def _request(
        self,
        url: str,
        params: dict | None = None,
        retries: int = 5
    ) -> Response:
        # Add default parameters
        if params != None:
            params.update({"limit": 1000, "expanded": True})
        else:
            params = {"limit": 1000, "expanded": True}
        # Start retry loop
        for attempt in range(retries):
            try:
                response = await self.client.get(
                    url = url,
                    params = params,
                    headers = self.headers
                )
                response.raise_for_status()
                return response
            # TODO - figure out a catch all
            except HTTPStatusError:
                # Edge Case: Token expiry mid-request: Auto-refresh and replay logic for requests if token expires.
                # ^ Workaround currently implemented is to reauth to API and hope not hit retry limit
                # API Token refresh
                if response.status_code == 401:
                    await self._invalidate_token()
                    await self._authenticate()
                # Retry limit - TODO: figure out how we handle this, is it just spit out to console or?
                if attempt == retries - 1:
                    raise RetryError("Exceeded request retry count")
            # TODO - need to figure out what this actually represents, think means network error,
            # as in, no route, int down, - really just that is not reachable from host running SDK.
            except RequestError:
                raise
            # TODO - define what we will do in event of Connect Timeouts... is there anything we can do?
            except ConnectTimeout:
                raise

    async def set_global_domain(self) -> None:
        """
        Retrieves the global domain from FMC and caches it in a class variable.
        Args:
            domain_name: The name of the domain to retrieve.
        """
        response = await self._request(
            url = "/api/fmc_platform/v1/info/domain"
        )
        for domain in response.json()["items"]:
            if domain["name"] == "Global":
                self.global_domain_uuid = domain["uuid"]
                return

    async def get_domain_by_name(self, domain_name: str) -> dict:
        """
        Retrieves a domain by its name.
        Args:
            domain_name: The name of the domain to retrieve.
        Returns:
            A dictionary representing the domain.
        Raises:
            FMCSDKError: If no domain is found with the given name or an API error occurs.
        """
        response = await self._request(
            url = "/api/fmc_platform/v1/info/domain"
        )
        for domain in response.json()["items"]:
            if domain_name == "Global" and domain["name"] == "Global":
                return domain
            if domain["name"].strip("Global/") == domain_name:
                return domain
        raise AsyncFMCError("No domain found by that name")

    async def get_all_domains(self) -> list[dict]:
        """
        Retrieves all domains.
        Returns:
            A list of `dict` representing the domain.
        """
        response = await self._request(
            url = "/api/fmc_platform/v1/info/domain"
        )
        return response.json()["items"]
    
    async def get_device_by_name(
        self, 
        device_name: str,
        domain_uuid: str = None, 
    ) -> dict:
        if domain_uuid == None:
            domain_uuid = self.global_domain_uuid
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords",
            params = {"expanded": True}
        )
        for device in response.json()["items"]:
            if device["name"] == device_name:
                return device
        raise AsyncFMCError("No device found by the name")

    async def get_all_devices(
        self, 
        domain_uuid: str = None, 
        device_uuid: str = None
    ) -> list[dict] | dict:
        if domain_uuid == None:
            domain_uuid = self.global_domain_uuid
        if device_uuid:
            url = f"/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords/{device_uuid}"
        else:
            url = f"/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords"
        response = await self._request(
            url = url
        )
        return response.json()["items"]