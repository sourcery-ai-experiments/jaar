from dataclasses import dataclass
from src._prime.road import EconomyID, PersonID, ProblemID, HealerID


@dataclass
class EconomyLink:
    economy_id: EconomyID
    weight: float
    _relative_weight: float = None
    _manager_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance

    def get_dict(self) -> dict:
        return {"economy_id": self.economy_id, "weight": self.weight}


def economylink_shop(economy_id: EconomyID, weight: float = None) -> EconomyLink:
    if weight is None:
        weight = 1
    return EconomyLink(economy_id=economy_id, weight=weight)


@dataclass
class HealerLink:
    healer_id: HealerID
    weight: float
    in_tribe: bool
    _economylinks: dict[EconomyID:EconomyLink] = None
    _relative_weight: float = None
    _manager_importance: float = None

    def set_economylinks_weight_metrics(self):
        total_economylinks_weight = sum(
            x_economylink.weight for x_economylink in self._economylinks.values()
        )
        for x_economylink in self._economylinks.values():
            x_economylink.set_relative_weight(
                x_economylink.weight / total_economylinks_weight
            )
            x_economylink.set_manager_importance(
                x_economylink._relative_weight * self._manager_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance
        self.set_economylinks_weight_metrics()

    def set_economylink(self, economylink: EconomyLink):
        self._economylinks[economylink.economy_id] = economylink

    def economylink_exists(self, economy_id: EconomyID):
        return self._economylinks.get(economy_id) != None

    def get_economylink(self, economy_id: EconomyID) -> EconomyLink:
        return self._economylinks.get(economy_id)

    def del_economylink(self, economy_id: EconomyID):
        self._economylinks.pop(economy_id)

    def get_economylinks_dict(self) -> dict:
        return {
            economylink_x.economy_id: economylink_x.get_dict()
            for economylink_x in self._economylinks.values()
        }

    def get_dict(self):
        return {
            "healer_id": self.healer_id,
            "weight": self.weight,
            "_economylinks": self.get_economylinks_dict(),
        }


def healerlink_shop(
    healer_id: HealerID, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    return HealerLink(
        healer_id=healer_id, weight=weight, in_tribe=in_tribe, _economylinks={}
    )


@dataclass
class ProblemUnit:
    problem_id: ProblemID
    weight: float = None
    _healerlinks: dict[PersonID:HealerLink] = None
    _relative_weight: float = None
    _manager_importance: float = None

    def set_healerlinks_weight_metrics(self):
        total_healerlinks_weight = sum(
            x_healerlink.weight for x_healerlink in self._healerlinks.values()
        )

        for x_healerlink in self._healerlinks.values():
            x_healerlink.set_relative_weight(
                x_healerlink.weight / total_healerlinks_weight
            )
            x_healerlink.set_manager_importance(
                x_healerlink._relative_weight * self._manager_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight
        self.set_manager_importance(self._relative_weight)

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance
        self.set_healerlinks_weight_metrics()

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.healer_id] = healerlink

    def get_healerlink(self, healer_id: HealerID) -> HealerLink:
        return self._healerlinks.get(healer_id)

    def del_healerlink(self, healer_id: HealerID):
        self._healerlinks.pop(healer_id)

    def economylink_exists(self, economy_id: EconomyID):
        return any(
            x_healerlink.economylink_exists(economy_id)
            for x_healerlink in self._healerlinks.values()
        )

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.healer_id: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self):
        return {
            "problem_id": self.problem_id,
            "weight": self.weight,
            "_healerlinks": self.get_healerlinks_dict(),
        }


def problemunit_shop(problem_id: ProblemID, weight: float = None) -> ProblemUnit:
    if weight is None:
        weight = 1
    return ProblemUnit(problem_id=problem_id, weight=weight, _healerlinks={})
