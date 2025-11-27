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