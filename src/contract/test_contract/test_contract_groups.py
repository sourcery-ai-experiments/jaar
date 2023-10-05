from src.contract.group import GroupBrand, balancelink_shop, groupunit_shop
from src.contract.party import PartyName, partyunit_shop, partylink_shop
from src.contract.idea import IdeaKid
from src.contract.required_idea import Road
from src.contract.examples.example_contracts import (
    contract_v001 as examples_contract_v001,
)
from src.contract.contract import (
    ContractUnit,
    get_partys_relevant_groups,
    get_party_relevant_groups,
)
from pytest import raises as pytest_raises


def test_contract_groups_set_groupunit_worksCorrectly():
    # GIVEN
    cx = ContractUnit()
    assert cx._groups is None
    swim_text = "swim"
    groupbrand_x = GroupBrand(swim_text)
    every1_groups = {groupbrand_x: groupunit_shop(brand=groupbrand_x)}
    cx2 = ContractUnit()

    # WHEN
    cx2.set_groupunit(groupunit=groupunit_shop(brand=groupbrand_x))

    # THEN
    assert len(cx2._groups) == 1
    assert len(cx2._groups) == len(every1_groups)
    assert cx2._groups.get(swim_text)._partys == every1_groups.get(swim_text)._partys
    assert cx2._groups.get(swim_text) == every1_groups.get(swim_text)
    assert cx2._groups == every1_groups

    bill_single_party_id = 30
    bill_group = groupunit_shop(
        brand=GroupBrand("bill"), uid=45, single_party_id=bill_single_party_id
    )
    assert bill_group != None


def test_contract_groups_del_groupunit_worksCorrectly():
    # GIVEN
    sx = ContractUnit()
    swim_text = "swimmers"
    group_x = groupunit_shop(brand=GroupBrand(swim_text))
    sx.set_groupunit(groupunit=group_x)
    assert sx._groups.get(swim_text) != None

    # WHEN
    sx.del_groupunit(groupbrand=swim_text)
    assert sx._groups.get(swim_text) is None
    assert sx._groups == {}


def test_example_has_groups():
    # GIVEN / WHEN
    cx = examples_contract_v001()

    # THEN
    assert cx._groups != None
    assert len(cx._groups) == 34
    everyone_partys_len = None
    everyone_group = cx._groups.get("Everyone")
    everyone_partys_len = len(everyone_group._partys)
    assert everyone_partys_len == 22

    # WHEN
    cx.set_contract_metrics()
    idea_dict = cx._idea_dict

    # THEN
    db_idea = idea_dict.get(f"{cx._economy_tag},D&B")
    print(f"{db_idea._label=} {db_idea._balancelinks=}")
    assert len(db_idea._balancelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._balancelinks=}")
    #         db_balancelink_len = len(idea._balancelinks)
    # assert db_balancelink_len == 3


def test_contract_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    prom_text = "prom"
    cx = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))

    assert len(cx._partys) == 3
    assert len(cx._groups) == 3
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)
    swim_road = f"{prom_text},{swim_text}"
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    assert cx._idearoot._balancelinks in (None, {})
    assert len(cx._idearoot._kids[swim_text]._balancelinks) == 3

    cx.add_idea(idea_kid=IdeaKid(_label="streets"), walk=swim_road)

    # WHEN
    idea_list = cx.get_idea_list()

    # THEN
    idea_prom = idea_list[1]
    idea_prom_swim = idea_list[2]

    assert len(idea_prom._balancelinks) == 3
    assert len(idea_prom._balanceheirs) == 3
    assert idea_prom_swim._balancelinks in (None, {})
    assert len(idea_prom_swim._balanceheirs) == 3

    print(f"{len(idea_list)}")
    print(f"{idea_list[0]._balancelinks}")
    print(f"{idea_list[0]._balanceheirs}")
    print(f"{idea_list[1]._balanceheirs}")
    assert len(cx._idearoot._kids["swim"]._balanceheirs) == 3


def test_contract_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    a_x = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))

    swim_text = "swim"
    swim_road = f"{prom_text},{swim_text}"

    a_x.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)

    swim_idea = a_x.get_idea_kid(road=swim_road)
    a_x.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    a_x.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    a_x.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    # idea_list = a_x.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._balancelinks}")
    # print(f"{idea_list[0]._balanceheirs}")
    # print(f"{idea_list[1]._balanceheirs}")
    assert len(a_x._idearoot._kids[swim_text]._balancelinks) == 3
    assert len(a_x._idearoot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    a_x.edit_idea_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_idea = a_x.get_idea_kid(road=swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._balancelinks=}")
    print(f"{swim_idea._balanceheirs=}")

    assert len(a_x._idearoot._kids[swim_text]._balancelinks) == 2
    assert len(a_x._idearoot._kids[swim_text]._balanceheirs) == 2


def test_contract_set_balancelink_CorrectlyCalculatesInheritedBalancelinkContractImportance():
    # GIVEN
    a_x = ContractUnit(_owner="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    a_x._idearoot.set_balancelink(balancelink=blink_rico)
    a_x._idearoot.set_balancelink(balancelink=blink_carm)
    a_x._idearoot.set_balancelink(balancelink=blink_patr)
    assert len(a_x._idearoot._balancelinks) == 3

    # WHEN
    idea_list = a_x.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._balanceheirs) == 3

    bheir_rico = idea_prom._balanceheirs.get(rico_text)
    bheir_carm = idea_prom._balanceheirs.get(carm_text)
    bheir_patr = idea_prom._balanceheirs.get(patr_text)
    assert bheir_rico._contract_credit == 0.5
    assert bheir_rico._contract_debt == 0.75
    assert bheir_carm._contract_credit == 0.25
    assert bheir_carm._contract_debt == 0.125
    assert bheir_patr._contract_credit == 0.25
    assert bheir_patr._contract_debt == 0.125
    assert (
        bheir_rico._contract_credit
        + bheir_carm._contract_credit
        + bheir_patr._contract_credit
        == 1
    )
    assert (
        bheir_rico._contract_debt
        + bheir_carm._contract_debt
        + bheir_patr._contract_debt
        == 1
    )

    # contract_credit_sum = 0
    # contract_debt_sum = 0
    # for group in a_x._idearoot._balanceheirs.values():
    #     print(f"{group=}")
    #     assert group._contract_credit != None
    #     assert group._contract_credit in [0.25, 0.5]
    #     assert group._contract_debt != None
    #     assert group._contract_debt in [0.75, 0.125]
    #     contract_credit_sum += group._contract_credit
    #     contract_debt_sum += group._contract_debt

    # assert contract_credit_sum == 1
    # assert contract_debt_sum == 1


def test_contract_get_idea_list_CorrectlyCalculates1LevelContractGroupContractImportance():
    # GIVEN
    prom_text = "prom"
    a_x = ContractUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    a_x._idearoot.set_balancelink(balancelink=blink_rico)
    a_x._idearoot.set_balancelink(balancelink=blink_carm)
    a_x._idearoot.set_balancelink(balancelink=blink_patr)

    assert len(a_x._groups) == 3

    # WHEN
    a_x.set_contract_metrics()

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._contract_credit == 0.5
    assert group_rico._contract_debt == 0.75
    assert group_carm._contract_credit == 0.25
    assert group_carm._contract_debt == 0.125
    assert group_patr._contract_credit == 0.25
    assert group_patr._contract_debt == 0.125
    assert (
        group_rico._contract_credit
        + group_carm._contract_credit
        + group_patr._contract_credit
        == 1
    )
    assert (
        group_rico._contract_debt
        + group_carm._contract_debt
        + group_patr._contract_debt
        == 1
    )

    # WHEN
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(sele_text)))
    bl_sele = balancelink_shop(brand=sele_text, creditor_weight=37)
    a_x._idearoot.set_balancelink(balancelink=bl_sele)
    assert len(a_x._groups) == 4
    a_x.set_contract_metrics()

    # THEN
    group_sele = a_x._groups.get(sele_text)
    assert group_rico._contract_credit != 0.5
    assert group_rico._contract_debt != 0.75
    assert group_carm._contract_credit != 0.25
    assert group_carm._contract_debt != 0.125
    assert group_patr._contract_credit != 0.25
    assert group_patr._contract_debt != 0.125
    assert group_sele._contract_credit != None
    assert group_sele._contract_debt != None
    assert (
        group_rico._contract_credit
        + group_carm._contract_credit
        + group_patr._contract_credit
        + group_sele._contract_credit
        == 1
    )
    assert (
        group_rico._contract_debt
        + group_carm._contract_debt
        + group_patr._contract_debt
        + group_sele._contract_debt
        == 1
    )


def test_contract_get_idea_list_CorrectlyCalculates3levelContractGroupContractImportance():
    # GIVEN
    prom_text = "prom"
    a_x = ContractUnit(_owner=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(a_x._groups) == 3

    # WHEN
    a_x.set_contract_metrics()

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._contract_credit == 0.5
    assert group_rico._contract_debt == 0.75
    assert group_carm._contract_credit == 0.25
    assert group_carm._contract_debt == 0.125
    assert group_patr._contract_credit == 0.25
    assert group_patr._contract_debt == 0.125
    assert (
        group_rico._contract_credit
        + group_carm._contract_credit
        + group_patr._contract_credit
        == 1
    )
    assert (
        group_rico._contract_debt
        + group_carm._contract_debt
        + group_patr._contract_debt
        == 1
    )


def test_contract_get_idea_list_CorrectlyCalculatesGroupContractImportanceLWwithGroupEmptyBranch():
    # GIVEN
    prom_text = "prom"
    a_x = ContractUnit(_owner=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(rico_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(carm_text)))
    a_x.set_partyunit(partyunit=partyunit_shop(name=PartyName(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    a_x._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    a_x.add_idea(idea_kid=IdeaKid(_label="hunt", _weight=3), walk="prom")

    assert a_x._idearoot._balancelinks is None

    # WHEN
    a_x.set_contract_metrics()

    # THEN
    assert a_x._idearoot._balancelinks == {}

    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._contract_credit == 0.125
    assert group_rico._contract_debt == 0.1875
    assert group_carm._contract_credit == 0.0625
    assert group_carm._contract_debt == 0.03125
    assert group_patr._contract_credit == 0.0625
    assert group_patr._contract_debt == 0.03125
    assert (
        group_rico._contract_credit
        + group_carm._contract_credit
        + group_patr._contract_credit
        == 0.25
    )
    assert (
        group_rico._contract_debt
        + group_carm._contract_debt
        + group_patr._contract_debt
        == 0.25
    )


def test_contract_edit_groupunit_brand_CorrectlyCreatesNewName():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(partylink=partylink_shop(name=rico_text))
    sx.set_groupunit(swim_group)
    assert len(sx._partys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(swim_text) != None
    assert sx._groups.get(swim_text).uid == 13
    assert sx._groups.get(swim_text)._single_party == False
    assert len(sx._groups.get(swim_text)._partys) == 1

    # WHEN
    jog_text = "jog"
    sx.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(jog_text).uid == 13
    assert sx._groups.get(swim_text) is None
    assert len(sx._partys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(jog_text)._single_party == False
    assert len(sx._groups.get(jog_text)._partys) == 1


def test_contract_edit_Groupunit_brand_raiseErrorNewNamePreviouslyExists():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text)
    swim_text = "swim"
    sx.set_groupunit(groupunit_shop(brand=swim_text, uid=13))
    jog_text = "jog"
    sx.set_groupunit(groupunit_shop(brand=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_groupunit_brand(
            old_brand=swim_text,
            new_brand=jog_text,
            allow_group_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Group '{swim_text}' change to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_contract_edit_groupunit_brand_CorrectlyMeldNames():
    # GIVEN
    sx = ContractUnit(_owner="prom")
    rico_text = "rico"
    sx.add_partyunit(name=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=5, debtor_weight=3)
    )
    sx.set_groupunit(swim_group)
    jog_text = "jog"
    jog_group = groupunit_shop(brand=jog_text, uid=13)
    jog_group.set_partylink(
        partylink=partylink_shop(name=rico_text, creditor_weight=7, debtor_weight=10)
    )
    sx.set_groupunit(jog_group)
    print(f"{sx._groups.get(jog_text)._partys.get(rico_text)=}")
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(jog_text).uid == 13

    # WHEN
    sx.edit_groupunit_brand(
        old_brand=swim_text,
        new_brand=jog_text,
        allow_group_overwite=True,
    )

    # THEN
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(swim_text) is None
    assert len(sx._partys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(jog_text)._single_party == False
    assert len(sx._groups.get(jog_text)._partys) == 1
    assert sx._groups.get(jog_text)._partys.get(rico_text).creditor_weight == 12
    assert sx._groups.get(jog_text)._partys.get(rico_text).debtor_weight == 13


def test_contract_edit_groupunit_brand_CorrectlyChangesBalancelinks():
    # GIVEN
    a_x = ContractUnit(_owner="prom")
    rico_text = "rico"
    a_x.add_partyunit(name=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    a_x.set_groupunit(swim_groupunit)
    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._owner},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._owner},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_label=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_balancelink = balancelink_shop(
        brand=swim_groupunit.brand, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    a_x.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 3


def test_contract_edit_groupunit_brand_CorrectlyMeldsBalancelinesBalancelinksBalanceHeirs():
    # GIVEN
    a_x = ContractUnit(_owner="prom")
    rico_text = "rico"
    a_x.add_partyunit(name=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    a_x.set_groupunit(swim_groupunit)

    jog_text = "jog"
    jog_groupunit = groupunit_shop(brand=jog_text, uid=13)
    a_x.set_groupunit(jog_groupunit)

    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._owner},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._owner},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_label=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_balancelink = balancelink_shop(
        brand=swim_groupunit.brand, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    jog_balancelink = balancelink_shop(
        brand=jog_groupunit.brand, creditor_weight=7, debtor_weight=10
    )
    camping_idea.set_balancelink(jog_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 7
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 10

    # WHEN
    a_x.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=True
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 12
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 13


def test_contract_add_idea_CreatesMissingGroups():
    # GIVEN
    owner_text = "bob"
    a_x = ContractUnit(_owner=owner_text)
    a_x.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{a_x._economy_tag},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _label=clean_cookery_text, promise=True)

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)
    assert len(a_x._groups) == 0
    assert a_x._groups.get(family_text) is None

    # WHEN
    a_x.add_idea(
        idea_kid=clean_cookery_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN
    assert len(a_x._groups) == 1
    assert a_x._groups.get(family_text) != None
    assert a_x._groups.get(family_text)._partys in (None, {})


def test_ContractUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    owner_text = "Noa"
    cx1 = ContractUnit(_owner=owner_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(name=xia_text)
    cx1.add_partyunit(name=zoa_text)

    work_text = "work"
    work_road = f"{cx1._economy_tag},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._economy_tag},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), walk=cx1._economy_tag)
    cx1.add_idea(IdeaKid(_label=swim_text), walk=cx1._economy_tag)
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=xia_text))
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=zoa_text))
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    assert len(cx1_swim_idea._balancelinks) == 2
    cx2 = ContractUnit(_owner=owner_text)
    cx2.add_partyunit(name=xia_text)

    # WHEN
    filtered_idea = cx2._get_filtered_balancelinks_idea(cx1_swim_idea)

    # THEN
    assert len(filtered_idea._balancelinks) == 1
    assert list(filtered_idea._balancelinks.keys()) == [xia_text]


def test_ContractUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    owner_text = "Noa"
    cx1 = ContractUnit(_owner=owner_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(name=xia_text)
    cx1.add_partyunit(name=zoa_text)

    work_text = "work"
    work_road = f"{cx1._economy_tag},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._economy_tag},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), walk=cx1._economy_tag)
    cx1.add_idea(IdeaKid(_label=swim_text), walk=cx1._economy_tag)
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=xia_text))
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=zoa_text))
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    assert len(cx1_swim_idea._balancelinks) == 2

    # WHEN
    cx2 = ContractUnit(_owner=owner_text)
    cx2.add_partyunit(name=xia_text)
    cx2.add_idea(
        idea_kid=cx1_swim_idea,
        walk=cx2._economy_tag,
        create_missing_ideas_groups=False,
    )

    # THEN
    cx2_swim_idea = cx2.get_idea_kid(swim_road)
    assert len(cx2_swim_idea._balancelinks) == 1
    assert list(cx2_swim_idea._balancelinks.keys()) == [xia_text]


def test_contract_add_idea_DoesNotOverwriteGroups():
    # GIVEN
    owner_text = "bob"
    a_x = ContractUnit(_owner=owner_text)
    a_x.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{a_x._economy_tag},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _label=clean_cookery_text, promise=True)

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(partylink=partylink_shop(name="ann1"))
    groupunit_z.set_partylink(partylink=partylink_shop(name="bet1"))
    a_x.set_groupunit(groupunit=groupunit_z)

    # assert len(a_x._groups) == 0
    # assert a_x._groups.get(family_text) is None
    assert len(a_x._groups) == 1
    assert len(a_x._groups.get(family_text)._partys) == 2

    # WHEN
    a_x.add_idea(
        idea_kid=clean_cookery_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN

    # assert len(a_x._groups) == 1
    # assert len(a_x._groups.get(family_text)._partys) == 0
    # groupunit_z = groupunit_shop(brand=family_text)
    # groupunit_z.set_partylink(partylink=partylink_shop(name="ann2"))
    # groupunit_z.set_partylink(partylink=partylink_shop(name="bet2"))
    # a_x.set_groupunit(groupunit=groupunit_z)

    assert len(a_x._groups) == 1
    assert len(a_x._groups.get(family_text)._partys) == 2


def test_contract_set_groupunits_create_missing_partys_DoesCreateMissingPartys():
    # GIVEN
    owner_text = "bob"
    a_x = ContractUnit(_owner=owner_text)
    a_x.set_partys_empty_if_null()
    a_x.set_groupunits_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7

    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11

    assert len(a_x._partys) == 0
    assert len(a_x._groups) == 0

    # WHEN
    a_x.set_groupunit(groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(a_x._partys) == 2
    assert len(a_x._groups) == 3
    assert a_x._partys.get(anna_text).creditor_weight == 3
    assert a_x._partys.get(anna_text).debtor_weight == 7

    assert a_x._partys.get(beto_text).creditor_weight == 5
    assert a_x._partys.get(beto_text).debtor_weight == 11


def test_contract_set_groupunits_create_missing_partys_DoesNotReplacePartys():
    # GIVEN
    owner_text = "bob"
    a_x = ContractUnit(_owner=owner_text)
    a_x.set_partys_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    a_x.set_partyunit(
        partyunit_shop(name=anna_text, creditor_weight=17, debtor_weight=88)
    )
    a_x.set_partyunit(
        partyunit_shop(name=beto_text, creditor_weight=46, debtor_weight=71)
    )
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7
    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11
    assert len(a_x._partys) == 2
    assert a_x._partys.get(anna_text).creditor_weight == 17
    assert a_x._partys.get(anna_text).debtor_weight == 88
    assert a_x._partys.get(beto_text).creditor_weight == 46
    assert a_x._partys.get(beto_text).debtor_weight == 71

    # WHEN
    a_x.set_groupunit(groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(a_x._partys) == 2
    assert a_x._partys.get(anna_text).creditor_weight == 17
    assert a_x._partys.get(anna_text).debtor_weight == 88
    assert a_x._partys.get(beto_text).creditor_weight == 46
    assert a_x._partys.get(beto_text).debtor_weight == 71


def test_contract_get_groupunits_dict_CorrectlyReturnsDictOfGroups():
    # GIVEN
    owner_text = "bob"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    wiggle_text = "wiggle"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text))
    sx.set_groupunit(groupunit=groupunit_shop(brand=wiggle_text))
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert len(sx._groups) == 3

    # WHEN
    groupunit_list_x = sx.get_groupunits_brand_list()

    # THEN
    assert groupunit_list_x[0] == ""
    assert groupunit_list_x[1] == fly_text
    assert groupunit_list_x[2] == swim_text
    assert groupunit_list_x[3] == wiggle_text
    assert len(groupunit_list_x) == 4


def test_contract_set_all_groupunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    owner_text = "bob"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text))
    sx.set_groupunit(groupunit=groupunit_shop(brand=walk_text))
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert sx._groups[swim_text].uid is None
    assert sx._groups[walk_text].uid is None
    assert sx._groups[fly_text].uid is None

    # WHEN
    sx.set_all_groupunits_uids_unique()

    # THEN
    assert sx._groups[swim_text].uid != None
    assert sx._groups[walk_text].uid != None
    assert sx._groups[fly_text].uid != None


def test_contract_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "bob"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert sx._groups[swim_text].uid == 3
    assert sx._groups[walk_text].uid == 3
    assert sx._groups[fly_text].uid is None

    # WHEN
    sx.set_all_groupunits_uids_unique()

    # THEN
    print(f"{sx._groups[swim_text].uid=}")
    print(f"{sx._groups[walk_text].uid=}")
    assert sx._groups[swim_text].uid != sx._groups[walk_text].uid
    assert sx._groups[walk_text].uid != 3
    assert sx._groups[walk_text].uid != 3
    assert sx._groups[fly_text].uid != None


def test_contract_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert sx._groups[swim_text].uid == 3
    assert sx._groups[walk_text].uid == 3
    assert sx._groups[fly_text].uid is None

    # WHEN
    sx.set_all_groupunits_uids_unique()

    # THEN
    print(f"{sx._groups[swim_text].uid=}")
    print(f"{sx._groups[walk_text].uid=}")
    assert sx._groups[swim_text].uid != sx._groups[walk_text].uid
    assert sx._groups[walk_text].uid != 3
    assert sx._groups[walk_text].uid != 3
    assert sx._groups[fly_text].uid != None


def test_contract_all_groupunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    owner_text = "Noa"
    sx = ContractUnit(_owner=owner_text)
    sx.set_partys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert sx._groups[swim_text].uid == 3
    assert sx._groups[walk_text].uid == 3
    assert sx._groups[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_groupunits_uids_are_unique() == False

    # WHEN2
    sx.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=4))

    # THEN
    assert sx.all_groupunits_uids_are_unique() == False

    # WHEN3
    sx.set_groupunit(groupunit=groupunit_shop(brand=fly_text, uid=5))

    # THEN
    assert sx.all_groupunits_uids_are_unique()


def test_get_partys_relevant_groups_CorrectlyReturnsEmptyDict():
    # GIVEN
    bob_text = "bob"
    cx_with_partys = ContractUnit(_owner=bob_text)
    cx_with_partys.set_partys_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    cx_with_partys.set_partyunit(partyunit=partyunit_shop(name=bob_text))
    cx_with_partys.set_partyunit(partyunit=partyunit_shop(name=sam_text))

    cx_with_groups = ContractUnit()
    cx_with_groups.set_partys_empty_if_null()
    cx_with_groups.set_groupunits_empty_if_null()

    # WHEN
    print(f"{len(cx_with_partys._partys)=} {len(cx_with_groups._groups)=}")
    relevant_x = get_partys_relevant_groups(
        cx_with_groups._groups, cx_with_partys._partys
    )

    # THEN
    assert relevant_x == {}


def test_get_partys_relevant_groups_CorrectlyReturns2SinglePartyGroups():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    cx_3groups = ContractUnit(_owner=bob_text)
    cx_3groups.set_partys_empty_if_null()
    cx_3groups.set_partyunit(partyunit=partyunit_shop(name=bob_text))
    cx_3groups.set_partyunit(partyunit=partyunit_shop(name=sam_text))
    cx_3groups.set_partyunit(partyunit=partyunit_shop(name=wil_text))

    cx_2partys = ContractUnit(_owner=bob_text)
    cx_2partys.set_partys_empty_if_null()
    cx_2partys.set_partyunit(partyunit=partyunit_shop(name=bob_text))
    cx_2partys.set_partyunit(partyunit=partyunit_shop(name=sam_text))

    # WHEN
    print(f"{len(cx_2partys._partys)=} {len(cx_3groups._groups)=}")
    mrg_x = get_partys_relevant_groups(cx_3groups._groups, cx_2partys._partys)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = ContractUnit(_owner=jes_text)
    bob_text = "Bob"
    jes_cx.set_partyunit(partyunit_shop(name=jes_text))
    jes_cx.set_partyunit(partyunit_shop(name=bob_text))

    hike_text = "hikers"
    jes_cx.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_cx._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_party_relevant_groups(jes_cx._groups, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_cx = ContractUnit(_owner=jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_cx.set_partyunit(partyunit_shop(name=jes_text))
    jes_cx.set_partyunit(partyunit_shop(name=bob_text))
    jes_cx.set_partyunit(partyunit_shop(name=noa_text))
    jes_cx.set_partyunit(partyunit_shop(name=eli_text))

    swim_text = "swimmers"
    jes_cx.set_groupunit(groupunit_shop(brand=swim_text))
    swim_group = jes_cx._groups.get(swim_text)
    swim_group.set_partylink(partylink_shop(bob_text))

    hike_text = "hikers"
    jes_cx.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_cx._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))
    hike_group.set_partylink(partylink_shop(noa_text))

    hunt_text = "hunters"
    jes_cx.set_groupunit(groupunit_shop(brand=hunt_text))
    hike_group = jes_cx._groups.get(hunt_text)
    hike_group.set_partylink(partylink_shop(noa_text))
    hike_group.set_partylink(partylink_shop(eli_text))

    # WHEN
    print(f"{len(jes_cx._partys)=} {len(jes_cx._groups)=}")
    bob_mrg = get_party_relevant_groups(jes_cx._groups, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
