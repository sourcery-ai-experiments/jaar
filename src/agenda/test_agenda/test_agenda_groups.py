from src.agenda.group import GroupBrand, balancelink_shop, groupunit_shop
from src.agenda.party import PartyPID, partyunit_shop, partylink_shop
from src.agenda.idea import ideacore_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as examples_agenda_v001,
)
from src.agenda.agenda import (
    agendaunit_shop,
    get_partys_relevant_groups,
    get_party_relevant_groups,
)
from pytest import raises as pytest_raises


def test_agenda_groups_get_groupunit_ReturnsCorrectObj():
    # GIVEN
    x_agenda = agendaunit_shop()
    swim_text = "swim"
    # x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text))
    swim_groups = {swim_text: groupunit_shop(brand=swim_text)}
    x_agenda._groups = swim_groups

    # WHEN
    swim_groupunit = x_agenda.get_groupunit(swim_text)

    # THEN
    assert swim_groupunit == groupunit_shop(brand=swim_text)


def test_agenda_groups_set_groupunit_worksCorrectly():
    # GIVEN
    swim_text = "swim"
    x_agenda = agendaunit_shop()

    # WHEN
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text))

    # THEN
    assert len(x_agenda._groups) == 1
    swim_groups = {swim_text: groupunit_shop(brand=swim_text)}
    assert len(x_agenda._groups) == len(swim_groups)
    assert x_agenda.get_groupunit(swim_text) != None
    swim_groupunit = x_agenda.get_groupunit(swim_text)
    assert swim_groupunit._partys == swim_groups.get(swim_text)._partys
    assert x_agenda.get_groupunit(swim_text) == swim_groups.get(swim_text)
    assert x_agenda._groups == swim_groups


def test_agenda_groups_set_groupunit_CorrectlyReplacesGroup():
    # GIVEN
    swim_text = "swim"
    x_agenda = agendaunit_shop()
    swim1_uid = 1
    swim1_group = groupunit_shop(swim_text, uid=swim1_uid)
    bob_text = "Bob"
    swim1_group.set_partylink(partylink_shop(bob_text))
    x_agenda.set_groupunit(swim1_group)
    assert len(x_agenda.get_groupunit(swim_text)._partys) == 1

    # WHEN
    yao_text = "Yao"
    swim2_uid = 2
    swim2_group = groupunit_shop(swim_text, uid=swim2_uid)
    swim2_group.set_partylink(partylink_shop(bob_text))
    swim2_group.set_partylink(partylink_shop(yao_text))
    x_agenda.set_groupunit(swim2_group, replace=False)

    # THEN
    assert x_agenda.get_groupunit(swim_text).uid == swim1_uid
    assert len(x_agenda.get_groupunit(swim_text)._partys) == 1

    # WHEN / THEN
    x_agenda.set_groupunit(swim2_group, replace=True)
    assert x_agenda.get_groupunit(swim_text).uid == swim2_uid
    assert len(x_agenda.get_groupunit(swim_text)._partys) == 2


def test_agenda_groups_set_groupunit_CorrectlySets_partylinks():
    # GIVEN
    swim_text = "swim"
    x_agenda = agendaunit_shop()
    swim1_uid = 1
    swim1_group = groupunit_shop(swim_text, uid=swim1_uid)
    bob_text = "Bob"
    swim1_group.set_partylink(partylink_shop(bob_text))
    x_agenda.set_groupunit(swim1_group)
    assert x_agenda.get_groupunit(swim_text).uid == swim1_uid
    assert len(x_agenda.get_groupunit(swim_text)._partys) == 1

    # WHEN
    yao_text = "Yao"
    swim2_uid = 2
    swim2_group = groupunit_shop(swim_text, uid=swim2_uid)
    swim2_group.set_partylink(partylink_shop(bob_text))
    swim2_group.set_partylink(partylink_shop(yao_text))
    x_agenda.set_groupunit(swim2_group, add_partylinks=True)

    # THEN
    assert x_agenda.get_groupunit(swim_text).uid == swim1_uid
    assert len(x_agenda.get_groupunit(swim_text)._partys) == 2


def test_agenda_groups_del_groupunit_worksCorrectly():
    # GIVEN
    x_agenda = agendaunit_shop()
    swim_text = "swimmers"
    swim_group = groupunit_shop(brand=GroupBrand(swim_text))
    x_agenda.set_groupunit(y_groupunit=swim_group)
    assert x_agenda.get_groupunit(swim_text) != None

    # WHEN
    x_agenda.del_groupunit(groupbrand=swim_text)
    assert x_agenda.get_groupunit(swim_text) is None
    assert x_agenda._groups == {}


def test_example_has_groups():
    # GIVEN / WHEN
    x_agenda = examples_agenda_v001()

    # THEN
    assert x_agenda._groups != None
    assert len(x_agenda._groups) == 34
    everyone_partys_len = None
    everyone_group = x_agenda.get_groupunit("Everyone")
    everyone_partys_len = len(everyone_group._partys)
    assert everyone_partys_len == 22

    # WHEN
    x_agenda.set_agenda_metrics()
    idea_dict = x_agenda._idea_dict

    # THEN
    print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_agenda.make_l1_road("D&B"))
    print(f"{db_idea._label=} {db_idea._balancelinks=}")
    assert len(db_idea._balancelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._balancelinks=}")
    #         db_balancelink_len = len(idea._balancelinks)
    # assert db_balancelink_len == 3


def test_agenda_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))

    assert len(x_agenda._partys) == 3
    assert len(x_agenda._groups) == 3
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(swim_text), pad=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)
    swim_road = x_agenda.make_road(prom_text, swim_text)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    assert x_agenda._idearoot._balancelinks in (None, {})
    assert len(x_agenda._idearoot._kids[swim_text]._balancelinks) == 3

    x_agenda.add_idea(ideacore_shop("streets"), pad=swim_road)

    # WHEN
    idea_list = x_agenda.get_idea_list()

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
    assert len(x_agenda._idearoot._kids["swim"]._balanceheirs) == 3


def test_agenda_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))

    swim_text = "swim"
    swim_road = x_agenda.make_road(prom_text, swim_text)

    x_agenda.add_idea(ideacore_shop(swim_text), pad=prom_text)
    balancelink_rico = balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    balancelink_carm = balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    balancelink_patr = balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)

    swim_idea = x_agenda.get_idea_kid(swim_road)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    x_agenda.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    # idea_list = x_agenda.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._balancelinks}")
    # print(f"{idea_list[0]._balanceheirs}")
    # print(f"{idea_list[1]._balanceheirs}")
    assert len(x_agenda._idearoot._kids[swim_text]._balancelinks) == 3
    assert len(x_agenda._idearoot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    x_agenda.edit_idea_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_idea = x_agenda.get_idea_kid(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._balancelinks=}")
    print(f"{swim_idea._balanceheirs=}")

    assert len(x_agenda._idearoot._kids[swim_text]._balancelinks) == 2
    assert len(x_agenda._idearoot._kids[swim_text]._balanceheirs) == 2


def test_agenda_set_balancelink_CorrectlyCalculatesInheritedBalanceLinkAgendaImportance():
    # GIVEN
    x_agenda = agendaunit_shop("prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_agenda._idearoot.set_balancelink(balancelink=blink_rico)
    x_agenda._idearoot.set_balancelink(balancelink=blink_carm)
    x_agenda._idearoot.set_balancelink(balancelink=blink_patr)
    assert len(x_agenda._idearoot._balancelinks) == 3

    # WHEN
    idea_list = x_agenda.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._balanceheirs) == 3

    bheir_rico = idea_prom._balanceheirs.get(rico_text)
    bheir_carm = idea_prom._balanceheirs.get(carm_text)
    bheir_patr = idea_prom._balanceheirs.get(patr_text)
    assert bheir_rico._agenda_credit == 0.5
    assert bheir_rico._agenda_debt == 0.75
    assert bheir_carm._agenda_credit == 0.25
    assert bheir_carm._agenda_debt == 0.125
    assert bheir_patr._agenda_credit == 0.25
    assert bheir_patr._agenda_debt == 0.125
    assert (
        bheir_rico._agenda_credit
        + bheir_carm._agenda_credit
        + bheir_patr._agenda_credit
        == 1
    )
    assert (
        bheir_rico._agenda_debt + bheir_carm._agenda_debt + bheir_patr._agenda_debt == 1
    )

    # agenda_credit_sum = 0
    # agenda_debt_sum = 0
    # for group in x_agenda._idearoot._balanceheirs.values():
    #     print(f"{group=}")
    #     assert group._agenda_credit != None
    #     assert group._agenda_credit in [0.25, 0.5]
    #     assert group._agenda_debt != None
    #     assert group._agenda_debt in [0.75, 0.125]
    #     agenda_credit_sum += group._agenda_credit
    #     agenda_debt_sum += group._agenda_debt

    # assert agenda_credit_sum == 1
    # assert agenda_debt_sum == 1


def test_agenda_get_idea_list_CorrectlyCalculates1LevelAgendaGroupAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    blink_rico = balancelink_shop(brand=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(brand=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_agenda._idearoot.set_balancelink(balancelink=blink_rico)
    x_agenda._idearoot.set_balancelink(balancelink=blink_carm)
    x_agenda._idearoot.set_balancelink(balancelink=blink_patr)

    assert len(x_agenda._groups) == 3

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    group_rico = x_agenda.get_groupunit(rico_text)
    group_carm = x_agenda.get_groupunit(carm_text)
    group_patr = x_agenda.get_groupunit(patr_text)
    assert group_rico._agenda_credit == 0.5
    assert group_rico._agenda_debt == 0.75
    assert group_carm._agenda_credit == 0.25
    assert group_carm._agenda_debt == 0.125
    assert group_patr._agenda_credit == 0.25
    assert group_patr._agenda_debt == 0.125
    assert (
        group_rico._agenda_credit
        + group_carm._agenda_credit
        + group_patr._agenda_credit
        == 1
    )
    assert (
        group_rico._agenda_debt + group_carm._agenda_debt + group_patr._agenda_debt == 1
    )

    # WHEN
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(sele_text)))
    bl_sele = balancelink_shop(brand=sele_text, creditor_weight=37)
    x_agenda._idearoot.set_balancelink(balancelink=bl_sele)
    assert len(x_agenda._groups) == 4
    x_agenda.set_agenda_metrics()

    # THEN
    group_sele = x_agenda.get_groupunit(sele_text)
    assert group_rico._agenda_credit != 0.5
    assert group_rico._agenda_debt != 0.75
    assert group_carm._agenda_credit != 0.25
    assert group_carm._agenda_debt != 0.125
    assert group_patr._agenda_credit != 0.25
    assert group_patr._agenda_debt != 0.125
    assert group_sele._agenda_credit != None
    assert group_sele._agenda_debt != None
    assert (
        group_rico._agenda_credit
        + group_carm._agenda_credit
        + group_patr._agenda_credit
        + group_sele._agenda_credit
        == 1
    )
    assert (
        group_rico._agenda_debt
        + group_carm._agenda_debt
        + group_patr._agenda_debt
        + group_sele._agenda_debt
        == 1
    )


def test_agenda_get_idea_list_CorrectlyCalculates3levelAgendaGroupAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(swim_text), pad=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(x_agenda._groups) == 3

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    group_rico = x_agenda.get_groupunit(rico_text)
    group_carm = x_agenda.get_groupunit(carm_text)
    group_patr = x_agenda.get_groupunit(patr_text)
    assert group_rico._agenda_credit == 0.5
    assert group_rico._agenda_debt == 0.75
    assert group_carm._agenda_credit == 0.25
    assert group_carm._agenda_debt == 0.125
    assert group_patr._agenda_credit == 0.25
    assert group_patr._agenda_debt == 0.125
    assert (
        group_rico._agenda_credit
        + group_carm._agenda_credit
        + group_patr._agenda_credit
        == 1
    )
    assert (
        group_rico._agenda_debt + group_carm._agenda_debt + group_patr._agenda_debt == 1
    )


def test_agenda_get_idea_list_CorrectlyCalculatesGroupAgendaImportanceLWwithGroupEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    swim_text = "swim"
    x_agenda.add_idea(ideacore_shop(swim_text), pad=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(pid=PartyPID(patr_text)))
    rico_balancelink = balancelink_shop(
        brand=rico_text, creditor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        brand=carm_text, creditor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(brand=patr_text, creditor_weight=10)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_agenda._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    x_agenda.add_idea(ideacore_shop("hunt", _weight=3), pad="prom")

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._idearoot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    group_rico = x_agenda.get_groupunit(rico_text)
    group_carm = x_agenda.get_groupunit(carm_text)
    group_patr = x_agenda.get_groupunit(patr_text)
    assert group_rico._agenda_credit == 0.125
    assert group_rico._agenda_debt == 0.1875
    assert group_carm._agenda_credit == 0.0625
    assert group_carm._agenda_debt == 0.03125
    assert group_patr._agenda_credit == 0.0625
    assert group_patr._agenda_debt == 0.03125
    assert (
        group_rico._agenda_credit
        + group_carm._agenda_credit
        + group_patr._agenda_credit
        == 0.25
    )
    assert (
        group_rico._agenda_debt + group_carm._agenda_debt + group_patr._agenda_debt
        == 0.25
    )


def test_agenda_edit_groupunit_brand_CorrectlyCreatesNewPID():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(pid=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(partylink=partylink_shop(pid=rico_text))
    agenda.set_groupunit(swim_group)
    assert len(agenda._partys) == 1
    assert len(agenda._groups) == 2
    assert agenda.get_groupunit(swim_text) != None
    assert agenda.get_groupunit(swim_text).uid == 13
    assert agenda.get_groupunit(swim_text)._single_party == False
    assert len(agenda.get_groupunit(swim_text)._partys) == 1

    # WHEN
    jog_text = "jog"
    agenda.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert agenda.get_groupunit(jog_text) != None
    assert agenda.get_groupunit(jog_text).uid == 13
    assert agenda.get_groupunit(swim_text) is None
    assert len(agenda._partys) == 1
    assert len(agenda._groups) == 2
    assert agenda.get_groupunit(jog_text)._single_party == False
    assert len(agenda.get_groupunit(jog_text)._partys) == 1


def test_agenda_edit_Groupunit_brand_raiseErrorNewPIDPreviouslyExists():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(pid=rico_text)
    swim_text = "swim"
    agenda.set_groupunit(groupunit_shop(brand=swim_text, uid=13))
    jog_text = "jog"
    agenda.set_groupunit(groupunit_shop(brand=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        agenda.edit_groupunit_brand(
            old_brand=swim_text,
            new_brand=jog_text,
            allow_group_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Group '{swim_text}' change to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_agenda_edit_groupunit_brand_CorrectlyMeldPIDs():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(pid=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(brand=swim_text, uid=13)
    swim_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=5, debtor_weight=3)
    )
    agenda.set_groupunit(swim_group)
    jog_text = "jog"
    jog_group = groupunit_shop(brand=jog_text, uid=13)
    jog_group.set_partylink(
        partylink=partylink_shop(pid=rico_text, creditor_weight=7, debtor_weight=10)
    )
    agenda.set_groupunit(jog_group)
    print(f"{agenda.get_groupunit(jog_text)._partys.get(rico_text)=}")
    assert agenda.get_groupunit(jog_text) != None
    assert agenda.get_groupunit(jog_text).uid == 13

    # WHEN
    agenda.edit_groupunit_brand(
        old_brand=swim_text,
        new_brand=jog_text,
        allow_group_overwite=True,
    )

    # THEN
    assert agenda.get_groupunit(jog_text) != None
    assert agenda.get_groupunit(swim_text) is None
    assert len(agenda._partys) == 1
    assert len(agenda._groups) == 2
    assert agenda.get_groupunit(jog_text)._single_party == False
    assert len(agenda.get_groupunit(jog_text)._partys) == 1
    assert agenda.get_groupunit(jog_text)._partys.get(rico_text).creditor_weight == 12
    assert agenda.get_groupunit(jog_text)._partys.get(rico_text).debtor_weight == 13


def test_agenda_edit_groupunit_brand_CorrectlyChangesBalanceLinks():
    # GIVEN
    x_agenda = agendaunit_shop("prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    x_agenda.set_groupunit(swim_groupunit)
    outdoor_text = "outdoors"
    outdoor_road = x_agenda.make_road(x_agenda._healer, outdoor_text)
    camping_text = "camping"
    camping_road = x_agenda.make_road(outdoor_road, camping_text)
    x_agenda.add_idea(ideacore_shop(camping_text), pad=outdoor_road)

    camping_idea = x_agenda.get_idea_kid(camping_road)
    swim_balancelink = balancelink_shop(
        brand=swim_groupunit.brand, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    x_agenda.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=False
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 5
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 3


def test_agenda_edit_groupunit_brand_CorrectlyMeldsBalanceLinesBalanceLinksBalanceHeirs():
    # GIVEN
    x_agenda = agendaunit_shop("prom")
    rico_text = "rico"
    x_agenda.add_partyunit(pid=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(brand=swim_text, uid=13)
    x_agenda.set_groupunit(swim_groupunit)

    jog_text = "jog"
    jog_groupunit = groupunit_shop(brand=jog_text, uid=13)
    x_agenda.set_groupunit(jog_groupunit)

    outdoor_text = "outdoors"
    outdoor_road = x_agenda.make_road(x_agenda._healer, outdoor_text)
    camping_text = "camping"
    camping_road = x_agenda.make_road(outdoor_road, camping_text)
    x_agenda.add_idea(ideacore_shop(camping_text), pad=outdoor_road)

    camping_idea = x_agenda.get_idea_kid(camping_road)
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
    x_agenda.edit_groupunit_brand(
        old_brand=swim_text, new_brand=jog_text, allow_group_overwite=True
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).creditor_weight == 12
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 13


def test_agenda_add_idea_CreatesMissingGroups():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    work_road = x_agenda.make_l1_road("work")
    new_idea_parent_road = x_agenda.make_road(work_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideacore_shop(
        _weight=40, _label=clean_cookery_text, promise=True
    )

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)
    assert len(x_agenda._groups) == 0
    assert x_agenda.get_groupunit(family_text) is None

    # WHEN
    x_agenda.add_idea(
        idea_kid=clean_cookery_idea,
        pad=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN
    assert len(x_agenda._groups) == 1
    assert x_agenda.get_groupunit(family_text) != None
    assert x_agenda.get_groupunit(family_text)._partys in (None, {})


def test_AgendaUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    x1_agenda = agendaunit_shop(healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_agenda.add_partyunit(pid=xia_text)
    x1_agenda.add_partyunit(pid=zoa_text)

    work_text = "work"
    work_road = x1_agenda.make_road(x1_agenda._economy_id, work_text)
    swim_text = "swim"
    swim_road = x1_agenda.make_road(x1_agenda._economy_id, swim_text)
    x1_agenda.add_idea(ideacore_shop(work_text), pad=x1_agenda._economy_id)
    x1_agenda.add_idea(ideacore_shop(swim_text), pad=x1_agenda._economy_id)
    x1_agenda.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(brand=xia_text)
    )
    x1_agenda.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(brand=zoa_text)
    )
    x1_agenda_swim_idea = x1_agenda.get_idea_kid(swim_road)
    assert len(x1_agenda_swim_idea._balancelinks) == 2
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.add_partyunit(pid=xia_text)

    # WHEN
    filtered_idea = x_agenda._get_filtered_balancelinks_idea(x1_agenda_swim_idea)

    # THEN
    assert len(filtered_idea._balancelinks) == 1
    assert list(filtered_idea._balancelinks.keys()) == [xia_text]


def test_AgendaUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    healer_text = "Noa"
    x1_agenda = agendaunit_shop(healer_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_agenda.add_partyunit(pid=xia_text)
    x1_agenda.add_partyunit(pid=zoa_text)

    work_text = "work"
    work_road = x1_agenda.make_road(x1_agenda._economy_id, work_text)
    swim_text = "swim"
    swim_road = x1_agenda.make_road(x1_agenda._economy_id, swim_text)
    x1_agenda.add_idea(ideacore_shop(work_text), pad=x1_agenda._economy_id)
    x1_agenda.add_idea(ideacore_shop(swim_text), pad=x1_agenda._economy_id)
    x1_agenda.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(brand=xia_text)
    )
    x1_agenda.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(brand=zoa_text)
    )
    x1_agenda_swim_idea = x1_agenda.get_idea_kid(swim_road)
    assert len(x1_agenda_swim_idea._balancelinks) == 2

    # WHEN
    x_agenda = agendaunit_shop(healer_text)
    x_agenda.add_partyunit(pid=xia_text)
    x_agenda.add_idea(
        idea_kid=x1_agenda_swim_idea,
        pad=x_agenda._economy_id,
        create_missing_ideas_groups=False,
    )

    # THEN
    x_agenda_swim_idea = x_agenda.get_idea_kid(swim_road)
    assert len(x_agenda_swim_idea._balancelinks) == 1
    assert list(x_agenda_swim_idea._balancelinks.keys()) == [xia_text]


def test_agenda_add_idea_DoesNotOverwriteGroups():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    work_road = x_agenda.make_l1_road("work")
    new_idea_parent_road = x_agenda.make_road(work_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideacore_shop(
        _weight=40, _label=clean_cookery_text, promise=True
    )

    family_text = "family"
    balancelink_z = balancelink_shop(brand=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(partylink=partylink_shop(pid="ann1"))
    groupunit_z.set_partylink(partylink=partylink_shop(pid="bet1"))
    x_agenda.set_groupunit(y_groupunit=groupunit_z)

    # assert len(x_agenda._groups) == 0
    # assert x_agenda.get_groupunit(family_text) is None
    assert len(x_agenda._groups) == 1
    assert len(x_agenda.get_groupunit(family_text)._partys) == 2

    # WHEN
    x_agenda.add_idea(
        idea_kid=clean_cookery_idea,
        pad=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN

    # assert len(x_agenda._groups) == 1
    # assert len(x_agenda.get_groupunit(family_text)._partys) == 0
    # groupunit_z = groupunit_shop(brand=family_text)
    # groupunit_z.set_partylink(partylink=partylink_shop(pid="ann2"))
    # groupunit_z.set_partylink(partylink=partylink_shop(pid="bet2"))
    # x_agenda.set_groupunit(y_groupunit=groupunit_z)

    assert len(x_agenda._groups) == 1
    assert len(x_agenda.get_groupunit(family_text)._partys) == 2


def test_agenda_set_groupunits_create_missing_partys_DoesCreateMissingPartys():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(pid=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(pid=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7

    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11

    assert len(x_agenda._partys) == 0
    assert len(x_agenda._groups) == 0

    # WHEN
    x_agenda.set_groupunit(y_groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(x_agenda._partys) == 2
    assert len(x_agenda._groups) == 3
    assert x_agenda._partys.get(anna_text).creditor_weight == 3
    assert x_agenda._partys.get(anna_text).debtor_weight == 7

    assert x_agenda._partys.get(beto_text).creditor_weight == 5
    assert x_agenda._partys.get(beto_text).debtor_weight == 11


def test_agenda_set_groupunits_create_missing_partys_DoesNotReplacePartys():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    x_agenda.set_partyunit(
        partyunit_shop(pid=anna_text, creditor_weight=17, debtor_weight=88)
    )
    x_agenda.set_partyunit(
        partyunit_shop(pid=beto_text, creditor_weight=46, debtor_weight=71)
    )
    groupunit_z = groupunit_shop(brand=family_text)
    groupunit_z.set_partylink(
        partylink=partylink_shop(pid=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_partylink(
        partylink=partylink_shop(pid=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._partys.get(anna_text).creditor_weight == 3
    assert groupunit_z._partys.get(anna_text).debtor_weight == 7
    assert groupunit_z._partys.get(beto_text).creditor_weight == 5
    assert groupunit_z._partys.get(beto_text).debtor_weight == 11
    assert len(x_agenda._partys) == 2
    assert x_agenda._partys.get(anna_text).creditor_weight == 17
    assert x_agenda._partys.get(anna_text).debtor_weight == 88
    assert x_agenda._partys.get(beto_text).creditor_weight == 46
    assert x_agenda._partys.get(beto_text).debtor_weight == 71

    # WHEN
    x_agenda.set_groupunit(y_groupunit=groupunit_z, create_missing_partys=True)

    # THEN
    assert len(x_agenda._partys) == 2
    assert x_agenda._partys.get(anna_text).creditor_weight == 17
    assert x_agenda._partys.get(anna_text).debtor_weight == 88
    assert x_agenda._partys.get(beto_text).creditor_weight == 46
    assert x_agenda._partys.get(beto_text).debtor_weight == 71


def test_agenda_get_groupunits_dict_CorrectlyReturnsDictOfGroups():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    swim_text = "swim"
    wiggle_text = "wiggle"
    fly_text = "fly"
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=wiggle_text))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=fly_text))
    assert len(x_agenda._groups) == 3

    # WHEN
    groupunit_list_x = x_agenda.get_groupunits_brand_list()

    # THEN
    assert groupunit_list_x[0] == ""
    assert groupunit_list_x[1] == fly_text
    assert groupunit_list_x[2] == swim_text
    assert groupunit_list_x[3] == wiggle_text
    assert len(groupunit_list_x) == 4


def test_agenda_set_all_groupunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=pad_text))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=fly_text))
    assert x_agenda._groups[swim_text].uid is None
    assert x_agenda._groups[pad_text].uid is None
    assert x_agenda._groups[fly_text].uid is None

    # WHEN
    x_agenda.set_all_groupunits_uids_unique()

    # THEN
    assert x_agenda._groups[swim_text].uid != None
    assert x_agenda._groups[pad_text].uid != None
    assert x_agenda._groups[fly_text].uid != None


def test_agenda_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    healer_text = "bob"
    x_agenda = agendaunit_shop(healer_text)
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text, uid=3))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=pad_text, uid=3))
    x_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=fly_text))
    assert x_agenda._groups[swim_text].uid == 3
    assert x_agenda._groups[pad_text].uid == 3
    assert x_agenda._groups[fly_text].uid is None

    # WHEN
    x_agenda.set_all_groupunits_uids_unique()

    # THEN
    print(f"{x_agenda._groups[swim_text].uid=}")
    print(f"{x_agenda._groups[pad_text].uid=}")
    assert x_agenda._groups[swim_text].uid != x_agenda._groups[pad_text].uid
    assert x_agenda._groups[pad_text].uid != 3
    assert x_agenda._groups[pad_text].uid != 3
    assert x_agenda._groups[fly_text].uid != None


def test_agenda_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    noa_text = "Noa"
    noa_agenda = agendaunit_shop(noa_text)
    swim_text = "swim"
    pad_text = "pad"
    fly_text = "fly"
    noa_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=swim_text, uid=3))
    noa_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=pad_text, uid=3))
    noa_agenda.set_groupunit(y_groupunit=groupunit_shop(brand=fly_text))
    assert noa_agenda._groups[swim_text].uid == 3
    assert noa_agenda._groups[pad_text].uid == 3
    assert noa_agenda._groups[fly_text].uid is None

    # WHEN
    noa_agenda.set_all_groupunits_uids_unique()

    # THEN
    print(f"{noa_agenda._groups[swim_text].uid=}")
    print(f"{noa_agenda._groups[pad_text].uid=}")
    assert noa_agenda._groups[swim_text].uid != noa_agenda._groups[pad_text].uid
    assert noa_agenda._groups[pad_text].uid != 3
    assert noa_agenda._groups[pad_text].uid != 3
    assert noa_agenda._groups[fly_text].uid != None


def test_agenda_all_groupunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    healer_text = "Noa"
    agenda = agendaunit_shop(healer_text)
    swim_text = "swim"
    run_text = "run"
    fly_text = "fly"
    climb_text = "climb"
    agenda.set_groupunit(groupunit_shop(brand=swim_text, uid=3))
    agenda.set_groupunit(groupunit_shop(brand=run_text, uid=3))
    agenda.set_groupunit(groupunit_shop(brand=fly_text))
    assert agenda._groups[swim_text].uid == 3
    assert agenda._groups[run_text].uid == 3
    assert agenda._groups[fly_text].uid is None

    # WHEN1 / THEN
    assert agenda.all_groupunits_uids_are_unique() == False

    # WHEN2
    agenda.set_groupunit(groupunit_shop(brand=swim_text, uid=4))
    # THEN
    assert agenda.all_groupunits_uids_are_unique() == False

    # WHEN3
    agenda.del_groupunit(groupbrand=fly_text)
    # THEN
    assert agenda.all_groupunits_uids_are_unique()

    # WHEN
    agenda.set_groupunit(groupunit_shop(brand=fly_text, uid=5))
    # THEN
    assert agenda.all_groupunits_uids_are_unique()

    # WHEN
    agenda.set_groupunit(groupunit_shop(brand=fly_text, uid=5))
    # THEN
    assert agenda.all_groupunits_uids_are_unique()

    # WHEN
    agenda.set_groupunit(groupunit_shop(brand=climb_text, uid=13))
    # THEN
    assert agenda.all_groupunits_uids_are_unique()


def test_get_partys_relevant_groups_CorrectlyReturnsEmptyDict():
    # GIVEN
    bob_text = "bob"
    agenda_with_partys = agendaunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    agenda_with_partys.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    agenda_with_partys.set_partyunit(partyunit=partyunit_shop(pid=sam_text))

    agenda_with_groups = agendaunit_shop()

    # WHEN
    print(f"{len(agenda_with_partys._partys)=} {len(agenda_with_groups._groups)=}")
    relevant_x = get_partys_relevant_groups(
        agenda_with_groups._groups, agenda_with_partys._partys
    )

    # THEN
    assert relevant_x == {}


def test_get_partys_relevant_groups_CorrectlyReturns2SinglePartyGroups():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    agenda_3groups = agendaunit_shop(bob_text)
    agenda_3groups.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    agenda_3groups.set_partyunit(partyunit=partyunit_shop(pid=sam_text))
    agenda_3groups.set_partyunit(partyunit=partyunit_shop(pid=wil_text))

    agenda_2partys = agendaunit_shop(bob_text)
    agenda_2partys.set_partyunit(partyunit=partyunit_shop(pid=bob_text))
    agenda_2partys.set_partyunit(partyunit=partyunit_shop(pid=sam_text))

    # WHEN
    print(f"{len(agenda_2partys._partys)=} {len(agenda_3groups._groups)=}")
    mrg_x = get_partys_relevant_groups(agenda_3groups._groups, agenda_2partys._partys)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(jes_text)
    bob_text = "Bob"
    jes_agenda.set_partyunit(partyunit_shop(pid=jes_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=bob_text))

    hike_text = "hikers"
    jes_agenda.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_agenda.get_groupunit(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_party_relevant_groups(jes_agenda._groups, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_party_relevant_groups_CorrectlyReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_agenda.set_partyunit(partyunit_shop(pid=jes_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(pid=eli_text))

    swim_text = "swimmers"
    jes_agenda.set_groupunit(groupunit_shop(brand=swim_text))
    swim_group = jes_agenda.get_groupunit(swim_text)
    swim_group.set_partylink(partylink_shop(bob_text))

    hike_text = "hikers"
    jes_agenda.set_groupunit(groupunit_shop(brand=hike_text))
    hike_group = jes_agenda.get_groupunit(hike_text)
    hike_group.set_partylink(partylink_shop(bob_text))
    hike_group.set_partylink(partylink_shop(noa_text))

    hunt_text = "hunters"
    jes_agenda.set_groupunit(groupunit_shop(brand=hunt_text))
    hike_group = jes_agenda.get_groupunit(hunt_text)
    hike_group.set_partylink(partylink_shop(noa_text))
    hike_group.set_partylink(partylink_shop(eli_text))

    # WHEN
    print(f"{len(jes_agenda._partys)=} {len(jes_agenda._groups)=}")
    bob_mrg = get_party_relevant_groups(jes_agenda._groups, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
