from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class UserSDK(SDKUtilities):
    async def get_all_users(
        self
    ) -> list[dict]:
        """
        Gathers all users from an FMC
        Returns:
            list[dict] of users
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/users/users"
        )
        return response.json()["items"]