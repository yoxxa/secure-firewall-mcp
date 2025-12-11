from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
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

    async def select_fmc_by_device_name(self, device_name: str) -> AsyncFMC | None:
        filtered_df = self.cache.data["standalone"].filter(
            (pl.col("device_name") == device_name),
        )
        # Indicates not found on any FMCs in cache
        if filtered_df.is_empty():
            return None
        for fmc in self.fmc_list:
            if fmc.host.strip("https://") == filtered_df["fmc_host"][0]:
                return fmc
            
    async def select_fmc_by_ha_pair_name(self, ha_pair_name: str) -> AsyncFMC | None:
        filtered_df = self.cache.data["ha_pair"].filter(
            (pl.col("ha_pair_name") == ha_pair_name),
        )
        # Indicates not found on any FMCs in cache
        if filtered_df.is_empty():
            return None
        for fmc in self.fmc_list:
            if fmc.host.strip("https://") == filtered_df["fmc_host"][0]:
                return fmc
            
    async def select_fmc_by_fmc_host(self, fmc_host: str) -> list[AsyncFMC]:
        return [fmc for fmc in self.fmc_list if fmc.host.strip("https://") == fmc_host]

    # TODO - add HA and Cluster
    # TODO - remove this for loop and just set a variable to load all at same time rather than 1 by 1
    async def run_initial_cache_collect(self) -> None:
        for fmc in self.fmc_list:
            try:
                for device in await fmc.get_all_devices():
                    await self.cache.extend_standalone_df(
                        device
                    )
            except AsyncFMCError:
                continue
            try:
                for ha_pair in await fmc.get_all_ha_pairs():
                    await self.cache.extend_ha_pair_df(
                        ha_pair
                    )
            except AsyncFMCError:
                continue

    async def init(self) -> None:
        await self.add_fmc_from_yaml()
        await self.run_initial_cache_collect()

manager = FMCManager()