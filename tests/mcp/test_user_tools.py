import pytest
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

@pytest.mark.asyncio
async def test_get_all_domains(
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getAllUsers", arguments={}
    )
    assert isinstance(result.data, list)