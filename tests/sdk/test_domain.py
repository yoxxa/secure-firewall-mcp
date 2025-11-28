import pytest
from sdk.fmc import AsyncFMC, AsyncFMCError

@pytest.mark.parametrize(
    "domain_name", 
    ["Perth", "Global",]
)
@pytest.mark.asyncio
async def test_get_domain_by_name_good_input(
    domain_name: str,
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_domain_by_name(domain_name)
    # Check if return correct data type 
    assert result is not None
    assert isinstance(result, dict)

@pytest.mark.parametrize(
    "domain_name", 
    ["INVALID_DOMAIN"]
)
@pytest.mark.asyncio
async def test_get_domain_by_name_bad_input(
    domain_name: str,
    fmc_client: AsyncFMC
):
    with pytest.raises(AsyncFMCError) as not_found_error:
        result = await fmc_client.get_domain_by_name(domain_name)

@pytest.mark.asyncio
async def test_get_all_domains(
    fmc_client: AsyncFMC
):
    result = await fmc_client.get_all_domains()
    assert result is not None
    assert isinstance(result, list)
    