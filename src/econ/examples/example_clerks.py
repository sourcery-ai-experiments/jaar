from src.agenda.agenda import AgendaUnit, agendaunit_shop, ideaunit_shop, WorldID
from src.agenda.examples.example_agendas import get_agenda_assignment_laundry_example1
from src.econ.clerk import clerkunit_shop, ClerkUnit
from src.econ.examples.clerk_env_kit import get_temp_econ_id

from random import randrange


def get_1node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_2node_agenda(world_id: WorldID = None) -> AgendaUnit:
    if world_id is None:
        world_id = get_temp_econ_id()
    a_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_owner_id=a_text)
    x_agenda.set_world_id(world_id)
    idea_b = ideaunit_shop(b_text)
    x_agenda.add_idea(idea_b, parent_road=get_temp_econ_id())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> AgendaUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(a_text)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_D_E_F_agenda() -> AgendaUnit:
    d_text = "D"
    x_agenda = agendaunit_shop(d_text)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("E"))
    x_agenda.add_l1_idea(ideaunit_shop("F"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_6node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeInsertH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), x_agenda.make_road(c_road, "H"))
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_5nodeHG_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("G"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRoot_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_7nodeJRootWithH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_clerkunit_2agenda(env_dir, econ_id) -> ClerkUnit:
    a_agenda = get_1node_agenda()
    j_agenda = get_Jnode2node_agenda()
    xio_text = "Xio"
    xio_clerkunit = clerkunit_shop(xio_text, env_dir, econ_id)
    xio_role = xio_clerkunit.get_role()
    xio_role.add_partyunit(a_agenda._owner_id)
    xio_role.add_partyunit(j_agenda._owner_id)
    xio_clerkunit.save_role_agenda(xio_role)
    xio_clerkunit._set_depot_agenda(a_agenda)
    xio_clerkunit._set_depot_agenda(j_agenda)
    return xio_clerkunit


def get_agenda_2CleanNodesRandomWeights(_owner_id: str = None) -> AgendaUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_agenda = agendaunit_shop(owner_id)
    casa_text = "casa"
    x_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_agenda_3CleanNodesRandomWeights(_owner_id: str = None) -> AgendaUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_agenda = agendaunit_shop(owner_id)
    casa_text = "casa"
    x_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    nursery_text = "clean nursery"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), promise=True)
    nursery_idea = ideaunit_shop(nursery_text, _weight=randrange(1, 50), promise=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.add_idea(nursery_idea, parent_road=casa_road)
    x_agenda.set_agenda_metrics()
    return x_agenda
