from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

class HealthAlert:
    mcp = FastMCP(
        name = "SecureFirewallHealthAlert",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

health_alert = HealthAlert()

async def register_health_alert_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `health_alert` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(health_alert.mcp)

@health_alert.mcp.tool(
    name = "getAllHealthAlerts",
    description = "Retrieves all health alerts from an FMC."
)
async def get_health_alerts(
    domain_uuid: str,
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
    for fmc in health_alert.fmc_manager.fmc_list:
        try:
            ctx.info(f"Gathering health alerts for {domain_uuid}")
            return await fmc.get_all_health_alerts(
                domain_uuid
            )
        except AsyncFMCError:
            ctx.error(f"No health issues found")
            raise ToolError
