from dataclasses import dataclass
from src._prime.road import PartyID
from src.agenda.party import get_default_depotlink_type
from src.tools.python import return0ifnone


@dataclass
class DeltaUnit:
    party_id: PartyID
    creditor_weight: float
    debtor_weight: float
    depotlink_type: str


def deltaunit_shop(
    party_id: PartyID,
    creditor_weight: float = None,
    debtor_weight: float = None,
    depotlink_type: str = None,
) -> DeltaUnit:
    if depotlink_type is None:
        depotlink_type = get_default_depotlink_type()

    return DeltaUnit(
        party_id=party_id,
        creditor_weight=return0ifnone(creditor_weight),
        debtor_weight=return0ifnone(debtor_weight),
        depotlink_type=depotlink_type,
    )
