from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

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
    domain_uuid: str,
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
    for fmc in device.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering FMC device {device_name}")
            return await fmc.get_device_by_name(
                domain_uuid,
                device_name
            )
        except AsyncFMCError:
            ctx.error(f"No device found by name {device_name}")
            raise ToolError

@device.mcp.tool(
    name = "getAllDevices",
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
    for fmc in device.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering devices for domain")
            return await fmc.get_all_devices()
        except AsyncFMCError:
            ctx.error(f"No devices found for {fmc}")
            raise ToolError