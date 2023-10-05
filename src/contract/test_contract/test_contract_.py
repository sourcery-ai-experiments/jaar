from src.contract.examples.example_contracts import (
    get_contract_1Task_1CE0MinutesRequired_1AcptFact,
    get_contract_with_4_levels,
)
from src.contract.contract import ContractUnit
from src.contract.road import get_default_economy_root_label as root_label
from src.contract.origin import originunit_shop
from pytest import raises as pytest_raises


def test_contract_exists():
    # GIVEN

    # WHEN
    owner_text = "Noa"
    new_obj = ContractUnit(_owner=owner_text)

    assert new_obj
    assert new_obj._owner == owner_text
    assert new_obj._economy_tag == root_label()
    assert new_obj._weight == 1
    assert new_obj._max_tree_traverse == 3
    assert new_obj._tree_traverse_count is None
    assert new_obj._rational == False
    assert new_obj._originunit == originunit_shop()
    assert new_obj._auto_output_to_public == False
    assert str(type(new_obj._idearoot)).find(".idea.IdeaRoot'>")


def test_contract_IsAbleToSetTaskAsComplete():
    contract_x = get_contract_1Task_1CE0MinutesRequired_1AcptFact()

    assert contract_x != None
    assert len(contract_x._idearoot._kids["obtain mail"]._requiredunits) == 1
    idea_list = contract_x.get_idea_list()
    # for idea in idea_list:
    #     print(idea._label)
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True

    ced_min_label = "CE0_minutes"
    ced_road = f"{contract_x._economy_tag},{ced_min_label}"
    contract_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = contract_x.get_idea_list()
    assert mail_idea.promise == True
    assert mail_idea._task == False


def test_contract_IsAbleToEditAcptFactUnitAnyAncestor_Idea_1():
    contract_x = get_contract_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_label = "CE0_minutes"
    ced_road = f"{contract_x._economy_tag},{ced_min_label}"
    contract_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    idea_list = contract_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == False

    contract_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    idea_list = contract_x.get_idea_list()
    mail_idea = idea_list[1]
    assert mail_idea.promise == True
    assert mail_idea._task == True


def test_contract_ideaoot_uid_isAlwaysEqualTo1():
    # GIVEN
    owner_text = "Zia"

    # WHEN
    sx = ContractUnit(_owner=owner_text)

    # THEN
    assert sx._idearoot._uid == 1


def test_contract_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    owner_text = "Zia"
    sx = ContractUnit(_owner=owner_text)
    assert sx._max_tree_traverse == 3

    # WHEN
    sx.set_max_tree_traverse(int_x=11)

    # THEN
    assert sx._max_tree_traverse == 11


def test_contract_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    owner_text = "Zia"
    sx = ContractUnit(_owner=owner_text)
    assert sx._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sx.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )


def test_contract_set_auto_output_to_public_SetsBoolCorrectlyGivenNoneOrBool():
    # GIVEN
    contract_x = get_contract_with_4_levels()

    # WHEN / THEN
    assert contract_x._auto_output_to_public == False
    contract_x._set_auto_output_to_public(None)
    assert contract_x._auto_output_to_public == False

    # WHEN / THEN
    assert contract_x._auto_output_to_public == False
    contract_x._set_auto_output_to_public(True)
    assert contract_x._auto_output_to_public

    # WHEN / THEN
    assert contract_x._auto_output_to_public
    contract_x._set_auto_output_to_public(True)
    assert contract_x._auto_output_to_public

    # WHEN / THEN
    assert contract_x._auto_output_to_public
    contract_x._set_auto_output_to_public(None)
    assert contract_x._auto_output_to_public

    # WHEN / THEN
    assert contract_x._auto_output_to_public
    contract_x._set_auto_output_to_public(False)
    assert contract_x._auto_output_to_public == False

    # WHEN / THEN
    contract_x._auto_output_to_public = None
    assert contract_x._auto_output_to_public is None
    contract_x._set_auto_output_to_public(None)
    assert contract_x._auto_output_to_public == False


def test_contract_init_CorrectlySetsGiven_auto_output_to_public():
    # GIVEN

    # WHEN
    owner_text = "Noa"
    new_obj = ContractUnit(_owner=owner_text, _auto_output_to_public=True)

    # THEN
    assert new_obj._auto_output_to_public == True


def test_contract_set_economy_tag_CorrectlySetsAttr():
    # GIVEN
    economy_tag_text = "Sun"
    owner_text = "Noa"
    new_obj = ContractUnit(_owner=owner_text, _auto_output_to_public=True)
    assert new_obj._economy_tag == root_label()

    # WHEN
    new_obj.set_economy_tag(economy_tag=economy_tag_text)

    # THEN
    assert new_obj._economy_tag == economy_tag_text
