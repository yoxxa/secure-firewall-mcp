from sdk.exceptions import AsyncFMCError
import pytest
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.exceptions import ToolError

# TODO: 
# - start to add expected failure cases and params to test error handling
# - split out into different endpoints

@pytest.mark.parametrize(
    "domain_name", 
    ["Perth", "Global",]
)
@pytest.mark.asyncio
async def test_get_domain_by_name_good_input(
    domain_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getDomainByName", 
        arguments={"domain_name": domain_name}
    )
    assert isinstance(result.data, dict)

@pytest.mark.parametrize(
    "domain_name", 
    ["INVALID_DOMAIN"]
)
@pytest.mark.asyncio
async def test_get_domain_by_name_bad_input(
    domain_name: str,
    mcp_client: Client[StreamableHttpTransport]
):
    with pytest.raises(ToolError) as not_found_error:
        result = await mcp_client.call_tool(
            name="getDomainByName", 
            arguments={"domain_name": domain_name}
        )

@pytest.mark.asyncio
async def test_get_all_domains(
    mcp_client: Client[StreamableHttpTransport]
):
    result = await mcp_client.call_tool(
        name="getAllDomains", arguments={}
    )
    assert isinstance(result.data, list)