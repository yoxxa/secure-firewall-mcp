from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class HAPairSDK(SDKUtilities):
    def __init__(self) -> None:
        pass
  
    async def get_ha_pair_by_name(
        self, 
        domain_uuid: str, 
        device_name: str
    ) -> dict:
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{domain_uuid}/devicehapairs/ftddevicehapairs",
        )
        for device in response.json()["items"]:
            if device["name"] == device_name:
                return device
        raise AsyncFMCError("No HA pair found by the name")

    async def get_all_ha_pairs(
        self
    ) -> list[dict] | dict:
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devicehapairs/ftddevicehapairs"
        )
        return response.json()["items"]