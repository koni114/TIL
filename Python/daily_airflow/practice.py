from airflow.operators.python import BaseOperator
from collections import defaultdict, Counter

class MovielensPopularityOperator(BaseOperator):
    def __init__(self, conn_id, start_date, end_date, min_ratings=4, top_n=5, **kwargs):
        super().__init__(** kwargs)
        self._conn_id = conn_id
        self._start_date = start_date
        self._end_date = end_date
        self._min_ratings = min_ratings
        self._top_n = top_n

    def execute(self, context):
        with MovielensHook(self._conn_id) as hook:
            ratings = hook.get_ratings(
                start_date=self._start_date,
                end_date=self._end_date,
            )

            ratings_sums = defaultdict(Counter)
            for rating in ratings:
                rating_sums[rating["movieId"]].update(
                    count=1,
                    rating=rating["rating"]
                )