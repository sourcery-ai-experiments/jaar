from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_exists():
    # GIVEN

    # WHEN
    x_agenda = AgendaUnit()

    assert x_agenda
    assert x_agenda._agent_id is None
    assert x_agenda._economy_id is None
    assert x_agenda._weight is None
    assert x_agenda._max_tree_traverse is None
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational is None
    assert x_agenda._originunit is None
    assert x_agenda._auto_output_to_public is None
    assert x_agenda._idearoot is None
    assert x_agenda._road_delimiter is None
    assert str(type(x_agenda._idearoot)).find("None") == 8


def test_agendaunit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    noa_text = "Noa"
    iowa_economy_id = "Iowa"
    slash_road_delimiter = "/"

    # WHEN
    x_agenda = agendaunit_shop(
        _agent_id=noa_text,
        _economy_id=iowa_economy_id,
        _road_delimiter=slash_road_delimiter,
    )

    assert x_agenda
    assert x_agenda._agent_id == noa_text
    assert x_agenda._economy_id == iowa_economy_id
    assert x_agenda._weight == 1
    assert x_agenda._max_tree_traverse == 3
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational == False
    assert x_agenda._originunit == originunit_shop()
    assert x_agenda._auto_output_to_public == False
    assert x_agenda._idearoot != None
    assert x_agenda._road_delimiter == slash_road_delimiter
    print(f"{type(x_agenda._idearoot)=}") == 0
    assert str(type(x_agenda._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_agendaunit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVE/ WHEN
    x_agenda = agendaunit_shop()

    assert x_agenda._agent_id == ""
    assert x_agenda._economy_id == root_label()
    assert x_agenda._road_delimiter == default_road_delimiter_if_none()


def test_agenda_IsAbleToSetTaskAsComplete():
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()

    assert x_agenda != None
    assert len(x_agenda._idearoot._kids["obtain mail"]._reasonunits) == 1
    idea_list = x_agenda.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_agenda.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_agenda_IsAbleToEditBeliefUnitAnyAncestor_Idea_1():
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Belief()
    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_agenda.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    x_agenda.set_belief(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = x_agenda.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_agenda_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    zia_text = "Zia"

    # WHEN
    zia_agenda = agendaunit_shop(_agent_id=zia_text)

    # THEN
    assert zia_agenda._idearoot._uid == 1


def test_agenda_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_agent_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN
    zia_agenda.set_max_tree_traverse(int_x=11)

    # THEN
    assert zia_agenda._max_tree_traverse == 11


def test_agenda_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_agent_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_agenda_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    x_agenda = get_agenda_with_4_levels()

    # WHEN / THEN
    assert x_agenda._auto_output_to_public == False
    x_agenda._set_auto_output_to_public(None)
    assert x_agenda._auto_output_to_public == False

    # WHEN / THEN
    assert x_agenda._auto_output_to_public == False
    x_agenda._set_auto_output_to_public(True)
    assert x_agenda._auto_output_to_public

    # WHEN / THEN
    assert x_agenda._auto_output_to_public
    x_agenda._set_auto_output_to_public(True)
    assert x_agenda._auto_output_to_public

    # WHEN / THEN
    assert x_agenda._auto_output_to_public
    x_agenda._set_auto_output_to_public(None)
    assert x_agenda._auto_output_to_public

    # WHEN / THEN
    assert x_agenda._auto_output_to_public
    x_agenda._set_auto_output_to_public(False)
    assert x_agenda._auto_output_to_public == False

    # WHEN / THEN
    x_agenda._auto_output_to_public = None
    assert x_agenda._auto_output_to_public is None
    x_agenda._set_auto_output_to_public(None)
    assert x_agenda._auto_output_to_public == False


def test_agenda_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    noa_text = "Noa"
    x_agenda = agendaunit_shop(_agent_id=noa_text, _auto_output_to_public=True)

    # THEN
    assert x_agenda._auto_output_to_public == True


def test_agenda_set_economy_id_CorrectlySetsAttr():
    # GIVEN
    economy_id_text = "Sun"
    noa_text = "Noa"
    x_agenda = agendaunit_shop(_agent_id=noa_text, _auto_output_to_public=True)
    assert x_agenda._economy_id == root_label()

    # WHEN
    x_agenda.set_economy_id(economy_id=economy_id_text)

    # THEN
    assert x_agenda._economy_id == economy_id_text


def test_agenda_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    economy_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _agent_id=noa_text,
        _economy_id=economy_id_text,
        _auto_output_to_public=True,
        _road_delimiter=slash_road_delimiter,
    )
    assert x_agenda._road_delimiter == slash_road_delimiter

    # WHEN
    at_node_delimiter = "@"
    x_agenda.set_road_delimiter(new_road_delimiter=at_node_delimiter)

    # THEN
    assert x_agenda._road_delimiter == at_node_delimiter


def test_agendaunit_make_road_ReturnsCorrectObj():
    # GIVEN
    economy_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _agent_id=noa_text,
        _economy_id=economy_id_text,
        _auto_output_to_public=True,
        _road_delimiter=slash_road_delimiter,
    )
    work_text = "work"
    v1_work_road = x_agenda.make_l1_road(work_text)

    # WHEN
    v2_work_road = x_agenda.make_l1_road(work_text)

    # THEN
    assert v1_work_road == v2_work_road
