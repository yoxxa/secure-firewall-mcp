from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from manager import manager
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from itertools import chain

device = FastMCP(
    name = "SecureFirewallDevice",
    instructions = """
## Purpose
Query and retrieve information about firewall devices managed by FMC instances. These tools provide visibility into your firewall infrastructure's inventory, status, and configuration.

## Available Tools

### getDeviceByName
Retrieve detailed information about a specific firewall device.

**Parameters**:
- `device_name` (required): Exact device name (case-sensitive)

**When to Use**:
- User asks about a specific FTD by name
- Need detailed status for troubleshooting
- Verifying device configuration or version

**Returns**:
- Device name, model, software version
- Management IP address and connectivity status
- Online/offline status, last check-in time
- Associated domain and access policy
- License information

**Example Queries**:
- "Show me details for device FW-DATACENTER-01"
- "What version is running on firewall-production?"
- "Is device XYZ online?"

### getAllDevices
Retrieve all devices across all configured FMC instances or a specific FMC instance.

**Parameters**:
- `fmc_host` (optional): Limit to specific FMC

**When to Use**:
- User needs infrastructure overview
- Creating device inventory
- Finding devices matching certain criteria
- User doesn't know exact device name

**Returns**:
- List of all managed devices with key attributes
- Summary statistics (total, online, offline)

**Example Queries**:
- "List all firewalls"
- "Show me every device managed by FMC-DC"
- "Which devices are offline?"
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
        try:
            return await fmc.get_device_by_name(device_name)
        except AsyncFMCError:
            ctx.error(f"Couldn't find {device_name} in cache")
    for fmc in manager.fmc_list:
        try:
            ctx.info(f"Gathering device by name {device_name}")
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
            ctx.info(f"Gathering devices for {fmc.host}")
            return await fmc.get_all_devices()
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