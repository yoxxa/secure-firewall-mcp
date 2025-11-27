from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
import asyncio

from sdk.fmc import AsyncFMC

class App:
    def __init__(self):
        self.mcp = FastMCP(
            name = "CiscoSecureFirewall",
            instructions = """
                This server provides tools for interfacing with the Cisco Secure Firewall API
                Use ....
            """
        )

app = App()

async def main():
    await app.mcp.run_async(
        transport="http",
        host="127.0.0.1",
        port=8080,
    )

if __name__ == "__main__":
    asyncio.run(main())