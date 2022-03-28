from flask import request, jsonify, current_app, Request, g


def create_endpoints(app, service):
    @app.route("/am_md_survey_rt", methods=["POST"])
    def am_md_survey_rt():
        df = service.am_md_survey.select_by_args_srv(request.json())
        return jsonify(df.to_dict())
