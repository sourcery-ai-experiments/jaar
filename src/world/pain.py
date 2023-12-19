from dataclasses import dataclass
from src.economy.economy import EconomyQID
from src.agenda.agenda import PersonID


@dataclass
class EconomyLink:
    economy_id: EconomyQID
    weight: float
    _relative_weight: float = None
    _manager_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance

    def get_dict(self) -> dict:
        return {"economy_id": self.economy_id, "weight": self.weight}


def economylink_shop(economy_id: EconomyQID, weight: float = None) -> EconomyLink:
    if weight is None:
        weight = 1
    return EconomyLink(economy_id=economy_id, weight=weight)


@dataclass
class HealerLink:
    person_id: PersonID
    weight: float
    in_tribe: bool
    _economylinks: dict[EconomyQID:EconomyLink] = None
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

    def set_economylinks_empty_if_none(self):
        if self._economylinks is None:
            self._economylinks = {}

    def set_economylink(self, economylink: EconomyLink):
        self._economylinks[economylink.economy_id] = economylink

    def get_economylink(self, economyeconomy_id: EconomyQID) -> EconomyLink:
        return self._economylinks.get(economyeconomy_id)

    def del_economylink(self, economyeconomy_id: EconomyQID):
        self._economylinks.pop(economyeconomy_id)

    def get_economylinks_dict(self) -> dict:
        return {
            economylink_x.economy_id: economylink_x.get_dict()
            for economylink_x in self._economylinks.values()
        }

    def get_dict(self):
        return {
            "person_id": self.person_id,
            "weight": self.weight,
            "_economylinks": self.get_economylinks_dict(),
        }


def healerlink_shop(
    person_id: PersonID, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_id=person_id, weight=weight, in_tribe=in_tribe)
    x_healer.set_economylinks_empty_if_none()
    return x_healer


class PainGenus(str):  # Created to help track the concept
    pass


@dataclass
class PainUnit:
    genus: PainGenus
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

    def set_healerlinks_empty_if_none(self):
        if self._healerlinks is None:
            self._healerlinks = {}

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.person_id] = healerlink

    def get_healerlink(self, person_id: PersonID) -> HealerLink:
        return self._healerlinks.get(person_id)

    def del_healerlink(self, person_id: PersonID):
        self._healerlinks.pop(person_id)

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.person_id: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self):
        return {
            "genus": self.genus,
            "weight": self.weight,
            "_healerlinks": self.get_healerlinks_dict(),
        }


def painunit_shop(genus: PainGenus, weight: float = None) -> PainUnit:
    if weight is None:
        weight = 1
    pain_x = PainUnit(genus=genus, weight=weight)
    pain_x.set_healerlinks_empty_if_none()
    return pain_x
