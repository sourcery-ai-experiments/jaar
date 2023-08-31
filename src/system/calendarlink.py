from dataclasses import dataclass


class InvalidCalendarLinkException(Exception):
    pass


@dataclass
class CalendarLink:
    calendar_desc: str
    link_type: str = None
    weight: float = None

    def set_link_type(self, link_type: str):
        if link_type not in (list(get_calendarlink_types())):
            raise InvalidCalendarLinkException(
                f"Calendarlink '{self.calendar_desc}' cannot have type '{link_type}'."
            )
        self.link_type = link_type

    def set_weight(self, weight: float):
        self.weight = weight

    def get_dict(self):
        return {
            "calendar_desc": self.calendar_desc,
            "link_type": self.link_type,
            "weight": self.weight,
        }


def calendarlink_shop(
    calendar_desc: str, link_type: str = None, weight: float = None
) -> CalendarLink:
    if link_type is None:
        link_type = "blind_trust"
    if weight is None:
        weight = 1
    sl = CalendarLink(calendar_desc=calendar_desc)
    sl.set_link_type(link_type=link_type)
    sl.set_weight(weight=weight)
    return sl


def get_calendar_from_calendars_dirlink_from_dict(x_dict: dict) -> CalendarLink:
    calendar_desc_text = "calendar_desc"
    link_type_text = "link_type"
    weight_text = "weight"
    return calendarlink_shop(
        calendar_desc=x_dict[calendar_desc_text],
        link_type=x_dict[link_type_text],
        weight=x_dict[weight_text],
    )


def get_calendarlink_types() -> dict[str:None]:
    return {"blind_trust": None, "bond_filter": None, "tributary": None, "ignore": None}
