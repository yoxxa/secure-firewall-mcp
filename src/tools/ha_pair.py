from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

ha_pair = FastMCP(
    name = "SecureFirewallHAPair",
    instructions = """
        EXPAND
    """
)

async def register_ha_pair_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `ha_pair` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(ha_pair)

@ha_pair.tool(
    name = "getHAPairByName",
    description = "Retrieves a HA pair from Cisco Secure Firewall by name."
)
async def get_ha_pair(
    ha_pair_name: str,
    ctx: Context | None = None
) -> dict:
    """
    Gathers a specific HA pair by name i.e. PERTH-FW 
    Args:
        ha_pair_name: name of device to collect
        ctx: MCP context
    Returns:
        API response data
    """
    fmc: AsyncFMC | None = await manager.select_fmc_by_ha_pair_name(ha_pair_name)
    if fmc:
        return await fmc.get_ha_pair_by_name(ha_pair_name)
    for fmc in manager.fmc_list:
        try:
            data = await fmc.get_ha_pair_by_name(ha_pair_name)
            await manager.add_ha_pair_to_cache(data)
            return data
        except AsyncFMCError:
            pass
    raise ToolError

@ha_pair.tool(
    name = "getAllHAPairs",
    description = "Retrieves all devices from Cisco Secure Firewall."
)
async def get_all_ha_pairs(
    fmc_host: str | None = None,
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all devices from FMC.
    Args:
        fmc_host: FMC to gather HA pairs from
        ctx: MCP context
    Returns:
        API response data
    """
    # Indicates they want to collect for a specific FMC
    if fmc_host:
        fmc = await manager.select_fmc_by_fmc_host(fmc_host)
        # fmc[0] = AsyncSDK from list comprehension result
        return await fmc[0].get_all_ha_pairs()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_ha_pairs())
            ctx.info(f"Gathering devices for {fmc.host}")
        except AsyncFMCError:
            pass
    return response