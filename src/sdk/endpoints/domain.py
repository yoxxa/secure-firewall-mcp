from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class DomainSDK(SDKUtilities):
    def __init__(self) -> None:
        pass

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