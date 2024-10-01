from router.data import find_by_custom_pipeline, update_customer_segment_by_dict
from utils.datetime_utils import datetime_now, datetime_diff_str
from utils.file_io_utils import read_file
from utils.knox_utils import KnoxUtils
from utils.log_utils import BD_ASSISTANT_LOGGER


class CustomerSegmentSendDstNoticeEmail:
    def __init__(self):
        pass

    def run(self):
        # 1. 현재 시간이 오전 09:00 가 넘었는지 먼저 확인.
        if datetime_now().hour < 9:
            return

        # 2. Mongodb 에서 파기예정메일 전송여부(sendDestructionNoticeEmail) = False
        # AND 파기 서약을 안한 경우, destruction_confirm = False
        user_list = self.get_user_and_query_noti_email()

        # user_dict = user_list[0]
        for user_dict in user_list:
            try:
                # 3. user_id + query --> 메일에 필요한 html template 작성
                html_template = self.get_email_content(
                    file_name='send_destruction_notice_email.html',
                    user_id=user_dict['user_id'],
                    query=user_dict['query']
                )
                # html_template=result_file
                response = KnoxUtils.send_email(
                    to=[user_dict['user_id'] + "@samsung.com"],
                    sender='jaehun.hur@samsung.com',  # TODO: 확인 필요.
                    content_text=html_template,
                    content_type='HTML',
                    subject="[BDAssistant]데이터 파기 예정일 안내 (D-7)")

                if response.status_code == 200:
                    # 4. 메일이 정상적으로 발송된 경우 sendDestructionNoticeEmail = True 로 변경.
                    update_customer_segment_by_dict(
                        update_key={"_id": user_dict['_id']},
                        update_values={"sendDestructionNoticeEmail": True}
                    )
                else:
                    BD_ASSISTANT_LOGGER.log(
                        "ERROR", f"Error while send_email by knox API response.status_code -> {response.status_code}"
                                 f" response.content -> {response.content}")
                    continue
            except Exception as e:
                BD_ASSISTANT_LOGGER.log(
                    "ERROR", f"Error while send destruction email user_dict -> {user_dict}, Error: {str(e)}")
                continue

    def get_user_and_query_noti_email(self):
        match_pipeline = [
            {'sendDestructionNoticeEmail': False},
            {'destructionConfirm': {'$exists': False}}
        ]

        doc = find_by_custom_pipeline([{'$match': {'$and': match_pipeline}},
                                       {'$project': {'userId': 1,
                                                     'query': 1,
                                                     'destructedAt': 1}
                                        }])
        user_list = []

        # d = doc[0]
        for d in doc:
            diff_day = datetime_diff_str(time_str1=d['destructedAt'],
                                         time_str2=datetime_now(str),
                                         unit='day')
            if diff_day == 6:
                user_list.append({'_id': d['_id'],
                                  'user_id': d['userId'],
                                  'query': d['query']})
        return user_list

    def get_email_content(self, file_name, user_id, query):
        # import aspose.words as aw
        # import io

        # TODO: html 을 read 하여 필요 부분을 동적으로 parsing 하여 string 으로 가져오게 하는
        # 코드 작성 필요
        

        result_file = read_file(
            file_dir='./services/customer_segment/htmls',
            file_name=file_name)

        return result_file
