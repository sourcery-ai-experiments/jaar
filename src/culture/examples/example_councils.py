from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    ideacore_shop,
)
from src.agenda.examples.example_agendas import get_agenda_assignment_laundry_example1
from src.culture.council import councilunit_shop, CouncilUnit
from src.culture.examples.council_env_kit import get_temp_culture_handle

from random import randrange


def get_1node_agenda() -> AgendaUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(_healer=a_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> AgendaUnit:
    healer_text = "J"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    a_text = "A"
    idea_a = ideacore_shop(_label=a_text)
    x_agenda.add_idea(idea_kid=idea_a, pad=get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_2node_agenda() -> AgendaUnit:
    healer_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_b = ideacore_shop(_label=b_text)
    x_agenda.add_idea(idea_kid=idea_b, pad=get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> AgendaUnit:
    a_text = "A"
    a_road = a_text
    x_agenda = agendaunit_shop(_healer=a_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    b_text = "B"
    idea_b = ideacore_shop(_label=b_text)
    c_text = "C"
    idea_c = ideacore_shop(_label=c_text)
    x_agenda.add_idea(idea_kid=idea_b, pad=a_road)
    x_agenda.add_idea(idea_kid=idea_c, pad=a_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_D_E_F_agenda() -> AgendaUnit:
    d_text = "D"
    d_road = d_text
    x_agenda = agendaunit_shop(_healer=d_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    b_text = "E"
    idea_b = ideacore_shop(_label=b_text)
    c_text = "F"
    idea_c = ideacore_shop(_label=c_text)
    x_agenda.add_idea(idea_kid=idea_b, pad=d_road)
    x_agenda.add_idea(idea_kid=idea_c, pad=d_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_6node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop(_healer="A")
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_b = ideacore_shop(_label="B")
    idea_c = ideacore_shop(_label="C")
    idea_d = ideacore_shop(_label="D")
    idea_e = ideacore_shop(_label="E")
    idea_f = ideacore_shop(_label="F")
    x_agenda.add_idea(idea_kid=idea_b, pad="A")
    x_agenda.add_idea(idea_kid=idea_c, pad="A")
    x_agenda.add_idea(idea_kid=idea_d, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_e, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_f, pad="A,C")
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeInsertH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop(_healer="A")
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_b = ideacore_shop(_label="B")
    idea_c = ideacore_shop(_label="C")
    idea_h = ideacore_shop(_label="H")
    idea_d = ideacore_shop(_label="D")
    idea_e = ideacore_shop(_label="E")
    idea_f = ideacore_shop(_label="F")
    x_agenda.add_idea(idea_kid=idea_b, pad="A")
    x_agenda.add_idea(idea_kid=idea_c, pad="A")
    x_agenda.add_idea(idea_kid=idea_e, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_f, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_h, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_d, pad="A,C,H")
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_5nodeHG_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop(_healer="A")
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_b = ideacore_shop(_label="B")
    idea_c = ideacore_shop(_label="C")
    idea_h = ideacore_shop(_label="H")
    idea_g = ideacore_shop(_label="G")
    x_agenda.add_idea(idea_kid=idea_b, pad="A")
    x_agenda.add_idea(idea_kid=idea_c, pad="A")
    x_agenda.add_idea(idea_kid=idea_h, pad="A,C")
    x_agenda.add_idea(idea_kid=idea_g, pad="A,C")
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRoot_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop(_healer="J")
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_a = ideacore_shop(_label="A")
    idea_b = ideacore_shop(_label="B")
    idea_c = ideacore_shop(_label="C")
    idea_d = ideacore_shop(_label="D")
    idea_e = ideacore_shop(_label="E")
    idea_f = ideacore_shop(_label="F")
    x_agenda.add_idea(idea_kid=idea_a, pad="J")
    x_agenda.add_idea(idea_kid=idea_b, pad="J,A")
    x_agenda.add_idea(idea_kid=idea_c, pad="J,A")
    x_agenda.add_idea(idea_kid=idea_d, pad="J,A,C")
    x_agenda.add_idea(idea_kid=idea_e, pad="J,A,C")
    x_agenda.add_idea(idea_kid=idea_f, pad="J,A,C")
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRootWithH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop(_healer="J")
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_a = ideacore_shop(_label="A")
    idea_b = ideacore_shop(_label="B")
    idea_c = ideacore_shop(_label="C")
    idea_e = ideacore_shop(_label="E")
    idea_f = ideacore_shop(_label="F")
    idea_h = ideacore_shop(_label="H")
    x_agenda.add_idea(idea_kid=idea_a, pad="J")
    x_agenda.add_idea(idea_kid=idea_b, pad="J,A")
    x_agenda.add_idea(idea_kid=idea_c, pad="J,A")
    x_agenda.add_idea(idea_kid=idea_e, pad="J,A,C")
    x_agenda.add_idea(idea_kid=idea_f, pad="J,A,C")
    x_agenda.add_idea(idea_kid=idea_h, pad="J,A,C")
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_healer_2agenda(env_dir, culture_handle) -> CouncilUnit:
    yao_text = "Xio"
    yao_healer = councilunit_shop(yao_text, env_dir, culture_handle)
    yao_healer.set_depot_agenda(get_1node_agenda(), depotlink_type="blind_trust")
    yao_healer.set_depot_agenda(get_Jnode2node_agenda(), depotlink_type="blind_trust")
    return yao_healer


def get_agenda_2CleanNodesRandomWeights(_healer: str = None) -> AgendaUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_agenda = agendaunit_shop(_healer=healer_text)
    casa_text = "casa"
    x_agenda.add_idea(idea_kid=ideacore_shop(_label=casa_text), pad="")
    casa_road = f"{x_agenda._culture_handle},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideacore_shop(
        _label=cookery_text, _weight=randrange(1, 50), promise=True
    )
    bedroom_idea = ideacore_shop(
        _label=bedroom_text, _weight=randrange(1, 50), promise=True
    )
    x_agenda.add_idea(idea_kid=cookery_idea, pad=casa_road)
    x_agenda.add_idea(idea_kid=bedroom_idea, pad=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_agenda_3CleanNodesRandomWeights(_healer: str = None) -> AgendaUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_agenda = agendaunit_shop(_healer=healer_text)
    casa_text = "casa"
    x_agenda.add_idea(idea_kid=ideacore_shop(_label=casa_text), pad="")
    casa_road = f"{x_agenda._culture_handle},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = ideacore_shop(
        _label=cookery_text, _weight=randrange(1, 50), promise=True
    )
    bedroom_idea = ideacore_shop(
        _label=bedroom_text, _weight=randrange(1, 50), promise=True
    )
    hallway_idea = ideacore_shop(
        _label=hallway_text, _weight=randrange(1, 50), promise=True
    )
    x_agenda.add_idea(idea_kid=cookery_idea, pad=casa_road)
    x_agenda.add_idea(idea_kid=bedroom_idea, pad=casa_road)
    x_agenda.add_idea(idea_kid=hallway_idea, pad=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda
