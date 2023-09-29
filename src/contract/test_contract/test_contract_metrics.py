from src.contract.examples.example_contracts import (
    contract_v001 as example_contracts_contract_v001,
)
from src.contract.party import PartyName, partyunit_shop
from src.contract.group import GroupName, grouplink_shop, groupunit_shop
from src.contract.contract import ContractUnit


def test_contract_get_tree_metrics_TracksRequiredsThatHaveNoAcptFactBases():
    lw_x = example_contracts_contract_v001()
    lw_x_metrics = lw_x.get_tree_metrics()

    print(f"{lw_x_metrics.level_count=}")
    print(f"{lw_x_metrics.required_bases=}")
    assert lw_x_metrics != None
    required_bases_x = lw_x_metrics.required_bases
    assert required_bases_x != None
    assert len(required_bases_x) > 0


def test_contract_get_missing_acptfact_bases_ReturnsAllBasesNotCoveredByAcptFacts():
    lw_x = example_contracts_contract_v001()
    missing_bases = lw_x.get_missing_acptfact_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    lw_x.set_acptfact(
        base="{root_label()},day_minute",
        pick="{root_label()},day_minute",
        open=0,
        nigh=1439,
    )
    missing_bases = lw_x.get_missing_acptfact_bases()

    assert len(missing_bases) == 11


def test_contract_3AdvocatesNoIdeaKid():
    # GIVEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    a_x = ContractUnit(_owner="prom")
    au_rico = partyunit_shop(name=rico_text, uid=7)
    au_carm = partyunit_shop(name=carm_text, uid=2)
    au_patr = partyunit_shop(name=patr_text, uid=13)
    # print(f"{rico=}")
    a_x.set_partyunit(partyunit=au_rico)
    a_x.set_partyunit(partyunit=au_carm)
    a_x.set_partyunit(partyunit=au_patr)
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName(rico_text), creditor_weight=10)
    )
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName(carm_text), creditor_weight=10)
    )
    a_x._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName(patr_text), creditor_weight=10)
    )

    # WHEN
    assert a_x.get_partys_metrics() != None
    partys_metrics = a_x.get_partys_metrics()

    # THEN
    grouplink_rico = partys_metrics[rico_text]
    grouplink_carm = partys_metrics[carm_text]
    grouplink_patr = partys_metrics[patr_text]
    assert grouplink_rico.name != None
    assert grouplink_carm.name != None
    assert grouplink_patr.name != None
    assert grouplink_rico.name == rico_text
    assert grouplink_carm.name == carm_text
    assert grouplink_patr.name == patr_text
    all_groups = a_x._groups
    groupunit_rico = all_groups[rico_text]
    groupunit_carm = all_groups[carm_text]
    groupunit_patr = all_groups[patr_text]
    assert groupunit_rico._single_party == True
    assert groupunit_carm._single_party == True
    assert groupunit_patr._single_party == True


def test_contract_get_partyunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    lw_x = ContractUnit(_owner="prom")
    lw_x.set_partyunit(partyunit=partyunit_shop(name=rico_text, uid=4))
    lw_x.set_partyunit(partyunit=partyunit_shop(name=carr_text, uid=13))
    lw_x.set_partyunit(partyunit=partyunit_shop(name=patr_text, uid=7))

    # WHEN/THEN
    assert lw_x.get_partyunits_uid_max() == 13


def test_contract_get_groupunits_uid_max_WorksCorrectly():
    # GIVEN
    rico_text = "rico"
    carr_text = "carmen"
    patr_text = "patrick"

    lw_x = ContractUnit(_owner="prom")
    lw_x.set_groupunit(groupunit=groupunit_shop(name=rico_text, uid=4))
    lw_x.set_groupunit(groupunit=groupunit_shop(name=carr_text, uid=12))
    lw_x.set_groupunit(groupunit=groupunit_shop(name=patr_text, uid=7))

    # WHEN/THEN
    assert lw_x.get_groupunits_uid_max() == 12
