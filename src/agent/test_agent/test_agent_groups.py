from src.agent.group import GroupName, grouplink_shop, groupunit_shop
from src.agent.ally import AllyName, allyunit_shop, allylink_shop
from src.agent.idea import IdeaKid
from src.agent.required import Road
from src.agent.examples.example_agents import agent_v001 as examples_agent_v001
from src.agent.agent import AgentUnit
from pytest import raises as pytest_raises


def test_agent_groups_set_groupunit_worksCorrectly():
    # GIVEN
    lw_x = AgentUnit()
    assert lw_x._groups is None
    swim_text = "swim"
    groupname_x = GroupName(swim_text)
    every1_groups = {groupname_x: groupunit_shop(name=groupname_x)}
    lw_x2 = AgentUnit()

    # WHEN
    lw_x2.set_groupunit(groupunit=groupunit_shop(name=groupname_x))

    # THEN
    assert len(lw_x2._groups) == 1
    assert len(lw_x2._groups) == len(every1_groups)
    assert lw_x2._groups.get(swim_text)._allys == every1_groups.get(swim_text)._allys
    assert lw_x2._groups.get(swim_text) == every1_groups.get(swim_text)
    assert lw_x2._groups == every1_groups

    bill_single_member_ally_id = 30
    bill_group = groupunit_shop(
        name=GroupName("bill"), uid=45, single_member_ally_id=bill_single_member_ally_id
    )
    assert bill_group != None


def test_agent_groups_del_groupunit_worksCorrectly():
    # GIVEN
    sx = AgentUnit()
    swim_text = "swimmers"
    group_x = groupunit_shop(name=GroupName(swim_text))
    sx.set_groupunit(groupunit=group_x)
    assert sx._groups.get(swim_text) != None

    # WHEN
    sx.del_groupunit(groupname=swim_text)
    assert sx._groups.get(swim_text) is None
    assert sx._groups == {}


def test_example_has_groups():
    # GIVEN / WHEN
    lw_x = examples_agent_v001()

    # THEN
    assert lw_x._groups != None
    assert len(lw_x._groups) == 34
    everyone_allys_len = None
    everyone_group = lw_x._groups.get("Everyone")
    everyone_allys_len = len(everyone_group._allys)
    assert everyone_allys_len == 22

    # WHEN
    lw_x.set_agent_metrics()
    idea_dict = lw_x._idea_dict

    # THEN
    db_idea = idea_dict.get("TlME,D&B")
    print(f"{db_idea._desc=} {db_idea._grouplinks=}")
    assert len(db_idea._grouplinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._desc == "D&B":
    #         print(f"{idea._desc=} {idea._grouplinks=}")
    #         db_grouplink_len = len(idea._grouplinks)
    # assert db_grouplink_len == 3


def test_agent_set_grouplink_correctly_sets_grouplinks():
    # GIVEN
    prom_text = "prom"
    lw_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    lw_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    lw_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    lw_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))

    assert len(lw_x._allys) == 3
    assert len(lw_x._groups) == 3
    swim_text = "swim"
    lw_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    grouplink_rico = grouplink_shop(name=GroupName(rico_text), creditor_weight=10)
    grouplink_carm = grouplink_shop(name=GroupName(carm_text), creditor_weight=10)
    grouplink_patr = grouplink_shop(name=GroupName(patr_text), creditor_weight=10)
    swim_road = f"{prom_text},{swim_text}"
    lw_x.edit_idea_attr(road=swim_road, grouplink=grouplink_rico)
    lw_x.edit_idea_attr(road=swim_road, grouplink=grouplink_carm)
    lw_x.edit_idea_attr(road=swim_road, grouplink=grouplink_patr)

    assert lw_x._idearoot._grouplinks in (None, {})
    assert len(lw_x._idearoot._kids[swim_text]._grouplinks) == 3

    lw_x.add_idea(idea_kid=IdeaKid(_desc="streets"), walk=swim_road)

    # WHEN
    idea_list = lw_x.get_idea_list()

    # THEN
    idea_prom = idea_list[1]
    idea_prom_swim = idea_list[2]

    assert len(idea_prom._grouplinks) == 3
    assert len(idea_prom._groupheirs) == 3
    assert idea_prom_swim._grouplinks in (None, {})
    assert len(idea_prom_swim._groupheirs) == 3

    print(f"{len(idea_list)}")
    print(f"{idea_list[0]._grouplinks}")
    print(f"{idea_list[0]._groupheirs}")
    print(f"{idea_list[1]._groupheirs}")
    assert len(lw_x._idearoot._kids["swim"]._groupheirs) == 3


def test_agent_set_grouplink_correctly_deletes_grouplinks():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))

    swim_text = "swim"
    swim_road = f"{prom_text},{swim_text}"

    a_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    grouplink_rico = grouplink_shop(name=GroupName(rico_text), creditor_weight=10)
    grouplink_carm = grouplink_shop(name=GroupName(carm_text), creditor_weight=10)
    grouplink_patr = grouplink_shop(name=GroupName(patr_text), creditor_weight=10)

    swim_idea = a_x.get_idea_kid(road=swim_road)
    a_x.edit_idea_attr(road=swim_road, grouplink=grouplink_rico)
    a_x.edit_idea_attr(road=swim_road, grouplink=grouplink_carm)
    a_x.edit_idea_attr(road=swim_road, grouplink=grouplink_patr)

    # idea_list = a_x.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._grouplinks) == 3
    assert len(swim_idea._groupheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._grouplinks}")
    # print(f"{idea_list[0]._groupheirs}")
    # print(f"{idea_list[1]._groupheirs}")
    assert len(a_x._idearoot._kids[swim_text]._grouplinks) == 3
    assert len(a_x._idearoot._kids[swim_text]._groupheirs) == 3

    # WHEN
    a_x.edit_idea_attr(road=swim_road, grouplink_del=rico_text)

    # THEN
    swim_idea = a_x.get_idea_kid(road=swim_road)
    print(f"{swim_idea._desc=}")
    print(f"{swim_idea._grouplinks=}")
    print(f"{swim_idea._groupheirs=}")

    assert len(a_x._idearoot._kids[swim_text]._grouplinks) == 2
    assert len(a_x._idearoot._kids[swim_text]._groupheirs) == 2


def test_agent_set_grouplink_CorrectlyCalculatesInheritedGroupLinkAgentImportance():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    blink_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = grouplink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_grouplink(grouplink=blink_rico)
    a_x._idearoot.set_grouplink(grouplink=blink_carm)
    a_x._idearoot.set_grouplink(grouplink=blink_patr)
    assert len(a_x._idearoot._grouplinks) == 3

    # WHEN
    idea_list = a_x.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._groupheirs) == 3

    bheir_rico = idea_prom._groupheirs.get(rico_text)
    bheir_carm = idea_prom._groupheirs.get(carm_text)
    bheir_patr = idea_prom._groupheirs.get(patr_text)
    assert bheir_rico._agent_credit == 0.5
    assert bheir_rico._agent_debt == 0.75
    assert bheir_carm._agent_credit == 0.25
    assert bheir_carm._agent_debt == 0.125
    assert bheir_patr._agent_credit == 0.25
    assert bheir_patr._agent_debt == 0.125
    assert (
        bheir_rico._agent_credit + bheir_carm._agent_credit + bheir_patr._agent_credit
        == 1
    )
    assert bheir_rico._agent_debt + bheir_carm._agent_debt + bheir_patr._agent_debt == 1

    # agent_credit_sum = 0
    # agent_debt_sum = 0
    # for group in a_x._idearoot._groupheirs.values():
    #     print(f"{group=}")
    #     assert group._agent_credit != None
    #     assert group._agent_credit in [0.25, 0.5]
    #     assert group._agent_debt != None
    #     assert group._agent_debt in [0.75, 0.125]
    #     agent_credit_sum += group._agent_credit
    #     agent_debt_sum += group._agent_debt

    # assert agent_credit_sum == 1
    # assert agent_debt_sum == 1


def test_agent_get_idea_list_CorrectlyCalculates1LevelAgentGroupAgentImportance():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    blink_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = grouplink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_grouplink(grouplink=blink_rico)
    a_x._idearoot.set_grouplink(grouplink=blink_carm)
    a_x._idearoot.set_grouplink(grouplink=blink_patr)

    assert len(a_x._groups) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._agent_credit == 0.5
    assert group_rico._agent_debt == 0.75
    assert group_carm._agent_credit == 0.25
    assert group_carm._agent_debt == 0.125
    assert group_patr._agent_credit == 0.25
    assert group_patr._agent_debt == 0.125
    assert (
        group_rico._agent_credit + group_carm._agent_credit + group_patr._agent_credit
        == 1
    )
    assert group_rico._agent_debt + group_carm._agent_debt + group_patr._agent_debt == 1

    # WHEN
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(sele_text)))
    bl_sele = grouplink_shop(name=sele_text, creditor_weight=37)
    a_x._idearoot.set_grouplink(grouplink=bl_sele)
    assert len(a_x._groups) == 4
    a_x.set_agent_metrics()

    # THEN
    group_sele = a_x._groups.get(sele_text)
    assert group_rico._agent_credit != 0.5
    assert group_rico._agent_debt != 0.75
    assert group_carm._agent_credit != 0.25
    assert group_carm._agent_debt != 0.125
    assert group_patr._agent_credit != 0.25
    assert group_patr._agent_debt != 0.125
    assert group_sele._agent_credit != None
    assert group_sele._agent_debt != None
    assert (
        group_rico._agent_credit
        + group_carm._agent_credit
        + group_patr._agent_credit
        + group_sele._agent_credit
        == 1
    )
    assert (
        group_rico._agent_debt
        + group_carm._agent_debt
        + group_patr._agent_debt
        + group_sele._agent_debt
        == 1
    )


def test_agent_get_idea_list_CorrectlyCalculates3levelAgentGroupAgentImportance():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    rico_grouplink = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_grouplink = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_grouplink = grouplink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=rico_grouplink)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=carm_grouplink)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=parm_grouplink)
    assert len(a_x._groups) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._agent_credit == 0.5
    assert group_rico._agent_debt == 0.75
    assert group_carm._agent_credit == 0.25
    assert group_carm._agent_debt == 0.125
    assert group_patr._agent_credit == 0.25
    assert group_patr._agent_debt == 0.125
    assert (
        group_rico._agent_credit + group_carm._agent_credit + group_patr._agent_credit
        == 1
    )
    assert group_rico._agent_debt + group_carm._agent_debt + group_patr._agent_debt == 1


def test_agent_get_idea_list_CorrectlyCalculatesGroupAgentImportanceLWwithGroupEmptyBranch():
    # GIVEN
    prom_text = "prom"
    a_x = AgentUnit(_desc=prom_text)
    swim_text = "swim"
    a_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    rico_grouplink = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_grouplink = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_grouplink = grouplink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=rico_grouplink)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=carm_grouplink)
    a_x._idearoot._kids[swim_text].set_grouplink(grouplink=parm_grouplink)

    # no grouplinks attached to this one
    a_x.add_idea(idea_kid=IdeaKid(_desc="hunt", _weight=3), walk="prom")

    assert a_x._idearoot._grouplinks is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x._idearoot._grouplinks == {}

    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._grouplinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._grouplinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._grouplinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._groupheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._groupheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._groupheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    group_rico = a_x._groups.get(rico_text)
    group_carm = a_x._groups.get(carm_text)
    group_patr = a_x._groups.get(patr_text)
    assert group_rico._agent_credit == 0.125
    assert group_rico._agent_debt == 0.1875
    assert group_carm._agent_credit == 0.0625
    assert group_carm._agent_debt == 0.03125
    assert group_patr._agent_credit == 0.0625
    assert group_patr._agent_debt == 0.03125
    assert (
        group_rico._agent_credit + group_carm._agent_credit + group_patr._agent_credit
        == 0.25
    )
    assert (
        group_rico._agent_debt + group_carm._agent_debt + group_patr._agent_debt == 0.25
    )


def test_agent_edit_groupunit_name_CorrectlyCreatesNewName():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(name=swim_text, uid=13)
    swim_group.set_allylink(allylink=allylink_shop(name=rico_text))
    sx.set_groupunit(swim_group)
    assert len(sx._allys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(swim_text) != None
    assert sx._groups.get(swim_text).uid == 13
    assert sx._groups.get(swim_text)._single_ally == False
    assert len(sx._groups.get(swim_text)._allys) == 1

    # WHEN
    jog_text = "jog"
    sx.edit_groupunit_name(
        old_name=swim_text, new_name=jog_text, allow_group_overwite=False
    )

    # THEN
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(jog_text).uid == 13
    assert sx._groups.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(jog_text)._single_ally == False
    assert len(sx._groups.get(jog_text)._allys) == 1


def test_agent_edit_groupunit_name_raiseErrorNewNameAlreadyExists():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    sx.set_groupunit(groupunit_shop(name=swim_text, uid=13))
    jog_text = "jog"
    sx.set_groupunit(groupunit_shop(name=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_groupunit_name(
            old_name=swim_text,
            new_name=jog_text,
            allow_group_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Group '{swim_text}' change to '{jog_text}' failed since it already exists."
    )


def test_agent_edit_groupunit_name_CorrectlyMeldNames():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_group = groupunit_shop(name=swim_text, uid=13)
    swim_group.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=5, debtor_weight=3)
    )
    sx.set_groupunit(swim_group)
    jog_text = "jog"
    jog_group = groupunit_shop(name=jog_text, uid=13)
    jog_group.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=10)
    )
    sx.set_groupunit(jog_group)
    print(f"{sx._groups.get(jog_text)._allys.get(rico_text)=}")
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(jog_text).uid == 13

    # WHEN
    sx.edit_groupunit_name(
        old_name=swim_text,
        new_name=jog_text,
        allow_group_overwite=True,
    )

    # THEN
    assert sx._groups.get(jog_text) != None
    assert sx._groups.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._groups) == 2
    assert sx._groups.get(jog_text)._single_ally == False
    assert len(sx._groups.get(jog_text)._allys) == 1
    assert sx._groups.get(jog_text)._allys.get(rico_text).creditor_weight == 12
    assert sx._groups.get(jog_text)._allys.get(rico_text).debtor_weight == 13


def test_agent_edit_groupUnit_name_CorrectlyChangesGroupLinks():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(name=swim_text, uid=13)
    a_x.set_groupunit(swim_groupunit)
    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_grouplink = grouplink_shop(
        name=swim_groupunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_grouplink(swim_grouplink)
    assert camping_idea._grouplinks.get(swim_text) != None
    assert camping_idea._grouplinks.get(swim_text).creditor_weight == 5
    assert camping_idea._grouplinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    a_x.edit_groupunit_name(
        old_name=swim_text, new_name=jog_text, allow_group_overwite=False
    )

    # THEN
    assert camping_idea._grouplinks.get(swim_text) is None
    assert camping_idea._grouplinks.get(jog_text) != None
    assert camping_idea._grouplinks.get(jog_text).creditor_weight == 5
    assert camping_idea._grouplinks.get(jog_text).debtor_weight == 3


def test_agent_edit_groupUnit_name_CorrectlyMeldsGroupLinesGroupLinksGroupHeirs():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_groupunit = groupunit_shop(name=swim_text, uid=13)
    a_x.set_groupunit(swim_groupunit)

    jog_text = "jog"
    jog_groupunit = groupunit_shop(name=jog_text, uid=13)
    a_x.set_groupunit(jog_groupunit)

    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_grouplink = grouplink_shop(
        name=swim_groupunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_grouplink(swim_grouplink)
    jog_grouplink = grouplink_shop(
        name=jog_groupunit.name, creditor_weight=7, debtor_weight=10
    )
    camping_idea.set_grouplink(jog_grouplink)
    assert camping_idea._grouplinks.get(swim_text) != None
    assert camping_idea._grouplinks.get(swim_text).creditor_weight == 5
    assert camping_idea._grouplinks.get(swim_text).debtor_weight == 3
    assert camping_idea._grouplinks.get(jog_text) != None
    assert camping_idea._grouplinks.get(jog_text).creditor_weight == 7
    assert camping_idea._grouplinks.get(jog_text).debtor_weight == 10

    # WHEN
    a_x.edit_groupunit_name(
        old_name=swim_text, new_name=jog_text, allow_group_overwite=True
    )

    # THEN
    assert camping_idea._grouplinks.get(swim_text) is None
    assert camping_idea._grouplinks.get(jog_text) != None
    assert camping_idea._grouplinks.get(jog_text).creditor_weight == 12
    assert camping_idea._grouplinks.get(jog_text).debtor_weight == 13


def test_agent_add_idea_CreatesMissingGroups():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    grouplink_z = grouplink_shop(name=family_text)
    clean_kitchen_idea.set_grouplink(grouplink=grouplink_z)
    assert len(a_x._groups) == 0
    assert a_x._groups.get(family_text) is None

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN
    assert len(a_x._groups) == 1
    assert a_x._groups.get(family_text) != None
    assert a_x._groups.get(family_text)._allys in (None, {})


def test_agent_add_idea_DoesNotOverwriteGroups():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_groupunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    grouplink_z = grouplink_shop(name=family_text)
    clean_kitchen_idea.set_grouplink(grouplink=grouplink_z)

    groupunit_z = groupunit_shop(name=family_text)
    groupunit_z.set_allylink(allylink=allylink_shop(name="ann1"))
    groupunit_z.set_allylink(allylink=allylink_shop(name="bet1"))
    a_x.set_groupunit(groupunit=groupunit_z)

    # assert len(a_x._groups) == 0
    # assert a_x._groups.get(family_text) is None
    assert len(a_x._groups) == 1
    assert len(a_x._groups.get(family_text)._allys) == 2

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_groups=True,
    )

    # THEN

    # assert len(a_x._groups) == 1
    # assert len(a_x._groups.get(family_text)._allys) == 0
    # groupunit_z = groupunit_shop(name=family_text)
    # groupunit_z.set_allylink(allylink=allylink_shop(name="ann2"))
    # groupunit_z.set_allylink(allylink=allylink_shop(name="bet2"))
    # a_x.set_groupunit(groupunit=groupunit_z)

    assert len(a_x._groups) == 1
    assert len(a_x._groups.get(family_text)._allys) == 2


def test_agent_set_groupunits_create_missing_allys_DoesCreateMissingAllys():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_allys_empty_if_null()
    a_x.set_groupunits_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    groupunit_z = groupunit_shop(name=family_text)
    groupunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._allys.get(anna_text).creditor_weight == 3
    assert groupunit_z._allys.get(anna_text).debtor_weight == 7

    assert groupunit_z._allys.get(beto_text).creditor_weight == 5
    assert groupunit_z._allys.get(beto_text).debtor_weight == 11

    assert len(a_x._allys) == 0
    assert len(a_x._groups) == 0

    # WHEN
    a_x.set_groupunit(groupunit=groupunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert len(a_x._groups) == 3
    assert a_x._allys.get(anna_text).creditor_weight == 3
    assert a_x._allys.get(anna_text).debtor_weight == 7

    assert a_x._allys.get(beto_text).creditor_weight == 5
    assert a_x._allys.get(beto_text).debtor_weight == 11


def test_agent_set_groupunits_create_missing_allys_DoesNotReplaceAllys():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_allys_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    a_x.set_allyunit(
        allyunit_shop(name=anna_text, creditor_weight=17, debtor_weight=88)
    )
    a_x.set_allyunit(
        allyunit_shop(name=beto_text, creditor_weight=46, debtor_weight=71)
    )
    groupunit_z = groupunit_shop(name=family_text)
    groupunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    groupunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert groupunit_z._allys.get(anna_text).creditor_weight == 3
    assert groupunit_z._allys.get(anna_text).debtor_weight == 7
    assert groupunit_z._allys.get(beto_text).creditor_weight == 5
    assert groupunit_z._allys.get(beto_text).debtor_weight == 11
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71

    # WHEN
    a_x.set_groupunit(groupunit=groupunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71


def test_agent_get_groupunits_dict_CorrectlyReturnsDictOfGroups():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text))
    sx.set_groupunit(groupunit=groupunit_shop(name=walk_text))
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text))
    assert len(sx._groups) == 3

    # WHEN
    groupunit_list_x = sx.get_groupunits_name_list()

    # THEN
    assert groupunit_list_x[0] == ""
    assert groupunit_list_x[1] == fly_text
    assert groupunit_list_x[2] == swim_text
    assert groupunit_list_x[3] == walk_text
    assert len(groupunit_list_x) == 4


def test_agent_set_all_groupunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text))
    sx.set_groupunit(groupunit=groupunit_shop(name=walk_text))
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text))
    assert sx._groups[swim_text].uid is None
    assert sx._groups[walk_text].uid is None
    assert sx._groups[fly_text].uid is None

    # WHEN
    sx.set_all_groupunits_uids_unique()

    # THEN
    assert sx._groups[swim_text].uid != None
    assert sx._groups[walk_text].uid != None
    assert sx._groups[fly_text].uid != None


def test_agent_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text))
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


def test_agent_set_all_groupunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text))
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


def test_agent_all_groupunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=walk_text, uid=3))
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text))
    assert sx._groups[swim_text].uid == 3
    assert sx._groups[walk_text].uid == 3
    assert sx._groups[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_groupunits_uids_are_unique() == False

    # WHEN2
    sx.set_groupunit(groupunit=groupunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_groupunits_uids_are_unique() == False

    # WHEN3
    sx.set_groupunit(groupunit=groupunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_groupunits_uids_are_unique()
