from dataclasses import dataclass
from src.heal.heal import HealUnit, HealKind, healunit_shop


@dataclass
class HealLink:
    kind: HealKind
    weight: float

    def get_dict(self) -> dict:
        return {"kind": self.kind, "weight": self.weight}


def heallink_shop(kind: HealKind, weight: float = None) -> HealLink:
    if weight is None:
        weight = 1
    return HealLink(kind=kind, weight=weight)


class PersonName(str):
    pass


@dataclass
class PersonLink:
    person_name: PersonName
    weight: float

    def get_dict(self):
        return {"person_name": self.person_name, "weight": self.weight}


def personlink_shop(person_name: PersonName, weight: float = None) -> PersonLink:
    if weight is None:
        weight = 1
    return PersonLink(person_name=person_name, weight=weight)


class PainKind(str):
    pass


@dataclass
class PainUnit:
    kind: PainKind
    _heallinks: dict[HealKind:HealLink] = None
    _personlinks: dict[PersonName:PersonLink] = None

    def set_heallinks_empty_if_none(self):
        if self._heallinks is None:
            self._heallinks = {}

    def set_heallink(self, heallink: HealLink):
        self._heallinks[heallink.kind] = heallink

    def get_heallink(self, healkind: HealKind) -> HealLink:
        return self._heallinks.get(healkind)

    def del_heallink(self, healkind: HealKind):
        self._heallinks.pop(healkind)

    def set_personlinks_empty_if_none(self):
        if self._personlinks is None:
            self._personlinks = {}

    def set_personlink(self, personlink: PersonLink):
        self._personlinks[personlink.person_name] = personlink

    def get_personlink(self, person_name: PersonName) -> PersonLink:
        return self._personlinks.get(person_name)

    def del_personlink(self, person_name: PersonName):
        self._personlinks.pop(person_name)

    def get_heallinks_dict(self) -> dict:
        return {
            heallink_x.kind: heallink_x.get_dict()
            for heallink_x in self._heallinks.values()
        }

    def get_personlinks_dict(self) -> dict:
        return {
            personlink_x.person_name: personlink_x.get_dict()
            for personlink_x in self._personlinks.values()
        }

    def get_dict(self):
        return {
            "kind": self.kind,
            "_heallinks": self.get_heallinks_dict(),
            "_personlinks": self.get_personlinks_dict(),
        }


def painunit_shop(kind: PainKind):
    pain_x = PainUnit(kind=kind)
    pain_x.set_heallinks_empty_if_none()
    pain_x.set_personlinks_empty_if_none()
    return pain_x
