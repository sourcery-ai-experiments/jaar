from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src._road.road import (
    get_default_econ_root_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_Exists():
    # GIVEN

    # WHEN
    x_agenda = AgendaUnit()

    assert x_agenda
    assert x_agenda._worker_id is None
    assert x_agenda._world_id is None
    assert x_agenda._weight is None
    assert x_agenda._max_tree_traverse is None
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational is None
    assert x_agenda._originunit is None
    assert x_agenda._auto_output_job_to_forum is None
    assert x_agenda._idearoot is None
    assert x_agenda._idea_dict is None
    assert x_agenda._econ_dict is None
    assert x_agenda._healers_dict is None
    assert x_agenda._road_delimiter is None
    assert x_agenda._party_creditor_pool is None
    assert x_agenda._party_debtor_pool is None
    assert x_agenda._meld_strategy is None
    assert x_agenda._econs_justified is None
    assert x_agenda._econs_buildable is None
    assert x_agenda._sum_healerhold_importance is None
    assert str(type(x_agenda._idearoot)).find("None") == 8


def test_AgendaUnit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    noa_text = "Noa"
    iowa_world_id = "Iowa"
    slash_road_delimiter = "/"
    override_meld_strategy = "override"

    # WHEN
    x_agenda = agendaunit_shop(
        _worker_id=noa_text,
        _world_id=iowa_world_id,
        _road_delimiter=slash_road_delimiter,
        _meld_strategy=override_meld_strategy,
    )
    assert x_agenda
    assert x_agenda._worker_id == noa_text
    assert x_agenda._world_id == iowa_world_id
    assert x_agenda._weight == 1
    assert x_agenda._max_tree_traverse == 3
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational == False
    assert x_agenda._originunit == originunit_shop()
    assert x_agenda._auto_output_job_to_forum == False
    assert x_agenda._idearoot != None
    assert x_agenda._idea_dict == {}
    assert x_agenda._econ_dict == {}
    assert x_agenda._healers_dict == {}
    assert x_agenda._road_delimiter == slash_road_delimiter
    assert x_agenda._party_creditor_pool is None
    assert x_agenda._party_debtor_pool is None
    assert x_agenda._meld_strategy == override_meld_strategy
    assert x_agenda._econs_justified == False
    assert x_agenda._econs_buildable == False
    assert x_agenda._sum_healerhold_importance == False
    print(f"{type(x_agenda._idearoot)=}") == 0
    assert str(type(x_agenda._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_AgendaUnit_shop_ReturnsCorrect_meld_strategy():
    # GIVEN
    noa_text = "Noa"
    iowa_world_id = "Iowa"
    # WHEN
    x_agenda = agendaunit_shop(noa_text, iowa_world_id)
    # THEN
    assert x_agenda._meld_strategy == "default"


def test_AgendaUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVE/ WHEN
    x_agenda = agendaunit_shop()

    assert x_agenda._worker_id == ""
    assert x_agenda._world_id == root_label()
    assert x_agenda._road_delimiter == default_road_delimiter_if_none()


def test_AgendaUnit_set_belief_IsAbleToSetTaskAsComplete():
    # GIVEN
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()
    mail_text = "obtain mail"
    assert x_agenda != None
    assert len(x_agenda._idearoot._kids[mail_text]._reasonunits) == 1
    idea_dict = x_agenda.get_idea_dict()
    # for idea in idea_dict:
    #     print(idea._label)
    mail_idea = idea_dict.get(x_agenda.make_l1_road(mail_text))
    assert mail_idea.promise == True
    assert mail_idea._task == True

    # WHEN
    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=85)
    x_agenda.set_agenda_metrics()

    # THEN
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_AgendaUnit_IsAbleToEditBeliefUnitAnyAncestor_Idea_1():
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()
    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_agenda.make_l1_road("obtain mail")
    idea_dict = x_agenda.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.promise == True
    assert mail_idea._task == False

    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_agenda.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_AgendaUnit_ideaoot_uid_isEqualTo1():
    # GIVEN
    zia_text = "Zia"

    # WHEN
    zia_agenda = agendaunit_shop(_worker_id=zia_text)

    # THEN
    assert zia_agenda._idearoot._uid == 1


def test_AgendaUnit_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN
    zia_agenda.set_max_tree_traverse(int_x=11)

    # THEN
    assert zia_agenda._max_tree_traverse == 11


def test_AgendaUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_AgendaUnit_set_party_creditor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    assert zia_agenda._party_creditor_pool is None
    assert zia_agenda._party_debtor_pool is None

    # WHEN
    x_party_creditor_pool = 11
    x_party_debtor_pool = 13
    zia_agenda.set_party_creditor_pool(x_party_creditor_pool)
    zia_agenda.set_party_debtor_pool(x_party_debtor_pool)
    # THEN
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool


def test_AgendaUnit_set_auto_output_job_to_forum_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()

    # WHEN / THEN
    assert x_agenda._auto_output_job_to_forum == False
    x_agenda._set_auto_output_job_to_forum(None)
    assert x_agenda._auto_output_job_to_forum == False

    # WHEN / THEN
    assert x_agenda._auto_output_job_to_forum == False
    x_agenda._set_auto_output_job_to_forum(True)
    assert x_agenda._auto_output_job_to_forum

    # WHEN / THEN
    assert x_agenda._auto_output_job_to_forum
    x_agenda._set_auto_output_job_to_forum(True)
    assert x_agenda._auto_output_job_to_forum

    # WHEN / THEN
    assert x_agenda._auto_output_job_to_forum
    x_agenda._set_auto_output_job_to_forum(None)
    assert x_agenda._auto_output_job_to_forum

    # WHEN / THEN
    assert x_agenda._auto_output_job_to_forum
    x_agenda._set_auto_output_job_to_forum(False)
    assert x_agenda._auto_output_job_to_forum == False

    # WHEN / THEN
    x_agenda._auto_output_job_to_forum = None
    assert x_agenda._auto_output_job_to_forum is None
    x_agenda._set_auto_output_job_to_forum(None)
    assert x_agenda._auto_output_job_to_forum == False


def test_AgendaUnit_shop_CorrectlySetsGiven_auto_output_job_to_forum():
    # GIVEN

    # WHEN
    noa_text = "Noa"
    x_agenda = agendaunit_shop(_worker_id=noa_text, _auto_output_job_to_forum=True)

    # THEN
    assert x_agenda._auto_output_job_to_forum == True


def test_AgendaUnit_set_world_id_CorrectlySetsAttr():
    # GIVEN
    world_id_text = "Sun"
    noa_text = "Noa"
    x_agenda = agendaunit_shop(_worker_id=noa_text, _auto_output_job_to_forum=True)
    assert x_agenda._world_id == root_label()

    # WHEN
    x_agenda.set_world_id(world_id=world_id_text)

    # THEN
    assert x_agenda._world_id == world_id_text


def test_AgendaUnit_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    world_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _worker_id=noa_text,
        _world_id=world_id_text,
        _auto_output_job_to_forum=True,
        _road_delimiter=slash_road_delimiter,
    )
    assert x_agenda._road_delimiter == slash_road_delimiter

    # WHEN
    at_node_delimiter = "@"
    x_agenda.set_road_delimiter(new_road_delimiter=at_node_delimiter)

    # THEN
    assert x_agenda._road_delimiter == at_node_delimiter


def test_AgendaUnit_make_road_ReturnsCorrectObj():
    # GIVEN
    world_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _worker_id=noa_text,
        _world_id=world_id_text,
        _auto_output_job_to_forum=True,
        _road_delimiter=slash_road_delimiter,
    )
    gig_text = "gig"
    v1_gig_road = x_agenda.make_l1_road(gig_text)

    # WHEN
    v2_gig_road = x_agenda.make_l1_road(gig_text)

    # THEN
    assert v1_gig_road == v2_gig_road


def test_AgendaUnit_set_meld_strategy_CorrectlySetsAttr():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    override_text = "override"
    assert noa_agenda._meld_strategy != override_text

    # WHEN
    noa_agenda.set_meld_strategy(override_text)

    # THEN
    assert noa_agenda._meld_strategy == override_text


def test_AgendaUnit_set_meld_strategy_RaisesErrorWithIneligible_meld_strategy():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    bad_override_text = "oVerride"
    assert noa_agenda._meld_strategy != bad_override_text

    # WHEN
    with pytest_raises(Exception) as excinfo:
        noa_agenda.set_meld_strategy(bad_override_text)
    assert str(excinfo.value) == f"'{bad_override_text}' is ineligible meld_strategy."
