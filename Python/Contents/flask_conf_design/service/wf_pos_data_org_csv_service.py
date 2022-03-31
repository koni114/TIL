from service.main import AppService


class wfPosDataOrgCsv(AppService):

    def read_data_srv(self, contents, sqlMgr):
        return contents