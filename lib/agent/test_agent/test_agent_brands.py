from lib.agent.brand import BrandName, brandlink_shop, brandunit_shop
from lib.agent.ally import AllyName, allyunit_shop, allylink_shop
from lib.agent.idea import IdeaKid
from lib.agent.required import Road
from lib.agent.examples.example_agents import agent_v001 as examples_agent_v001
from lib.agent.agent import AgentUnit
from pytest import raises as pytest_raises


def test_agent_brands_set_brandunit_worksCorrectly():
    # GIVEN
    lw_x = AgentUnit()
    assert lw_x._brands is None
    swim_text = "swim"
    brandname_x = BrandName(swim_text)
    every1_brands = {brandname_x: brandunit_shop(name=brandname_x)}
    lw_x2 = AgentUnit()

    # WHEN
    lw_x2.set_brandunit(brandunit=brandunit_shop(name=brandname_x))

    # THEN
    assert len(lw_x2._brands) == 1
    assert len(lw_x2._brands) == len(every1_brands)
    assert lw_x2._brands.get(swim_text)._allys == every1_brands.get(swim_text)._allys
    assert lw_x2._brands.get(swim_text) == every1_brands.get(swim_text)
    assert lw_x2._brands == every1_brands

    bill_single_member_ally_id = 30
    bill_brand = brandunit_shop(
        name=BrandName("bill"), uid=45, single_member_ally_id=bill_single_member_ally_id
    )
    assert bill_brand != None


def test_agent_brands_del_brandunit_worksCorrectly():
    # GIVEN
    sx = AgentUnit()
    swim_text = "swimmers"
    brand_x = brandunit_shop(name=BrandName(swim_text))
    sx.set_brandunit(brandunit=brand_x)
    assert sx._brands.get(swim_text) != None

    # WHEN
    sx.del_brandunit(brandname=swim_text)
    assert sx._brands.get(swim_text) is None
    assert sx._brands == {}


def test_example_has_brands():
    # GIVEN / WHEN
    lw_x = examples_agent_v001()

    # THEN
    assert lw_x._brands != None
    assert len(lw_x._brands) == 34
    everyone_allys_len = None
    everyone_brand = lw_x._brands.get("Everyone")
    everyone_allys_len = len(everyone_brand._allys)
    assert everyone_allys_len == 22

    # WHEN
    lw_x.set_agent_metrics()
    idea_dict = lw_x._idea_dict

    # THEN
    db_idea = idea_dict.get("TlME,D&B")
    print(f"{db_idea._desc=} {db_idea._brandlinks=}")
    assert len(db_idea._brandlinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._desc == "D&B":
    #         print(f"{idea._desc=} {idea._brandlinks=}")
    #         db_brandlink_len = len(idea._brandlinks)
    # assert db_brandlink_len == 3


def test_agent_set_brandlink_correctly_sets_brandlinks():
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
    assert len(lw_x._brands) == 3
    swim_text = "swim"
    lw_x.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=prom_text)
    brandlink_rico = brandlink_shop(name=BrandName(rico_text), creditor_weight=10)
    brandlink_carm = brandlink_shop(name=BrandName(carm_text), creditor_weight=10)
    brandlink_patr = brandlink_shop(name=BrandName(patr_text), creditor_weight=10)
    swim_road = f"{prom_text},{swim_text}"
    lw_x.edit_idea_attr(road=swim_road, brandlink=brandlink_rico)
    lw_x.edit_idea_attr(road=swim_road, brandlink=brandlink_carm)
    lw_x.edit_idea_attr(road=swim_road, brandlink=brandlink_patr)

    assert lw_x._idearoot._brandlinks in (None, {})
    assert len(lw_x._idearoot._kids[swim_text]._brandlinks) == 3

    lw_x.add_idea(idea_kid=IdeaKid(_desc="streets"), walk=swim_road)

    # WHEN
    idea_list = lw_x.get_idea_list()

    # THEN
    idea_prom = idea_list[1]
    idea_prom_swim = idea_list[2]

    assert len(idea_prom._brandlinks) == 3
    assert len(idea_prom._brandheirs) == 3
    assert idea_prom_swim._brandlinks in (None, {})
    assert len(idea_prom_swim._brandheirs) == 3

    print(f"{len(idea_list)}")
    print(f"{idea_list[0]._brandlinks}")
    print(f"{idea_list[0]._brandheirs}")
    print(f"{idea_list[1]._brandheirs}")
    assert len(lw_x._idearoot._kids["swim"]._brandheirs) == 3


def test_agent_set_brandlink_correctly_deletes_brandlinks():
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
    brandlink_rico = brandlink_shop(name=BrandName(rico_text), creditor_weight=10)
    brandlink_carm = brandlink_shop(name=BrandName(carm_text), creditor_weight=10)
    brandlink_patr = brandlink_shop(name=BrandName(patr_text), creditor_weight=10)

    swim_idea = a_x.get_idea_kid(road=swim_road)
    a_x.edit_idea_attr(road=swim_road, brandlink=brandlink_rico)
    a_x.edit_idea_attr(road=swim_road, brandlink=brandlink_carm)
    a_x.edit_idea_attr(road=swim_road, brandlink=brandlink_patr)

    # idea_list = a_x.get_idea_list()
    # idea_prom = idea_list[1]
    assert len(swim_idea._brandlinks) == 3
    assert len(swim_idea._brandheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._brandlinks}")
    # print(f"{idea_list[0]._brandheirs}")
    # print(f"{idea_list[1]._brandheirs}")
    assert len(a_x._idearoot._kids[swim_text]._brandlinks) == 3
    assert len(a_x._idearoot._kids[swim_text]._brandheirs) == 3

    # WHEN
    a_x.edit_idea_attr(road=swim_road, brandlink_del=rico_text)

    # THEN
    swim_idea = a_x.get_idea_kid(road=swim_road)
    print(f"{swim_idea._desc=}")
    print(f"{swim_idea._brandlinks=}")
    print(f"{swim_idea._brandheirs=}")

    assert len(a_x._idearoot._kids[swim_text]._brandlinks) == 2
    assert len(a_x._idearoot._kids[swim_text]._brandheirs) == 2


def test_agent_set_brandlink_CorrectlyCalculatesInheritedBrandLinkAgentImportance():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(rico_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(carm_text)))
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(patr_text)))
    blink_rico = brandlink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = brandlink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = brandlink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_brandlink(brandlink=blink_rico)
    a_x._idearoot.set_brandlink(brandlink=blink_carm)
    a_x._idearoot.set_brandlink(brandlink=blink_patr)
    assert len(a_x._idearoot._brandlinks) == 3

    # WHEN
    idea_list = a_x.get_idea_list()

    # THEN
    idea_prom = idea_list[0]
    assert len(idea_prom._brandheirs) == 3

    bheir_rico = idea_prom._brandheirs.get(rico_text)
    bheir_carm = idea_prom._brandheirs.get(carm_text)
    bheir_patr = idea_prom._brandheirs.get(patr_text)
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
    # for brand in a_x._idearoot._brandheirs.values():
    #     print(f"{brand=}")
    #     assert brand._agent_credit != None
    #     assert brand._agent_credit in [0.25, 0.5]
    #     assert brand._agent_debt != None
    #     assert brand._agent_debt in [0.75, 0.125]
    #     agent_credit_sum += brand._agent_credit
    #     agent_debt_sum += brand._agent_debt

    # assert agent_credit_sum == 1
    # assert agent_debt_sum == 1


def test_agent_get_idea_list_CorrectlyCalculates1LevelAgentBrandAgentImportance():
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
    blink_rico = brandlink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    blink_carm = brandlink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    blink_patr = brandlink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot.set_brandlink(brandlink=blink_rico)
    a_x._idearoot.set_brandlink(brandlink=blink_carm)
    a_x._idearoot.set_brandlink(brandlink=blink_patr)

    assert len(a_x._brands) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    brand_rico = a_x._brands.get(rico_text)
    brand_carm = a_x._brands.get(carm_text)
    brand_patr = a_x._brands.get(patr_text)
    assert brand_rico._agent_credit == 0.5
    assert brand_rico._agent_debt == 0.75
    assert brand_carm._agent_credit == 0.25
    assert brand_carm._agent_debt == 0.125
    assert brand_patr._agent_credit == 0.25
    assert brand_patr._agent_debt == 0.125
    assert (
        brand_rico._agent_credit + brand_carm._agent_credit + brand_patr._agent_credit
        == 1
    )
    assert brand_rico._agent_debt + brand_carm._agent_debt + brand_patr._agent_debt == 1

    # WHEN
    a_x.set_allyunit(allyunit=allyunit_shop(name=AllyName(sele_text)))
    bl_sele = brandlink_shop(name=sele_text, creditor_weight=37)
    a_x._idearoot.set_brandlink(brandlink=bl_sele)
    assert len(a_x._brands) == 4
    a_x.set_agent_metrics()

    # THEN
    brand_sele = a_x._brands.get(sele_text)
    assert brand_rico._agent_credit != 0.5
    assert brand_rico._agent_debt != 0.75
    assert brand_carm._agent_credit != 0.25
    assert brand_carm._agent_debt != 0.125
    assert brand_patr._agent_credit != 0.25
    assert brand_patr._agent_debt != 0.125
    assert brand_sele._agent_credit != None
    assert brand_sele._agent_debt != None
    assert (
        brand_rico._agent_credit
        + brand_carm._agent_credit
        + brand_patr._agent_credit
        + brand_sele._agent_credit
        == 1
    )
    assert (
        brand_rico._agent_debt
        + brand_carm._agent_debt
        + brand_patr._agent_debt
        + brand_sele._agent_debt
        == 1
    )


def test_agent_get_idea_list_CorrectlyCalculates3levelAgentBrandAgentImportance():
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
    rico_brandlink = brandlink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_brandlink = brandlink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_brandlink = brandlink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=rico_brandlink)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=carm_brandlink)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=parm_brandlink)
    assert len(a_x._brands) == 3

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    brand_rico = a_x._brands.get(rico_text)
    brand_carm = a_x._brands.get(carm_text)
    brand_patr = a_x._brands.get(patr_text)
    assert brand_rico._agent_credit == 0.5
    assert brand_rico._agent_debt == 0.75
    assert brand_carm._agent_credit == 0.25
    assert brand_carm._agent_debt == 0.125
    assert brand_patr._agent_credit == 0.25
    assert brand_patr._agent_debt == 0.125
    assert (
        brand_rico._agent_credit + brand_carm._agent_credit + brand_patr._agent_credit
        == 1
    )
    assert brand_rico._agent_debt + brand_carm._agent_debt + brand_patr._agent_debt == 1


def test_agent_get_idea_list_CorrectlyCalculatesBrandAgentImportanceLWwithBrandEmptyBranch():
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
    rico_brandlink = brandlink_shop(name=rico_text, creditor_weight=20, debtor_weight=6)
    carm_brandlink = brandlink_shop(name=carm_text, creditor_weight=10, debtor_weight=1)
    parm_brandlink = brandlink_shop(name=patr_text, creditor_weight=10)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=rico_brandlink)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=carm_brandlink)
    a_x._idearoot._kids[swim_text].set_brandlink(brandlink=parm_brandlink)

    # no brandlinks attached to this one
    a_x.add_idea(idea_kid=IdeaKid(_desc="hunt", _weight=3), walk="prom")

    assert a_x._idearoot._brandlinks is None

    # WHEN
    a_x.set_agent_metrics()

    # THEN
    assert a_x._idearoot._brandlinks == {}

    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._brandlinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._brandlinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._brandlinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._brandheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._brandheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        a_x._idearoot._kids["hunt"]._brandheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    brand_rico = a_x._brands.get(rico_text)
    brand_carm = a_x._brands.get(carm_text)
    brand_patr = a_x._brands.get(patr_text)
    assert brand_rico._agent_credit == 0.125
    assert brand_rico._agent_debt == 0.1875
    assert brand_carm._agent_credit == 0.0625
    assert brand_carm._agent_debt == 0.03125
    assert brand_patr._agent_credit == 0.0625
    assert brand_patr._agent_debt == 0.03125
    assert (
        brand_rico._agent_credit + brand_carm._agent_credit + brand_patr._agent_credit
        == 0.25
    )
    assert (
        brand_rico._agent_debt + brand_carm._agent_debt + brand_patr._agent_debt == 0.25
    )


def test_agent_edit_brandunit_name_CorrectlyCreatesNewName():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_brand = brandunit_shop(name=swim_text, uid=13)
    swim_brand.set_allylink(allylink=allylink_shop(name=rico_text))
    sx.set_brandunit(swim_brand)
    assert len(sx._allys) == 1
    assert len(sx._brands) == 2
    assert sx._brands.get(swim_text) != None
    assert sx._brands.get(swim_text).uid == 13
    assert sx._brands.get(swim_text)._single_ally == False
    assert len(sx._brands.get(swim_text)._allys) == 1

    # WHEN
    jog_text = "jog"
    sx.edit_brandunit_name(
        old_name=swim_text, new_name=jog_text, allow_brand_overwite=False
    )

    # THEN
    assert sx._brands.get(jog_text) != None
    assert sx._brands.get(jog_text).uid == 13
    assert sx._brands.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._brands) == 2
    assert sx._brands.get(jog_text)._single_ally == False
    assert len(sx._brands.get(jog_text)._allys) == 1


def test_agent_edit_brandunit_name_raiseErrorNewNameAlreadyExists():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    sx.set_brandunit(brandunit_shop(name=swim_text, uid=13))
    jog_text = "jog"
    sx.set_brandunit(brandunit_shop(name=jog_text, uid=13))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_brandunit_name(
            old_name=swim_text,
            new_name=jog_text,
            allow_brand_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Brand '{swim_text}' change to '{jog_text}' failed since it already exists."
    )


def test_agent_edit_brandunit_name_CorrectlyMeldNames():
    # GIVEN
    sx = AgentUnit(_desc="prom")
    rico_text = "rico"
    sx.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_brand = brandunit_shop(name=swim_text, uid=13)
    swim_brand.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=5, debtor_weight=3)
    )
    sx.set_brandunit(swim_brand)
    jog_text = "jog"
    jog_brand = brandunit_shop(name=jog_text, uid=13)
    jog_brand.set_allylink(
        allylink=allylink_shop(name=rico_text, creditor_weight=7, debtor_weight=10)
    )
    sx.set_brandunit(jog_brand)
    print(f"{sx._brands.get(jog_text)._allys.get(rico_text)=}")
    assert sx._brands.get(jog_text) != None
    assert sx._brands.get(jog_text).uid == 13

    # WHEN
    sx.edit_brandunit_name(
        old_name=swim_text,
        new_name=jog_text,
        allow_brand_overwite=True,
    )

    # THEN
    assert sx._brands.get(jog_text) != None
    assert sx._brands.get(swim_text) is None
    assert len(sx._allys) == 1
    assert len(sx._brands) == 2
    assert sx._brands.get(jog_text)._single_ally == False
    assert len(sx._brands.get(jog_text)._allys) == 1
    assert sx._brands.get(jog_text)._allys.get(rico_text).creditor_weight == 12
    assert sx._brands.get(jog_text)._allys.get(rico_text).debtor_weight == 13


def test_agent_edit_brandUnit_name_CorrectlyChangesBrandLinks():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_brandunit = brandunit_shop(name=swim_text, uid=13)
    a_x.set_brandunit(swim_brandunit)
    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_brandlink = brandlink_shop(
        name=swim_brandunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_brandlink(swim_brandlink)
    assert camping_idea._brandlinks.get(swim_text) != None
    assert camping_idea._brandlinks.get(swim_text).creditor_weight == 5
    assert camping_idea._brandlinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = "jog"
    a_x.edit_brandunit_name(
        old_name=swim_text, new_name=jog_text, allow_brand_overwite=False
    )

    # THEN
    assert camping_idea._brandlinks.get(swim_text) is None
    assert camping_idea._brandlinks.get(jog_text) != None
    assert camping_idea._brandlinks.get(jog_text).creditor_weight == 5
    assert camping_idea._brandlinks.get(jog_text).debtor_weight == 3


def test_agent_edit_brandUnit_name_CorrectlyMeldsBrandLinesBrandLinksBrandHeirs():
    # GIVEN
    a_x = AgentUnit(_desc="prom")
    rico_text = "rico"
    a_x.add_allyunit(name=rico_text)
    swim_text = "swim"
    swim_brandunit = brandunit_shop(name=swim_text, uid=13)
    a_x.set_brandunit(swim_brandunit)

    jog_text = "jog"
    jog_brandunit = brandunit_shop(name=jog_text, uid=13)
    a_x.set_brandunit(jog_brandunit)

    outdoor_text = "outdoors"
    outdoor_road = Road(f"{a_x._desc},{outdoor_text}")
    camping_text = "camping"
    camping_road = Road(f"{a_x._desc},{outdoor_text},{camping_text}")
    a_x.add_idea(walk=outdoor_road, idea_kid=IdeaKid(_desc=camping_text))

    camping_idea = a_x.get_idea_kid(camping_road)
    swim_brandlink = brandlink_shop(
        name=swim_brandunit.name, creditor_weight=5, debtor_weight=3
    )
    camping_idea.set_brandlink(swim_brandlink)
    jog_brandlink = brandlink_shop(
        name=jog_brandunit.name, creditor_weight=7, debtor_weight=10
    )
    camping_idea.set_brandlink(jog_brandlink)
    assert camping_idea._brandlinks.get(swim_text) != None
    assert camping_idea._brandlinks.get(swim_text).creditor_weight == 5
    assert camping_idea._brandlinks.get(swim_text).debtor_weight == 3
    assert camping_idea._brandlinks.get(jog_text) != None
    assert camping_idea._brandlinks.get(jog_text).creditor_weight == 7
    assert camping_idea._brandlinks.get(jog_text).debtor_weight == 10

    # WHEN
    a_x.edit_brandunit_name(
        old_name=swim_text, new_name=jog_text, allow_brand_overwite=True
    )

    # THEN
    assert camping_idea._brandlinks.get(swim_text) is None
    assert camping_idea._brandlinks.get(jog_text) != None
    assert camping_idea._brandlinks.get(jog_text).creditor_weight == 12
    assert camping_idea._brandlinks.get(jog_text).debtor_weight == 13


def test_agent_add_idea_CreatesMissingBrands():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_brandunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    brandlink_z = brandlink_shop(name=family_text)
    clean_kitchen_idea.set_brandlink(brandlink=brandlink_z)
    assert len(a_x._brands) == 0
    assert a_x._brands.get(family_text) is None

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_brands=True,
    )

    # THEN
    assert len(a_x._brands) == 1
    assert a_x._brands.get(family_text) != None
    assert a_x._brands.get(family_text)._allys in (None, {})


def test_agent_add_idea_DoesNotOverwriteBrands():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_brandunits_empty_if_null()
    new_idea_parent_road = f"{src_text},work,cleaning"
    clean_kitchen_text = "clean_kitchen"
    clean_kitchen_idea = IdeaKid(_weight=40, _desc=clean_kitchen_text, promise=True)

    family_text = "family"
    brandlink_z = brandlink_shop(name=family_text)
    clean_kitchen_idea.set_brandlink(brandlink=brandlink_z)

    brandunit_z = brandunit_shop(name=family_text)
    brandunit_z.set_allylink(allylink=allylink_shop(name="ann1"))
    brandunit_z.set_allylink(allylink=allylink_shop(name="bet1"))
    a_x.set_brandunit(brandunit=brandunit_z)

    # assert len(a_x._brands) == 0
    # assert a_x._brands.get(family_text) is None
    assert len(a_x._brands) == 1
    assert len(a_x._brands.get(family_text)._allys) == 2

    # WHEN
    a_x.add_idea(
        idea_kid=clean_kitchen_idea,
        walk=new_idea_parent_road,
        create_missing_ideas_brands=True,
    )

    # THEN

    # assert len(a_x._brands) == 1
    # assert len(a_x._brands.get(family_text)._allys) == 0
    # brandunit_z = brandunit_shop(name=family_text)
    # brandunit_z.set_allylink(allylink=allylink_shop(name="ann2"))
    # brandunit_z.set_allylink(allylink=allylink_shop(name="bet2"))
    # a_x.set_brandunit(brandunit=brandunit_z)

    assert len(a_x._brands) == 1
    assert len(a_x._brands.get(family_text)._allys) == 2


def test_agent_set_brandunits_create_missing_allys_DoesCreateMissingAllys():
    # GIVEN
    src_text = "src"
    a_x = AgentUnit(_desc=src_text)
    a_x.set_allys_empty_if_null()
    a_x.set_brandunits_empty_if_null()
    family_text = "family"
    anna_text = "anna"
    beto_text = "beto"
    brandunit_z = brandunit_shop(name=family_text)
    brandunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    brandunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert brandunit_z._allys.get(anna_text).creditor_weight == 3
    assert brandunit_z._allys.get(anna_text).debtor_weight == 7

    assert brandunit_z._allys.get(beto_text).creditor_weight == 5
    assert brandunit_z._allys.get(beto_text).debtor_weight == 11

    assert len(a_x._allys) == 0
    assert len(a_x._brands) == 0

    # WHEN
    a_x.set_brandunit(brandunit=brandunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert len(a_x._brands) == 3
    assert a_x._allys.get(anna_text).creditor_weight == 3
    assert a_x._allys.get(anna_text).debtor_weight == 7

    assert a_x._allys.get(beto_text).creditor_weight == 5
    assert a_x._allys.get(beto_text).debtor_weight == 11


def test_agent_set_brandunits_create_missing_allys_DoesNotReplaceAllys():
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
    brandunit_z = brandunit_shop(name=family_text)
    brandunit_z.set_allylink(
        allylink=allylink_shop(name=anna_text, creditor_weight=3, debtor_weight=7)
    )
    brandunit_z.set_allylink(
        allylink=allylink_shop(name=beto_text, creditor_weight=5, debtor_weight=11)
    )

    assert brandunit_z._allys.get(anna_text).creditor_weight == 3
    assert brandunit_z._allys.get(anna_text).debtor_weight == 7
    assert brandunit_z._allys.get(beto_text).creditor_weight == 5
    assert brandunit_z._allys.get(beto_text).debtor_weight == 11
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71

    # WHEN
    a_x.set_brandunit(brandunit=brandunit_z, create_missing_allys=True)

    # THEN
    assert len(a_x._allys) == 2
    assert a_x._allys.get(anna_text).creditor_weight == 17
    assert a_x._allys.get(anna_text).debtor_weight == 88
    assert a_x._allys.get(beto_text).creditor_weight == 46
    assert a_x._allys.get(beto_text).debtor_weight == 71


def test_agent_get_brandunits_dict_CorrectlyReturnsDictOfBrands():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text))
    sx.set_brandunit(brandunit=brandunit_shop(name=walk_text))
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text))
    assert len(sx._brands) == 3

    # WHEN
    brandunit_list_x = sx.get_brandunits_name_list()

    # THEN
    assert brandunit_list_x[0] == ""
    assert brandunit_list_x[1] == fly_text
    assert brandunit_list_x[2] == swim_text
    assert brandunit_list_x[3] == walk_text
    assert len(brandunit_list_x) == 4


def test_agent_set_all_brandunits_uids_unique_CorrectlySetsEmptyBrandUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text))
    sx.set_brandunit(brandunit=brandunit_shop(name=walk_text))
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text))
    assert sx._brands[swim_text].uid is None
    assert sx._brands[walk_text].uid is None
    assert sx._brands[fly_text].uid is None

    # WHEN
    sx.set_all_brandunits_uids_unique()

    # THEN
    assert sx._brands[swim_text].uid != None
    assert sx._brands[walk_text].uid != None
    assert sx._brands[fly_text].uid != None


def test_agent_set_all_brandunits_uids_unique_CorrectlySetsChangesSameBrandUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=walk_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text))
    assert sx._brands[swim_text].uid == 3
    assert sx._brands[walk_text].uid == 3
    assert sx._brands[fly_text].uid is None

    # WHEN
    sx.set_all_brandunits_uids_unique()

    # THEN
    print(f"{sx._brands[swim_text].uid=}")
    print(f"{sx._brands[walk_text].uid=}")
    assert sx._brands[swim_text].uid != sx._brands[walk_text].uid
    assert sx._brands[walk_text].uid != 3
    assert sx._brands[walk_text].uid != 3
    assert sx._brands[fly_text].uid != None


def test_agent_set_all_brandunits_uids_unique_CorrectlySetsChangesSameBrandUIDs():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=walk_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text))
    assert sx._brands[swim_text].uid == 3
    assert sx._brands[walk_text].uid == 3
    assert sx._brands[fly_text].uid is None

    # WHEN
    sx.set_all_brandunits_uids_unique()

    # THEN
    print(f"{sx._brands[swim_text].uid=}")
    print(f"{sx._brands[walk_text].uid=}")
    assert sx._brands[swim_text].uid != sx._brands[walk_text].uid
    assert sx._brands[walk_text].uid != 3
    assert sx._brands[walk_text].uid != 3
    assert sx._brands[fly_text].uid != None


def test_agent_all_brandunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    src_text = "src"
    sx = AgentUnit(_desc=src_text)
    sx.set_allys_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=walk_text, uid=3))
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text))
    assert sx._brands[swim_text].uid == 3
    assert sx._brands[walk_text].uid == 3
    assert sx._brands[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_brandunits_uids_are_unique() == False

    # WHEN2
    sx.set_brandunit(brandunit=brandunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_brandunits_uids_are_unique() == False

    # WHEN3
    sx.set_brandunit(brandunit=brandunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_brandunits_uids_are_unique()
