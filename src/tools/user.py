from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

class User:
    mcp = FastMCP(
        name = "SecureFirewallUser",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

user = User()

async def register_user_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `user` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(user.mcp)

@user.mcp.tool(
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
    for fmc in user.fmc_manager.fmc_list:
        try:
            ctx.info("Gathered FMC domains")
            return await fmc.get_all_users()
        except AsyncFMCError:
            raise ToolError