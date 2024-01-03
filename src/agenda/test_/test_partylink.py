from src.agenda.party import (
    PartyPID,
    partylink_shop,
    partylinks_get_from_json,
)
from src.tools.python import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyLink_exists():
    # GIVEN
    bikers_pid = PartyPID("Yao")

    # WHEN
    party_link_x = partylink_shop(pid=bikers_pid)

    # THEN
    assert party_link_x.pid == bikers_pid
    assert party_link_x.creditor_weight == 1.0
    assert party_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    party_link_x = partylink_shop(
        pid=bikers_pid,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
        _agenda_credit=0.7,
        _agenda_debt=0.51,
        _agenda_intent_credit=0.66,
        _agenda_intent_debt=0.55,
    )

    # THEN
    assert party_link_x.creditor_weight == bikers_creditor_weight
    assert party_link_x.debtor_weight == bikers_debtor_weight
    assert party_link_x._agenda_credit != None
    assert party_link_x._agenda_credit == 0.7
    assert party_link_x._agenda_debt == 0.51
    assert party_link_x._agenda_intent_credit == 0.66
    assert party_link_x._agenda_intent_debt == 0.55


def test_partylink_shop_set_agenda_credit_debt_CorrectlyWorks():
    # GIVEN
    bikers_pid = PartyPID("Yao")
    bikers_creditor_weight = 3.0
    partylinks_sum_creditor_weight = 60
    group_agenda_credit = 0.5
    group_agenda_intent_credit = 0.98

    bikers_debtor_weight = 13.0
    partylinks_sum_debtor_weight = 26.0
    group_agenda_debt = 0.9
    group_agenda_intent_debt = 0.5151

    party_link_x = partylink_shop(
        pid=bikers_pid,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert party_link_x._agenda_credit is None
    assert party_link_x._agenda_debt is None
    assert party_link_x._agenda_intent_credit is None
    assert party_link_x._agenda_intent_debt is None

    # WHEN
    party_link_x.set_agenda_credit_debt(
        partylinks_creditor_weight_sum=partylinks_sum_creditor_weight,
        partylinks_debtor_weight_sum=partylinks_sum_debtor_weight,
        group_agenda_credit=group_agenda_credit,
        group_agenda_debt=group_agenda_debt,
        group_agenda_intent_credit=group_agenda_intent_credit,
        group_agenda_intent_debt=group_agenda_intent_debt,
    )

    # THEN
    assert party_link_x._agenda_credit == 0.025
    assert party_link_x._agenda_debt == 0.45
    assert party_link_x._agenda_intent_credit == 0.049
    assert party_link_x._agenda_intent_debt == 0.25755


def test_partylink_shop_reset_agenda_credit_debt():
    # GIVEN
    biker_pid = "maria"
    biker_party = partylink_shop(pid=biker_pid, _agenda_credit=0.04, _agenda_debt=0.7)
    print(f"{biker_party}")

    assert biker_party._agenda_credit != None
    assert biker_party._agenda_debt != None

    # WHEN
    biker_party.reset_agenda_credit_debt()

    # THEN
    assert biker_party._agenda_credit == 0
    assert biker_party._agenda_debt == 0


def test_partylink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_pid = "Yao"
    biker_pid = PartyPID(str_pid)
    biker_party_link = partylink_shop(
        pid=biker_pid, creditor_weight=12, debtor_weight=19
    )
    print(f"{biker_party_link}")

    # WHEN
    biker_dict = biker_party_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "pid": biker_pid,
        "creditor_weight": 12,
        "debtor_weight": 19,
    }


def test_partylink_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"pid": yao_text, "creditor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partylinks_get_from_json(partylinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_pid = PartyPID(yao_text)
    yao_partylink = partylink_shop(pid=yao_pid, creditor_weight=12, debtor_weight=19)
    partylinks_dict = {yao_partylink.pid: yao_partylink}
    assert yao_obj_dict == partylinks_dict


def test_partylink_meld_RaiseSamePIDException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partylink_shop(pid=todd_text)
    mery_text = "Merry"
    mery_party = partylink_shop(pid=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyLink='{todd_party.pid}' not the same as PartyLink='{mery_party.pid}"
    )


def test_partylink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partylink_shop(pid=todd_text, creditor_weight=12, debtor_weight=19)
    todd_party2 = partylink_shop(pid=todd_text, creditor_weight=33, debtor_weight=3)
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 45
    assert todd_party1.debtor_weight == 22
