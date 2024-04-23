from singer_sdk import typing as th

config_jsonschema = th.PropertiesList(
    th.Property(
        "access_key",
        th.StringType,
        required=True,
        description="Your AWS Account Access Key."
    ),
    th.Property(
        "secret_key",
        th.StringType,
        required=True,
        description="Your AWS Account Secret Key."
    ),
    th.Property(
        "session_token",
        th.StringType,
        description="Your AWS Account Session Token if required for authentication."
    ),
    th.Property(
        "start_date",
        th.StringType,
        required=True,
        description="The start date for retrieving Amazon Web Services cost."
    ),
    th.Property(
        "end_date",
        th.DateTimeType,
        description="The end date for retrieving Amazon Web Services cost."
    ),
    th.Property(
        "granularity",
        th.StringType,
        required=True,
        description="Sets the Amazon Web Services cost granularity to \
                    MONTHLY or DAILY , or HOURLY."
    ),
    th.Property(
        "metrics",
        th.ArrayType(th.StringType),
        required=True,
        description="Which metrics are returned in the query. Valid \
                    values are AmortizedCost, BlendedCost, \
                    NetAmortizedCost, NetUnblendedCost, \
                    NormalizedUsageAmount, UnblendedCost, and \
                    UsageQuantity.\
                    See boto3 docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_with_resources.html\
                    "
    ),
    th.Property(
        "stream_name",
        th.StringType,
        required = False,
        description="Name of stream, often results in names of tables objects."
    ),
    th.Property(
        "filter",
        th.ObjectType(
            th.Property(
                "Dimensions",
                th.ObjectType(
                    th.Property("Key",th.StringType),
                    th.Property("Values",th.ArrayType(
                        th.StringType
                    ))
                )
            )
        ),
        required=False,
        description="See boto3 client explorer params: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_with_resources.html"
    ),
    th.Property(
        "groupby",
        th.ArrayType(
            th.ObjectType(
                th.Property("Type",th.StringType),
                th.Property("Key",th.StringType)
            )
        ),
        required=False,
        description="See boto3 client explorer params: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_with_resources.html"
    ),
).to_dict()