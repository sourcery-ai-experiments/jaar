from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop, AgendaUnit


def casa_text() -> str:
    return "casa"


def cook_text() -> str:
    return "cook"


def eat_text() -> str:
    return "eat"


def hungry_text() -> str:
    return "hungry"


def full_text() -> str:
    return "full"


def clean_text():
    return "clean"


def run_text():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), casa_text())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_text())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_text())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_text())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_text())


def clean_road() -> RoadUnit:
    return create_road(casa_road(), clean_text())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_text())


def get_example_zia_speaker() -> AgendaUnit:
    zia_text = "Zia"
    zia_speaker = agendaunit_shop(zia_text)
    zia_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    zia_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    yao_text = "Yao"
    zia_speaker.add_partyunit(yao_text, debtor_weight=12)
    cook_ideaunit = zia_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_speaker.edit_idea_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    zia_speaker.set_belief(eat_road(), full_road())
    zia_speaker.set_party_pool(100)
    return zia_speaker


def get_example_yao_speaker() -> AgendaUnit:
    yao_text = "Yao"
    zia_text = "Zia"
    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.add_partyunit(yao_text, debtor_weight=12)
    yao_speaker.add_partyunit(zia_text, debtor_weight=36)
    yao_speaker.set_party_pool(100)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_speaker.edit_idea_attr(
        cook_road(), reason_base=eat_road(), reason_premise=hungry_road()
    )
    yao_speaker.set_belief(eat_road(), hungry_road())
    return yao_speaker
