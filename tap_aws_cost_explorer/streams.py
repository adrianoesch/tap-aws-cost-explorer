"""Stream type classes for tap-aws-cost-explorer."""

import datetime, json
from pathlib import Path
from typing import Optional, Iterable

import pendulum
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_aws_cost_explorer.client import AWSCostExplorerStream

class CostAndUsageWithResourcesStream(AWSCostExplorerStream):
    """Define custom stream."""
    primary_keys = ["metric_name", "groupby_values","filter_config","time_period_start"]
    replication_key = "time_period_start"
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("time_period_start", th.DateTimeType),
        th.Property("time_period_end", th.DateTimeType),
        th.Property("groupby_keys", th.StringType),
        th.Property("groupby_values", th.StringType),
        th.Property("filter_config", th.StringType),
        th.Property("metric_name", th.StringType),
        th.Property("amount_unit", th.StringType),
        th.Property("amount", th.NumberType),
    ).to_dict()
    
    def __init__(self,tap):
        self.name = tap.config.get('stream_name','costs')
        super().__init__(tap)

    def _get_end_date(self):
        if self.config.get("end_date") is None:
            return datetime.datetime.today() - datetime.timedelta(days=1)
        return th.cast(datetime.datetime, pendulum.parse(self.config["end_date"]))

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects."""
        next_page = True
        start_date = self.get_starting_timestamp(context)
        end_date = self._get_end_date()
        filter_config_str = json.dumps(self.config.get('filter',{}))
        groupby_keys_str = ','.join([i.get('Key') for i in self.config.get('groupby',[]) ])

        while next_page:
            response = self.conn.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime("%Y-%m-%d"),
                    'End': end_date.strftime("%Y-%m-%d")
                },
                Granularity=self.config.get("granularity"),
                Metrics=self.config.get("metrics"),
                GroupBy=self.config.get('groupby',[]),
                Filter=self.config.get('filter',{})
            )
            next_page = response.get("NextPageToken")

            for row in response.get("ResultsByTime"):
                has_groups = len(row.get('Groups',[])) > 0
                if has_groups:
                    for group in row['Groups']:
                        for k,v in group['Metrics'].items():
                            yield {
                                "time_period_start": row.get("TimePeriod").get("Start"),
                                "time_period_end": row.get("TimePeriod").get("End"),
                                "groupby_keys": groupby_keys_str,
                                "groupby_values": ','.join(group['Keys']),
                                "filter_config": filter_config_str,
                                "metric_name": k,
                                "amount_unit": v.get("Unit"),
                                "amount": float(v.get("Amount"))
                            }
                else:
                    for k, v in row.get("Total").items():
                        yield {
                            "time_period_start": row.get("TimePeriod").get("Start"),
                            "time_period_end": row.get("TimePeriod").get("End"),
                            "metric_name": k,
                            "groupby_keys": None,
                            "groupby_values": None,
                            "filter_config": filter_config_str,
                            "amount": v.get("Amount"),
                            "amount_unit": v.get("Unit")
                        }
