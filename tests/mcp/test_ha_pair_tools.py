from sdk.exceptions import AsyncFMCError
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.exceptions import ToolError

@pytest.mark.parametrize(
    "domain_uuid, device_name", 
    [
        ("e276abec-e0f2-11e3-8169-6d9ed49b625f", "PERTH-FW")
    ]
)
@pytest.mark.asyncio
async def test_get_device_by_name_good_input(
    domain_uuid: str,
    device_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getHAPairByName", arguments=
        {
            "domain_uuid": domain_uuid,
            "device_name": device_name
        }
    )
    assert isinstance(result.data, dict)

@pytest.mark.parametrize(
    "domain_uuid, device_name", 
    [
        ("e276abec-e0f2-11e3-8169-6d9ed49b625f", "INVALID_DEVICE")
    ]
)
@pytest.mark.asyncio
async def test_get_device_by_name_bad_input(
    domain_uuid: str,
    device_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    with pytest.raises(ToolError) as device_not_found:
        result = await mcp_client.call_tool(
            name="getHAPairByName", arguments=
            {
                "domain_uuid": domain_uuid,
                "device_name": device_name
            }
        )

@pytest.mark.asyncio
async def test_get_all_devices(
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name = "getAllHAPair",
        arguments = {}
    )
    assert isinstance(result.data, list)