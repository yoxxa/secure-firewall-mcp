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
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all users on an FMC  
    Args:
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in manager.fmc_list:
        try:
            ctx.info("Gathered FMC domains")
            return await fmc.get_all_users()
        except AsyncFMCError:
            raise ToolError