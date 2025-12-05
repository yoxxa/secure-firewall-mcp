import polars as pl

class Cache:
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
                    ("name", pl.String), 
                    ("uuid", pl.String)
                ]
            ),
            "cluster": pl.DataFrame(
                schema=[
                    ("name", pl.String), 
                    ("uuid", pl.String)
                ]
            )
        })

    async def update_standalone_df(self, data: dict) -> None:
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