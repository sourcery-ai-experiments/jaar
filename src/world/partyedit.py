from dataclasses import dataclass
from src._prime.road import PartyID, PersonID
from src.agenda.party import get_default_depotlink_type, PartyUnit
from src.tools.python import get_0_if_None


@dataclass
class PartyEditUnit(PartyUnit):
    deal_member: PersonID = None
    creditor_change: float = None
    debtor_change: float = None

    def set_deal_member(self, x_deal_member: PersonID):
        self.deal_member = x_deal_member


class partyeditrunit_shop_Exception(Exception):
    pass


def partyeditunit_shop(
    deal_member: PersonID = None,
    party_id: PartyID = None,
    creditor_change: float = None,
    debtor_change: float = None,
    depotlink_type: str = None,
) -> PartyEditUnit:
    if party_id is None:
        raise partyeditrunit_shop_Exception("party_id may not be None")

    if depotlink_type is None:
        depotlink_type = get_default_depotlink_type()

    return PartyEditUnit(
        deal_member=deal_member,
        party_id=party_id,
        creditor_change=get_0_if_None(creditor_change),
        debtor_change=get_0_if_None(debtor_change),
        depotlink_type=depotlink_type,
    )
