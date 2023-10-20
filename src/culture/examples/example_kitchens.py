from src.agenda.agenda import (
    DealUnit,
    agendaunit_shop,
    ideacore_shop,
    assigned_unit_shop,
)
from src.culture.kitchen import kitchenunit_shop, KitchenUnit
from src.culture.examples.kitchen_env_kit import get_temp_culture_handle

from random import randrange


def get_1node_agenda() -> DealUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(_healer=a_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> DealUnit:
    healer_text = "J"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    a_text = "A"
    idea_a = ideacore_shop(_label=a_text)
    x_agenda.add_idea(idea_kid=idea_a, pad=get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_2node_agenda() -> DealUnit:
    healer_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_healer=healer_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    idea_b = ideacore_shop(_label=b_text)
    x_agenda.add_idea(idea_kid=idea_b, pad=get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> DealUnit:
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


def get_3node_D_E_F_agenda() -> DealUnit:
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


def get_6node_agenda() -> DealUnit:
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


def get_7nodeInsertH_agenda() -> DealUnit:
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


def get_5nodeHG_agenda() -> DealUnit:
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


def get_7nodeJRoot_agenda() -> DealUnit:
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


def get_7nodeJRootWithH_agenda() -> DealUnit:
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


def get_healer_2agenda(env_dir, culture_handle) -> KitchenUnit:
    yao_text = "Xio"
    yao_healer = kitchenunit_shop(yao_text, env_dir, culture_handle)
    yao_healer.set_depot_agenda(get_1node_agenda(), depotlink_type="blind_trust")
    yao_healer.set_depot_agenda(get_Jnode2node_agenda(), depotlink_type="blind_trust")
    return yao_healer


def get_agenda_2CleanNodesRandomWeights(_healer: str = None) -> DealUnit:
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


def get_agenda_3CleanNodesRandomWeights(_healer: str = None) -> DealUnit:
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


def get_agenda_assignment_laundry_example1() -> DealUnit:
    america_text = "America"
    america_agenda = agendaunit_shop(_healer=america_text)
    joachim_text = "Joachim"
    america_agenda.add_partyunit(america_text)
    america_agenda.add_partyunit(joachim_text)

    root_road = america_agenda._culture_handle
    casa_text = "casa"
    casa_road = f"{root_road},{casa_text}"
    america_agenda.add_idea(ideacore_shop(_label=casa_text), pad=root_road)

    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    america_agenda.add_idea(ideacore_shop(_label=basket_text), pad=casa_road)

    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    america_agenda.add_idea(ideacore_shop(_label=b_full_text), pad=basket_road)

    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    america_agenda.add_idea(ideacore_shop(_label=b_smel_text), pad=basket_road)

    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    america_agenda.add_idea(ideacore_shop(_label=b_bare_text), pad=basket_road)

    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    america_agenda.add_idea(ideacore_shop(_label=b_fine_text), pad=basket_road)

    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    america_agenda.add_idea(ideacore_shop(_label=b_half_text), pad=basket_road)

    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    america_agenda.add_idea(
        ideacore_shop(_label=laundry_task_text, promise=True), pad=casa_road
    )

    # make laundry requirement
    basket_idea = america_agenda.get_idea_kid(road=basket_road)
    america_agenda.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_full_road
    )
    # make laundry requirement
    america_agenda.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_smel_road
    )
    # assign Joachim to task
    joachim_assignunit = assigned_unit_shop()
    joachim_assignunit.set_suffgroup(joachim_text)
    america_agenda.edit_idea_attr(
        road=laundry_task_road, assignedunit=joachim_assignunit
    )
    america_agenda.set_acptfact(base=basket_road, pick=b_full_road)

    return america_agenda
