import time
import datetime
from dateutil.parser import parse
from libs.util.logger import get_logger, get_caller, INFO, WARNING, ERROR, MORE, DETAIL, DEBUG

logger = get_logger()


def wait_next_100m_sec():
    """
    현재 시간을 기준으로 다음 100ms 까지 대기하는 함수. 0.1 초 단위로 처리하는 로직에서 사용
    :return: time.sleep
    """
    time_val = datetime.datetime.now()
    wait_sec = float(100_000 - time_val.microsecond % 100_000) / 1_000_000
    logger.logcc(DETAIL, f"sleep for {wait_sec} mirco seconds")
    time.sleep(wait_sec)


def wait_next_sec():
    """
    다음 1 sec 까지 대기 함수. 11초 단위로 처리하는 로직에서 사용
    ex) 12시 11분 37.xx초 --> 12초 11분 38초 까지 대기
        13시 9분 2.xx초   --> 13시  9분 3초 까지 대기
    """
    time_val = datetime.datetime.now()
    wait_sec = float(1_000_000 - time_val.microsecond % 1_000_000) / 1_000_000
    logger.logcc(MORE, f"sleep for {wait_sec} micro seconds")
    time.sleep(wait_sec)


def wait_next_10_sec():
    """
    다음 10 sec 까지 대기 함수. 10초 단위로 처리하는 로직에서 사용
    ex) 12시 11분 37초 --> 12초 11분 40초 까지 대기
        13시 9분 2초   --> 13시  9분 10초 까지 대기
    :return:
    """
    time_val = datetime.datetime.now()
    wait_sec = (9 - time_val.second % 10) + float(1_000_000 - time_val.microsecond % 1_000_000) / 1_000_000
    logger.logcc(MORE, f"sleep for {wait_sec} seconds")
    time.sleep(wait_sec)


def sleep_sec(secs):
    time.sleep(secs)


def sleep_mins(mins):
    time.sleep(mins * 60)


def str_date_time(date=None, days=0, seconds=0, minutes=0, hours=0, weeks=0, time_stamp=None,
                  show_milliseconds=False, sep_disable=False):
    """
    return "YYYY-MM-DD HH:MM:SS" 형태의 문자열로 리턴.
    days, seconds, minutes, hours, weeks 값을 입력하면, 해당 값 만큼 추가하여 리턴.

    :param show_milliseconds: milliseconds 단위까지 표기여부
    :param sep_disable: '-' 추가 여부 True --> 2022-01-01.. False --> 20220101
    """
    if date:
        time_val = parse(date)
    elif time_stamp:
        time_val = datetime.datetime.fromtimestamp(int(time_stamp))
    else:
        time_val = datetime.datetime.now()
    time_val += datetime.timedelta(days=days, seconds=seconds, minutes=minutes,
                                   hours=hours, weeks=weeks)

    if show_milliseconds:
        if sep_disable:
            result_date_time = time_val.strftime("%Y%m%d%H%M%S%f")[:-3]
        else:
            result_date_time = time_val.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    else:
        if sep_disable:
            result_date_time = time_val.strftime("%Y%m%d%H%M%S")
        else:
            result_date_time = time_val.strftime("%Y-%m-%d %H:%M:%S")

    return result_date_time


def str_date(date=None, days=0, seconds=0, minutes=0, hours=0, weeks=0, sep="-"):
    """
    return string of date("YYYY-MM-DD")
    after sum from options
    """
    try:
        result_date_time = str_date_time(date=date,
                                         days=days,
                                         seconds=seconds,
                                         minutes=minutes,
                                         hours=hours,
                                         weeks=weeks)
        return result_date_time.split()[0] if sep == "-" else result_date_time.split()[0].replace("-", sep)
    except Exception as e:
        logger.logc(ERROR, f"{e.__class__.__name__} | {e}")
    return None


def dif_secs(early_date, last_date):
    """
    return sec difference from early_date to last_date,
    input type is str_date_time(string)
    """
    dif = parse(last_date) - parse(early_date)
    logger.logc(DEBUG, dif)
    return dif.seconds + dif.days * 86400


def dif_mins(early_date, last_date):
    """
    return mins difference from early_date to last_date,
    input type is str_date_time(string)
    """
    mins = divmod(dif_secs(early_date, last_date), 60)[0]
    return mins


def dif_hours(early_date, last_date):
    """
    return hours difference from early_date to last_date,
    input type is str_date_time(string)
    """
    return float(round(dif_secs(early_date, last_date)/3600, 2))


def dif_days(early_date, last_date):
    """
    return days difference from early_date to last_date,
    input type is str_date_time(string)
    """
    dif = parse(last_date) - parse(early_date)
    return dif.days


def dif_date_time(early_date, last_date):
    """
    return date(x, days, hh:mm:ss) from early_date to last_date,
    input type --> str_date_time(string)
    """
    dif = parse(last_date) - parse(early_date)
    return str(dif)












