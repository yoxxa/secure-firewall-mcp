import pytest
from sdk import AsyncFMC
from sdk.exceptions import AsyncFMCError

@pytest.mark.parametrize(
    "domain_uuid, device_name", 
    [
        ("e276abec-e0f2-11e3-8169-6d9ed49b625f", "PERTH-FW")
    ]
)
@pytest.mark.asyncio
async def test_get_ha_pair_by_name_good_input(
    domain_uuid: str,
    device_name: str,
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_ha_pair_by_name(domain_uuid, device_name)
    # Check if return correct data type 
    assert result is not None
    assert isinstance(result, dict)

@pytest.mark.parametrize(
    "domain_uuid, device_name", 
    [
        ("e276abec-e0f2-11e3-8169-6d9ed49b625f", "INVALID_DEVICE")
    ]
)
@pytest.mark.asyncio
async def test_get_device_by_name_bad_input(
    domain_uuid: str,
    device_name: str,
    fmc_client: AsyncFMC
):
    with pytest.raises(AsyncFMCError) as not_found_error:
        result = await fmc_client.get_ha_pair_by_name(domain_uuid, device_name)

@pytest.mark.asyncio
async def test_get_all_devices(
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_all_ha_pairs()
    assert result is not None
    assert isinstance(result, list)