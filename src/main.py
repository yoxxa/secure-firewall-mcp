# Local imports
from sdk import AsyncFMC
from sdk.manager import FMCManager
from tools.domain import domain, register_domain_tools
from tools.device import device, register_device_tools
from tools.health_alert import health_alert, register_health_alert_tools
from tools.audit_log import audit_log, register_audit_log_tools
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
        self.fmc_manager = FMCManager()

    def load_fmc_manager(self) -> None:
        domain.fmc_manager = self.fmc_manager
        device.fmc_manager = self.fmc_manager
        health_alert.fmc_manager = self.fmc_manager
        audit_log.fmc_manager = self.fmc_manager

    async def register_tools(self) -> None:
        """
        Extends main MCP server to include `domain` tools
        Args:
            mcp: the main MCP server to extend
        Returns:
            main MCP server with added endpoints
        """
        await register_domain_tools(self.mcp)
        await register_device_tools(self.mcp)
        await register_health_alert_tools(self.mcp)
        await register_audit_log_tools(self.mcp)

async def main():
    app = App()
    # Just adding a single FMC for now
    await app.fmc_manager.add_fmc(                
        AsyncFMC(
            host = os.getenv("FMC_HOST"),
            username = os.getenv("FMC_USERNAME"),
            password = os.getenv("FMC_PASSWORD")
        )
    )
    app.load_fmc_manager()
    await app.register_tools()
    await app.mcp.run_async(
        transport="http",
        host="127.0.0.1",
        port=8080,
    )

if __name__ == "__main__":
    asyncio.run(main())