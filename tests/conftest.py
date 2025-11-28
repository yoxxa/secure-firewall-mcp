from sdk.fmc import AsyncFMC
import pytest_asyncio
from fastmcp import Client
from dotenv import load_dotenv
import os

load_dotenv(
    dotenv_path = "src/creds/.env"
)

@pytest_asyncio.fixture
async def mcp_client():
    async with Client("http://localhost:8080/mcp") as client:
        yield client

@pytest_asyncio.fixture
async def fmc_client():
    async with AsyncFMC(
        host = os.getenv("FMC_HOST"),
        username = os.getenv("FMC_USERNAME"),
        password = os.getenv("FMC_PASSWORD")
    ) as client:
        yield client