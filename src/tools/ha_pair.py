from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

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
async def get_device(
    domain_uuid: str,
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
    for fmc in ha_pair.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering HA pair {device_name}")
            return await fmc.get_ha_pair_by_name(
                domain_uuid,
                device_name
            )
        except AsyncFMCError:
            ctx.error(f"No HA pair found by name {device_name}")
            raise ToolError

@ha_pair.mcp.tool(
    name = "getAllHAPair",
    description = "Retrieves all devices from Cisco Secure Firewall."
)
async def get_devices(
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all devices from FMC.
    Args:
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in ha_pair.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering devices for domain")
            return await fmc.get_all_ha_pairs()
        except AsyncFMCError:
            ctx.error(f"No devices found for {fmc}")
            raise ToolError