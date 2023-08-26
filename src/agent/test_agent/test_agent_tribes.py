from src.agent.tribe import TribeName, tribelink_shop, tribeunit_shop
from src.agent.ally import AllyName, allyunit_shop, allylink_shop
from src.agent.idea import IdeaKid
from src.agent.required import Road
from src.agent.examples.example_agents import agent_v001 as examples_agent_v001
from src.agent.agent import AgentUnit
from pytest import raises as pytest_raises


def test_agent_tribes_set_tribeunit_worksCorrectly():
    # GIVEN
    lw_x = AgentUnit()
    assert lw_x._tribes is None
    swim_text = "swim"
    tribename_x = TribeName(swim_text)
    every1_tribes = {tribename_x: tribeunit_shop(name=tribename_x)}
    lw_x2 = AgentUnit()

    # WHEN
    lw_x2.set_tribeunit(tribeunit=tribeunit_shop(name=tribename_x))

    # THEN
    assert len(lw_x2._tribes) == 1
    assert len(lw_x2._tribes) == len(every1_tribes)
    assert lw_x2._tribes.get(swim_text)._allys == every1_tribes.get(swim_text)._allys
    assert lw_x2._tribes.get(swim_text) == every1_tribes.get(swim_text)
    assert lw_x2._tribes == every1_tribes

    bill_single_member_ally_id = 30
    bill_tribe = tribeunit_shop(
        name=TribeName("bill"), uid=45, single_member_ally_id=bill_single_member_ally_id
    )
    assert bill_tribe != None


def test_agent_tribes_del_tribeunit_worksCorrectly():
    # GIVEN
    sx = AgentUnit()
    swim_text = "swimmers"
    tribe_x = tribeunit_shop(name=TribeName(swim_text))
    sx.set_tribeunit(tribeunit=tribe_x)
    assert sx._tribes.get(swim_text) != None

    # WHEN
    sx.del_tribeunit(tribename=swim_text)
    assert sx._tribes.get(swim_text) is None
    assert sx._tribes == {}


def test_example_has_tribes():
    # GIVEN / WHEN
    lw_x = examples_agent_v001()

    # THEN
    assert lw_x._tribes != None
    assert len(lw_x._tribes) == 34
    everyone_allys_len = None
    everyone_tribe = lw_x._tribes.get("Everyone")
    everyone_allys_len = len(everyone_tribe._allys)
    assert everyone_allys_len == 22

    # WHEN
    lw_x.set_agent_metrics()
    idea_dict = lw_x._idea_dict

    # THEN
    db_idea = idea_dict.get("TlME,D&B")
    print(f"{db_idea._desc=} {db_idea._tribelinks=}")
    assert len(db_idea._tribelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._desc == "D&B":
    #         print(f"{idea._desc=} {idea._tribelinks=}")
    #         db_tribelink_len = len(idea._tribelinks)
    # assert db_tribelink_len == 3


def test_agent_set_tribelink_correctly_sets_tribelinks():
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
    assert len(lw_x._tribes) == 3
    swim_text = "swim"
    lw_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    tribelink_rico = tribelink_shop(name=TribeName(rico_text), creditor_weight=10)
    tribelink_carm = tribelink_shop(name=TribeName(carm_text), creditor_weight=10)
    tribelink_patr = tribelink_shop(name=TribeName(patr_text), creditor_weight=10)
    swim_road = f"{prom_text},{swim_text}"
    lw_x.edit_idea_attr(road=swim_road, tribelink=tribelink_rico)
    lw_x.edit_idea_attr(road=swim_road, tribelink=tribelink_carm)
    lw_x.edit_idea_attr(road=swim_road, tribelink=tribelink_patr)

    assert lw_x._idearoot._tribelinks in (None, {})
    assert len(lw_x._idearoot._kids[swim_text]._tribelinks) == 3

    lw_x.add_idea(idea_kid=IdeaKid(_desc="streets"), walk=swim_road)

    # WHEN
    idea_list = lw_x.get_idea_list()

    # THEN
    idea_prom = idea_list[1]
    idea_prom_swim = idea_list[2]

    assert len(idea_prom._tribelinks) == 3
    assert len(idea_prom._tribeheirs) == 3
    assert idea_prom_swim._tribelinks in (None, {})
    assert len(idea_prom_swim._tribeheirs) == 3

    print(f"{len(idea_list)}")
    print(f"{idea_list[0]._tribelinks}")
    print(f"{idea_list[0]._tribeheirs}")
    print(f"{idea_list[1]._tribeheirs}")
    assert len(lw_x._idearoot._kids["swim"]._tribeheirs) == 3


def test_agent_set_tribelink_correctly_deletes_tribelinks():
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
    tribelink_rico = tribelink_shop(name=TribeName(rico_text), creditor_weight=10)
    tribelink_carm = tribelink_shop(name=TribeName(carm_text), creditor_weight=10)
    tribelink_patr = tribelink_shop(name=TribeName(patr_text), creditor_weight=10)

    swim_idea = a_x.get_idea_kid(road=swim_road)
    a_x.edit_idea_attr(road=swim_road, tribelink=tribelink_rico)
    a_x.edit_idea_attr(road=swim_road, tribelink=tribelink_carm)
    a_x.edit_idea_attr(road=swim_road, tribelink=tribelink_patr)

    # idea_list = a_x.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._tribelinks) == 3
    assert len(swim_idea._tribeheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._tribelinks}")
    # print(f"{idea_list[0]._tribeheirs}")
    # print(f"{idea_list[1]._tribeheirs}")
    assert len(a_x._idearoot._kids[swim_text]._tribelinks) == 3
    assert len(a_x._idearoot._kids[swim_text]._tribeheirs) == 3

    # WHEN
    a_x.edit_idea_attr(road=swim_road, tribelink_del=rico_text)

    # THEN
    swim_idea = a_x.get_idea_kid(road=swim_road)
    print(f"{swim_idea._desc=}")
    print(f"{swim_idea._tribelinks=}")
    print(f"{swim_idea._tribeheirs=}")

    assert len(a_x._idearoot._kids[swim_text]._tribelinks) == 2
    assert len(a_x._idearoot._kids[swim_text]._tribeheirs) == 2


def test_agent_set_tribelink_CorrectlyCalculatesInheritedTribeLinkAgentImportance():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    blink_rico = tribelink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = tribelink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = tribelink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_tribelink(tribelink=blink_rico)
    a_x._idearoot.set_tribelink(tribelink=blink_carm)
    a_x._idearoot.set_tribelink(tribelink=blink_patr)
    assert len(a_x._idearoot._tribelinks) == 3

    # WHEN
    idea_list = a_x.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._tribeheirs) == 3

    bheir_rico = idea_prom._tribeheirs.get(rico_text)
    bheir_carm = idea_prom._tribeheirs.get(carm_text)
    bheir_patr = idea_prom._tribeheirs.get(patr_text)
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
    # for tribe in a_x._idearoot._tribeheirs.values():
    #     print(f"{tribe=}")
    #     assert tribe._agent_credit != None
    #     assert tribe._agent_credit in [0.25, 0.5]
    #     assert tribe._agent_debt != None
    #     assert tribe._agent_debt in [0.75, 0.125]
    #     agent_credit_sum += tribe._agent_credit
    #     agent_debt_sum += tribe._agent_debt

    # assert agent_credit_sum == 1
    # assert agent_debt_sum == 1


def test_agent_get_idea_list_CorrectlyCalculates1LevelAgentTribeAgentImportance():
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
    blink_rico = tribelink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = tribelink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = tribelink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_tribelink(tribelink=blink_rico)
    a_x._idearoot.set_tribelink(tribelink=blink_carm)
    a_x._idearoot.set_tribelink(tribelink=blink_patr)

    assert len(a_x._tribes) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    tribe_rico = a_x._tribes.get(rico_text)
    tribe_carm = a_x._tribes.get(carm_text)
    tribe_patr = a_x._tribes.get(patr_text)
    assert tribe_rico._agent_credit == 0.5
    assert tribe_rico._agent_debt == 0.75
    assert tribe_carm._agent_credit == 0.25
    assert tribe_carm._agent_debt == 0.125
    assert tribe_patr._agent_credit == 0.25
    assert tribe_patr._agent_debt == 0.125
    assert (
        tribe_rico._agent_credit + tribe_carm._agent_credit + tribe_patr._agent_credit
        == 1
    )
    assert tribe_rico._agent_debt + tribe_carm._agent_debt + tribe_patr._agent_debt == 1

    # WHEN
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(sele_text)))
    bl_sele = tribelink_shop(name=sele_text, creditor_weight=37)
    a_x._idearoot.set_tribelink(tribelink=bl_sele)
    assert len(a_x._tribes) == 4
    a_x.set_agent_metrics()

    # THEN
    tribe_sele = a_x._tribes.get(sele_text)
    assert tribe_rico._agent_credit != 0.5
    assert tribe_rico._agent_debt != 0.75
    assert tribe_carm._agent_credit != 0.25
    assert tribe_carm._agent_debt != 0.125
    assert tribe_patr._agent_credit != 0.25
    assert tribe_patr._agent_debt != 0.125
    assert tribe_sele._agent_credit != None
    assert tribe_sele._agent_debt != None
    assert (
        tribe_rico._agent_credit
        + tribe_carm._agent_credit
        + tribe_patr._agent_credit
        + tribe_sele._agent_credit
        == 1
    )
    assert (
        tribe_rico._agent_debt
        + tribe_carm._agent_debt
        + tribe_patr._agent_debt
        + tribe_sele._agent_debt
        == 1
    )


def test_agent_get_idea_list_CorrectlyCalculates3levelAgentTribeAgentImportance():
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
    rico_tribelink = tribelink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_tribelink = tribelink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_tribelink = tribelink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=rico_tribelink)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=carm_tribelink)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=parm_tribelink)
    assert len(a_x._tribes) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    tribe_rico = a_x._tribes.get(rico_text)
    tribe_carm = a_x._tribes.get(carm_text)
    tribe_patr = a_x._tribes.get(patr_text)
    assert tribe_rico._agent_credit == 0.5
    assert tribe_rico._agent_debt == 0.75
    assert tribe_carm._agent_credit == 0.25
    assert tribe_carm._agent_debt == 0.125
    assert tribe_patr._agent_credit == 0.25
    assert tribe_patr._agent_debt == 0.125
    assert (
        tribe_rico._agent_credit + tribe_carm._agent_credit + tribe_patr._agent_credit
        == 1
    )
    assert tribe_rico._agent_debt + tribe_carm._agent_debt + tribe_patr._agent_debt == 1


def test_agent_get_idea_list_CorrectlyCalculatesTribeAgentImportanceLWwithTribeEmptyBranch():
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
    rico_tribelink = tribelink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_tribelink = tribelink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_tribelink = tribelink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=rico_tribelink)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=carm_tribelink)
    a_x._idearoot._kids[swim_text].set_tribelink(tribelink=parm_tribelink)

    # no tribelinks attached to this one
    a_x.add_idea(idea_kid=IdeaKid(_desc="hunt", _weight=3), walk="prom")

    assert a_x._idearoot._tribelinks is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x._idearoot._tribelinks == {}

    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._tribelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._tribelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._tribelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._tribeheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._tribeheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._tribeheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    tribe_rico = a_x._tribes.get(rico_text)
    tribe_carm = a_x._tribes.get(carm_text)
    tribe_patr = a_x._tribes.get(patr_text)
    assert tribe_rico._agent_credit == 0.125
    assert tribe_rico._agent_debt == 0.1875
    assert tribe_carm._agent_credit == 0.0625
    assert tribe_carm._agent_debt == 0.03125
    assert tribe_patr._agent_credit == 0.0625
    assert tribe_patr._agent_debt == 0.03125
    assert (
        tribe_rico._agent_credit + tribe_carm._agent_credit + tribe_patr._agent_credit
        == 0.25
    )
    assert (
        tribe_rico._agent_debt + tribe_carm._agent_debt + tribe_patr._agent_debt == 0.25
    )


def test_agent_edit_tribeunit_name_CorrectlyCreatesNewName():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_tribe = tribeunit_shop(name=swim_text, uid=13)
    swim_tribe.set_allylink(allylink=allylink_shop(name=rico_text))
    sx.set_tribeunit(swim_tribe)
    assert len(sx._allys) == 1
    assert len(sx._tribes) == 2
    assert sx._tribes.get(swim_text) != None
    assert sx._tribes.get(swim_text).uid == 13
    assert sx._tribes.get(swim_text)._single_ally == False
    assert len(sx._tribes.get(swim_text)._allys) == 1

    # WHEN
    jog_text = "jog"
    sx.edit_tribeunit_name(
        old_name=swim_text, new_name=jog_text, allow_tribe_overwite=False
    )

    # THEN
    assert sx._tribes.get(jog_text) != None
    assert sx._tribes.get(jog_text).uid == 13
    assert sx._tribes.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._tribes) == 2
    assert sx._tribes.get(jog_text)._single_ally == False
    assert len(sx._tribes.get(jog_text)._allys) == 1


def test_agent_edit_tribeunit_name_raiseErrorNewNameAlreadyExists():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    sx.set_tribeunit(tribeunit_shop(name=swim_text, uid=13))
    jog_text = "jog"
    sx.set_tribeunit(tribeunit_shop(name=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_tribeunit_name(
            old_name=swim_text,
            new_name=jog_text,
            allow_tribe_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Tribe '{swim_text}' change to '{jog_text}' failed since it already exists."
    )


def test_agent_edit_tribeunit_name_CorrectlyMeldNames():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_tribe = tribeunit_shop(name=swim_text, uid=13)
    swim_tribe.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=5, debtor_weight=3)
    )
    sx.set_tribeunit(swim_tribe)
    jog_text = "jog"
    jog_tribe = tribeunit_shop(name=jog_text, uid=13)
    jog_tribe.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=10)
    )
    sx.set_tribeunit(jog_tribe)
    print(f"{sx._tribes.get(jog_text)._allys.get(rico_text)=}")
    assert sx._tribes.get(jog_text) != None
    assert sx._tribes.get(jog_text).uid == 13

    # WHEN
    sx.edit_tribeunit_name(
        old_name=swim_text,
        new_name=jog_text,
        allow_tribe_overwite=True,
    )

    # THEN
    assert sx._tribes.get(jog_text) != None
    assert sx._tribes.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._tribes) == 2
    assert sx._tribes.get(jog_text)._single_ally == False
    assert len(sx._tribes.get(jog_text)._allys) == 1
    assert sx._tribes.get(jog_text)._allys.get(rico_text).creditor_weight == 12
    assert sx._tribes.get(jog_text)._allys.get(rico_text).debtor_weight == 13


def test_agent_edit_tribeUnit_name_CorrectlyChangesTribeLinks():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_tribeunit = tribeunit_shop(name=swim_text, uid=13)
    a_x.set_tribeunit(swim_tribeunit)
    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_tribelink = tribelink_shop(
        name=swim_tribeunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_tribelink(swim_tribelink)
    assert camping_idea._tribelinks.get(swim_text) != None
    assert camping_idea._tribelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._tribelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    a_x.edit_tribeunit_name(
        old_name=swim_text, new_name=jog_text, allow_tribe_overwite=False
    )

    # THEN
    assert camping_idea._tribelinks.get(swim_text) is None
    assert camping_idea._tribelinks.get(jog_text) != None
    assert camping_idea._tribelinks.get(jog_text).creditor_weight == 5
    assert camping_idea._tribelinks.get(jog_text).debtor_weight == 3


def test_agent_edit_tribeUnit_name_CorrectlyMeldsTribeLinesTribeLinksTribeHeirs():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_tribeunit = tribeunit_shop(name=swim_text, uid=13)
    a_x.set_tribeunit(swim_tribeunit)

    jog_text = "jog"
    jog_tribeunit = tribeunit_shop(name=jog_text, uid=13)
    a_x.set_tribeunit(jog_tribeunit)

    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_tribelink = tribelink_shop(
        name=swim_tribeunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_tribelink(swim_tribelink)
    jog_tribelink = tribelink_shop(
        name=jog_tribeunit.name, creditor_weight=7, debtor_weight=10
    )
    camping_idea.set_tribelink(jog_tribelink)
    assert camping_idea._tribelinks.get(swim_text) != None
    assert camping_idea._tribelinks.get(swim_text).creditor_weight == 5
    assert camping_idea._tribelinks.get(swim_text).debtor_weight == 3
    assert camping_idea._tribelinks.get(jog_text) != None
    assert camping_idea._tribelinks.get(jog_text).creditor_weight == 7
    assert camping_idea._tribelinks.get(jog_text).debtor_weight == 10

    # WHEN
    a_x.edit_tribeunit_name(
        old_name=swim_text, new_name=jog_text, allow_tribe_overwite=True
    )

    # THEN
    assert camping_idea._tribelinks.get(swim_text) is None
    assert camping_idea._tribelinks.get(jog_text) != None
    assert camping_idea._tribelinks.get(jog_text).creditor_weight == 12
    assert camping_idea._tribelinks.get(jog_text).debtor_weight == 13


def test_agent_add_idea_CreatesMissingTribes():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_tribeunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    tribelink_z = tribelink_shop(name=family_text)
    clean_kitchen_idea.set_tribelink(tribelink=tribelink_z)
    assert len(a_x._tribes) == 0
    assert a_x._tribes.get(family_text) is None

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_tribes=True,
    )

    # THEN
    assert len(a_x._tribes) == 1
    assert a_x._tribes.get(family_text) != None
    assert a_x._tribes.get(family_text)._allys in (None, {})


def test_agent_add_idea_DoesNotOverwriteTribes():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_tribeunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    tribelink_z = tribelink_shop(name=family_text)
    clean_kitchen_idea.set_tribelink(tribelink=tribelink_z)

    tribeunit_z = tribeunit_shop(name=family_text)
    tribeunit_z.set_allylink(allylink=allylink_shop(name="ann1"))
    tribeunit_z.set_allylink(allylink=allylink_shop(name="bet1"))
    a_x.set_tribeunit(tribeunit=tribeunit_z)

    # assert len(a_x._tribes) == 0
    # assert a_x._tribes.get(family_text) is None
    assert len(a_x._tribes) == 1
    assert len(a_x._tribes.get(family_text)._allys) == 2

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_tribes=True,
    )

    # THEN

    # assert len(a_x._tribes) == 1
    # assert len(a_x._tribes.get(family_text)._allys) == 0
    # tribeunit_z = tribeunit_shop(name=family_text)
    # tribeunit_z.set_allylink(allylink=allylink_shop(name="ann2"))
    # tribeunit_z.set_allylink(allylink=allylink_shop(name="bet2"))
    # a_x.set_tribeunit(tribeunit=tribeunit_z)

    assert len(a_x._tribes) == 1
    assert len(a_x._tribes.get(family_text)._allys) == 2


def test_agent_set_tribeunits_create_missing_allys_DoesCreateMissingAllys():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_allys_empty_if_null()
    a_x.set_tribeunits_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    tribeunit_z = tribeunit_shop(name=family_text)
    tribeunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    tribeunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert tribeunit_z._allys.get(anna_text).creditor_weight == 3
    assert tribeunit_z._allys.get(anna_text).debtor_weight == 7

    assert tribeunit_z._allys.get(beto_text).creditor_weight == 5
    assert tribeunit_z._allys.get(beto_text).debtor_weight == 11

    assert len(a_x._allys) == 0
    assert len(a_x._tribes) == 0

    # WHEN
    a_x.set_tribeunit(tribeunit=tribeunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert len(a_x._tribes) == 3
    assert a_x._allys.get(anna_text).creditor_weight == 3
    assert a_x._allys.get(anna_text).debtor_weight == 7

    assert a_x._allys.get(beto_text).creditor_weight == 5
    assert a_x._allys.get(beto_text).debtor_weight == 11


def test_agent_set_tribeunits_create_missing_allys_DoesNotReplaceAllys():
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
    tribeunit_z = tribeunit_shop(name=family_text)
    tribeunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    tribeunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert tribeunit_z._allys.get(anna_text).creditor_weight == 3
    assert tribeunit_z._allys.get(anna_text).debtor_weight == 7
    assert tribeunit_z._allys.get(beto_text).creditor_weight == 5
    assert tribeunit_z._allys.get(beto_text).debtor_weight == 11
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71

    # WHEN
    a_x.set_tribeunit(tribeunit=tribeunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71


def test_agent_get_tribeunits_dict_CorrectlyReturnsDictOfTribes():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=walk_text))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text))
    assert len(sx._tribes) == 3

    # WHEN
    tribeunit_list_x = sx.get_tribeunits_name_list()

    # THEN
    assert tribeunit_list_x[0] == ""
    assert tribeunit_list_x[1] == fly_text
    assert tribeunit_list_x[2] == swim_text
    assert tribeunit_list_x[3] == walk_text
    assert len(tribeunit_list_x) == 4


def test_agent_set_all_tribeunits_uids_unique_CorrectlySetsEmptyTribeUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=walk_text))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text))
    assert sx._tribes[swim_text].uid is None
    assert sx._tribes[walk_text].uid is None
    assert sx._tribes[fly_text].uid is None

    # WHEN
    sx.set_all_tribeunits_uids_unique()

    # THEN
    assert sx._tribes[swim_text].uid != None
    assert sx._tribes[walk_text].uid != None
    assert sx._tribes[fly_text].uid != None


def test_agent_set_all_tribeunits_uids_unique_CorrectlySetsChangesSameTribeUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=walk_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text))
    assert sx._tribes[swim_text].uid == 3
    assert sx._tribes[walk_text].uid == 3
    assert sx._tribes[fly_text].uid is None

    # WHEN
    sx.set_all_tribeunits_uids_unique()

    # THEN
    print(f"{sx._tribes[swim_text].uid=}")
    print(f"{sx._tribes[walk_text].uid=}")
    assert sx._tribes[swim_text].uid != sx._tribes[walk_text].uid
    assert sx._tribes[walk_text].uid != 3
    assert sx._tribes[walk_text].uid != 3
    assert sx._tribes[fly_text].uid != None


def test_agent_set_all_tribeunits_uids_unique_CorrectlySetsChangesSameTribeUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=walk_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text))
    assert sx._tribes[swim_text].uid == 3
    assert sx._tribes[walk_text].uid == 3
    assert sx._tribes[fly_text].uid is None

    # WHEN
    sx.set_all_tribeunits_uids_unique()

    # THEN
    print(f"{sx._tribes[swim_text].uid=}")
    print(f"{sx._tribes[walk_text].uid=}")
    assert sx._tribes[swim_text].uid != sx._tribes[walk_text].uid
    assert sx._tribes[walk_text].uid != 3
    assert sx._tribes[walk_text].uid != 3
    assert sx._tribes[fly_text].uid != None


def test_agent_all_tribeunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=walk_text, uid=3))
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text))
    assert sx._tribes[swim_text].uid == 3
    assert sx._tribes[walk_text].uid == 3
    assert sx._tribes[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_tribeunits_uids_are_unique() == False

    # WHEN2
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_tribeunits_uids_are_unique() == False

    # WHEN3
    sx.set_tribeunit(tribeunit=tribeunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_tribeunits_uids_are_unique()
