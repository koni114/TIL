import importlib
import sys
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime as dt

from view import create_endpoints
from libs.util.logger import getLogger, INFO, MORE, DETAIL, ERROR

logger = getLogger()


class Services:
    pass


def create_app(app_name, app_config):
    app = Flask(app_name)
    app.config.from_object(app_config)

    CORS(app) #
    services = Services

    import model.wf_pos_data_org_csv_sql as wf_pos_data_org_csv_sql
    import service.wf_pos_data_org_csv_service as wf_pos_data_org_csv_service
    wf_pos_data_org_csv_sqlmgr = wf_pos_data_org_csv_sql.wfPosDataOrgCsvSqlMgr()
    services.wf_pos_data_org_csv = wf_pos_data_org_csv_service.wfPosDataOrgCsv(sqlMgr=wf_pos_data_org_csv_sqlmgr)

    # end point 들을 생성
    create_endpoints(app, services)
    logger.logc(INFO, f"created completed")
    return app








