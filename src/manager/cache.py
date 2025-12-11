import polars as pl

class Cache:
    """
    Caches data for searching and selecting `AsyncFMC`
    """
    def __init__(self):
        self.data = dict({
            "standalone": pl.DataFrame(
                schema=[
                    ("fmc_host", pl.String), 
                    ("device_name", pl.String),
                    ("device_uuid", pl.String),
                    ("domain_name", pl.String),
                    ("domain_uuid", pl.String),
                    ("acp_name", pl.String),
                    ("acp_uuid", pl.String)
                ]
            ),
            "ha_pair": pl.DataFrame(
                schema=[
                    ("fmc_host", pl.String),
                    ("ha_pair_name", pl.String),
                    ("ha_pair_uuid", pl.String),
                    ("primary_device", pl.String),
                    ("secondary_device", pl.String)
                ]
            ),
            "cluster": pl.DataFrame(
                schema=[
                    ("name", pl.String), 
                    ("uuid", pl.String)
                ]
            )
        })

    async def extend_standalone_df(self, data: dict) -> None:
        """
        Extends the cache standalone FTD df to include this device
        Args:
            data: data from `device` endpoint
        """
        df = pl.DataFrame({
            "fmc_host": [data["links"]["self"].strip("https://").split("/")[0]],
            "device_name": [data["name"]],
            "device_uuid": [data["id"]],
            "domain_name": [data["metadata"]["domain"]["name"]],
            "domain_uuid": [data["metadata"]["domain"]["id"]],
            "acp_name": [data["accessPolicy"]["name"]],
            "acp_uuid": [data["accessPolicy"]["id"]]
        })
        self.data["standalone"].extend(df)

    async def extend_ha_pair_df(self, data: dict) -> None:
        """
        Extends the cache HA pair df to include this device
        Args:
            data: data from `ha_pair` endpoint
        """
        df = pl.DataFrame({
            "fmc_host": [data["links"]["self"].strip("https://").split("/")[0]],
            "ha_pair_name": [data["name"]],
            "ha_pair_uuid": [data["id"]],
            "primary_device": [data["primary"]["name"]],
            "secondary_device": [data["secondary"]["name"]]
        })
        self.data["ha_pair"].extend(df)