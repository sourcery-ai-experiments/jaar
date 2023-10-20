from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesRequired_1AcptFact,
    get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop, DealUnit
from src.agenda.road import get_default_culture_root_label as root_label
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises


def test_DealUnit_exists():
    # GIVEN

    # WHEN
    x_agenda = DealUnit()

    assert x_agenda
    assert x_agenda._healer is None
    assert x_agenda._culture_handle is None
    assert x_agenda._weight is None
    assert x_agenda._max_tree_traverse is None
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational is None
    assert x_agenda._originunit is None
    assert x_agenda._auto_output_to_public is None
    assert x_agenda._idearoot is None
    assert str(type(x_agenda._idearoot)).find("None") == 8


def test_agendaunit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    healer_text = "Noa"

    # WHEN
    x_agenda = agendaunit_shop(_healer=healer_text)

    assert x_agenda
    assert x_agenda._healer == healer_text
    assert x_agenda._culture_handle == root_label()
    assert x_agenda._weight == 1
    assert x_agenda._max_tree_traverse == 3
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational == False
    assert x_agenda._originunit == originunit_shop()
    assert x_agenda._auto_output_to_public == False
    assert x_agenda._idearoot != None
    print(f"{type(x_agenda._idearoot)=}") == 0
    assert str(type(x_agenda._idearoot)).find(".idea.IdeaRoot'>") > 0


def test_agendaunit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVE/ WHEN
    x_agenda = agendaunit_shop()

    assert x_agenda._healer == ""


def test_agenda_IsAbleToSetTaskAsComplete():
    x_agenda = get_agenda_1Task_1CE0MinutesRequired_1AcptFact()

    assert x_agenda != None
    assert len(x_agenda._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = x_agenda.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{x_agenda._culture_handle},{ced_min_label}"
    x_agenda.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_agenda.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_agenda_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    x_agenda = get_agenda_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{x_agenda._culture_handle},{ced_min_label}"
    x_agenda.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = x_agenda.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    x_agenda.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = x_agenda.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_agenda_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    healer_text = "Zia"

    # WHEN
    x_agenda = agendaunit_shop(_healer=healer_text)

    # THEN
    assert x_agenda._idearoot._uid == 1


def test_agenda_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(_healer=healer_text)
    assert x_agenda._max_tree_traverse == 3

    # WHEN
    x_agenda.set_max_tree_traverse(int_x=11)

    # THEN
    assert x_agenda._max_tree_traverse == 11


def test_agenda_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(_healer=healer_text)
    assert x_agenda._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda.set_max_tree_traverse(int_x=1)
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
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text, _auto_output_to_public=True)

    # THEN
    assert x_agenda._auto_output_to_public == True


def test_agenda_set_culture_handle_CorrectlySetsAttr():
    # GIVEN
    culture_handle_text = "Sun"
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text, _auto_output_to_public=True)
    assert x_agenda._culture_handle == root_label()

    # WHEN
    x_agenda.set_culture_handle(culture_handle=culture_handle_text)

    # THEN
    assert x_agenda._culture_handle == culture_handle_text
