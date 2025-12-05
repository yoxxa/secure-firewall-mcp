from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from manager import FMCManager
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from itertools import chain

class Device:
    mcp = FastMCP(
        name = "SecureFirewallDevice",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

device = Device()

async def register_device_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `device` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(device.mcp)

@device.mcp.tool(
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
    fmc: AsyncFMC | None = await device.fmc_manager.select_fmc_by_device_name(device_name)
    if fmc:
        return await fmc.get_device_by_name(device_name)
    for fmc in device.fmc_manager.fmc_list:
        try:
            data = await fmc.get_device_by_name(device_name)
            return await device.fmc_manager.update_standalone_cache(data)
        except AsyncFMCError:
            pass
    raise ToolError

@device.mcp.tool(
    name = "getAllDevices",
    description = "Retrieves all devices from Cisco Secure Firewall."
)
async def get_devices(
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
        fmc = [fmc for fmc in device.fmc_manager.fmc_list if fmc.host.strip("https://") == fmc_host]
        # fmc[0] = AsyncSDK from list comprehension result
        return await fmc[0].get_all_devices()
    response = list([])
    for fmc in device.fmc_manager.fmc_list:
        try:
            response.extend(await fmc.get_all_devices())
            ctx.info(f"Gathering devices for {fmc.host}")
        except AsyncFMCError:
            pass
    return response