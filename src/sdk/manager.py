from sdk import AsyncFMC
from asyncio import Lock

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