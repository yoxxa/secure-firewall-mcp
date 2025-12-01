from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

class JobHistorySDK:
    mcp = FastMCP(
        name = "SecureFirewallJobHistory",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

job_history = JobHistorySDK()

async def register_job_history_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `job_history` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(job_history.mcp)

@job_history.mcp.tool(
    name = "getAllJobHistory",
    description = "Retrieves all jobs from Cisco Secure Firewall."
)
async def get_all_job_history(
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all job history on an FMC  
    Args:
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in job_history.fmc_manager.fmc_list:
        try:
            ctx.info("Gathered FMC job history")
            return await fmc.get_all_job_history()
        except AsyncFMCError:
            raise ToolError