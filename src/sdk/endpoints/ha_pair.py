from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class HAPairSDK(SDKUtilities):
    async def get_ha_pair_by_name(
        self, 
        device_name: str
    ) -> dict:
        """
        Gathers HA pairs matching `device_name` from an FMC
        Args:
            device_name: HA pairs to gather data from API
        Returns:
            device: dict of HA pair
        Raises:
            AsyncFMCError: 404, HA pair not found
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devicehapairs/ftddevicehapairs",
        )
        for device in response.json()["items"]:
            if device["name"] == device_name:
                return device
        raise AsyncFMCError("No HA pair found by the name")

    async def get_all_ha_pairs(
        self
    ) -> list[dict]:
        """
        Gathers all HA pairs from an FMC
        Returns:
            list[dict] of HA pairs
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devicehapairs/ftddevicehapairs"
        )
        return response.json()["items"]