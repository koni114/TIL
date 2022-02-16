# day 2 mission

import pandas as pd
import numpy as np

# 0.5 를 기준으로 올림 또는 내림


a = np.array([-4.62, -2.19, 0, 1.57, 3.40, 4.06])

np.round(a)
np.round(a, 1)
np.rint(a)
np.fix(a)
np.ceil(a)
np.floor(a)
np.trunc(a)

b = np.array([1, 2, 3, 4])
c = np.array([[1, 2], [3, 4]])

np.prod(b)
np.prod(c, axis=0)
np.prod(c, axis=1)
np.sum(b)
np.sum(b, keepdims=True)

d = np.array([[1, 2], [3, np.nan]])
np.nanprod(d, axis=0)
np.nanprod(d, axis=1)
np.nansum(d, axis=0)
np.nansum(d, axis=1)

e = np.array([1, 2, 3, 4])
f = np.array([[1, 2, 3], [4, 5, 6]])

np.cumprod(e)
np.cumprod(f, axis=0)
np.cumprod(f,axis=1)

