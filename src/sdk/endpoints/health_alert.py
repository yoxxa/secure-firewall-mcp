from sdk.core.utilities import SDKUtilities
from sdk.exceptions import AsyncFMCError

class HealthAlertSDK(SDKUtilities):
    async def get_all_health_alerts(self) -> list[dict]:
        """
        Retrieves all red and yellow health alerts for global domain.
        Returns:
            A list[dict] representing the global domain health alerts.
        """
        response = await self._request(
            url = f"/api/fmc_config/v1/domain/{self.global_domain_uuid}/health/alerts",
            params = {"limit": 1000, "expanded": True, "filter": "status:red,yellow;"}
        )
        red_alert_list = list()
        for alert in response.json()["items"]:
            if alert["status"] != "GREEN":
                red_alert_list.append(alert)
        return red_alert_list