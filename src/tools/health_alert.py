from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

health_alert = FastMCP(
    name = "SecureFirewallHealthAlert",
    instructions = """
        EXPAND
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
    Gathers all red and yellow health alerts for a domain, i.e. Tokyo 
    Args:
        device_name: name of device to collect
        ctx: MCP context
    Returns:
        API response data
    """
    if fmc_host:
        fmc = manager.select_fmc_by_fmc_host(fmc_host)
        # fmc[0] = AsyncSDK from list comprehension result
        return await fmc[0].get_all_health_alerts()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_health_alerts())
            ctx.info(f"Gathering devices for {fmc.host}")
        except AsyncFMCError:
            pass
    return response