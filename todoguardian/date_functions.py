import re
import calendar
from datetime import date, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU


def convert_pattern_to_date(pattern: str, offset: date | None = None) -> date:
    """
    Transforms a date pattern into a proper date.

    Allowed patterns:
    * [0-9][dwmyb]
    * 'yesterday', 'today' or 'tomorrow'
    * days of the week (monday - friday)
    """
    result = None
    offset = offset or timezone.localdate()

    relative_pattern = re.match("(?P<length>-?[0-9]+)(?P<period>[dwmyb])$", pattern, re.I)

    monday = "mo(n(day)?)?$"
    tuesday = "tu(e(sday)?)?$"
    wednesday = "we(d(nesday)?)?$"
    thursday = "th(u(rsday)?)?$"
    friday = "fr(i(day)?)?$"
    saturday = "sa(t(urday)?)?$"
    sunday = "su(n(day)?)?$"
    weekday_pattern = re.match("|".join([monday, tuesday, wednesday, thursday, friday, saturday, sunday]), pattern)

    if relative_pattern:
        length = relative_pattern.group("length")
        period = relative_pattern.group("period")
        result = _convert_pattern(length, period, offset)

    elif weekday_pattern:
        result = _convert_weekday_pattern(weekday_pattern.group(0))

    elif re.match("tod(ay)?$", pattern):
        result = _convert_pattern("0", "d")

    elif re.match("tom(orrow)?$", pattern):
        result = _convert_pattern("1", "d")

    elif re.match("yes(terday)?$", pattern):
        result = _convert_pattern("-1", "d")

    return result


def _convert_pattern(length: str, unit: str, offset: date | None = None) -> date:
    result = None

    offset = offset or timezone.localdate()
    length = int(length)

    match unit:
        case "d":
            result = offset + relativedelta(days=length)
        case "w":
            result = offset + relativedelta(weeks=length)
        case "m":
            result = offset + relativedelta(months=length)
        case "y":
            result = offset + relativedelta(years=length)
        case "b":
            result = offset
            days = length
            delta = 1 if days > 0 else -1

            while abs(days) > 0:
                result = result + relativedelta(days=delta)
                weekday = result.weekday()

                if weekday >= 5:
                    continue

                days = days - 1 if delta > 0 else days + 1
        case _:
            raise NotImplementedError

    return result


def _convert_weekday_pattern(weekday: str) -> date:
    weekday_to_relativedelta = {"mo": MO(+1), "tu": TU(+1), "we": WE(+1), "th": TH(+1), "fr": FR(+1), "sa": SA(+1), "su": SU(+1)}

    return timezone.localdate() + relativedelta(days=1, weekday=weekday_to_relativedelta[weekday[:2]])
