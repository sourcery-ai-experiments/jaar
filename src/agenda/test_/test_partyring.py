from src.agenda.party import (
    PartyPID,
    PartyTitle,
    partyrings_get_from_json,
    PartyRing,
)
from src.agenda.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyPID_exists():
    cersei_pid = PartyPID("Cersei")
    assert cersei_pid != None
    assert str(type(cersei_pid)).find(".party.PartyPID") > 0


def test_PartyTitle_exists():
    cersei_pid = PartyTitle("Cersei")
    assert cersei_pid != None
    assert str(type(cersei_pid)).find(".party.PartyTitle") > 0


def test_partyrings_exists():
    cersei_pid = PartyPID("Cersei")
    friend_link = PartyRing(pid=cersei_pid)
    assert friend_link.pid == cersei_pid


def test_partyrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    party_pid = PartyPID("bob")
    party_ring = PartyRing(pid=party_pid)
    print(f"{party_ring}")

    # WHEN
    x_dict = party_ring.get_dict()

    # THEN
    assert x_dict != None
    assert x_dict == {"pid": str(party_pid)}


def test_partyrings_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {yao_text: {"pid": yao_text}}
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partyrings_get_from_json(partyrings_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None
    yao_partyring = PartyRing(pid=yao_text)
    partyrings_dict = {yao_partyring.pid: yao_partyring}
    assert yao_obj_dict == partyrings_dict
