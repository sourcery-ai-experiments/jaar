from src.agenda.group import groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.basis_agendas import (
    create_empty_agenda,
    create_listen_basis,
    get_default_work_agenda,
)


def test_create_empty_agenda_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    penny_float = 0.7
    yao_duty = agendaunit_shop(yao_text, _road_delimiter=slash_text, _penny=penny_float)
    yao_duty.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_missing_debtor_weight = 22
    role_zia_partyunit = yao_duty.get_party(zia_text)
    role_zia_partyunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_partyunit.add_missing_debtor_weight(zia_missing_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_duty.set_groupunit(swim_group)
    yao_duty.set_party_credor_pool(zia_credor_pool, True)
    yao_duty.set_party_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_empty_job = create_empty_agenda(yao_duty, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_duty._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_duty._real_id
    assert yao_empty_job._last_atom_id is None
    assert yao_empty_job.get_groupunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_duty._road_delimiter
    assert yao_empty_job._planck == yao_duty._planck
    assert yao_empty_job._penny == yao_duty._penny
    assert yao_empty_job._monetary_desc is None
    assert yao_empty_job._party_credor_pool != yao_duty._party_credor_pool
    assert yao_empty_job._party_credor_pool is None
    assert yao_empty_job._party_debtor_pool != yao_duty._party_debtor_pool
    assert yao_empty_job._party_debtor_pool is None
    yao_empty_job.calc_agenda_metrics()
    assert yao_empty_job._partys == {}


def test_create_listen_basis_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_role = agendaunit_shop(yao_text, _road_delimiter=slash_text)
    yao_role.add_l1_idea(ideaunit_shop("Iowa"))
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_credor_pool = 87
    zia_debtor_pool = 81
    yao_role.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_missing_debtor_weight = 22
    role_zia_partyunit = yao_role.get_party(zia_text)
    role_zia_partyunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_partyunit.add_missing_debtor_weight(zia_missing_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_role.set_groupunit(swim_group)
    yao_role.set_party_credor_pool(zia_credor_pool, True)
    yao_role.set_party_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_basis_job = create_listen_basis(yao_role)

    # THEN
    assert yao_basis_job._owner_id == yao_role._owner_id
    assert yao_basis_job._real_id == yao_role._real_id
    assert yao_basis_job._last_atom_id == yao_role._last_atom_id
    assert yao_basis_job.get_groupunits_dict() == yao_role.get_groupunits_dict()
    assert yao_basis_job._road_delimiter == yao_role._road_delimiter
    assert yao_basis_job._planck == yao_role._planck
    assert yao_basis_job._monetary_desc == yao_role._monetary_desc
    assert yao_basis_job._party_credor_pool == yao_role._party_credor_pool
    assert yao_basis_job._party_debtor_pool == yao_role._party_debtor_pool
    yao_basis_job.calc_agenda_metrics()
    assert len(yao_basis_job._idea_dict) != len(yao_role._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_partyunit = yao_basis_job.get_party(zia_text)
    assert yao_basis_job.get_partys_dict().keys() == yao_role.get_partys_dict().keys()
    assert job_zia_partyunit._irrational_debtor_weight == 0
    assert job_zia_partyunit._missing_debtor_weight == 0


def test_get_default_work_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    five_planck = 5
    sue_party_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_atom_id = 7
    sue_max_tree_traverse = 9
    sue_agendaunit = agendaunit_shop(sue_text, blue_text, slash_text, five_planck)
    sue_agendaunit.set_last_atom_id(last_atom_id)
    sue_agendaunit.add_partyunit(bob_text, 3, 4)
    swim_text = "/swimmers"
    swim_groupunit = groupunit_shop(swim_text, _road_delimiter=slash_text)
    swim_groupunit.edit_partylink(bob_text)
    sue_agendaunit.set_groupunit(swim_groupunit)
    sue_agendaunit.set_party_pool(sue_party_pool)
    sue_agendaunit.add_l1_idea(ideaunit_shop(casa_text))
    sue_agendaunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_work_agenda = get_default_work_agenda(sue_agendaunit)

    # THEN
    default_work_agenda.calc_agenda_metrics()
    assert default_work_agenda._owner_id == sue_agendaunit._owner_id
    assert default_work_agenda._owner_id == sue_text
    assert default_work_agenda._real_id == sue_agendaunit._real_id
    assert default_work_agenda._real_id == blue_text
    assert default_work_agenda._road_delimiter == slash_text
    assert default_work_agenda._planck == five_planck
    assert default_work_agenda._party_credor_pool is None
    assert default_work_agenda._party_debtor_pool is None
    assert default_work_agenda._max_tree_traverse == sue_max_tree_traverse
    assert len(default_work_agenda.get_partys_dict()) == 1
    assert len(default_work_agenda.get_groupunits_dict()) == 1
    assert len(default_work_agenda._idea_dict) == 1
