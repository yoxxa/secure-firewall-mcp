from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from sdk.manager import FMCManager

class Domain:
    mcp = FastMCP(
        name = "SecureFirewallDomain",
        instructions = """
            EXPAND
        """
    )
    fmc_manager: FMCManager = None

domain = Domain()

async def register_domain_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `domain` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(domain.mcp)

@domain.mcp.tool(
    name = "getDomainByName",
    description = "Retrieves a domain from Cisco Secure Firewall."
)
async def get_domain(
    domain_name: str,
    ctx: Context | None = None
) -> dict | None:
    """
    Gathers a specific domain by name i.e. Michigan-DC 
    Args:
        domain_name: the single domain to collect
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in domain.fmc_manager.fmc_list:
        try:
            ctx.info("Gathered FMC domains")
            return await fmc.get_domain_by_name(domain_name)
        except AsyncFMCError:
            ctx.error(f"No domain found by name {domain_name}")
            raise ToolError

@domain.mcp.tool(
    name = "getAllDomains",
    description = "Retrieves all domains from Cisco Secure Firewall."
)
async def get_domains(
    ctx: Context | None = None
) -> list[dict]:
    """
    Gathers all domains on an FMC  
    Args:
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in domain.fmc_manager.fmc_list:
        try:
            ctx.info("Gathered FMC domains")
            return await fmc.get_all_domains()
        except AsyncFMCError:
            raise ToolError