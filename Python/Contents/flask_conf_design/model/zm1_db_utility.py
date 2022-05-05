class DataManagerBase(object):
    def __init__(self, sqlMgr=None):
        self.sqlMgr = sqlMgr
        self.conn = None  # ConnectionPool 정의 필요


class DataManager4Pas(DataManagerBase):
    pass

