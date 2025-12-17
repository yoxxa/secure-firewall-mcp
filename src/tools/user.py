from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

user = FastMCP(
    name = "SecureFirewallUser",
    instructions = """
## Purpose
Retrieve local user account information, access details, and role assignments across FMC instances. These tools support access audits, account management, and security reviews.

## Available Tools

### getAllUsers
Retrieve detailed information for a specific user account.

**Parameters**:
- `fmc_host` (optional): Specific FMC to query

**When to Use**:
- User asks about specific account
- Investigating access or permissions
- Verifying account status
- Security review of individual user

**Returns**:
- Username and display name
- Email address
- Assigned roles and permissions
- Account status (active/disabled)
- Last login timestamp
- Account creation date
- Associated domain(s)

**Example Queries**:
- "Show me details for user jsmith"
- "What permissions does admin have?"
- "When did user firewall-ops last login?"
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
        ctx.info(f"Gathering users for {fmc.host}")
        return await fmc.get_all_users()
    response = list([])
    for fmc in manager.fmc_list:
        try:
            response.extend(await fmc.get_all_job_history())
            ctx.info(f"Gathering users for {fmc.host}")
        except AsyncFMCError:
            pass
    return response