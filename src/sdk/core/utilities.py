from sdk.exceptions import RetryError, AsyncFMCError
from httpx import HTTPStatusError, ConnectTimeout, RequestError, Response
from requests.auth import HTTPBasicAuth

class SDKUtilities:
    """
    Core utilities required for SDK operations like authentication and request building
    """
    def __init__(self) -> None:
        pass

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
        Invalidate existing stored API token.
        """
        async with self._lock:
            self._token = None

    # Depending on if we do the data structure with multiple FMCs, likely will need to revise auth strategy.
    async def _authenticate(self) -> None:
        """
        Retrieves a fresh API token from FMC and sets the new token.
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
        retries: int = 5,
        timeout: int = 10
    ) -> Response:
        """
        Manages creation and selection of multiple AsyncFMC objects
        Args:
            url: FMC endpoint to gather data from
            params: parameters to pass into request
            retries: number of times to retry request before failing
            timeout: time to wait on request before failing
        Returns:
            Response object with data from request
        """
        # Add default parameters
        if params == None:
            params = dict({"limit": 1000, "expanded": True})
        # Start retry loop
        for attempt in range(retries):
            try:
                response = await self.client.get(
                    url = url,
                    params = params,
                    headers = self.headers,
                    timeout = timeout
                )
                response.raise_for_status()
                paging = response.json()["paging"]
                # Check if pagination needed
                if paging["pages"] == 1:
                    return response
                limit = paging["limit"]
                _response = list()
                _response.extend(response.json()["items"])
                for page in range(1, paging["pages"]):
                    params.update({
                            "limit": limit,
                            "offset": limit * page,
                            "expanded": True
                    })
                    response = await self.client.get(
                        url = url,
                        params = params,
                        headers = self.headers,
                        timeout = timeout
                    )
                    response.raise_for_status()
                    _response.extend(response.json()["items"])
                return _response
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
            # TODO - uplift this error, think only means that there are no records, i.e. a 404
            except KeyError:
                raise AsyncFMCError("Response failed")