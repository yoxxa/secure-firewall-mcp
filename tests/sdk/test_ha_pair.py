import pytest
from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError

@pytest.mark.parametrize(
    "device_name", 
    [
        "PERTH-FW"
    ]
)
@pytest.mark.asyncio
async def test_get_ha_pair_by_name_good_input(
    device_name: str,
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_ha_pair_by_name(device_name)
    # Check if return correct data type 
    assert result is not None
    assert isinstance(result, dict)

@pytest.mark.parametrize(
    "device_name", 
    [
        "INVALID_DEVICE"
    ]
)
@pytest.mark.asyncio
async def test_get_ha_pair_by_name_bad_input(
    device_name: str,
    fmc_client: AsyncFMC
):
    with pytest.raises(AsyncFMCError) as not_found_error:
        result = await fmc_client.get_ha_pair_by_name(device_name)

@pytest.mark.asyncio
async def test_get_all_devices(
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_all_ha_pairs()
    assert result is not None
    assert isinstance(result, list)