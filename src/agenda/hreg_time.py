from src.agenda.required_idea import Road, SuffFactUnit
from src.agenda.idea import IdeaBare as YB
from dataclasses import dataclass
from datetime import datetime


class InvalidSuffFactUnitException(Exception):
    pass


@dataclass
class SuffFactUnitHregTime:
    _weekday: str = None
    _every_x_days: int = None  # builds jajatime(minute)
    _every_x_months: int = None  # builds myagenda,time,months
    _on_x_monthday: int = None  # " build myagenda,time,month,monthday
    _every_x_years: int = None  # builds myagenda,time,years

    _every_x_weeks: int = None  # builds jajatime(minute)
    _x_week_remainder: int = None

    _between_hr_min_open: int = None  # clock and y o'clock" build jajatime(minutes)
    _between_hr_min_nigh: int = None  # clock and y o'clock" build jajatime(minutes)
    _between_weekday_open: int = None  # and y weekday" build jajatime(minutes)
    _every_x_day: int = None  # of the year"

    _start_hr: int = None
    _start_minute: int = None
    _event_minutes: int = None

    def set_weekly_event(
        self,
        every_x_weeks: int,
        remainder_weeks: int,
        weekday: str,
        start_hr: int,
        start_minute: int,
        event_minutes: int,
    ):
        if every_x_weeks <= remainder_weeks:
            raise InvalidSuffFactUnitException(
                "remainder_weeks reqquires being at least 1 less than every_x_weeks"
            )

        self._set_every_x_weeks(every_x_weeks)
        self.set_x_remainder_weeks(remainder_weeks)
        self._set_start_hr(start_hr)
        self._set_start_minute(start_minute)
        self._set_event_minutes(event_minutes)
        self._set_weekday(weekday)
        self._clear_every_x_days()
        self._clear_every_x_months()
        self._clear_every_x_years()

    def set_days_event(
        self,
        every_x_days: int,
        remainder_days: int,
        start_hr: int,
        start_minute: int,
        event_minutes: int,
    ):
        if every_x_days <= remainder_days:
            raise InvalidSuffFactUnitException(
                "remainder_weeks reqquires being at least 1 less than every_x_weeks"
            )

        self._set_every_x_days(every_x_days)
        self.set_x_remainder_days(remainder_days)
        self._set_start_hr(start_hr)
        self._set_start_minute(start_minute)
        self._set_event_minutes(event_minutes)
        self._clear_every_x_weeks()
        self._clear_every_x_months()
        self._clear_every_x_years()

    def set_x_remainder_weeks(self, remainder_weeks: int):
        if remainder_weeks < 0:
            raise InvalidSuffFactUnitException("remainder_weeks reqquires being >= 0")
        self._x_week_remainder = remainder_weeks

    def set_x_remainder_days(self, remainder_days: int):
        if remainder_days < 0:
            raise InvalidSuffFactUnitException("remainder_weeks reqquires being >= 0")
        self._x_days_remainder = remainder_days

    def _set_every_x_days(
        self,
        every_x_days: int,
    ):
        self._every_x_days = every_x_days

    def _set_every_x_weeks(
        self,
        every_x_weeks: int,
    ):
        self._every_x_weeks = every_x_weeks

    def _clear_every_x_weeks(self):
        self._every_x_weeks = None

    def _clear_every_x_days(self):
        self._every_x_days = None

    def _clear_every_x_months(self):
        self._every_x_months = None

    def _clear_every_x_years(self):
        self._every_x_years = None

    def _set_start_hr(self, start_hr):
        self._start_hr = start_hr

    def _set_start_minute(self, start_minute):
        self._start_minute = start_minute

    def _set_event_minutes(self, event_minutes):
        self._event_minutes = event_minutes

    def _set_weekday(self, weekday: str):
        if weekday in {
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        }:
            self._weekday = weekday
            self._set_open_weekday()

    def _set_open_weekday(self):
        b = None
        m = 1440
        if self._weekday == "Sunday":
            b = 1 * m
        elif self._weekday == "Monday":
            b = 2 * m
        elif self._weekday == "Tuesday":
            b = 3 * m
        elif self._weekday == "Wednesday":
            b = 4 * m
        elif self._weekday == "Thursday":
            b = 5 * m
        elif self._weekday == "Friday":
            b = 6 * m
        elif self._weekday == "Saturday":
            b = 0 * m

        self._between_weekday_open = b

    def get_jajatime_open(self):
        x_open = None
        if self._every_x_weeks != None and self._x_week_remainder != None:
            x_open = (
                (self._x_week_remainder * 10080)
                + (self._start_hr * 60)
                + (self._start_minute)
            )
            self._set_open_weekday()
            x_open += self._between_weekday_open
        elif self._every_x_days != None and self._x_days_remainder != None:
            x_open = (
                (self._x_days_remainder * 1440)
                + (self._start_hr * 60)
                + (self._start_minute)
            )

        return x_open

    @property
    def jajatime_divisor(self):
        if self._every_x_weeks != None and self._x_week_remainder != None:
            return self._every_x_weeks * 10080
        elif self._every_x_days != None and self._x_days_remainder != None:
            return self._every_x_days * 1440

    @property
    def jajatime_open(self):
        return self.get_jajatime_open()

    @property
    def jajatime_nigh(self):
        return self.get_jajatime_open() + self._event_minutes


def _get_time_hreg_src_idea(c400_count: int):
    time = "time"
    min_text = "minutes"
    list_x = []
    list_x += _get_time_hreg_ced(local_root=time, tech=min_text, c400_count=c400_count)
    return list_x


def _get_time_hreg_ced(local_root: str, tech: str, c400_count: int):
    if tech == "days":
        m = 1
    elif tech == "hours":
        m = 24
    elif tech == "minutes":
        m = 1440

    rt = local_root
    tech_root = Road(f"{local_root},tech")
    jaja = "jajatime"
    st = f"{local_root},{jaja}"
    c4 = f"{tech_root},400 year cycle"
    day_road = f"{tech_root},day"
    week_road = f"{tech_root},week"
    c400 = c400_count

    list_x = [YB(n=jaja, b=0, c=146097 * c400_count * m, rr=local_root)]
    list_x.append(YB(mn=1, md=c400, mr=True, sr=c4, rr=st, n="400 year cycle"))
    list_x.append(YB(mn=1, md=210379680, mr=False, sr=c4, rr=st, n="400 year cycles"))
    list_x.append(YB(mn=1, md=1 * m, mr=False, sr=None, rr=st, n="days"))
    list_x.append(YB(mn=1, md=1022679.0, mr=True, sr=day_road, rr=st, n="day"))
    list_x.append(YB(mn=1, md=7 * m, mr=False, sr=None, rr=st, n="weeks"))
    list_x.append(YB(mn=1, md=146097.0, mr=True, sr=week_road, rr=st, n="week"))
    list_x.append(YB(mn=1, md=1, rr=st, n="years"))

    list_x += _get_time_hreg_years(local_root=rt, jajatime=jaja)

    list_x += _get_time_hreg_cycle400(local_root=rt, multipler=m)
    list_x += _get_time_hreg_4year_noleap(local_root=rt, multipler=m)
    list_x += _get_time_hreg_4year_withleap(local_root=rt, multipler=m)
    list_x += _get_time_hreg_365year(local_root=rt, multipler=m)
    list_x += _get_time_hreg_366year(local_root=rt, multipler=m)
    list_x += _get_time_hreg_month(local_root=rt, multipler=m)
    list_x += _get_time_hreg_day(local_root=rt, multipler=m)
    list_x += _get_time_hreg_hour(local_root=rt, multipler=m)
    list_x += _get_time_hreg_weekday_idea(local_root=rt, multipler=m, jajatime=jaja)

    return list_x


def _get_time_hreg_years(local_root: str, jajatime: str):
    years = "years"
    jaja_r = Road(f"{local_root},{jajatime},{years}")
    yrs_d = [
        [2010, 1057158720, 1057684320],
        [2011, 1057684320, 1058209920],
        [2012, 1058209920, 1058736960],
        [2013, 1058736960, 1059262560],
        [2014, 1059262560, 1059788160],
        [2015, 1059788160, 1060313760],
        [2016, 1060313760, 1060840800],
        [2017, 1060840800, 1061366400],
        [2018, 1061366400, 1061892000],
        [2019, 1061892000, 1062417600],
        [2020, 1062417600, 1062944640],
        [2021, 1062944640, 1063470240],
        [2022, 1063470240, 1063995840],
        [2023, 1063995840, 1064521440],
        [2024, 1064521440, 1065048480],
        [2025, 1065048480, 1065574080],
        [2026, 1065574080, 1066099680],
        [2027, 1066099680, 1066625280],
        [2028, 1066625280, 1067152320],
        [2029, 1067152320, 1067677920],
        [2030, 1067677920, 1068203520],
    ]
    hreg_list = []
    for yr_x in yrs_d:
        yr_t = yr_x[0]
        yr_min = yr_x[1]
        yr_max = yr_x[2]
        nm_x = f"{yr_t} by minute"
        nm_y = YB(n=nm_x, rr=jaja_r, b=yr_min, c=yr_max)
        hreg_list.append(nm_y)
        m_r = Road(f"{jaja_r},{nm_x}")
        map_x = "morph"
        m_y = YB(n=map_x, rr=m_r, a=-yr_min, md=yr_max - yr_min)
        hreg_list.append(m_y)
        f_n = f"{yr_t} as year"
        f_r = Road(f"{m_r},{map_x}")
        f_y = YB(n=f_n, rr=f_r, a=yr_t)
        hreg_list.append(f_y)

    return hreg_list


def _get_time_hreg_weekday_idea(local_root: str, multipler: int, jajatime: str):
    m = multipler
    week = "week"
    nr = f"{local_root},{jajatime},week"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=week, b=0 * m, c=7 * m, nr=nr, rr=tech_root)]
    week_road = f"{tech_root},{week}"
    hreg_list.append(YB(b=1 * m, c=2 * m, rr=week_road, n="Sunday"))
    hreg_list.append(YB(b=2 * m, c=3 * m, rr=week_road, n="Monday"))
    hreg_list.append(YB(b=3 * m, c=4 * m, rr=week_road, n="Tuesday"))
    hreg_list.append(YB(b=4 * m, c=5 * m, rr=week_road, n="Wednesday"))
    hreg_list.append(YB(b=5 * m, c=6 * m, rr=week_road, n="Thursday"))
    hreg_list.append(YB(b=6 * m, c=7 * m, rr=week_road, n="Friday"))
    hreg_list.append(YB(b=0 * m, c=1 * m, rr=week_road, n="Saturday"))
    return hreg_list


def _get_time_hreg_cycle400(local_root: str, multipler: int):
    m = multipler
    tech = "400 year cycle"
    nr_400 = f"{local_root},jajatime,{tech}"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, b=0, c=146097 * m, nr=nr_400, rr=tech_root)]
    rt = f"{tech_root},{tech}"
    yr4wl = "4year with leap"
    yr4ol = "4year wo leap"
    l_yr4wl = f"{tech_root},{yr4wl}"
    l_yr4ol = f"{tech_root},{yr4ol}"

    node_0_100 = "0-100-25 leap years"
    rr_0_100 = f"{rt},{node_0_100}"
    hreg_list.append(YB(b=0, c=36525 * m, rr=rt, n=node_0_100))
    hreg_list.append(YB(mn=1, md=25, mr=True, sr=l_yr4wl, rr=rr_0_100, n=yr4wl))
    node_1_4 = "100-104-0 leap years"
    rr_1_4 = f"{rt},{node_1_4}"
    hreg_list.append(YB(b=36525 * m, c=37985 * m, rr=rt, n=node_1_4))
    hreg_list.append(YB(mn=1, md=1, mr=True, sr=l_yr4ol, rr=rr_1_4, n=yr4ol))
    node_1_96 = "104-200-24 leap years"
    rr_1_96 = f"{rt},{node_1_96}"
    hreg_list.append(YB(b=37985 * m, c=73049 * m, rr=rt, n=node_1_96))
    hreg_list.append(YB(mn=1, md=24, mr=True, sr=l_yr4wl, rr=rr_1_96, n=yr4wl))
    node_2_4 = "200-204-0 leap years"
    rr_2_4 = f"{rt},{node_2_4}"
    hreg_list.append(YB(b=73049 * m, c=74509 * m, rr=rt, n=node_2_4))
    hreg_list.append(YB(mn=1, md=1, mr=True, sr=l_yr4ol, rr=rr_2_4, n=yr4ol))
    node_2_96 = "204-300-24 leap years"
    rr_2_96 = f"{rt},{node_2_96}"
    hreg_list.append(YB(b=74509 * m, c=109573 * m, rr=rt, n=node_2_96))
    hreg_list.append(YB(mn=1, md=24, mr=True, sr=l_yr4wl, rr=rr_2_96, n=yr4wl))
    node_3_4 = "300-304-0 leap years"
    rr_3_4 = f"{rt},{node_3_4}"
    hreg_list.append(YB(b=109573 * m, c=111033 * m, rr=rt, n=node_3_4))
    hreg_list.append(YB(mn=1, md=1, mr=True, sr=l_yr4ol, rr=rr_3_4, n=yr4ol))
    node_3_96 = "304-400-24 leap years"
    rr_3_96 = f"{rt},{node_3_96}"
    hreg_list.append(YB(b=111033 * m, c=146097 * m, rr=rt, n=node_3_96))
    hreg_list.append(YB(mn=1, md=24, mr=True, sr=l_yr4wl, rr=rr_3_96, n=yr4wl))
    return hreg_list


def _get_time_hreg_4year_noleap(local_root: str, multipler: int):
    m = multipler
    tech = "4year wo leap"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, b=0, c=1460 * m, rr=tech_root)]
    rt = f"{tech_root},{tech}"
    y365 = f"{tech_root},365 year"
    node_1_4 = "1-year"
    hreg_list.append(YB(b=0, c=365 * m, rr=rt, sr=y365, n=node_1_4))
    node_1_96 = "2-year"
    hreg_list.append(YB(b=365 * m, c=730 * m, rr=rt, sr=y365, n=node_1_96))
    node_2_4 = "3-year"
    hreg_list.append(YB(b=730 * m, c=1095 * m, rr=rt, sr=y365, n=node_2_4))
    node_2_96 = "4-year"
    hreg_list.append(YB(b=1095 * m, c=1460 * m, rr=rt, sr=y365, n=node_2_96))
    return hreg_list


def _get_time_hreg_4year_withleap(local_root: str, multipler: int):
    m = multipler
    tech = "4year with leap"

    c400 = "400 year cycle"
    node_0_100 = "0-100-25 leap years"
    tech_root = Road(f"{local_root},tech")
    nr_yr4wl = f"{tech_root},{c400},{node_0_100},{tech}"
    hreg_list = [YB(n=tech, rr=tech_root, nr=nr_yr4wl)]

    hreg_list = [YB(n=tech, rr=tech_root, nr=nr_yr4wl)]
    rt = f"{tech_root},{tech}"
    y365 = f"{tech_root},365 year"
    y366 = f"{tech_root},366 year"

    node_1_4 = "1-year"
    hreg_list.append(YB(b=0, c=366 * m, rr=rt, sr=y366, n=node_1_4))
    node_1_96 = "2-year"
    hreg_list.append(YB(b=366 * m, c=731 * m, rr=rt, sr=y365, n=node_1_96))
    node_2_4 = "3-year"
    hreg_list.append(YB(b=731 * m, c=1096 * m, rr=rt, sr=y365, n=node_2_4))
    node_2_96 = "4-year"
    hreg_list.append(YB(b=1096 * m, c=1461 * m, rr=rt, sr=y365, n=node_2_96))
    return hreg_list


def _get_time_hreg_366year(local_root: str, multipler: int):
    m = multipler
    tech = "366 year"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, b=0, c=366 * m, rr=tech_root)]
    rt = f"{tech_root},{tech}"

    Jan = "Jan"
    Feb29 = "Feb29"
    Mar = "Mar"
    Apr = "Apr"
    May = "May"
    Jun = "Jun"
    Jul = "Jul"
    Aug = "Aug"
    Sep = "Sep"
    Oct = "Oct"
    Nov = "Nov"
    Dec = "Dec"

    sr_m = "month"
    r_Jan = f"{tech_root},{sr_m},{Jan}"
    r_Feb29 = f"{tech_root},{sr_m},{Feb29}"
    r_Mar = f"{tech_root},{sr_m},{Mar}"
    r_Apr = f"{tech_root},{sr_m},{Apr}"
    r_May = f"{tech_root},{sr_m},{May}"
    r_Jun = f"{tech_root},{sr_m},{Jun}"
    r_Jul = f"{tech_root},{sr_m},{Jul}"
    r_Aug = f"{tech_root},{sr_m},{Aug}"
    r_Sep = f"{tech_root},{sr_m},{Sep}"
    r_Oct = f"{tech_root},{sr_m},{Oct}"
    r_Nov = f"{tech_root},{sr_m},{Nov}"
    r_Dec = f"{tech_root},{sr_m},{Dec}"

    hreg_list.append(YB(b=0 * m, c=31 * m, rr=rt, sr=r_Jan, n=f"1-{Jan}"))
    hreg_list.append(YB(b=31 * m, c=60 * m, rr=rt, sr=r_Feb29, n=f"2-{Feb29}"))
    hreg_list.append(YB(b=60 * m, c=91 * m, rr=rt, sr=r_Mar, n=f"3-{Mar}"))
    hreg_list.append(YB(b=91 * m, c=121 * m, rr=rt, sr=r_Apr, n=f"4-{Apr}"))
    hreg_list.append(YB(b=121 * m, c=152 * m, rr=rt, sr=r_May, n=f"5-{May}"))
    hreg_list.append(YB(b=152 * m, c=182 * m, rr=rt, sr=r_Jun, n=f"6-{Jun}"))
    hreg_list.append(YB(b=182 * m, c=213 * m, rr=rt, sr=r_Jul, n=f"7-{Jul}"))
    hreg_list.append(YB(b=213 * m, c=244 * m, rr=rt, sr=r_Aug, n=f"8-{Aug}"))
    hreg_list.append(YB(b=244 * m, c=274 * m, rr=rt, sr=r_Sep, n=f"9-{Sep}"))
    hreg_list.append(YB(b=274 * m, c=305 * m, rr=rt, sr=r_Oct, n=f"10-{Oct}"))
    hreg_list.append(YB(b=305 * m, c=335 * m, rr=rt, sr=r_Nov, n=f"11-{Nov}"))
    hreg_list.append(YB(b=335 * m, c=366 * m, rr=rt, sr=r_Dec, n=f"12-{Dec}"))

    return hreg_list


def _get_time_hreg_365year(local_root: str, multipler: int):
    m = multipler
    tech = "365 year"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, b=0, c=365 * m, rr=tech_root)]
    rt = f"{tech_root},{tech}"

    Jan = "Jan"
    Feb28 = "Feb28"
    Mar = "Mar"
    Apr = "Apr"
    May = "May"
    Jun = "Jun"
    Jul = "Jul"
    Aug = "Aug"
    Sep = "Sep"
    Oct = "Oct"
    Nov = "Nov"
    Dec = "Dec"

    sr_m = "month"
    r_Jan = f"{tech_root},{sr_m},{Jan}"
    r_Feb28 = f"{tech_root},{sr_m},{Feb28}"
    r_Mar = f"{tech_root},{sr_m},{Mar}"
    r_Apr = f"{tech_root},{sr_m},{Apr}"
    r_May = f"{tech_root},{sr_m},{May}"
    r_Jun = f"{tech_root},{sr_m},{Jun}"
    r_Jul = f"{tech_root},{sr_m},{Jul}"
    r_Aug = f"{tech_root},{sr_m},{Aug}"
    r_Sep = f"{tech_root},{sr_m},{Sep}"
    r_Oct = f"{tech_root},{sr_m},{Oct}"
    r_Nov = f"{tech_root},{sr_m},{Nov}"
    r_Dec = f"{tech_root},{sr_m},{Dec}"

    hreg_list.append(YB(b=0 * m, c=31 * m, rr=rt, sr=r_Jan, n=f"1-{Jan}"))
    hreg_list.append(YB(b=31 * m, c=59 * m, rr=rt, sr=r_Feb28, n=f"2-{Feb28}"))
    hreg_list.append(YB(b=59 * m, c=90 * m, rr=rt, sr=r_Mar, n=f"3-{Mar}"))
    hreg_list.append(YB(b=90 * m, c=120 * m, rr=rt, sr=r_Apr, n=f"4-{Apr}"))
    hreg_list.append(YB(b=120 * m, c=151 * m, rr=rt, sr=r_May, n=f"5-{May}"))
    hreg_list.append(YB(b=151 * m, c=181 * m, rr=rt, sr=r_Jun, n=f"6-{Jun}"))
    hreg_list.append(YB(b=181 * m, c=212 * m, rr=rt, sr=r_Jul, n=f"7-{Jul}"))
    hreg_list.append(YB(b=212 * m, c=243 * m, rr=rt, sr=r_Aug, n=f"8-{Aug}"))
    hreg_list.append(YB(b=243 * m, c=273 * m, rr=rt, sr=r_Sep, n=f"9-{Sep}"))
    hreg_list.append(YB(b=273 * m, c=304 * m, rr=rt, sr=r_Oct, n=f"10-{Oct}"))
    hreg_list.append(YB(b=304 * m, c=334 * m, rr=rt, sr=r_Nov, n=f"11-{Nov}"))
    hreg_list.append(YB(b=334 * m, c=365 * m, rr=rt, sr=r_Dec, n=f"12-{Dec}"))

    return hreg_list


def _get_time_hreg_month(local_root: str, multipler: int):
    m = multipler
    tech = "month"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, rr=tech_root)]
    rt = f"{tech_root},{tech}"

    Jan = "Jan"
    Feb28 = "Feb28"
    Feb29 = "Feb29"
    Mar = "Mar"
    Apr = "Apr"
    May = "May"
    Jun = "Jun"
    Jul = "Jul"
    Aug = "Aug"
    Sep = "Sep"
    Oct = "Oct"
    Nov = "Nov"
    Dec = "Dec"

    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Jan))
    hreg_list.append(YB(b=0, c=28 * m, rr=rt, n=Feb28))
    hreg_list.append(YB(b=0, c=29 * m, rr=rt, n=Feb29))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Mar))
    hreg_list.append(YB(b=0, c=30 * m, rr=rt, n=Apr))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=May))
    hreg_list.append(YB(b=0, c=30 * m, rr=rt, n=Jun))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Jul))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Aug))
    hreg_list.append(YB(b=0, c=30 * m, rr=rt, n=Sep))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Oct))
    hreg_list.append(YB(b=0, c=30 * m, rr=rt, n=Nov))
    hreg_list.append(YB(b=0, c=31 * m, rr=rt, n=Dec))

    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Jan}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Feb28}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Feb29}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Mar}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Apr}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{May}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Jun}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Jul}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Aug}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Sep}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Oct}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Nov}", n="days"))
    hreg_list.append(YB(mn=1, md=1440, mr=True, rr=f"{rt},{Dec}", n="days"))

    return hreg_list


def _get_time_hreg_day(local_root: str, multipler: int):
    if multipler not in (1, 60):
        multipler = 60
    m = multipler
    tech = "day"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, rr=tech_root, b=0, c=24 * m)]
    rt = f"{tech_root},{tech}"
    hr = f"{tech_root},hour"
    hreg_list.append(YB(b=0 * m, c=1 * m, rr=rt, sr=hr, n="0-12am"))
    hreg_list.append(YB(b=1 * m, c=2 * m, rr=rt, sr=hr, n="1-1am"))
    hreg_list.append(YB(b=2 * m, c=3 * m, rr=rt, sr=hr, n="2-2am"))
    hreg_list.append(YB(b=3 * m, c=4 * m, rr=rt, sr=hr, n="3-3am"))
    hreg_list.append(YB(b=4 * m, c=5 * m, rr=rt, sr=hr, n="4-4am"))
    hreg_list.append(YB(b=5 * m, c=6 * m, rr=rt, sr=hr, n="5-5am"))
    hreg_list.append(YB(b=6 * m, c=7 * m, rr=rt, sr=hr, n="6-6am"))
    hreg_list.append(YB(b=7 * m, c=8 * m, rr=rt, sr=hr, n="7-7am"))
    hreg_list.append(YB(b=8 * m, c=9 * m, rr=rt, sr=hr, n="8-8am"))
    hreg_list.append(YB(b=9 * m, c=10 * m, rr=rt, sr=hr, n="9-9am"))
    hreg_list.append(YB(b=10 * m, c=11 * m, rr=rt, sr=hr, n="10-10am"))
    hreg_list.append(YB(b=11 * m, c=12 * m, rr=rt, sr=hr, n="11-11am"))
    hreg_list.append(YB(b=12 * m, c=13 * m, rr=rt, sr=hr, n="12-12pm"))
    hreg_list.append(YB(b=13 * m, c=14 * m, rr=rt, sr=hr, n="13-1pm"))
    hreg_list.append(YB(b=14 * m, c=15 * m, rr=rt, sr=hr, n="14-2pm"))
    hreg_list.append(YB(b=15 * m, c=16 * m, rr=rt, sr=hr, n="15-3pm"))
    hreg_list.append(YB(b=16 * m, c=17 * m, rr=rt, sr=hr, n="16-4pm"))
    hreg_list.append(YB(b=17 * m, c=18 * m, rr=rt, sr=hr, n="17-5pm"))
    hreg_list.append(YB(b=18 * m, c=19 * m, rr=rt, sr=hr, n="18-6pm"))
    hreg_list.append(YB(b=19 * m, c=20 * m, rr=rt, sr=hr, n="19-7pm"))
    hreg_list.append(YB(b=20 * m, c=21 * m, rr=rt, sr=hr, n="20-8pm"))
    hreg_list.append(YB(b=21 * m, c=22 * m, rr=rt, sr=hr, n="21-9pm"))
    hreg_list.append(YB(b=22 * m, c=23 * m, rr=rt, sr=hr, n="22-10pm"))
    hreg_list.append(YB(b=23 * m, c=24 * m, rr=rt, sr=hr, n="23-11pm"))
    return hreg_list


def _get_time_hreg_ced_timelines(local_root: str):
    year = "years"
    hreg_list = [YB(n=year, b=0, c=400 * 7, rr=local_root)]
    year_road = f"{local_root},{year}"
    hreg_list.append(YB(n="100 years war", b=1337, c=1453, rr=year_road))
    # hreg_list.append(
    #     YB(n="timline by hours", b=0, c=146097 * 7 * 24, rr=local_root)
    # )
    # hreg_list.append(
    #     YB(n="timline by minutes", b=0, c=146097 * 7 * 24 * 60, rr=local_root)
    # )
    return hreg_list


def _get_time_hreg_hour(local_root: str, multipler: int):
    if multipler != 1:
        multipler = 1
    m = multipler
    tech = "hour"
    tech_root = Road(f"{local_root},tech")
    hreg_list = [YB(n=tech, rr=tech_root, b=0, c=60 * m)]
    rt = f"{tech_root},{tech}"
    # minute = "minute"
    # hr = f"{local_root},{minute}"
    hr = None
    hreg_list.append(YB(b=0 * m, c=1 * m, rr=rt, n="0-:00"))
    hreg_list.append(YB(b=1 * m, c=2 * m, rr=rt, n="1-:01"))
    hreg_list.append(YB(b=2 * m, c=3 * m, rr=rt, n="2-:02"))
    hreg_list.append(YB(b=3 * m, c=4 * m, rr=rt, n="3-:03"))
    hreg_list.append(YB(b=4 * m, c=5 * m, rr=rt, n="4-:04"))
    hreg_list.append(YB(b=5 * m, c=6 * m, rr=rt, n="5-:05"))
    hreg_list.append(YB(b=6 * m, c=7 * m, rr=rt, n="6-:06"))
    hreg_list.append(YB(b=7 * m, c=8 * m, rr=rt, n="7-:07"))
    hreg_list.append(YB(b=8 * m, c=9 * m, rr=rt, n="8-:08"))
    hreg_list.append(YB(b=9 * m, c=10 * m, rr=rt, n="9-:09"))
    hreg_list.append(YB(b=10 * m, c=11 * m, rr=rt, n="10-:10"))
    hreg_list.append(YB(b=11 * m, c=12 * m, rr=rt, n="11-:11"))
    hreg_list.append(YB(b=12 * m, c=13 * m, rr=rt, n="12-:12"))
    hreg_list.append(YB(b=13 * m, c=14 * m, rr=rt, n="13-:13"))
    hreg_list.append(YB(b=14 * m, c=15 * m, rr=rt, n="14-:14"))
    hreg_list.append(YB(b=15 * m, c=16 * m, rr=rt, n="15-:15"))
    hreg_list.append(YB(b=16 * m, c=17 * m, rr=rt, n="16-:16"))
    hreg_list.append(YB(b=17 * m, c=18 * m, rr=rt, n="17-:17"))
    hreg_list.append(YB(b=18 * m, c=19 * m, rr=rt, n="18-:18"))
    hreg_list.append(YB(b=19 * m, c=20 * m, rr=rt, n="19-:19"))
    hreg_list.append(YB(b=20 * m, c=21 * m, rr=rt, n="20-:20"))
    hreg_list.append(YB(b=21 * m, c=22 * m, rr=rt, n="21-:21"))
    hreg_list.append(YB(b=22 * m, c=23 * m, rr=rt, n="22-:22"))
    hreg_list.append(YB(b=23 * m, c=24 * m, rr=rt, n="23-:23"))
    hreg_list.append(YB(b=24 * m, c=25 * m, rr=rt, n="24-:24"))
    hreg_list.append(YB(b=25 * m, c=26 * m, rr=rt, n="25-:25"))
    hreg_list.append(YB(b=26 * m, c=27 * m, rr=rt, n="26-:26"))
    hreg_list.append(YB(b=27 * m, c=28 * m, rr=rt, n="27-:27"))
    hreg_list.append(YB(b=28 * m, c=29 * m, rr=rt, n="28-:28"))
    hreg_list.append(YB(b=29 * m, c=30 * m, rr=rt, n="29-:29"))
    hreg_list.append(YB(b=30 * m, c=31 * m, rr=rt, n="30-:30"))
    hreg_list.append(YB(b=31 * m, c=32 * m, rr=rt, n="31-:31"))
    hreg_list.append(YB(b=32 * m, c=33 * m, rr=rt, n="32-:32"))
    hreg_list.append(YB(b=33 * m, c=34 * m, rr=rt, n="33-:33"))
    hreg_list.append(YB(b=34 * m, c=35 * m, rr=rt, n="34-:34"))
    hreg_list.append(YB(b=35 * m, c=36 * m, rr=rt, n="35-:35"))
    hreg_list.append(YB(b=36 * m, c=37 * m, rr=rt, n="36-:36"))
    hreg_list.append(YB(b=37 * m, c=38 * m, rr=rt, n="37-:37"))
    hreg_list.append(YB(b=38 * m, c=39 * m, rr=rt, n="38-:38"))
    hreg_list.append(YB(b=39 * m, c=40 * m, rr=rt, n="39-:39"))
    hreg_list.append(YB(b=40 * m, c=41 * m, rr=rt, n="40-:40"))
    hreg_list.append(YB(b=41 * m, c=42 * m, rr=rt, n="41-:41"))
    hreg_list.append(YB(b=42 * m, c=43 * m, rr=rt, n="42-:42"))
    hreg_list.append(YB(b=43 * m, c=44 * m, rr=rt, n="43-:43"))
    hreg_list.append(YB(b=44 * m, c=45 * m, rr=rt, n="44-:44"))
    hreg_list.append(YB(b=45 * m, c=46 * m, rr=rt, n="45-:45"))
    hreg_list.append(YB(b=46 * m, c=47 * m, rr=rt, n="46-:46"))
    hreg_list.append(YB(b=47 * m, c=48 * m, rr=rt, n="47-:47"))
    hreg_list.append(YB(b=48 * m, c=49 * m, rr=rt, n="48-:48"))
    hreg_list.append(YB(b=49 * m, c=50 * m, rr=rt, n="49-:49"))
    hreg_list.append(YB(b=50 * m, c=51 * m, rr=rt, n="50-:50"))
    hreg_list.append(YB(b=51 * m, c=52 * m, rr=rt, n="51-:51"))
    hreg_list.append(YB(b=52 * m, c=53 * m, rr=rt, n="52-:52"))
    hreg_list.append(YB(b=53 * m, c=54 * m, rr=rt, n="53-:53"))
    hreg_list.append(YB(b=54 * m, c=55 * m, rr=rt, n="54-:54"))
    hreg_list.append(YB(b=55 * m, c=56 * m, rr=rt, n="55-:55"))
    hreg_list.append(YB(b=56 * m, c=57 * m, rr=rt, n="56-:56"))
    hreg_list.append(YB(b=57 * m, c=58 * m, rr=rt, n="57-:57"))
    hreg_list.append(YB(b=58 * m, c=59 * m, rr=rt, n="58-:58"))
    hreg_list.append(YB(b=59 * m, c=60 * m, rr=rt, n="59-59"))
    return hreg_list


def get_jajatime_legible_from_dt(dt: datetime) -> str:
    weekday_text = dt.strftime("%A")
    monthhandle_text = dt.strftime("%B")
    monthday_text = get_number_with_letter_ending(int(dt.strftime("%d")))
    year_text = dt.strftime("%Y")
    hour_int = int(dt.strftime("%H"))
    min_int = int(dt.strftime("%M"))
    min1440 = (hour_int * 60) + min_int
    return f"{weekday_text[:3]} {monthhandle_text[:3]} {monthday_text}, {year_text} at {convert1440toReadableTime(min1440)}"


def convert1440toHHMM(min1440: int):
    x_open_minutes = (
        f"0{min1440 % 60:.0f}" if min1440 % 60 < 10 else f"{min1440 % 60:.0f}"
    )
    return f"{min1440 // 60:.0f}:{x_open_minutes}"


def convert1440toReadableTime(min1440: int):
    x_open_minutes = (
        f"0{min1440 % 60:.0f}" if min1440 % 60 < 10 else f"{min1440 % 60:.0f}"
    )
    open_24hr = int(f"{min1440 // 60:.0f}")
    open_12hr = ""
    am_pm = ""
    if min1440 < 720:
        am_pm = "am"
        open_12hr = open_24hr
    else:
        am_pm = "pm"
        open_12hr = open_24hr - 12

    if open_24hr == 0:
        open_12hr = 12

    if x_open_minutes == "00":
        return f"{open_12hr}{am_pm}"
    else:
        return f"{open_12hr}:{x_open_minutes}{am_pm}"


def get_time_min_from_dt(dt: datetime) -> float:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_delta = dt - ce_src
    return round(min_time_delta.total_seconds() / 60) + 527040


def get_24hr():
    return [""] + [str(x) for x in range(24)]


def get_60min():
    return [""] + [str(x) for x in range(60)]


def get_number_with_letter_ending(num: int) -> str:
    tens_digit = num % 100
    singles_digit = num % 10
    if tens_digit in [11, 12, 13] or singles_digit not in [1, 2, 3]:
        return f"{num}th"
    elif singles_digit == 1:
        return f"{num}st"
    elif singles_digit == 2:
        return f"{num}nd"
    else:
        return f"{num}rd"
