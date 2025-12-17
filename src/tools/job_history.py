from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

job_history = FastMCP(
    name = "SecureFirewallJobHistory",
    instructions = """
        EXPAND
    """
)

async def register_job_history_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `job_history` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(job_history)

@job_history.tool(
    name = "getAllJobHistory",
    description = "Retrieves all jobs from Cisco Secure Firewall."
)
async def get_all_job_history(
    fmc_host: str | None = None,
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all job history on an FMC  
    Args:
        fmc_host: FMC to gather job history from
        ctx: MCP context
    Returns:
        API response data
    """
    if fmc_host:
        fmc = manager.select_fmc_by_fmc_host(fmc_host)
        ctx.info(f"Gathering job history for {fmc.host}")        
        return await fmc.get_all_ha_pairs()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_job_history())
            ctx.info(f"Gathering job history for {fmc.host}")
        except AsyncFMCError:
            pass
    return response