from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class DeviceSDK(SDKUtilities):
    def __init__(self) -> None:
        pass
  
    async def get_device_by_name(
        self, 
        domain_uuid: str, 
        device_name: str
    ) -> dict:
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords",
            params = {"expanded": True}
        )
        for device in response.json()["items"]:
            if device["name"] == device_name:
                return device
        raise AsyncFMCError("No device found by the name")

    async def get_all_devices(
        self
    ) -> list[dict] | dict:
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devices/devicerecords"
        )
        return response.json()["items"]