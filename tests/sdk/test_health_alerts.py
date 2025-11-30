import pytest
from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError

@pytest.mark.parametrize(
    "domain_uuid", 
    [
        "e276abec-e0f2-11e3-8169-6d9ed49b625f"
    ]
)
@pytest.mark.asyncio
async def test_get_all_health_alerts(
    domain_uuid: str,
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_all_health_alerts(domain_uuid)
    # Check if return correct data type 
    assert result is not None
    assert isinstance(result, list)