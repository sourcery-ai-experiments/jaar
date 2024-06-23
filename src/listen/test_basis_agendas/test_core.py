from src.agenda.belief import beliefunit_shop
from src.agenda.other import otherlink_shop
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
    yao_duty.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    role_zia_otherunit = yao_duty.get_other(zia_text)
    role_zia_otherunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_otherunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    swim_belief = beliefunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_belief.set_otherlink(otherlink_shop(zia_text))
    yao_duty.set_beliefunit(swim_belief)
    yao_duty.set_other_credor_pool(zia_credor_pool, True)
    yao_duty.set_other_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_empty_job = create_empty_agenda(yao_duty, x_owner_id=zia_text)

    # THEN
    assert yao_empty_job._owner_id != yao_duty._owner_id
    assert yao_empty_job._owner_id == zia_text
    assert yao_empty_job._real_id == yao_duty._real_id
    assert yao_empty_job._last_atom_id is None
    assert yao_empty_job.get_beliefunits_dict() == {}
    assert yao_empty_job._road_delimiter == yao_duty._road_delimiter
    assert yao_empty_job._pixel == yao_duty._pixel
    assert yao_empty_job._penny == yao_duty._penny
    assert yao_empty_job._monetary_desc is None
    assert yao_empty_job._other_credor_pool != yao_duty._other_credor_pool
    assert yao_empty_job._other_credor_pool is None
    assert yao_empty_job._other_debtor_pool != yao_duty._other_debtor_pool
    assert yao_empty_job._other_debtor_pool is None
    yao_empty_job.calc_agenda_metrics()
    assert yao_empty_job._others == {}


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
    yao_role.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    zia_irrational_debtor_weight = 11
    zia_inallocable_debtor_weight = 22
    role_zia_otherunit = yao_role.get_other(zia_text)
    role_zia_otherunit.add_irrational_debtor_weight(zia_irrational_debtor_weight)
    role_zia_otherunit.add_inallocable_debtor_weight(zia_inallocable_debtor_weight)
    swim_belief = beliefunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_belief.set_otherlink(otherlink_shop(zia_text))
    yao_role.set_beliefunit(swim_belief)
    yao_role.set_other_credor_pool(zia_credor_pool, True)
    yao_role.set_other_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_basis_job = create_listen_basis(yao_role)

    # THEN
    assert yao_basis_job._owner_id == yao_role._owner_id
    assert yao_basis_job._real_id == yao_role._real_id
    assert yao_basis_job._last_atom_id == yao_role._last_atom_id
    assert yao_basis_job.get_beliefunits_dict() == yao_role.get_beliefunits_dict()
    assert yao_basis_job._road_delimiter == yao_role._road_delimiter
    assert yao_basis_job._pixel == yao_role._pixel
    assert yao_basis_job._monetary_desc == yao_role._monetary_desc
    assert yao_basis_job._other_credor_pool == yao_role._other_credor_pool
    assert yao_basis_job._other_debtor_pool == yao_role._other_debtor_pool
    yao_basis_job.calc_agenda_metrics()
    assert len(yao_basis_job._idea_dict) != len(yao_role._idea_dict)
    assert len(yao_basis_job._idea_dict) == 1
    job_zia_otherunit = yao_basis_job.get_other(zia_text)
    assert yao_basis_job.get_others_dict().keys() == yao_role.get_others_dict().keys()
    assert job_zia_otherunit._irrational_debtor_weight == 0
    assert job_zia_otherunit._inallocable_debtor_weight == 0


def test_get_default_work_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    five_pixel = 5
    sue_other_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_atom_id = 7
    sue_max_tree_traverse = 9
    sue_agendaunit = agendaunit_shop(sue_text, blue_text, slash_text, five_pixel)
    sue_agendaunit.set_last_atom_id(last_atom_id)
    sue_agendaunit.add_otherunit(bob_text, 3, 4)
    swim_text = "/swimmers"
    swim_beliefunit = beliefunit_shop(swim_text, _road_delimiter=slash_text)
    swim_beliefunit.edit_otherlink(bob_text)
    sue_agendaunit.set_beliefunit(swim_beliefunit)
    sue_agendaunit.set_other_pool(sue_other_pool)
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
    assert default_work_agenda._pixel == five_pixel
    assert default_work_agenda._other_credor_pool is None
    assert default_work_agenda._other_debtor_pool is None
    assert default_work_agenda._max_tree_traverse == sue_max_tree_traverse
    assert len(default_work_agenda.get_others_dict()) == 1
    assert len(default_work_agenda.get_beliefunits_dict()) == 1
    assert len(default_work_agenda._idea_dict) == 1
