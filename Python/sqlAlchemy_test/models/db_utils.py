import cx_Oracle


def get_sqlalchemy_db_url():
    host='localhost'
    port=1521
    sid='XE'
    user='testuser'
    password='testuser'
    sid = cx_Oracle.makedsn(host, port, sid=sid)

    ora_url = 'oracle://{user}:{password}@{sid}'.format(
        user=user,
        password=password,
        sid=sid
    )

    return ora_url
