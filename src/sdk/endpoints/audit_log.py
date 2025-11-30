from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class AuditLogSDK(SDKUtilities):
    def __init__(self) -> None:
        pass

    async def get_audit_records(self, domain_uuid: str) -> list[dict]:
        """
        Retrieves all audit records for a domain.
        Args:
            domain_uuid: The UUID of the domain to retrieve.
        Returns:
            A list[dict] representing the domain audit records.
        """
        response = await self._request(
            url = f"/api/fmc_platform/v1/domain/{domain_uuid}/audit/auditrecords",
        )
        return response