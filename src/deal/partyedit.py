from dataclasses import dataclass
from src._prime.road import PartyID, PersonID
from src.agenda.party import get_default_depotlink_type
from src.tools.python import return0ifnone


@dataclass
class PartyEditUnit:
    member: PersonID = None
    party_id: PartyID = None
    creditor_weight: float = None
    debtor_weight: float = None
    depotlink_type: str = None

    def set_member(self, x_member: PersonID):
        self.member = x_member


class partyeditrunit_shop_Exception(Exception):
    pass


def partyeditunit_shop(
    member: PersonID = None,
    party_id: PartyID = None,
    creditor_weight: float = None,
    debtor_weight: float = None,
    depotlink_type: str = None,
) -> PartyEditUnit:
    if party_id is None:
        raise partyeditrunit_shop_Exception("party_id may not be None")

    if depotlink_type is None:
        depotlink_type = get_default_depotlink_type()

    return PartyEditUnit(
        member=member,
        party_id=party_id,
        creditor_weight=return0ifnone(creditor_weight),
        debtor_weight=return0ifnone(debtor_weight),
        depotlink_type=depotlink_type,
    )
