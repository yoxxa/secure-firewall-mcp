import pytest
from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError

@pytest.mark.asyncio
async def test_get_all_job_history(
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_all_job_history()
    # Check if return correct data type 
    assert result is not None
    assert isinstance(result, list)