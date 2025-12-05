from sdk.exceptions import AsyncFMCError
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.exceptions import ToolError

@pytest.mark.parametrize(
    "device_name", 
    [
        "FTD-HA-PRIMARY"
    ]
)
@pytest.mark.asyncio
async def test_get_device_by_name_good_input(
    device_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getDeviceByName", arguments=
        {
            "device_name": device_name
        }
    )
    assert isinstance(result.data, dict)

@pytest.mark.parametrize(
    "device_name", 
    [
        "INVALID_DEVICE"
    ]
)
@pytest.mark.asyncio
async def test_get_device_by_name_bad_input(
    device_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    with pytest.raises(ToolError) as device_not_found:
        result = await mcp_client.call_tool(
            name="getDeviceByName", arguments=
            {
                "device_name": device_name
            }
        )

@pytest.mark.asyncio
async def test_get_all_devices(
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name = "getAllDevices",
        arguments = {}
    )
    assert isinstance(result.data, list)