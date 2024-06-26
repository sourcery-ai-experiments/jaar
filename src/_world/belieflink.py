from src._instrument.python import get_1_if_None
from dataclasses import dataclass


class BeliefID(str):  # Created to help track the concept
    pass


@dataclass
class BeliefCore:
    belief_id: BeliefID = None


@dataclass
class BeliefLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str:str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }


def belieflink_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> BeliefLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BeliefLink(
        belief_id=belief_id, credor_weight=credor_weight, debtor_weight=debtor_weight
    )
