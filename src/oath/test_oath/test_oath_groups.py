from src.oath.group import GroupBrand, balancelink_shop, groupunit_shop
from src.oath.party import PartyTitle, partyunit_shop, partylink_shop
from src.oath.idea import IdeaKid
from src.oath.required_idea import Road
from src.oath.examples.example_oaths import (
    oath_v001 as examples_oath_v001,
)
from src.oath.oath import (
    OathUnit,
    get_partys_relevant_groups,
    get_party_relevant_groups,
)
from pytest import raises as pytest_raises


def test_oath_groups_set_groupunit_worksCorrectly():
    # GIVEN
    cx = OathUnit()
    assert cx._groups is None
    swim_text = "swim"
    groupbrand_x = GroupBrand(swim_text)
    every1_groups = {groupbrand_x: groupunit_shop(brand=groupbrand_x)}
    cx2 = OathUnit()

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


def test_oath_groups_del_groupunit_worksCorrectly():
    # GIVEN
    oath = OathUnit()
    swim_text = "swimmers"
    group_x = groupunit_shop(brand=GroupBrand(swim_text))
    oath.set_groupunit(groupunit=group_x)
    assert oath._groups.get(swim_text) != None

    # WHEN
    oath.del_groupunit(groupbrand=swim_text)
    assert oath._groups.get(swim_text) is None
    assert oath._groups == {}


def test_example_has_groups():
    # GIVEN / WHEN
    cx = examples_oath_v001()

    # THEN
    assert cx._groups != None
    assert len(cx._groups) == 34
    everyone_partys_len = None
    everyone_group = cx._groups.get("Everyone")
    everyone_partys_len = len(everyone_group._partys)
    assert everyone_partys_len == 22

    # WHEN
    cx.set_oath_metrics()
    idea_dict = cx._idea_dict

    # THEN
    db_idea = idea_dict.get(f"{cx._cure_handle},D&B")
    print(f"{db_idea._label=} {db_idea._balancelinks=}")
    assert len(db_idea._balancelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._balancelinks=}")
    #         db_balancelink_len = len(idea._balancelinks)
    # assert db_balancelink_len == 3


def test_oath_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    prom_text = "prom"
    cx = OathUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    cx.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    cx.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))

    assert len(cx._partys) == 3
    assert len(cx._groups) == 3
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)
    swim_road = f"{prom_text},{swim_text}"
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    cx.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    assert cx._idearoot._balancelinks in (None, {})
    assert len(cx._idearoot._kids[swim_text]._balancelinks) == 3

    cx.add_idea(idea_kid=IdeaKid(_label="streets"), pad=swim_road)

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


def test_oath_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_oath = OathUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))

    swim_text = "swim"
    swim_road = f"{prom_text},{swim_text}"

    x_oath.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)

    swim_idea = x_oath.get_idea_kid(road=swim_road)
    x_oath.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    x_oath.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    x_oath.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    # idea_list = x_oath.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._balancelinks}")
    # print(f"{idea_list[0]._balanceheirs}")
    # print(f"{idea_list[1]._balanceheirs}")
    assert len(x_oath._idearoot._kids[swim_text]._balancelinks) == 3
    assert len(x_oath._idearoot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    x_oath.edit_idea_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_idea = x_oath.get_idea_kid(road=swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._balancelinks=}")
    print(f"{swim_idea._balanceheirs=}")

    assert len(x_oath._idearoot._kids[swim_text]._balancelinks) == 2
    assert len(x_oath._idearoot._kids[swim_text]._balanceheirs) == 2


def test_oath_set_balancelink_CorrectlyCalculatesInheritedBalancelinkOathImportance():
    # GIVEN
    x_oath = OathUnit(_healer="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_oath._idearoot.set_balancelink(balancelink=blink_rico)
    x_oath._idearoot.set_balancelink(balancelink=blink_carm)
    x_oath._idearoot.set_balancelink(balancelink=blink_patr)
    assert len(x_oath._idearoot._balancelinks) == 3

    # WHEN
    idea_list = x_oath.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._balanceheirs) == 3

    bheir_rico = idea_prom._balanceheirs.get(rico_text)
    bheir_carm = idea_prom._balanceheirs.get(carm_text)
    bheir_patr = idea_prom._balanceheirs.get(patr_text)
    assert bheir_rico._oath_credit == 0.5
    assert bheir_rico._oath_debt == 0.75
    assert bheir_carm._oath_credit == 0.25
    assert bheir_carm._oath_debt == 0.125
    assert bheir_patr._oath_credit == 0.25
    assert bheir_patr._oath_debt == 0.125
    assert (
        bheir_rico._oath_credit + bheir_carm._oath_credit + bheir_patr._oath_credit == 1
    )
    assert bheir_rico._oath_debt + bheir_carm._oath_debt + bheir_patr._oath_debt == 1

    # oath_credit_sum = 0
    # oath_debt_sum = 0
    # for group in x_oath._idearoot._balanceheirs.values():
    #     print(f"{group=}")
    #     assert group._oath_credit != None
    #     assert group._oath_credit in [0.25, 0.5]
    #     assert group._oath_debt != None
    #     assert group._oath_debt in [0.75, 0.125]
    #     oath_credit_sum += group._oath_credit
    #     oath_debt_sum += group._oath_debt

    # assert oath_credit_sum == 1
    # assert oath_debt_sum == 1


def test_oath_get_idea_list_CorrectlyCalculates1LevelOathGroupOathImportance():
    # GIVEN
    prom_text = "prom"
    x_oath = OathUnit(_healer=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_oath._idearoot.set_balancelink(balancelink=blink_rico)
    x_oath._idearoot.set_balancelink(balancelink=blink_carm)
    x_oath._idearoot.set_balancelink(balancelink=blink_patr)

    assert len(x_oath._groups) == 3

    # WHEN
    x_oath.set_oath_metrics()

    # THEN
    group_rico = x_oath._groups.get(rico_text)
    group_carm = x_oath._groups.get(carm_text)
    group_patr = x_oath._groups.get(patr_text)
    assert group_rico._oath_credit == 0.5
    assert group_rico._oath_debt == 0.75
    assert group_carm._oath_credit == 0.25
    assert group_carm._oath_debt == 0.125
    assert group_patr._oath_credit == 0.25
    assert group_patr._oath_debt == 0.125
    assert (
        group_rico._oath_credit + group_carm._oath_credit + group_patr._oath_credit == 1
    )
    assert group_rico._oath_debt + group_carm._oath_debt + group_patr._oath_debt == 1

    # WHEN
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(sele_text)))
    bl_sele = balancelink_shop(brand=sele_text, creditor_weight=37)
    x_oath._idearoot.set_balancelink(balancelink=bl_sele)
    assert len(x_oath._groups) == 4
    x_oath.set_oath_metrics()

    # THEN
    group_sele = x_oath._groups.get(sele_text)
    assert group_rico._oath_credit != 0.5
    assert group_rico._oath_debt != 0.75
    assert group_carm._oath_credit != 0.25
    assert group_carm._oath_debt != 0.125
    assert group_patr._oath_credit != 0.25
    assert group_patr._oath_debt != 0.125
    assert group_sele._oath_credit != None
    assert group_sele._oath_debt != None
    assert (
        group_rico._oath_credit
        + group_carm._oath_credit
        + group_patr._oath_credit
        + group_sele._oath_credit
        == 1
    )
    assert (
        group_rico._oath_debt
        + group_carm._oath_debt
        + group_patr._oath_debt
        + group_sele._oath_debt
        == 1
    )


def test_oath_get_idea_list_CorrectlyCalculates3levelOathGroupOathImportance():
    # GIVEN
    prom_text = "prom"
    x_oath = OathUnit(_healer=prom_text)
    swim_text = "swim"
    x_oath.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(x_oath._groups) == 3

    # WHEN
    x_oath.set_oath_metrics()

    # THEN
    group_rico = x_oath._groups.get(rico_text)
    group_carm = x_oath._groups.get(carm_text)
    group_patr = x_oath._groups.get(patr_text)
    assert group_rico._oath_credit == 0.5
    assert group_rico._oath_debt == 0.75
    assert group_carm._oath_credit == 0.25
    assert group_carm._oath_debt == 0.125
    assert group_patr._oath_credit == 0.25
    assert group_patr._oath_debt == 0.125
    assert (
        group_rico._oath_credit + group_carm._oath_credit + group_patr._oath_credit == 1
    )
    assert group_rico._oath_debt + group_carm._oath_debt + group_patr._oath_debt == 1


def test_oath_get_idea_list_CorrectlyCalculatesGroupOathImportanceLWwithGroupEmptyBranch():
    # GIVEN
    prom_text = "prom"
    x_oath = OathUnit(_healer=prom_text)
    swim_text = "swim"
    x_oath.add_idea(idea_kid=IdeaKid(_label=swim_text), pad=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(rico_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(carm_text)))
    x_oath.set_partyunit(partyunit=partyunit_shop(title=PartyTitle(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_oath._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    x_oath.add_idea(idea_kid=IdeaKid(_label="hunt", _weight=3), pad="prom")

    assert x_oath._idearoot._balancelinks is None

    # WHEN
    x_oath.set_oath_metrics()

    # THEN
    assert x_oath._idearoot._balancelinks == {}

    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_oath._idearoot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    group_rico = x_oath._groups.get(rico_text)
    group_carm = x_oath._groups.get(carm_text)
    group_patr = x_oath._groups.get(patr_text)
    assert group_rico._oath_credit == 0.125
    assert group_rico._oath_debt == 0.1875
    assert group_carm._oath_credit == 0.0625
    assert group_carm._oath_debt == 0.03125
    assert group_patr._oath_credit == 0.0625
    assert group_patr._oath_debt == 0.03125
    assert (
        group_rico._oath_credit + group_carm._oath_credit + group_patr._oath_credit
        == 0.25
    )
    assert group_rico._oath_debt + group_carm._oath_debt + group_patr._oath_debt == 0.25


def test_oath_edit_groupunit_brand_CorrectlyCreatesNewTitle():
    # GIVEN
    oath = OathUnit(_healer="prom")
    rico_text = "rico"
    oath.add_partyunit(title=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(partylink=partylink_shop(title=rico_text))
    oath.set_groupunit(swim_group)
    assert len(oath._partys) == 1
    assert len(oath._groups) == 2
    assert oath._groups.get(swim_text) != None
    assert oath._groups.get(swim_text).uid == 13
    assert oath._groups.get(swim_text)._single_party == False
    assert len(oath._groups.get(swim_text)._partys) == 1

    # WHEN
    jog_text = "jog"
    oath.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert oath._groups.get(jog_text) != None
    assert oath._groups.get(jog_text).uid == 13
    assert oath._groups.get(swim_text) is None
    assert len(oath._partys) == 1
    assert len(oath._groups) == 2
    assert oath._groups.get(jog_text)._single_party == False
    assert len(oath._groups.get(jog_text)._partys) == 1


def test_oath_edit_Groupunit_brand_raiseErrorNewTitlePreviouslyExists():
    # GIVEN
    oath = OathUnit(_healer="prom")
    rico_text = "rico"
    oath.add_partyunit(title=rico_text)
    swim_text = "swim"
    oath.set_groupunit(groupunit_shop(brand=swim_text, uid=13))
    jog_text = "jog"
    oath.set_groupunit(groupunit_shop(brand=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        oath.edit_groupunit_brand(
            old_brand=swim_text,
            new_brand=jog_text,
            allow_group_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Group '{swim_text}' change to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_oath_edit_groupunit_brand_CorrectlyMeldTitles():
    # GIVEN
    oath = OathUnit(_healer="prom")
    rico_text = "rico"
    oath.add_partyunit(title=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=5, debtor_weight=3)
    )
    oath.set_groupunit(swim_group)
    jog_text = "jog"
    jog_group = groupunit_shop(brand=jog_text, uid=13)
    jog_group.set_partylink(
        partylink=partylink_shop(title=rico_text, creditor_weight=7, debtor_weight=10)
    )
    oath.set_groupunit(jog_group)
    print(f"{oath._groups.get(jog_text)._partys.get(rico_text)=}")
    assert oath._groups.get(jog_text) != None
    assert oath._groups.get(jog_text).uid == 13

    # WHEN
    oath.edit_groupunit_brand(
        old_brand=swim_text,
        new_brand=jog_text,
        allow_group_overwite=True,
    )

    # THEN
    assert oath._groups.get(jog_text) != None
    assert oath._groups.get(swim_text) is None
    assert len(oath._partys) == 1
    assert len(oath._groups) == 2
    assert oath._groups.get(jog_text)._single_party == False
    assert len(oath._groups.get(jog_text)._partys) == 1
    assert oath._groups.get(jog_text)._partys.get(rico_text).creditor_weight == 12
    assert oath._groups.get(jog_text)._partys.get(rico_text).debtor_weight == 13


def test_oath_edit_groupunit_brand_CorrectlyChangesBalancelinks():
    # GIVEN
    x_oath = OathUnit(_healer="prom")
    rico_text = "rico"
    x_oath.add_partyunit(title=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    x_oath.set_groupunit(swim_groupunit)
    outdoor_text = "outdoors"
    outdoor_road = Road(f"{x_oath._healer},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{x_oath._healer},{outdoor_text},{camping_text}")
    x_oath.add_idea(pad=outdoor_road, idea_kid=IdeaKid(_label=camping_text))

    camping_idea = x_oath.get_idea_kid(camping_road)
    swim_balancelink = balancelink_shop(
        brand=swim_groupunit.brand, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    x_oath.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 3


def test_oath_edit_groupunit_brand_CorrectlyMeldsBalancelinesBalancelinksBalanceHeirs():
    # GIVEN
    x_oath = OathUnit(_healer="prom")
    rico_text = "rico"
    x_oath.add_partyunit(title=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    x_oath.set_groupunit(swim_groupunit)

    jog_text = "jog"
    jog_groupunit = groupunit_shop(brand=jog_text, uid=13)
    x_oath.set_groupunit(jog_groupunit)

    outdoor_text = "outdoors"
    outdoor_road = Road(f"{x_oath._healer},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{x_oath._healer},{outdoor_text},{camping_text}")
    x_oath.add_idea(pad=outdoor_road, idea_kid=IdeaKid(_label=camping_text))

    camping_idea = x_oath.get_idea_kid(camping_road)
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
    x_oath.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=True
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 12
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 13


def test_oath_add_idea_CreatesMissingGroups():
    # GIVEN
    healer_text = "bob"
    x_oath = OathUnit(_healer=healer_text)
    x_oath.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{x_oath._cure_handle},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _label=clean_cookery_text, promise=True)

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)
    assert len(x_oath._groups) == 0
    assert x_oath._groups.get(family_text) is None

    # WHEN
    x_oath.add_idea(
        idea_kid=clean_cookery_idea,
        pad=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN
    assert len(x_oath._groups) == 1
    assert x_oath._groups.get(family_text) != None
    assert x_oath._groups.get(family_text)._partys in (None, {})


def test_OathUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    cx1 = OathUnit(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(title=xia_text)
    cx1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{cx1._cure_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._cure_handle},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), pad=cx1._cure_handle)
    cx1.add_idea(IdeaKid(_label=swim_text), pad=cx1._cure_handle)
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=xia_text))
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=zoa_text))
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    assert len(cx1_swim_idea._balancelinks) == 2
    cx2 = OathUnit(_healer=healer_text)
    cx2.add_partyunit(title=xia_text)

    # WHEN
    filtered_idea = cx2._get_filtered_balancelinks_idea(cx1_swim_idea)

    # THEN
    assert len(filtered_idea._balancelinks) == 1
    assert list(filtered_idea._balancelinks.keys()) == [xia_text]


def test_OathUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    cx1 = OathUnit(_healer=healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    cx1.add_partyunit(title=xia_text)
    cx1.add_partyunit(title=zoa_text)

    work_text = "work"
    work_road = f"{cx1._cure_handle},{work_text}"
    swim_text = "swim"
    swim_road = f"{cx1._cure_handle},{swim_text}"
    cx1.add_idea(IdeaKid(_label=work_text), pad=cx1._cure_handle)
    cx1.add_idea(IdeaKid(_label=swim_text), pad=cx1._cure_handle)
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=xia_text))
    cx1.edit_idea_attr(road=swim_road, balancelink=balancelink_shop(brand=zoa_text))
    cx1_swim_idea = cx1.get_idea_kid(swim_road)
    assert len(cx1_swim_idea._balancelinks) == 2

    # WHEN
    cx2 = OathUnit(_healer=healer_text)
    cx2.add_partyunit(title=xia_text)
    cx2.add_idea(
        idea_kid=cx1_swim_idea,
        pad=cx2._cure_handle,
        create_missing_ideas_groups=False,
    )

    # THEN
    cx2_swim_idea = cx2.get_idea_kid(swim_road)
    assert len(cx2_swim_idea._balancelinks) == 1
    assert list(cx2_swim_idea._balancelinks.keys()) == [xia_text]


def test_oath_add_idea_DoesNotOverwriteGroups():
    # GIVEN
    healer_text = "bob"
    x_oath = OathUnit(_healer=healer_text)
    x_oath.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{x_oath._cure_handle},work,cleaning"
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = IdeaKid(_weight=40, _label=clean_cookery_text, promise=True)

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(partylink=partylink_shop(title="ann1"))
    groupunit_z.set_partylink(partylink=partylink_shop(title="bet1"))
    x_oath.set_groupunit(groupunit=groupunit_z)

    # assert len(x_oath._groups) == 0
    # assert x_oath._groups.get(family_text) is None
    assert len(x_oath._groups) == 1
    assert len(x_oath._groups.get(family_text)._partys) == 2

    # WHEN
    x_oath.add_idea(
        idea_kid=clean_cookery_idea,
        pad=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN

    # assert len(x_oath._groups) == 1
    # assert len(x_oath._groups.get(family_text)._partys) == 0
    # groupunit_z = groupunit_shop(brand=family_text)
    # groupunit_z.set_partylink(partylink=partylink_shop(title="ann2"))
    # groupunit_z.set_partylink(partylink=partylink_shop(title="bet2"))
    # x_oath.set_groupunit(groupunit=groupunit_z)

    assert len(x_oath._groups) == 1
    assert len(x_oath._groups.get(family_text)._partys) == 2


def test_oath_set_groupunits_create_missing_partys_DoesCreateMissingPartys():
    # GIVEN
    healer_text = "bob"
    x_oath = OathUnit(_healer=healer_text)
    x_oath.set_partys_empty_if_null()
    x_oath.set_groupunits_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(title=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(title=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7

    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11

    assert len(x_oath._partys) == 0
    assert len(x_oath._groups) == 0

    # WHEN
    x_oath.set_groupunit(groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(x_oath._partys) == 2
    assert len(x_oath._groups) == 3
    assert x_oath._partys.get(anna_text).creditor_weight == 3
    assert x_oath._partys.get(anna_text).debtor_weight == 7

    assert x_oath._partys.get(beto_text).creditor_weight == 5
    assert x_oath._partys.get(beto_text).debtor_weight == 11


def test_oath_set_groupunits_create_missing_partys_DoesNotReplacePartys():
    # GIVEN
    healer_text = "bob"
    x_oath = OathUnit(_healer=healer_text)
    x_oath.set_partys_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    x_oath.set_partyunit(
        partyunit_shop(title=anna_text, creditor_weight=17, debtor_weight=88)
    )
    x_oath.set_partyunit(
        partyunit_shop(title=beto_text, creditor_weight=46, debtor_weight=71)
    )
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(title=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(title=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7
    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11
    assert len(x_oath._partys) == 2
    assert x_oath._partys.get(anna_text).creditor_weight == 17
    assert x_oath._partys.get(anna_text).debtor_weight == 88
    assert x_oath._partys.get(beto_text).creditor_weight == 46
    assert x_oath._partys.get(beto_text).debtor_weight == 71

    # WHEN
    x_oath.set_groupunit(groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(x_oath._partys) == 2
    assert x_oath._partys.get(anna_text).creditor_weight == 17
    assert x_oath._partys.get(anna_text).debtor_weight == 88
    assert x_oath._partys.get(beto_text).creditor_weight == 46
    assert x_oath._partys.get(beto_text).debtor_weight == 71


def test_oath_get_groupunits_dict_CorrectlyReturnsDictOfGroups():
    # GIVEN
    healer_text = "bob"
    oath = OathUnit(_healer=healer_text)
    oath.set_partys_empty_if_null()
    swim_text = "swim"
    wiggle_text = "wiggle"
    fly_text = "fly"
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text))
    oath.set_groupunit(groupunit=groupunit_shop(brand=wiggle_text))
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert len(oath._groups) == 3

    # WHEN
    groupunit_list_x = oath.get_groupunits_brand_list()

    # THEN
    assert groupunit_list_x[0] == ""
    assert groupunit_list_x[1] == fly_text
    assert groupunit_list_x[2] == swim_text
    assert groupunit_list_x[3] == wiggle_text
    assert len(groupunit_list_x) == 4


def test_oath_set_all_groupunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    healer_text = "bob"
    oath = OathUnit(_healer=healer_text)
    oath.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text))
    oath.set_groupunit(groupunit=groupunit_shop(brand=pad_text))
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert oath._groups[swim_text].uid is None
    assert oath._groups[pad_text].uid is None
    assert oath._groups[fly_text].uid is None

    # WHEN
    oath.set_all_groupunits_uids_unique()

    # THEN
    assert oath._groups[swim_text].uid != None
    assert oath._groups[pad_text].uid != None
    assert oath._groups[fly_text].uid != None


def test_oath_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "bob"
    oath = OathUnit(_healer=healer_text)
    oath.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=pad_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert oath._groups[swim_text].uid == 3
    assert oath._groups[pad_text].uid == 3
    assert oath._groups[fly_text].uid is None

    # WHEN
    oath.set_all_groupunits_uids_unique()

    # THEN
    print(f"{oath._groups[swim_text].uid=}")
    print(f"{oath._groups[pad_text].uid=}")
    assert oath._groups[swim_text].uid != oath._groups[pad_text].uid
    assert oath._groups[pad_text].uid != 3
    assert oath._groups[pad_text].uid != 3
    assert oath._groups[fly_text].uid != None


def test_oath_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "Noa"
    oath = OathUnit(_healer=healer_text)
    oath.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=pad_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert oath._groups[swim_text].uid == 3
    assert oath._groups[pad_text].uid == 3
    assert oath._groups[fly_text].uid is None

    # WHEN
    oath.set_all_groupunits_uids_unique()

    # THEN
    print(f"{oath._groups[swim_text].uid=}")
    print(f"{oath._groups[pad_text].uid=}")
    assert oath._groups[swim_text].uid != oath._groups[pad_text].uid
    assert oath._groups[pad_text].uid != 3
    assert oath._groups[pad_text].uid != 3
    assert oath._groups[fly_text].uid != None


def test_oath_all_groupunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    healer_text = "Noa"
    oath = OathUnit(_healer=healer_text)
    oath.set_partys_empty_if_null()
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=pad_text, uid=3))
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text))
    assert oath._groups[swim_text].uid == 3
    assert oath._groups[pad_text].uid == 3
    assert oath._groups[fly_text].uid is None

    # WHEN1 / THEN
    assert oath.all_groupunits_uids_are_unique() == False

    # WHEN2
    oath.set_groupunit(groupunit=groupunit_shop(brand=swim_text, uid=4))

    # THEN
    assert oath.all_groupunits_uids_are_unique() == False

    # WHEN3
    oath.set_groupunit(groupunit=groupunit_shop(brand=fly_text, uid=5))

    # THEN
    assert oath.all_groupunits_uids_are_unique()


def test_get_partys_relevant_groups_CorrectlyReturnsEmptyDict():
    # GIVEN
    bob_text = "bob"
    oath_with_partys = OathUnit(_healer=bob_text)
    oath_with_partys.set_partys_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    oath_with_partys.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    oath_with_partys.set_partyunit(partyunit=partyunit_shop(title=sam_text))

    oath_with_groups = OathUnit()
    oath_with_groups.set_partys_empty_if_null()
    oath_with_groups.set_groupunits_empty_if_null()

    # WHEN
    print(f"{len(oath_with_partys._partys)=} {len(oath_with_groups._groups)=}")
    relevant_x = get_partys_relevant_groups(
        oath_with_groups._groups, oath_with_partys._partys
    )

    # THEN
    assert relevant_x == {}


def test_get_partys_relevant_groups_CorrectlyReturns2SinglePartyGroups():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    oath_3groups = OathUnit(_healer=bob_text)
    oath_3groups.set_partys_empty_if_null()
    oath_3groups.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    oath_3groups.set_partyunit(partyunit=partyunit_shop(title=sam_text))
    oath_3groups.set_partyunit(partyunit=partyunit_shop(title=wil_text))

    oath_2partys = OathUnit(_healer=bob_text)
    oath_2partys.set_partys_empty_if_null()
    oath_2partys.set_partyunit(partyunit=partyunit_shop(title=bob_text))
    oath_2partys.set_partyunit(partyunit=partyunit_shop(title=sam_text))

    # WHEN
    print(f"{len(oath_2partys._partys)=} {len(oath_3groups._groups)=}")
    mrg_x = get_partys_relevant_groups(oath_3groups._groups, oath_2partys._partys)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_oath = OathUnit(_healer=jes_text)
    bob_text = "Bob"
    jes_oath.set_partyunit(partyunit_shop(title=jes_text))
    jes_oath.set_partyunit(partyunit_shop(title=bob_text))

    hike_text = "hikers"
    jes_oath.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_oath._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_party_relevant_groups(jes_oath._groups, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_oath = OathUnit(_healer=jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_oath.set_partyunit(partyunit_shop(title=jes_text))
    jes_oath.set_partyunit(partyunit_shop(title=bob_text))
    jes_oath.set_partyunit(partyunit_shop(title=noa_text))
    jes_oath.set_partyunit(partyunit_shop(title=eli_text))

    swim_text = "swimmers"
    jes_oath.set_groupunit(groupunit_shop(brand=swim_text))
    swim_group = jes_oath._groups.get(swim_text)
    swim_group.set_partylink(partylink_shop(bob_text))

    hike_text = "hikers"
    jes_oath.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_oath._groups.get(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))
    hike_group.set_partylink(partylink_shop(noa_text))

    hunt_text = "hunters"
    jes_oath.set_groupunit(groupunit_shop(brand=hunt_text))
    hike_group = jes_oath._groups.get(hunt_text)
    hike_group.set_partylink(partylink_shop(noa_text))
    hike_group.set_partylink(partylink_shop(eli_text))

    # WHEN
    print(f"{len(jes_oath._partys)=} {len(jes_oath._groups)=}")
    bob_mrg = get_party_relevant_groups(jes_oath._groups, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
