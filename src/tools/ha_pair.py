from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import FMCManager

class HAPair:
    mcp = FastMCP(
        name = "SecureFirewallHAPair",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

ha_pair = HAPair()

async def register_ha_pair_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `ha_pair` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(ha_pair.mcp)

@ha_pair.mcp.tool(
    name = "getHAPairByName",
    description = "Retrieves a HA pair from Cisco Secure Firewall by name."
)
async def get_ha_pair(
    device_name: str,
    ctx: Context | None = None
) -> dict:
    """
    Gathers a specific HA pair by name i.e. PERTH-FW 
    Args:
        device_name: name of device to collect
        ctx: MCP context
    Returns:
        API response data
    """
    fmc: AsyncFMC | None = await ha_pair.fmc_manager.select_fmc_by_device_name(device_name)
    if fmc:
        return await fmc.get_device_by_name(device_name)
    for fmc in ha_pair.fmc_manager.fmc_list:
        try:
            data = await fmc.get_ha_pair_by_name(device_name)
            # TODO - build update_ha_cache() and change this
            #await ha_pair.fmc_manager.update_standalone_cache(data)
            return data
        except AsyncFMCError:
            pass
    raise ToolError

@ha_pair.mcp.tool(
    name = "getAllHAPair",
    description = "Retrieves all devices from Cisco Secure Firewall."
)
async def get_all_ha_pairs(
    #fmc_host: str | None = None,
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all devices from FMC.
    Args:
        ctx: MCP context
    Returns:
        API response data
    """
    # TODO - fix below if statement
    # Indicates they want to collect for a specific FMC
    #if fmc_host:
    #    fmc = [fmc for fmc in ha_pair.fmc_manager.fmc_list if fmc.host.strip("https://") == fmc_host]
        # fmc[0] = AsyncSDK from list comprehension result
    #    return await fmc[0].get_all_ha_pairs()
    response = list([])
    for fmc in ha_pair.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering devices for {fmc.host}")
            response.extend(await fmc.get_all_ha_pairs())
        except AsyncFMCError:
            pass
    return response