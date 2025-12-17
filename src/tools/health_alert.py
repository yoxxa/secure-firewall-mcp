from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

health_alert = FastMCP(
    name = "SecureFirewallHealthAlert",
    instructions = """
## Purpose
Monitor and retrieve system health alerts, warnings, and notifications from FMC instances. These tools provide proactive visibility into system issues requiring attention.

## Available Tools

### getAllHealthAlerts
Retrieve current health alerts for all or a specific FMC instance.

**Parameters**:
- `fmc_host` (optional): selected FMC hostname or IP address

**When to Use**:
- User asks about system health or warnings
- Troubleshooting specific FMC issues
- Monitoring specific deployment

**Returns**:
- Alert description and details
- Severity level (RED/YELLOW/GREEN)
- Timestamp when alert was generated
- Affected device or component
- Recommended action (when available)

**Example Queries**:
- "Show me health alerts for FMC-PROD"
- "Are there any red health alerts for any FMCs?"
- "What warnings exist for the datacenter FMC?"
    """
)

async def register_health_alert_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `health_alert` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(health_alert)

@health_alert.tool(
    name = "getAllHealthAlerts",
    description = "Retrieves all health alerts from an FMC."
)
async def get_all_health_alerts(
    fmc_host: str | None = None,
    ctx: Context | None = None
) -> list:
    """
    Gathers all red and yellow health alerts for a FMC, i.e. Tokyo-FMC 
    Args:
        device_name: name of device to collect
        ctx: MCP context
    Returns:
        API response data
    """
    if fmc_host:
        fmc = manager.select_fmc_by_fmc_host(fmc_host)
        ctx.info(f"Gathering health alerts for {fmc.host}")
        return await fmc.get_all_health_alerts()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_health_alerts())
            ctx.info(f"Gathering health alerts for {fmc.host}")
        except AsyncFMCError:
            pass
    return response