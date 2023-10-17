from src.pact.examples.example_pacts import (
    pact_v001 as example_pacts_pact_v001,
)
from src.pact.party import PartyTitle, partyunit_shop
from src.pact.group import GroupBrand, balancelink_shop, groupunit_shop
from src.pact.pact import PactUnit


def test_pact_get_tree_metrics_TracksRequiredsThatHaveNoAcptFactBases():
    x_pact = example_pacts_pact_v001()
    x_pact_metrics = x_pact.get_tree_metrics()

    print(f"{x_pact_metrics.level_count=}")
    print(f"{x_pact_metrics.required_bases=}")
    assert x_pact_metrics != None
    required_bases_x = x_pact_metrics.required_bases
    assert required_bases_x != None
    assert len(required_bases_x) > 0


def test_pact_get_missing_acptfact_bases_ReturnsAllBasesNotCoveredByAcptFacts():
    x_pact = example_pacts_pact_v001()
    missing_bases = x_pact.get_missing_acptfact_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    x_pact.set_acptfact(
        base="{root_label()},day_minute",
        pick="{root_label()},day_minute",
        open=0,
        nigh=1439,
    )
    missing_bases = x_pact.get_missing_acptfact_bases()

    assert len(missing_bases) == 11


def test_pact_3AdvocatesNoIdeaKid():
    # GIVEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    x_pact = PactUnit(_healer="prom")
    au_rico = partyunit_shop(title=rico_text, uid=7)
    au_carm = partyunit_shop(title=carm_text, uid=2)
    au_patr = partyunit_shop(title=patr_text, uid=13)
    # print(f"{rico=}")
    x_pact.set_partyunit(partyunit=au_rico)
    x_pact.set_partyunit(partyunit=au_carm)
    x_pact.set_partyunit(partyunit=au_patr)
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(rico_text), creditor_weight=10)
    )
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(carm_text), creditor_weight=10)
    )
    x_pact._idearoot.set_balancelink(
        balancelink=balancelink_shop(brand=GroupBrand(patr_text), creditor_weight=10)
    )

    # WHEN
    assert x_pact.get_partys_metrics() != None
    partys_metrics = x_pact.get_partys_metrics()

    # THEN
    balancelink_rico = partys_metrics[rico_text]
    balancelink_carm = partys_metrics[carm_text]
    balancelink_patr = partys_metrics[patr_text]
    assert balancelink_rico.brand != None
    assert balancelink_carm.brand != None
    assert balancelink_patr.brand != None
    assert balancelink_rico.brand == rico_text
    assert balancelink_carm.brand == carm_text
    assert balancelink_patr.brand == patr_text
    all_groups = x_pact._groups
    groupunit_rico = all_groups[rico_text]
    groupunit_carm = all_groups[carm_text]
    groupunit_patr = all_groups[patr_text]
    assert groupunit_rico._single_party == True
    assert groupunit_carm._single_party == True
    assert groupunit_patr._single_party == True


def test_pact_get_partyunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    x_pact = PactUnit(_healer="prom")
    x_pact.set_partyunit(partyunit=partyunit_shop(title=rico_text, uid=4))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=carr_text, uid=13))
    x_pact.set_partyunit(partyunit=partyunit_shop(title=patr_text, uid=7))

    # WHEN/THEN
    assert x_pact.get_partyunits_uid_max() == 13


def test_pact_get_groupunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    x_pact = PactUnit(_healer="prom")
    x_pact.set_groupunit(groupunit=groupunit_shop(brand=rico_text, uid=4))
    x_pact.set_groupunit(groupunit=groupunit_shop(brand=carr_text, uid=12))
    x_pact.set_groupunit(groupunit=groupunit_shop(brand=patr_text, uid=7))

    # WHEN/THEN
    assert x_pact.get_groupunits_uid_max() == 12
