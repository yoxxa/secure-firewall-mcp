from sdk.exceptions import AsyncFMCError
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.exceptions import ToolError

@pytest.mark.parametrize(
    "domain_uuid", 
    [
        "e276abec-e0f2-11e3-8169-6d9ed49b625f"
    ]
)
@pytest.mark.asyncio
async def test_get_all_audit_logs(
    domain_uuid: str,
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getAllAuditLogs", arguments=
        {
            "domain_uuid": domain_uuid,
        }
    )
    assert isinstance(result.data, list)