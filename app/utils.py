from datetime import datetime, timedelta
import re


def uuid1_time_to_datetime(time: int):
    """
    Start datetime is on October 15th, 1582.
    WHY? https://en.wikipedia.org/wiki/1582

    add the time from uuid.uui1().time
    divided by 10 (ignoring the remainder thus //)
    """
    return datetime(1582, 10, 15) + timedelta(microseconds=time // 10)


def extract_asin(url):
    result = re.search(r'/dp/([a-zA-Z0-9]+)', url)
    if result:
        return result.group(1)
    return None


def extract_price(string):
    # result = re.search(r'\d+\.\d+', string)
    # if result:
    #     return float(result.group())
    # return None
    if string:
        # remove non digit characters from the string and convert it to an integer
        return int(''.join([char for char in string if char.isdigit()]))
    return None