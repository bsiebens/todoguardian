import re
from datetime import date

from dateutil.relativedelta import FR, MO, SA, SU, TH, TU, WE, relativedelta
from dateutil import parser
from django.utils import timezone


def to_date(pattern: str, offset: date | None = None) -> date | None:
    """
    Takes a pattern for a relative date and converts that into an absolute date.

    Following patterns are accepted:
    * [0-9][dwmyb] (b = business days)
    * `yesterday`, `today` or `tomorrow`
    * days of the week: monday through sunday

    Absolute dates are calculated in relation the offset date. If not set, a default value of
    `timezone.localdate()` will be used as offet.
    """
    # Check if offset is set, if not set to today
    if offset is None:
        offset = timezone.localdate()

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
        return _calculate_date_from_pattern(length, period, offset)

    elif weekday_pattern:
        return _calculate_date_from_weekday(weekday_pattern.group(0))

    elif re.match("tod(ay)?$", pattern):
        return _calculate_date_from_pattern(0, "d")

    elif re.match("tom(orrow)?$", pattern):
        return _calculate_date_from_pattern(1, "d")

    elif re.match("yes(terday)?$", pattern):
        return _calculate_date_from_pattern(-1, "d")

    else:
        # Maybe it's a string we can convert directly into a date?
        try:
            return parser.parse(pattern).date()

        except parser.ParserError:
            return None


def _calculate_date_from_pattern(length: int | str, period: str, offset: date | None = None) -> date | None:
    """Returns a given date based on the supplied pattern, calculting from the offset. If offset is None, today is used."""
    if offset is None:
        offset = timezone.localdate()

    if type(length) is str:
        length = int(length)

    match period:
        case "d":
            return offset + relativedelta(days=length)
        case "w":
            return offset + relativedelta(weeks=length)
        case "m":
            return offset + relativedelta(months=length)
        case "y":
            return offset + relativedelta(years=length)
        case "b":
            result = offset
            days = length
            delta = 1 if days > 0 else -1

            while abs(days) > 0:
                result = result + relativedelta(days=delta)
                if result.weekday() >= 5:
                    continue

                days = days - delta

            return result
        case _:
            return None


def _calculate_date_from_weekday(weekday: str) -> date:
    """Converts a given weekday into an absolute day, always taking the next option (so if today = monday, monday will given the next monday)."""
    weekday_to_relativedelta = {
        "mo": MO(+1),
        "tu": TU(+1),
        "we": WE(+1),
        "th": TH(+1),
        "fr": FR(+1),
        "sa": SA(+1),
        "su": SU(+1),
    }

    return timezone.localdate() + relativedelta(days=1, weekday=weekday_to_relativedelta[weekday[:2]])
