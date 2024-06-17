from src._road.finance import default_planck_if_none, default_penny_if_none
from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Fact,
)
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_Exists():
    # GIVEN

    # WHEN
    x_agenda = AgendaUnit()

    assert x_agenda
    assert x_agenda._real_id is None
    assert x_agenda._owner_id is None
    assert x_agenda._weight is None
    assert x_agenda._others is None
    assert x_agenda._beliefs is None
    assert x_agenda._idearoot is None
    assert x_agenda._max_tree_traverse is None
    assert x_agenda._road_delimiter is None
    assert x_agenda._planck is None
    assert x_agenda._penny is None
    assert x_agenda._monetary_desc is None
    assert x_agenda._other_credor_pool is None
    assert x_agenda._other_debtor_pool is None
    assert x_agenda._last_atom_id is None
    assert x_agenda._meld_strategy is None
    assert x_agenda._originunit is None

    assert x_agenda._idea_dict is None
    assert x_agenda._econ_dict is None
    assert x_agenda._healers_dict is None
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational is None
    assert x_agenda._econs_justified is None
    assert x_agenda._econs_buildable is None
    assert x_agenda._sum_healerhold_importance is None
    assert str(type(x_agenda._idearoot)).find("None") == 8


def test_AgendaUnit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    slash_road_delimiter = "/"
    override_meld_strategy = "override"
    five_planck = 5
    penny_float = 0.8

    # WHEN
    x_agenda = agendaunit_shop(
        _owner_id=noa_text,
        _real_id=iowa_real_id,
        _road_delimiter=slash_road_delimiter,
        _meld_strategy=override_meld_strategy,
        _planck=five_planck,
        _penny=penny_float,
    )
    assert x_agenda
    assert x_agenda._owner_id == noa_text
    assert x_agenda._real_id == iowa_real_id
    assert x_agenda._weight == 1
    assert x_agenda._others == {}
    assert x_agenda._beliefs == {}
    assert x_agenda._idearoot != None
    assert x_agenda._max_tree_traverse == 3
    assert x_agenda._road_delimiter == slash_road_delimiter
    assert x_agenda._planck == five_planck
    assert x_agenda._penny == penny_float
    assert x_agenda._monetary_desc is None
    assert x_agenda._other_credor_pool is None
    assert x_agenda._other_debtor_pool is None
    assert x_agenda._last_atom_id is None
    assert x_agenda._meld_strategy == override_meld_strategy
    assert x_agenda._originunit == originunit_shop()

    assert x_agenda._idea_dict == {}
    assert x_agenda._econ_dict == {}
    assert x_agenda._healers_dict == {}
    assert x_agenda._tree_traverse_count is None
    assert x_agenda._rational is False
    assert x_agenda._econs_justified is False
    assert x_agenda._econs_buildable is False
    assert x_agenda._sum_healerhold_importance == 0
    print(f"{type(x_agenda._idearoot)=}") == 0
    assert str(type(x_agenda._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_AgendaUnit_shop_ReturnsCorrect_meld_strategy():
    # GIVEN
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    # WHEN
    x_agenda = agendaunit_shop(noa_text, iowa_real_id)
    # THEN
    assert x_agenda._meld_strategy == "default"


def test_AgendaUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVEN / WHEN
    x_agenda = agendaunit_shop()

    assert x_agenda._owner_id == ""
    assert x_agenda._real_id == root_label()
    assert x_agenda._road_delimiter == default_road_delimiter_if_none()
    assert x_agenda._planck == default_planck_if_none()
    assert x_agenda._penny == default_penny_if_none()


def test_AgendaUnit_set_fact_IsAbleToSetTaskAsComplete():
    # GIVEN
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Fact()
    mail_text = "obtain mail"
    assert x_agenda != None
    assert len(x_agenda._idearoot._kids[mail_text]._reasonunits) == 1
    idea_dict = x_agenda.get_idea_dict()
    # for idea in idea_dict:
    #     print(idea._label)
    mail_idea = idea_dict.get(x_agenda.make_l1_road(mail_text))
    assert mail_idea.pledge == True
    assert mail_idea._task == True

    # WHEN
    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    x_agenda.calc_agenda_metrics()

    # THEN
    assert mail_idea.pledge == True
    assert mail_idea._task is False


def test_AgendaUnit_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    x_agenda = get_agenda_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = x_agenda.make_l1_road(ced_min_label)
    x_agenda.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_agenda.make_l1_road("obtain mail")
    idea_dict = x_agenda.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    x_agenda.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_agenda.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True


def test_AgendaUnit_ideaoot_uid_isEqualTo1():
    # GIVEN
    zia_text = "Zia"

    # WHEN
    zia_agenda = agendaunit_shop(_owner_id=zia_text)

    # THEN
    assert zia_agenda._idearoot._uid == 1


def test_AgendaUnit_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN
    zia_agenda.set_max_tree_traverse(int_x=11)

    # THEN
    assert zia_agenda._max_tree_traverse == 11


def test_AgendaUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    assert zia_agenda._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_AgendaUnit_set_real_id_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    x_agenda = agendaunit_shop(_owner_id=noa_text)
    assert x_agenda._real_id == root_label()

    # WHEN
    x_agenda.set_real_id(real_id=real_id_text)

    # THEN
    assert x_agenda._real_id == real_id_text


def test_AgendaUnit_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _owner_id=noa_text,
        _real_id=real_id_text,
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
    real_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_agenda = agendaunit_shop(
        _owner_id=noa_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    casa_text = "casa"
    v1_casa_road = x_agenda.make_l1_road(casa_text)

    # WHEN
    v2_casa_road = x_agenda.make_l1_road(casa_text)

    # THEN
    assert v1_casa_road == v2_casa_road


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


def test_AgendaUnit_set_monetary_desc_SetsAttrCorrectly():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    noa_monetary_desc = "Folos"
    assert noa_agenda._monetary_desc != noa_monetary_desc

    # WHEN
    noa_agenda.set_monetary_desc(noa_monetary_desc)

    # THEN
    assert noa_agenda._monetary_desc == noa_monetary_desc


def test_AgendaUnit_set_last_atom_id_SetsAttrCorrectly():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    assert noa_agenda._last_atom_id is None

    # WHEN
    x_last_atom_id = 89
    noa_agenda.set_last_atom_id(x_last_atom_id)

    # THEN
    assert noa_agenda._last_atom_id == x_last_atom_id


def test_AgendaUnit_set_last_atom_id_RaisesError():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    old_last_atom_id = 89
    noa_agenda.set_last_atom_id(old_last_atom_id)

    # WHEN / THEN
    new_last_atom_id = 72
    assert new_last_atom_id < old_last_atom_id
    with pytest_raises(Exception) as excinfo:
        noa_agenda.set_last_atom_id(new_last_atom_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_atom_id to {new_last_atom_id} because it is less than {old_last_atom_id}."
    )


def test_AgendaUnit_del_last_atom_id_SetsAttrCorrectly():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa", "Texas")
    old_last_atom_id = 89
    noa_agenda.set_last_atom_id(old_last_atom_id)
    assert noa_agenda._last_atom_id != None

    # WHEN
    noa_agenda.del_last_atom_id()

    # WHEN
    assert noa_agenda._last_atom_id is None
