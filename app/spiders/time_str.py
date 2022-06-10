# -*- coding: utf-8 -*-
"""
@desc:
@version: python3
@author: ??
@time: 2019/6/4 17:41
"""
from loguru import logger
import datetime
import time
import re


def get_now():
    """
    获取当前格式化日期
    :return: %Y-%m-%d %H:%M:%S
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_now_14():
    """
    获取当前格式化日期，长度14位
    :return: %Y%m%d%H%M%S
    """
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def get_now_filename():
    """
    获取当前格式化日期
    :return: %Y-%m-%d_%H_%M_%S
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def get_minutes_ago(minutes):
    """
    获取过去时间 格式化日期
    :param minutes: 过去的分钟 now-minutes
    :return: %Y-%m-%d %H:%M:%S
    """
    return (
        datetime.datetime.now() - datetime.timedelta(minutes=minutes)
    ).strftime("%Y-%m-%d %H:%M:%S")


def get_today():
    """
    获取当前日期
    :return: %Y-%m-%d
    """
    return datetime.datetime.today().strftime("%Y-%m-%d")


def get_day_ago(days):
    """
    过去的某天
    :param days: 过去的天数 today-days
    :return: %Y-%m-%d
    """
    ago = datetime.datetime.today() - datetime.timedelta(int(days))
    return ago.strftime("%Y-%m-%d")


def get_today_8():
    """
    获取当前日期，长度8位
    :return: %Y%m%d
    """
    return datetime.datetime.now().strftime("%Y%m%d")


def get_month_range(start_day, end_day):
    """
    获取两个时间之间所有的月份
    :param start_day: datetime.datetime.now()
    :param end_day: datetime.datetime.now()
    :return: ["2019-07"]
    """
    months = (
        (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
    )
    month_range = []
    for mon in range(start_day.month - 1, start_day.month + months):
        t_year = start_day.year + mon // 12
        t_mon = mon % 12 + 1
        month_range.append("%s-%02d" % (t_year, t_mon))
    return month_range


def get_weekday(start_day, num):
    """
    输出从当天开始的连续n天
    :param start_day: 形如'%Y-%m-%d'
    :param num: 要输出的连续的天数
    """
    weekdic = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    start_day = datetime.datetime.strptime(start_day, "%Y-%m-%d")
    res = []
    for i in range(num):
        res.append(
            (start_day.strftime("%Y-%m-%d"), weekdic.get(start_day.weekday()))
        )
        start_day += datetime.timedelta(1)
    return res


def format_rq_str(rq_str, str_seq="-"):
    """
    格式化日期串
        1993-4-2 --> 1993-04-02
        1993/4/2 --> 1993-04-02
    :param rq_str:
    :param str_seq:
    :return:
    """
    re_rs = re.match(
        r"(\d{4})" + str_seq + r"(\d+)" + str_seq + r"(\d+)", rq_str
    )
    if not re_rs:
        return rq_str
    re_rs_vals = re_rs.groups()
    return "%s-%02d-%02d" % (
        re_rs_vals[0],
        int(re_rs_vals[1]),
        int(re_rs_vals[2]),
    )


def format_rq_str_by_re(in_str):
    """
    对日期做格式化
    :param in_str:
    :return:
    """
    if not in_str:
        return ""
    re_rs = re.findall(r"(\d{4})[-/.]+(\d{1,2})[-/.]+(\d{1,2})", in_str)
    if re_rs:
        try:
            f_obj = datetime.datetime(*tuple(map(int, re_rs[0])))
            return f_obj.strftime("%Y-%m-%d")
        except BaseException:
            pass
    return ""


def get_rq_list(nyr_text):
    """
    从一段文字中提取日期
    :param nyr_text:
    :return:
        format_nyr("自2019年3月1日")
        ['2019-03-01']
        format_nyr("生成日期：2018年09月11日, 2019年03月01日生效")
        ['2018-09-11', '2019-03-01']
        format_nyr("生成日期：生效")
        []
    """
    re_pattern = r"(\d+)年(\d+)月(\d+)日"
    rs = [
        datetime.datetime(int(row[0]), int(row[1]), int(row[2])).strftime(
            "%Y-%m-%d"
        )
        for row in re.findall(re_pattern, nyr_text)
    ]
    return rs


def get_int_time_from_str(src_str, format_str="%Y-%m-%d %H:%M:%S"):
    """
    通过字符串转换得到时间戳
    :param src_str:
    :param format_str:
    :return:
    """
    return int(time.mktime(time.strptime(src_str, format_str)))


def get_str_from_int_time(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """
    从时间戳转到字符串格式
    :param timestamp:
    :param format_str:
    :return:
    """
    struct_time = time.localtime(int(timestamp))
    return time.strftime(format_str, struct_time)


def get_timestamp():
    """
    返回时间戳
    :return:
    """
    return int(round(time.time()))


def check_timestamp(timestr, seconds):
    """
    检查传入时间戳与当前的差额是否超过 seconds
        now - timestr > seconds
    :param timestr: str(int)
    :param seconds: 秒
    :return:
    """
    if not str(timestr).isdigit():
        logger.info("timestr 必须是int类型")
        return True
    # 获取当前时间戳
    n_timestr = get_timestamp()
    if (n_timestr - int(str(timestr))) > seconds:
        return True
    return False


def get_last_minute_interval(cnt):
    """
    最后一个时段的时间串
    :param cnt: 几分钟一次
    :return:
    """
    _cnt = str(cnt)
    if not _cnt.isdigit() or int(_cnt) < 1:
        _cnt = "1"
    now_obj = datetime.datetime.now()
    now_min = now_obj.minute
    rs = "%s%02d" % (
        now_obj.strftime("%Y%m%d%H"),
        now_min - (now_min % int(_cnt)),
    )
    return rs
