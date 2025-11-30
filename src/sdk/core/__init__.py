from sdk.endpoints.domain import DomainSDK
from sdk.endpoints.device import DeviceSDK
from sdk.endpoints.health_alert import HealthAlertSDK

class CoreFMC(
    DomainSDK,
    DeviceSDK,
    HealthAlertSDK
):
    def __init__(self) -> None:
        pass