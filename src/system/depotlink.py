from dataclasses import dataclass


class InvalidCalendarLinkException(Exception):
    pass


@dataclass
class CalendarLink:
    calendar_owner: str
    depotlink_type: str = None
    weight: float = None

    def set_depotlink_type(self, depotlink_type: str):
        if depotlink_type not in (list(get_depotlink_types())):
            raise InvalidCalendarLinkException(
                f"Calendarlink '{self.calendar_owner}' cannot have type '{depotlink_type}'."
            )
        self.depotlink_type = depotlink_type

    def set_weight(self, weight: float):
        self.weight = weight

    def get_dict(self):
        return {
            "calendar_owner": self.calendar_owner,
            "depotlink_type": self.depotlink_type,
            "weight": self.weight,
        }


def depotlink_shop(
    calendar_owner: str, depotlink_type: str = None, weight: float = None
) -> CalendarLink:
    if depotlink_type is None:
        depotlink_type = "blind_trust"
    if weight is None:
        weight = 1
    sl = CalendarLink(calendar_owner=calendar_owner)
    sl.set_depotlink_type(depotlink_type=depotlink_type)
    sl.set_weight(weight=weight)
    return sl


def get_calendar_from_calendars_dirlink_from_dict(x_dict: dict) -> CalendarLink:
    calendar_owner_text = "calendar_owner"
    depotlink_type_text = "depotlink_type"
    weight_text = "weight"
    return depotlink_shop(
        calendar_owner=x_dict[calendar_owner_text],
        depotlink_type=x_dict[depotlink_type_text],
        weight=x_dict[weight_text],
    )


def get_depotlink_types() -> dict[str:None]:
    return {"blind_trust": None, "bond_filter": None, "tributary": None, "ignore": None}
