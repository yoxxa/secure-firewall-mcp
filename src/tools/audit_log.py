from sdk.exceptions import AsyncFMCError
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from manager import manager

audit_log = FastMCP(
    name = "SecureFirewallAuditLog",
    instructions = """
        EXPAND
    """
)

async def register_audit_log_tools(mcp: FastMCP) -> None:
    """
    Extends main MCP server to include `audit_log` tools
    Args:
        mcp: the main MCP server to extend
    Returns:
        main MCP server with added endpoints
    """
    await mcp.import_server(audit_log)

@audit_log.tool(
    name = "getAllAuditLogs",
    description = "Retrieves all health alerts from an FMC."
)
async def get_audit_log(
    domain_uuid: str,
    ctx: Context | None = None
) -> list:
    """
    Gathers all audit logs for a domain, i.e. Tokyo 
    Args:
        device_uuid: UUID of domain to collect
        ctx: MCP context
    Returns:
        API response data
    """
    for fmc in manager.fmc_list:
        try:
            ctx.info(f"Gathering audit log for {domain_uuid}")
            return await fmc.get_audit_records(
                domain_uuid
            )
        except AsyncFMCError:
            ctx.error(f"No audit logs found")
            raise ToolError
