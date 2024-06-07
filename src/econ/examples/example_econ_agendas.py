from src._instrument.file import delete_dir
from src.agenda.agenda import AgendaUnit, agendaunit_shop, ideaunit_shop, RealID
from src.agenda.examples.example_agendas import (
    get_agenda_with7amCleanTableReason,
    get_agenda_base_time_example,
    get_agenda_x1_3levels_1reason_1beliefs,
)
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import temp_real_id, get_texas_agendahub
from random import randrange


def get_1node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_Jnode2node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_2node_agenda(real_id: RealID = None) -> AgendaUnit:
    if real_id is None:
        real_id = temp_real_id()
    a_text = "A"
    b_text = "B"
    x_agenda = agendaunit_shop(_owner_id=a_text)
    x_agenda.set_real_id(real_id)
    idea_b = ideaunit_shop(b_text)
    x_agenda.add_idea(idea_b, parent_road=temp_real_id())
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_3node_agenda() -> AgendaUnit:
    a_text = "A"
    x_agenda = agendaunit_shop(a_text)
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_3node_D_E_F_agenda() -> AgendaUnit:
    d_text = "D"
    x_agenda = agendaunit_shop(d_text)
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("E"))
    x_agenda.add_l1_idea(ideaunit_shop("F"))
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_6node_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_7nodeInsertH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), x_agenda.make_road(c_road, "H"))
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_5nodeHG_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("A")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("B"))
    x_agenda.add_l1_idea(ideaunit_shop("C"))
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.add_idea(ideaunit_shop("G"), c_road)
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_7nodeJRoot_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("D"), c_road)
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_7nodeJRootWithH_agenda() -> AgendaUnit:
    x_agenda = agendaunit_shop("J")
    x_agenda.set_real_id(temp_real_id())
    x_agenda.add_l1_idea(ideaunit_shop("A"))

    a_road = x_agenda.make_l1_road("A")
    x_agenda.add_idea(ideaunit_shop("B"), a_road)
    x_agenda.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_agenda.make_l1_road("C")
    x_agenda.add_idea(ideaunit_shop("E"), c_road)
    x_agenda.add_idea(ideaunit_shop("F"), c_road)
    x_agenda.add_idea(ideaunit_shop("H"), c_road)
    x_agenda.calc_agenda_metrics()
    return x_agenda


def get_agenda_2CleanNodesRandomWeights(_owner_id: str = None) -> AgendaUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_agenda = agendaunit_shop(owner_id)
    casa_text = "casa"
    x_agenda.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.calc_agenda_metrics()
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
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    nursery_idea = ideaunit_shop(nursery_text, _weight=randrange(1, 50), pledge=True)
    x_agenda.add_idea(cookery_idea, parent_road=casa_road)
    x_agenda.add_idea(bedroom_idea, parent_road=casa_road)
    x_agenda.add_idea(nursery_idea, parent_road=casa_road)
    x_agenda.calc_agenda_metrics()
    return x_agenda


def setup_test_example_environment():
    # _delete_and_set_ex3()
    _delete_and_set_ex4()
    # _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex4():
    ex4_id = "ex4"
    ex4_agendahub = get_texas_agendahub()
    ex4_agendahub.real_id = ex4_id
    x_econ = econunit_shop(ex4_agendahub)
    delete_dir(x_econ.agendahub.econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.agendahub.save_job_agenda(get_7nodeJRootWithH_agenda())
    x_econ.agendahub.save_job_agenda(get_agenda_with7amCleanTableReason())
    x_econ.agendahub.save_job_agenda(get_agenda_base_time_example())
    x_econ.agendahub.save_job_agenda(get_agenda_x1_3levels_1reason_1beliefs())


def _delete_and_set_ex6(ex6_id: str = None):
    if ex6_id is None:
        ex6_id = "ex6"
    ex6_agendahub = get_texas_agendahub()
    ex6_agendahub.real_id = ex6_id
    x_econ = econunit_shop(ex6_agendahub)
    delete_dir(x_econ.agendahub.econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=False)

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_job_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.agendahub.save_job_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.agendahub.save_job_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.agendahub.save_job_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.agendahub.save_job_agenda(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

    return x_econ
