from __future__ import print_function

import random
import string
from datetime import datetime, timedelta


def random_datetime(lo="1/1/2008 1:30 PM", hi="1/1/2009 1:30 PM"):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    start = datetime.strptime(lo, "%m/%d/%Y %I:%M %p")
    end = datetime.strptime(hi, "%m/%d/%Y %I:%M %p")
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_float(lo=1.0, hi=1.0e3):
    return float(random.uniform(lo, hi))


def random_int(lo=1, hi=1e3):
    return random.randint(lo, hi)


def random_str(size=10, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
