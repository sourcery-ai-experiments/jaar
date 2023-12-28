from src.agenda.agenda import AgendaUnit, agendaunit_shop, ideacore_shop
from src.agenda.examples.example_agendas import get_agenda_assignment_laundry_example1
from src.economy.clerk import clerkunit_shop, clerkUnit
from src.economy.examples.clerk_env_kit import get_temp_economy_id

from random import randrange


def get_1node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("A"), parent_road=x_agenda._economy_id)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_2node_agenda() -> AgendaUnit:
    healer_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_economy_id(get_temp_economy_id())
    idea_b = ideacore_shop(b_text)
    x_agenda.add_idea(idea_b, parent_road=get_temp_economy_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> AgendaUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(a_text)
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("B"), parent_road=x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop("C"), parent_road=x_agenda._economy_id)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_D_E_F_agenda() -> AgendaUnit:
    d_text = "D"
    x_agenda = agendaunit_shop(d_text)
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("E"), parent_road=x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop("F"), parent_road=x_agenda._economy_id)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_6node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("B"), x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop("C"), x_agenda._economy_id)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideacore_shop("D"), c_road)
    x_agenda.add_idea(ideacore_shop("E"), c_road)
    x_agenda.add_idea(ideacore_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeInsertH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("B"), x_agenda.make_road(x_agenda._economy_id))
    x_agenda.add_idea(ideacore_shop("C"), x_agenda.make_road(x_agenda._economy_id))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideacore_shop("H"), c_road)
    x_agenda.add_idea(ideacore_shop("D"), c_road)
    x_agenda.add_idea(ideacore_shop("E"), c_road)
    x_agenda.add_idea(ideacore_shop("F"), x_agenda.make_road(c_road, "H"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_5nodeHG_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("B"), x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop("C"), x_agenda._economy_id)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideacore_shop("H"), c_road)
    x_agenda.add_idea(ideacore_shop("G"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRoot_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("A"), x_agenda._economy_id)

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideacore_shop("B"), a_road)
    x_agenda.add_idea(ideacore_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideacore_shop("D"), c_road)
    x_agenda.add_idea(ideacore_shop("E"), c_road)
    x_agenda.add_idea(ideacore_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRootWithH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.add_idea(ideacore_shop("A"), x_agenda._economy_id)

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideacore_shop("B"), a_road)
    x_agenda.add_idea(ideacore_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideacore_shop("E"), c_road)
    x_agenda.add_idea(ideacore_shop("F"), c_road)
    x_agenda.add_idea(ideacore_shop("H"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_healer_2agenda(env_dir, economy_id) -> clerkUnit:
    yao_text = "Xio"
    yao_healer = clerkunit_shop(yao_text, env_dir, economy_id)
    yao_healer.set_depot_agenda(get_1node_agenda(), depotlink_type="blind_trust")
    yao_healer.set_depot_agenda(get_Jnode2node_agenda(), depotlink_type="blind_trust")
    return yao_healer


def get_agenda_2CleanNodesRandomWeights(_healer: str = None) -> AgendaUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_agenda = agendaunit_shop(healer_text)
    casa_text = "casa"
    x_agenda.add_idea(ideacore_shop(casa_text), parent_road=x_agenda._economy_id)
    casa_road = f"{x_agenda._economy_id},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideacore_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideacore_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_agenda_3CleanNodesRandomWeights(_healer: str = None) -> AgendaUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_agenda = agendaunit_shop(healer_text)
    casa_text = "casa"
    x_agenda.add_idea(ideacore_shop(casa_text), parent_road=x_agenda._economy_id)
    casa_road = f"{x_agenda._economy_id},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = ideacore_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideacore_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = ideacore_shop(hallway_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.add_idea(hallway_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda
