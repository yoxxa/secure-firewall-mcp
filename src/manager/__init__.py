from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError
from manager.cache import Cache
from manager.exceptions import FMCManagerError
from asyncio import Lock
from yaml import load, Loader
import os
import polars as pl
from httpx import ConnectTimeout
from logging import Logger

class FMCManager:
    """
    Manages creation and selection of multiple AsyncFMC objects
    """
    def __init__(self) -> None:      
        self.fmc_list = list()
        self._lock = Lock()
        self.cache = Cache()
        self.logger = Logger("fmc_manager")

    async def add_fmc(self, fmc: AsyncFMC) -> None:
        """
        Async SDK for Firepower Management Center
        Args:
            fmc: FMC host to add to manager
        """
        async with self._lock:
            try:
                await fmc.set_global_domain()
                self.fmc_list.append(
                    fmc
                )
            # Errors when FMC does not successfully get appended to fmc_list 
            except ConnectTimeout:
                raise FMCManagerError(f"Failed to connect to host: {fmc.host}")

    async def get_fmc_list(self) -> list[AsyncFMC]:
        return self.fmc_list
    
    async def add_fmc_from_yaml(self) -> None:
        """
        Add all FMC hosts defined in `fmc_hosts.yaml`
        """
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
        """
        Select an FMC by searching the cache for a matching device name
        Args:
            device_name: FTD device name to match on
        Returns:
            AsyncFMC with device or None to represent not found in cache
        """
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
        """
        Select an FMC by searching the cache for a matching HA pair name
        Args:
            host: HA pair name to match on
        Returns:
            AsyncFMC with HA pair or None to represent not found in cache
        """
        filtered_df = self.cache.data["ha_pair"].filter(
            (pl.col("ha_pair_name") == ha_pair_name),
        )
        # Indicates not found on any FMCs in cache
        if filtered_df.is_empty():
            return None
        for fmc in self.fmc_list:
            if fmc.host.strip("https://") == filtered_df["fmc_host"][0]:
                return fmc
            
    # TODO - refactor to return [0]
    async def select_fmc_by_fmc_host(self, fmc_host: str) -> list[AsyncFMC]:
        """
        Select an FMC by searching the FMC list for a matching FMC name 
        Args:
            fmc_host: FMC host to match on
        Returns:
            list of AsyncFMC, where [0] equals matching FMC
        """
        return [fmc for fmc in self.fmc_list if fmc.host.strip("https://") == fmc_host][0]

    # TODO - add HA and Cluster
    # TODO - remove this for loop and just set a variable to load all at same time rather than 1 by 1
    async def run_initial_cache_collect(self) -> None:
        """
        Gather all required cache data before running the MCP server
        """
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

    async def check_fmc_list_not_empty(self) -> None:
        if not self.fmc_list:
            raise FMCManagerError("FMC host list empty, must set hosts in `fmc_hosts.yaml`")

    async def init(self) -> None:
        """
        Initialise all required data before running the main MCP server
        """
        await self.add_fmc_from_yaml()
        await self.check_fmc_list_not_empty()
        await self.run_initial_cache_collect()

    async def add_standalone_to_cache(self, data: dict) -> None:
        """
        Adds a standalone FTD device to the Cache of FMCManager
        Args:
            data: standalone FTD device to add to cache
        """
        async with self._lock:
            await self.cache.extend_standalone_df(
                data
            )

    async def add_ha_pair_to_cache(self, data: dict) -> None:
        """
        Adds a HA pair to the Cache of FMCManager
        Args:
            data: HA pair to add to cache
        """
        async with self._lock:
            await self.cache.extend_ha_pair_df(
                data
            )

manager = FMCManager()