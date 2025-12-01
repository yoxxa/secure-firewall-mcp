from sdk import AsyncFMC
from asyncio import Lock
from yaml import load, Loader
import os

class FMCManager:
    def __init__(self) -> None:      
        self.fmc_list = list()
        self._lock = Lock()

    async def add_fmc(self, fmc: AsyncFMC) -> None:
        async with self._lock:
            await fmc.set_global_domain()
            self.fmc_list.append(
                fmc
            )

    async def get_fmc_list(self) -> list[AsyncFMC]:
        return self.fmc_list
    
    async def add_fmc_from_yaml(self) -> None:
        with open("fmc_hosts.yaml", "rb") as file:
            data = load(
                file.read(), 
                Loader = Loader
            )
            for host in data["hosts"]:
                await self.add_fmc(
                    AsyncFMC(
                        host = host,
                        username = os.getenv("FMC_USERNAME"),
                        password = os.getenv("FMC_PASSWORD"),
                    )
                )