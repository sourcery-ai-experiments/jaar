from src.agent.examples.example_agents import agent_v001 as example_agents_agent_v001
from src.agent.ally import AllyName, allyunit_shop
from src.agent.brand import BrandName, brandlink_shop, brandunit_shop
from src.agent.agent import AgentUnit


def test_agent_get_tree_metrics_TracksRequiredsThatHaveNoAcptFactBases():
    lw_x = example_agents_agent_v001()
    lw_x_metrics = lw_x.get_tree_metrics()

    print(f"{lw_x_metrics.levelCount=}")
    print(f"{lw_x_metrics.required_bases=}")
    assert lw_x_metrics != None
    required_bases_x = lw_x_metrics.required_bases
    assert required_bases_x != None
    assert len(required_bases_x) > 0


def test_agent_get_missing_acptfact_bases_ReturnsAllBasesNotCoveredByAcptFacts():
    lw_x = example_agents_agent_v001()
    missing_bases = lw_x.get_missing_acptfact_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    lw_x.set_acptfact(base="TlME,day_minute", pick="TlME,day_minute", open=0, nigh=1439)
    missing_bases = lw_x.get_missing_acptfact_bases()

    assert len(missing_bases) == 11


def test_agent_3AdvocatesNoIdeaKid():
    # GIVEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    a_x = AgentUnit(_desc="prom")
    au_rico = allyunit_shop(name=rico_text, uid=7)
    au_carm = allyunit_shop(name=carm_text, uid=2)
    au_patr = allyunit_shop(name=patr_text, uid=13)
    # print(f"{rico=}")
    a_x.set_allyunit(allyunit=au_rico)
    a_x.set_allyunit(allyunit=au_carm)
    a_x.set_allyunit(allyunit=au_patr)
    a_x._idearoot.set_brandlink(
        brandlink=brandlink_shop(name=BrandName(rico_text), creditor_weight=10)
    )
    a_x._idearoot.set_brandlink(
        brandlink=brandlink_shop(name=BrandName(carm_text), creditor_weight=10)
    )
    a_x._idearoot.set_brandlink(
        brandlink=brandlink_shop(name=BrandName(patr_text), creditor_weight=10)
    )

    # WHEN
    assert a_x.get_allys_metrics() != None
    allys_metrics = a_x.get_allys_metrics()

    # THEN
    brandlink_rico = allys_metrics[rico_text]
    brandlink_carm = allys_metrics[carm_text]
    brandlink_patr = allys_metrics[patr_text]
    assert brandlink_rico.name != None
    assert brandlink_carm.name != None
    assert brandlink_patr.name != None
    assert brandlink_rico.name == rico_text
    assert brandlink_carm.name == carm_text
    assert brandlink_patr.name == patr_text
    all_brands = a_x._brands
    brandunit_rico = all_brands[rico_text]
    brandunit_carm = all_brands[carm_text]
    brandunit_patr = all_brands[patr_text]
    assert brandunit_rico._single_ally == True
    assert brandunit_carm._single_ally == True
    assert brandunit_patr._single_ally == True


def test_agent_get_allyunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    lw_x = AgentUnit(_desc="prom")
    lw_x.set_allyunit(allyunit=allyunit_shop(name=rico_text, uid=4))
    lw_x.set_allyunit(allyunit=allyunit_shop(name=carr_text, uid=13))
    lw_x.set_allyunit(allyunit=allyunit_shop(name=patr_text, uid=7))

    # WHEN/THEN
    assert lw_x.get_allyunits_uid_max() == 13


def test_agent_get_brandunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    lw_x = AgentUnit(_desc="prom")
    lw_x.set_brandunit(brandunit=brandunit_shop(name=rico_text, uid=4))
    lw_x.set_brandunit(brandunit=brandunit_shop(name=carr_text, uid=12))
    lw_x.set_brandunit(brandunit=brandunit_shop(name=patr_text, uid=7))

    # WHEN/THEN
    assert lw_x.get_brandunits_uid_max() == 12
