from sdk.endpoints.domain import DomainSDK
from sdk.endpoints.device import DeviceSDK
from sdk.endpoints.health_alert import HealthAlertSDK
from sdk.endpoints.audit_log import AuditLogSDK
from sdk.endpoints.user import UserSDK

class CoreFMC(
    DomainSDK,
    DeviceSDK,
    HealthAlertSDK,
    AuditLogSDK,
    UserSDK
):
    def __init__(self) -> None:
        pass