from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

ha_pair = FastMCP(
    name = "SecureFirewallHAPair",
    instructions = """
## Purpose
Query and monitor high availability firewall configurations. These tools provide visibility into redundant firewall deployments, failover status, and synchronization health.

## Available Tools

### getHAPairByName
Retrieve detailed configuration and status for a specific HA pair.

**Parameters**:
- `ha_pair_name` (required): Exact HA pair name

**When to Use**:
- User asks about specific redundancy cluster
- Troubleshooting failover or sync issues
- Verifying HA configuration

**Returns**:
- Primary and secondary device information
- Current active/standby status
- Synchronization state (in-sync/out-of-sync)
- Last failover time and reason
- HA link status

**Example Queries**:
- "Show me HA pair DATACENTER-PRIMARY"
- "What's the sync status of cluster-prod?"
- "Which device is active in pair XYZ?"

### getAllHAPairs
Retrieve all HA pair configurations across all FMCs or on a singular FMC.

**When to Use**:
- User needs redundancy overview
- Checking all HA pairs for issues
- Creating HA architecture documentation

**Parameters**:
- `fmc_host` (optional): Limit to specific FMC

**Returns**:
- List of all HA pairs with status
- Summary of sync health across pairs

**Example Queries**:
- "List all HA pairs"
- "Show me every redundant firewall cluster"
- "Are any HA pairs out of sync?"
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
        try:
            return await fmc.get_ha_pair_by_name(ha_pair_name)
        except AsyncFMCError:
            ctx.error(f"Couldn't find {ha_pair_name} in cache")
    for fmc in manager.fmc_list:
        try:
            ctx.info(f"Gathering HA pair by name {ha_pair_name}")
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
        ctx.info(f"Gathering HA pairs for {fmc.host}")
        return await fmc.get_all_ha_pairs()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_ha_pairs())
            ctx.info(f"Gathering HA pairs for {fmc.host}")
        except AsyncFMCError:
            pass
    return response