from datetime import timedelta
import pandas as pd

from feast import (
    Entity,
    FeatureService,
    FeatureView,
    Field,
    FileSource,
    PushSource,
    RequestSource,
)

from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64

df = pd.read_parquet("feature_repo/data/driver_stats.parquet")
