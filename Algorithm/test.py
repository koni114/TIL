from collections import defaultdict
from collections import Counter

a = defaultdict(int)
a["A"] = 5
a["B"] = 10

a = [1, 2, 3, 4, 5, 5, 5, 6, 6]
counter_a = Counter(a)
counter_a.most_common(1)

