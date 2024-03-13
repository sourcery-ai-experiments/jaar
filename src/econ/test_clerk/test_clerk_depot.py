from src.agenda.agenda import agendaunit_shop
from src.econ.clerk import clerkunit_shop
from src.econ.examples.example_clerks import get_clerkunit_2agenda
from src.econ.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_econ_id,
)


def test_clerkunit_set_depot_agenda_SetsCorrectInfo(clerk_dir_setup_cleanup):
    # GIVEN
    x_clerk = get_clerkunit_2agenda(get_temp_clerkunit_dir(), get_temp_econ_id())
    assert x_clerk._role.get_partys_depotlink_count() == 2
    print(f"{x_clerk._role._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_clerk.set_depot_agenda(agendaunit_shop(zia_text), assignment_text)
    zoa_text = "Zoa"
    x_clerk.set_depot_agenda(agendaunit_shop(zoa_text), assignment_text)

    # THEN
    print(f"{x_clerk._role._partys.keys()=}")
    assert x_clerk._role.get_partys_depotlink_count() == 4


def test_clerkunit_set_depot_agenda_CorrectlySets_creditor_pool(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_clerkunit_dir()
    yao_clerkunit = clerkunit_shop(yao_text, env_dir, get_temp_econ_id())
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_party_creditor_pool = 5000
    zia_agenda.set_party_creditor_pool(zia_party_creditor_pool)
    assignment_text = "assignment"
    yao_clerkunit.set_depot_agenda(zia_agenda, assignment_text)
    before_zia_agenda = yao_clerkunit.open_depot_agenda(zia_text)
    assert before_zia_agenda._party_creditor_pool == zia_party_creditor_pool
    print(f"{zia_agenda._owner_id=}")
    print(f"{zia_agenda._party_creditor_pool=}")

    # WHEN
    zia_creditor_weight = 70
    yao_clerkunit.set_depot_agenda(
        zia_agenda, assignment_text, creditor_weight=zia_creditor_weight
    )

    # THEN
    after_zia_depot_agenda = yao_clerkunit.open_depot_agenda(zia_text)
    assert after_zia_depot_agenda._party_creditor_pool == zia_creditor_weight


def test_clerkunit_set_depot_agenda_CorrectlySets_debtor_pool(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_clerkunit_dir()
    yao_clerkunit = clerkunit_shop(yao_text, env_dir, get_temp_econ_id())
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_party_debtor_pool = 5000
    zia_agenda.set_party_debtor_pool(zia_party_debtor_pool)
    assignment_text = "assignment"
    yao_clerkunit.set_depot_agenda(zia_agenda, assignment_text)
    before_zia_agenda = yao_clerkunit.open_depot_agenda(zia_text)
    assert before_zia_agenda._party_debtor_pool == zia_party_debtor_pool
    print(f"{zia_agenda._owner_id=}")
    print(f"{zia_agenda._party_debtor_pool=}")

    # WHEN
    zia_debtor_weight = 70
    yao_clerkunit.set_depot_agenda(
        zia_agenda, assignment_text, debtor_weight=zia_debtor_weight
    )

    # THEN
    after_zia_depot_agenda = yao_clerkunit.open_depot_agenda(zia_text)
    assert after_zia_depot_agenda._party_debtor_pool == zia_debtor_weight
