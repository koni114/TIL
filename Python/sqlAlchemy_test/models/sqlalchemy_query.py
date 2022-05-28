import os
import pandas as pd
import numpy as np

from models.table import Customers, Vendors, Products, Orders, OrderItems
from models.database import DBSession

"""
SELECT DISTINCT vend_ids
FROM Products
WHERE ROWNUM <= 10;
"""

with DBSession as db:
    db.query()


