from sdk import AsyncFMC
from manager.cache import Cache
from asyncio import Lock
from yaml import load, Loader
import os
import polars as pl

class FMCManager:
    def __init__(self) -> None:      
        self.fmc_list = list()
        self._lock = Lock()
        self.cache = Cache()

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

    async def update_standalone_cache(self, data: dict) -> None: 
        await self.cache.update_standalone_df(
            data
        )

    async def select_fmc_by_device_name(self, device_name: str) -> AsyncFMC | None:
        filtered_df = self.cache.data["standalone"].filter(
            (pl.col("device_name") == device_name),
        )
        # Indicates not found on any FMCs in cache
        if filtered_df.is_empty():
            return None
        for fmc in self.fmc_list:
            if fmc.host.strip("https://") == filtered_df["fmc_host"][0]:
                print("RETURNING FMC OBJ")
                return fmc
            
    async def run_initial_cache_collect(self) -> None:
        for fmc in self.fmc_list:
            for device in await fmc.get_all_devices():
                await self.update_standalone_cache(
                    device
                )

    async def init(self) -> None:
        await self.add_fmc_from_yaml()
        await self.run_initial_cache_collect()

manager = FMCManager()