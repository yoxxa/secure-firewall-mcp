# Local imports
from manager import manager
from tools.device import register_device_tools
from tools.health_alert import register_health_alert_tools
from tools.audit_log import register_audit_log_tools
from tools.user import register_user_tools
from tools.job_history import register_job_history_tools
from tools.ha_pair import register_ha_pair_tools
# External imports
from fastmcp import FastMCP
import asyncio
from dotenv import load_dotenv
import os
from starlette.responses import JSONResponse

load_dotenv(
    dotenv_path = "src/creds/.env"
)

class App:
    """
    App container stores primary FastMCP server and FMCManager objects
    """
    mcp = FastMCP(
        name = "CiscoSecureFirewall",
        instructions = """
            This server provides tools for interfacing with the Cisco Secure Firewall API
            Use ....
        """
    )
    fmc_manager = manager
    
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request):
        return JSONResponse({
            "status": "healthy",
            "service": "secure-firewall-mcp",
            "version": "2025-11-13"
        })

    async def register_tools(self) -> None:
        """
        Extends main MCP server to include all other tools
        """
        await register_device_tools(self.mcp)
        await register_health_alert_tools(self.mcp)
        await register_audit_log_tools(self.mcp)
        await register_user_tools(self.mcp)
        await register_job_history_tools(self.mcp)
        await register_ha_pair_tools(self.mcp)

async def main():
    app = App()
    await app.fmc_manager.init()
    await app.register_tools()
    await app.mcp.run_async(
        transport="http",
        host="0.0.0.0",
        port=8080,
    )

if __name__ == "__main__":
    asyncio.run(main())