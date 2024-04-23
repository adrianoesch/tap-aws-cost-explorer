"""AWSCostExplorer tap class."""

from typing import List

from singer_sdk import Tap, Stream

from tap_aws_cost_explorer.schema import config_jsonschema
from tap_aws_cost_explorer.streams import CostAndUsageWithResourcesStream


class TapAWSCostExplorer(Tap):
    """AWSCostExplorer tap class."""
    name = "tap-aws-cost-explorer"
    config_jsonschema = config_jsonschema

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [CostAndUsageWithResourcesStream(tap=self)]
