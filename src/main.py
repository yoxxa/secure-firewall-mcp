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

load_dotenv(
    dotenv_path = "src/creds/.env"
)

class App:
    def __init__(self):
        self.mcp = FastMCP(
            name = "CiscoSecureFirewall",
            instructions = """
                This server provides tools for interfacing with the Cisco Secure Firewall API
                Use ....
            """
        )
        self.fmc_manager = manager

    async def register_tools(self) -> None:
        """
        Extends main MCP server to include `domain` tools
        Args:
            mcp: the main MCP server to extend
        Returns:
            main MCP server with added endpoints
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
        host="127.0.0.1",
        port=8080,
    )

if __name__ == "__main__":
    asyncio.run(main())