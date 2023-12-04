from src.agenda.road import Road, is_sub_road
from src.culture.culture import CultureQID
from src.world.person import PersonID, PersonUnit, personunit_shop
from dataclasses import dataclass


@dataclass
class CultureAddress:
    culture_qid: CultureQID
    person_ids: dict[PersonID:int]

    def set_person_ids_empty_if_none(self):
        if self.person_ids is None:
            self.person_ids = {}

    def add_person_id(self, person_id: PersonID):
        self.person_ids[person_id] = 0


def cultureaddress_shop(
    culture_qid: CultureQID, person_ids: dict[PersonID:int] = None
) -> CultureAddress:
    x_cultureaddress = CultureAddress(person_ids=person_ids, culture_qid=culture_qid)
    x_cultureaddress.set_person_ids_empty_if_none()
    return x_cultureaddress


def create_cultureaddress(person_id: PersonID, culture_qid: CultureQID):
    x_cultureaddress = cultureaddress_shop(culture_qid=culture_qid)
    x_cultureaddress.add_person_id(person_id)
    return x_cultureaddress


class ConcernSubRoadException(Exception):
    pass


@dataclass
class ConcernUnit:
    cultureaddress: CultureAddress
    _concern_subject: Road = None
    _concern_good: Road = None
    _concern_bad: Road = None
    _action_subject: Road = None
    _action_postive: Road = None
    _action_negative: Road = None

    def set_good(self, subject_road: Road, good_road: Road, bad_road: Road):
        self._check_subject_road(subject_road)
        if is_sub_road(bad_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_bad '{bad_road}' failed because subject road '{subject_road}' is not subroad"
            )
        if is_sub_road(good_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_good '{good_road}' failed because subject road '{subject_road}' is not subroad"
            )
        self._concern_subject = subject_road
        self._concern_good = good_road
        self._concern_bad = bad_road

    def set_action(self, subject_road: Road, positive_road: Road, negative_road: Road):
        self._check_subject_road(subject_road)
        if is_sub_road(negative_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting action_negative '{negative_road}' failed because subject road '{subject_road}' is not subroad"
            )
        if is_sub_road(positive_road, subject_road) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting action_positive '{positive_road}' failed because subject road '{subject_road}' is not subroad"
            )
        self._action_subject = subject_road
        self._action_postive = positive_road
        self._action_negative = negative_road

    def _check_subject_road(self, road: Road) -> bool:
        if is_sub_road(road, self.cultureaddress.culture_qid) == False:
            raise ConcernSubRoadException(
                f"ConcernUnit setting concern_subject '{road}' failed because culture_qid is not first node."
            )


def concernunit_shop(
    cultureaddress: CultureAddress,
    concern_subject: Road = None,
    concern_good: Road = None,
    concern_bad: Road = None,
    action_subject: Road = None,
    action_postive: Road = None,
    action_negative: Road = None,
) -> ConcernUnit:
    x_concernunit = ConcernUnit(cultureaddress=cultureaddress)
    x_concernunit.set_good(concern_subject, concern_good, concern_bad)
    x_concernunit.set_action(action_subject, action_postive, action_negative)
    return x_concernunit


class PersonExistsException(Exception):
    pass


class WorldMark(str):  # Created to help track the concept
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    _persons_dir: str = None
    _world_dir: str = None
    _personunits: dict[PersonID:PersonUnit] = None

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"

    def _set_personunits_empty_if_null(self):
        if self._personunits is None:
            self._personunits = {}

    def personunit_exists(self, person_id: PersonID):
        return self._personunits.get(person_id) != None

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._personunits[personunit.pid] = personunit

    def set_personunit(self, personunit: PersonUnit):
        self._set_person_in_memory(personunit)

    def add_personunit(self, person_id: PersonID):
        x_personunit = personunit_shop(person_id, self._get_person_dir(person_id))
        if self.personunit_exists(x_personunit.pid) == False:
            self.set_personunit(x_personunit)
        else:
            raise PersonExistsException(
                f"add_personunit fail: {x_personunit.pid} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def add_cultural_connection(
        self,
        cultureaddress: CultureAddress,
        council_person_id: PersonID,
    ):
        culture_qid = cultureaddress.culture_qid

        for culture_person_id in cultureaddress.person_ids.keys():
            if self.personunit_exists(culture_person_id) == False:
                self.add_personunit(culture_person_id)
            x_personunit = self.get_personunit_from_memory(culture_person_id)

            if x_personunit.cultureunit_exists(culture_qid) == False:
                x_personunit.add_cultureunit(culture_qid)
            x_culture = x_personunit.get_cultureunit(culture_qid)

            if self.personunit_exists(council_person_id) == False:
                self.add_personunit(council_person_id)

            if x_culture.councilunit_exists(culture_person_id) == False:
                x_culture.add_councilunit(culture_person_id)
            if x_culture.councilunit_exists(council_person_id) == False:
                x_culture.add_councilunit(council_person_id)


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_personunits_empty_if_null()
    return world_x
