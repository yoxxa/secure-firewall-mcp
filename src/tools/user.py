from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

user = FastMCP(
    name = "SecureFirewallUser",
    instructions = """
        EXPAND
    """
)

async def register_user_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `user` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(user)

@user.tool(
    name = "getAllUsers",
    description = "Retrieves all users from Cisco Secure Firewall."
)
async def get_users(
    fmc_host: str | None = None,
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all users on an FMC  
    Args:
        fmc_host: FMC to gather hosts from
        ctx: MCP context
    Returns:
        API response data
    """
    if fmc_host:
        fmc = manager.select_fmc_by_fmc_host(fmc_host)
        # fmc[0] = AsyncSDK from list comprehension result
        return await fmc[0].get_all_users()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_job_history())
            ctx.info(f"Gathering devices for {fmc.host}")
        except AsyncFMCError:
            pass
    return response