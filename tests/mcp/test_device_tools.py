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

@pytest.mark.parametrize(
    "fmc_host", 
    [
        "10.66.228.172"
    ]
)
@pytest.mark.asyncio
async def test_get_all_devices_by_single_fmc(
    fmc_host: str,
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name = "getAllDevices",
        arguments = {"fmc_host": fmc_host}
    )
    assert isinstance(result.data, list)

@pytest.mark.parametrize(
    "fmc_host", 
    [
        "10.66.228.180"
    ]
)
@pytest.mark.asyncio
async def test_get_all_devices_by_bad_fmc_input(
    fmc_host: str,
    mcp_client: Client[StreamableHttpTransport]
):
    with pytest.raises(ToolError) as device_not_found:
        result = await mcp_client.call_tool(
            name = "getAllDevices",
            arguments = {"fmc_host": fmc_host}
        )