from src._road.finance import default_pixel_if_none, default_penny_if_none
from src._truth.examples.example_truths import (
    get_truth_1Task_1CE0MinutesReason_1Fact,
)
from src._truth.truth import truthunit_shop, TruthUnit
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    default_road_delimiter_if_none,
)
from src._truth.origin import originunit_shop
from pytest import raises as pytest_raises


def test_TruthUnit_Exists():
    # GIVEN

    # WHEN
    x_truth = TruthUnit()

    assert x_truth
    assert x_truth._real_id is None
    assert x_truth._owner_id is None
    assert x_truth._weight is None
    assert x_truth._others is None
    assert x_truth._beliefs is None
    assert x_truth._idearoot is None
    assert x_truth._max_tree_traverse is None
    assert x_truth._road_delimiter is None
    assert x_truth._pixel is None
    assert x_truth._penny is None
    assert x_truth._monetary_desc is None
    assert x_truth._other_credor_pool is None
    assert x_truth._other_debtor_pool is None
    assert x_truth._last_atom_id is None
    assert x_truth._meld_strategy is None
    assert x_truth._originunit is None

    assert x_truth._idea_dict is None
    assert x_truth._econ_dict is None
    assert x_truth._healers_dict is None
    assert x_truth._tree_traverse_count is None
    assert x_truth._rational is None
    assert x_truth._econs_justified is None
    assert x_truth._econs_buildable is None
    assert x_truth._sum_healerhold_importance is None
    assert str(type(x_truth._idearoot)).find("None") == 8


def test_TruthUnit_shop_ReturnsCorrectObjectWithFilledFields():
    # GIVEN
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    slash_road_delimiter = "/"
    override_meld_strategy = "override"
    five_pixel = 5
    penny_float = 1

    # WHEN
    x_truth = truthunit_shop(
        _owner_id=noa_text,
        _real_id=iowa_real_id,
        _road_delimiter=slash_road_delimiter,
        _meld_strategy=override_meld_strategy,
        _pixel=five_pixel,
        _penny=penny_float,
    )
    assert x_truth
    assert x_truth._owner_id == noa_text
    assert x_truth._real_id == iowa_real_id
    assert x_truth._weight == 1
    assert x_truth._others == {}
    assert x_truth._beliefs == {}
    assert x_truth._idearoot != None
    assert x_truth._max_tree_traverse == 3
    assert x_truth._road_delimiter == slash_road_delimiter
    assert x_truth._pixel == five_pixel
    assert x_truth._penny == penny_float
    assert x_truth._monetary_desc is None
    assert x_truth._other_credor_pool is None
    assert x_truth._other_debtor_pool is None
    assert x_truth._last_atom_id is None
    assert x_truth._meld_strategy == override_meld_strategy
    assert x_truth._originunit == originunit_shop()

    assert x_truth._idea_dict == {}
    assert x_truth._econ_dict == {}
    assert x_truth._healers_dict == {}
    assert x_truth._tree_traverse_count is None
    assert x_truth._rational is False
    assert x_truth._econs_justified is False
    assert x_truth._econs_buildable is False
    assert x_truth._sum_healerhold_importance == 0
    print(f"{type(x_truth._idearoot)=}") == 0
    assert str(type(x_truth._idearoot)).find(".idea.IdeaUnit'>") > 0


def test_TruthUnit_shop_ReturnsCorrect_meld_strategy():
    # GIVEN
    noa_text = "Noa"
    iowa_real_id = "Iowa"
    # WHEN
    x_truth = truthunit_shop(noa_text, iowa_real_id)
    # THEN
    assert x_truth._meld_strategy == "default"


def test_TruthUnit_shop_ReturnsCorrectObjectWithCorrectEmptyField():
    # GIVEN / WHEN
    x_truth = truthunit_shop()

    assert x_truth._owner_id == ""
    assert x_truth._real_id == root_label()
    assert x_truth._road_delimiter == default_road_delimiter_if_none()
    assert x_truth._pixel == default_pixel_if_none()
    assert x_truth._penny == default_penny_if_none()


def test_TruthUnit_set_fact_IsAbleToSetTaskAsComplete():
    # GIVEN
    x_truth = get_truth_1Task_1CE0MinutesReason_1Fact()
    mail_text = "obtain mail"
    assert x_truth != None
    assert len(x_truth._idearoot._kids[mail_text]._reasonunits) == 1
    idea_dict = x_truth.get_idea_dict()
    # for idea in idea_dict:
    #     print(idea._label)
    mail_idea = idea_dict.get(x_truth.make_l1_road(mail_text))
    assert mail_idea.pledge == True
    assert mail_idea._task == True

    # WHEN
    ced_min_label = "CE0_minutes"
    ced_road = x_truth.make_l1_road(ced_min_label)
    x_truth.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    x_truth.calc_truth_metrics()

    # THEN
    assert mail_idea.pledge == True
    assert mail_idea._task is False


def test_TruthUnit_IsAbleToEditFactUnitAnyAncestor_Idea_1():
    x_truth = get_truth_1Task_1CE0MinutesReason_1Fact()
    ced_min_label = "CE0_minutes"
    ced_road = x_truth.make_l1_road(ced_min_label)
    x_truth.set_fact(base=ced_road, pick=ced_road, open=82, nigh=85)
    mail_road = x_truth.make_l1_road("obtain mail")
    idea_dict = x_truth.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task is False

    x_truth.set_fact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_dict = x_truth.get_idea_dict()
    mail_idea = idea_dict.get(mail_road)
    assert mail_idea.pledge == True
    assert mail_idea._task == True


def test_TruthUnit_ideaoot_uid_isEqualTo1():
    # GIVEN
    zia_text = "Zia"

    # WHEN
    zia_truth = truthunit_shop(_owner_id=zia_text)

    # THEN
    assert zia_truth._idearoot._uid == 1


def test_TruthUnit_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_truth = truthunit_shop(_owner_id=zia_text)
    assert zia_truth._max_tree_traverse == 3

    # WHEN
    zia_truth.set_max_tree_traverse(int_x=11)

    # THEN
    assert zia_truth._max_tree_traverse == 11


def test_TruthUnit_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    zia_text = "Zia"
    zia_truth = truthunit_shop(_owner_id=zia_text)
    assert zia_truth._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        zia_truth.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_TruthUnit_set_real_id_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    x_truth = truthunit_shop(_owner_id=noa_text)
    assert x_truth._real_id == root_label()

    # WHEN
    x_truth.set_real_id(real_id=real_id_text)

    # THEN
    assert x_truth._real_id == real_id_text


def test_TruthUnit_set_road_delimiter_CorrectlySetsAttr():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_truth = truthunit_shop(
        _owner_id=noa_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    assert x_truth._road_delimiter == slash_road_delimiter

    # WHEN
    at_node_delimiter = "@"
    x_truth.set_road_delimiter(new_road_delimiter=at_node_delimiter)

    # THEN
    assert x_truth._road_delimiter == at_node_delimiter


def test_TruthUnit_make_road_ReturnsCorrectObj():
    # GIVEN
    real_id_text = "Sun"
    noa_text = "Noa"
    slash_road_delimiter = "/"
    x_truth = truthunit_shop(
        _owner_id=noa_text,
        _real_id=real_id_text,
        _road_delimiter=slash_road_delimiter,
    )
    casa_text = "casa"
    v1_casa_road = x_truth.make_l1_road(casa_text)

    # WHEN
    v2_casa_road = x_truth.make_l1_road(casa_text)

    # THEN
    assert v1_casa_road == v2_casa_road


def test_TruthUnit_set_meld_strategy_CorrectlySetsAttr():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    override_text = "override"
    assert noa_truth._meld_strategy != override_text

    # WHEN
    noa_truth.set_meld_strategy(override_text)

    # THEN
    assert noa_truth._meld_strategy == override_text


def test_TruthUnit_set_meld_strategy_RaisesErrorWithIneligible_meld_strategy():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    bad_override_text = "oVerride"
    assert noa_truth._meld_strategy != bad_override_text

    # WHEN
    with pytest_raises(Exception) as excinfo:
        noa_truth.set_meld_strategy(bad_override_text)
    assert str(excinfo.value) == f"'{bad_override_text}' is ineligible meld_strategy."


def test_TruthUnit_set_monetary_desc_SetsAttrCorrectly():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    noa_monetary_desc = "Folos"
    assert noa_truth._monetary_desc != noa_monetary_desc

    # WHEN
    noa_truth.set_monetary_desc(noa_monetary_desc)

    # THEN
    assert noa_truth._monetary_desc == noa_monetary_desc


def test_TruthUnit_set_last_atom_id_SetsAttrCorrectly():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    assert noa_truth._last_atom_id is None

    # WHEN
    x_last_atom_id = 89
    noa_truth.set_last_atom_id(x_last_atom_id)

    # THEN
    assert noa_truth._last_atom_id == x_last_atom_id


def test_TruthUnit_set_last_atom_id_RaisesError():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    old_last_atom_id = 89
    noa_truth.set_last_atom_id(old_last_atom_id)

    # WHEN / THEN
    new_last_atom_id = 72
    assert new_last_atom_id < old_last_atom_id
    with pytest_raises(Exception) as excinfo:
        noa_truth.set_last_atom_id(new_last_atom_id)
    assert (
        str(excinfo.value)
        == f"Cannot set _last_atom_id to {new_last_atom_id} because it is less than {old_last_atom_id}."
    )


def test_TruthUnit_del_last_atom_id_SetsAttrCorrectly():
    # GIVEN
    noa_truth = truthunit_shop("Noa", "Texas")
    old_last_atom_id = 89
    noa_truth.set_last_atom_id(old_last_atom_id)
    assert noa_truth._last_atom_id != None

    # WHEN
    noa_truth.del_last_atom_id()

    # WHEN
    assert noa_truth._last_atom_id is None
