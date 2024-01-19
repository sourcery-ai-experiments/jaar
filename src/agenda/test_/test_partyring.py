from src.agenda.party import (
    PartyID,
    PartyTitle,
    partyrings_get_from_json,
    PartyRing,
)
from src.tools.python import x_is_json, x_get_json


def test_PartyID_exists():
    cersei_pid = PartyID("Cersei")
    assert cersei_pid != None
    assert str(type(cersei_pid)).find(".road.PartyID") > 0


def test_PartyTitle_exists():
    cersei_pid = PartyTitle("Cersei")
    assert cersei_pid != None
    assert str(type(cersei_pid)).find(".party.PartyTitle") > 0


def test_partyrings_exists():
    cersei_pid = PartyID("Cersei")
    friend_link = PartyRing(pid=cersei_pid)
    assert friend_link.pid == cersei_pid


def test_partyrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    party_id = PartyID("Bob")
    party_ring = PartyRing(pid=party_id)
    print(f"{party_ring}")

    # WHEN
    x_dict = party_ring.get_dict()

    # THEN
    assert x_dict != None
    assert x_dict == {"pid": str(party_id)}


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
