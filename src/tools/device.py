from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from manager import manager
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from itertools import chain

device = FastMCP(
    name = "SecureFirewallDevice",
    instructions = """
        EXPAND
    """
)

async def register_device_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `device` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(device)

@device.tool(
    name = "getDeviceByName",
    description = "Retrieves a device from Cisco Secure Firewall by name."
)
async def get_device(
    device_name: str,
    ctx: Context | None = None
) -> dict:
    """
    Gathers a specific device by name i.e. PERTH-FW 
    Args:
        device_name: name of device to collect
        ctx: MCP context
    Returns:
        API response data
    """
    fmc: AsyncFMC | None = await manager.select_fmc_by_device_name(device_name)
    if fmc:
        return await fmc.get_device_by_name(device_name)
    for fmc in manager.fmc_list:
        try:
            data = await fmc.get_device_by_name(device_name)
            await manager.add_standalone_to_cache(data)
            return data
        except AsyncFMCError:
            pass
    raise ToolError

# TODO - add domain_name as optional user input in same fashion as `fmc_host` 
@device.tool(
    name = "getAllDevices",
    description = "Retrieves all devices from Cisco Secure Firewall."
)
async def get_all_devices(
    fmc_host: str | None = None,
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all devices from FMC.
    Args:
        fmc_host: FMC to gather all devices from
        ctx: MCP context
    Returns:
        API response data
    """
    # Indicates they want to collect for a specific FMC
    if fmc_host:
        try:
            fmc = await manager.select_fmc_by_fmc_host(fmc_host)
            # fmc[0] = AsyncSDK from list comprehension result
            return await fmc[0].get_all_devices()
        except:
            raise AsyncFMCError(f"Cannot return all devices for {fmc_host}")
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_devices())
            ctx.info(f"Gathering devices for {fmc.host}")
        except AsyncFMCError:
            pass
    return response