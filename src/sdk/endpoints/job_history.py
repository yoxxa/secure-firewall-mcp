from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class JobHistorySDK(SDKUtilities):
    def __init__(self) -> None:
        pass

    async def get_all_job_history(self) -> list[dict]:
        """
        Retrieves all job history for an FMC.
        Returns:
            A list[dict] representing job history.
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/deployment/jobhistories",
        )
        return response.json()["items"]