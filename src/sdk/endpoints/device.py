from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class DeviceSDK(SDKUtilities):
    async def get_device_by_name(
        self, 
        device_name: str
    ) -> dict:
        """
        Gathers FTD devices matching `device_name` from an FMC
        Args:
            device_name: FMC host to gather data from API
        Returns:
            device: dict of device
        Raises:
            AsyncFMCError: 404, device not found
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devices/devicerecords",
        )
        for device in response.json()["items"]:
            if device["name"] == device_name:
                return device
        raise AsyncFMCError("No device found by the name")

    async def get_all_devices(
        self
    ) -> list[dict]:
        """
        Gathers all FTD devices from an FMC
        Returns:
            list[dict] of devices
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/devices/devicerecords"
        )
        return response.json()["items"]