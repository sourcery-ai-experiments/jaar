from src.agenda.party import PartyID
from src.tools.python import x_is_json, x_get_json


def test_PartyID_exists():
    cersei_party_id = PartyID("Cersei")
    assert cersei_party_id != None
    assert str(type(cersei_party_id)).find(".road.PartyID") > 0
