from src._prime.road import default_road_delimiter_if_none, RoadUnit
from src.agenda.party import partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import assigned_unit_shop
from src.agenda.agenda import agendaunit_shop, balancelink_shop
from src.economy.economy import EconomyUnit, EconomyID

# from src.world.lobby import EconomyDELETEMEaddress, RequestUnit
from src.world.pain import PainGenus, painunit_shop, healerlink_shop, economylink_shop
from src.world.person import PersonID, PersonUnit, personunit_shop
from dataclasses import dataclass


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
    _road_delimiter: str = None

    # def apply_requestunit(self, x_requestunit: RequestUnit):
    #     # create any missing requestees
    #     for requestee_pid in x_requestunit._requestee_pids.keys():
    #         self.set_personunit(requestee_pid, replace_alert=False)
    #     self.set_personunit(x_requestunit._requester_pid, replace_alert=False)

    #     # apply request to economys
    #     x_economydeletemeaddress = x_requestunit._wantunit.economydeletemeaddress
    #     # for x_treasurer_pid in x_economydeletemeaddress.treasurer_pids.keys():
    #     self._apply_requestunit_to_economy(
    #         x_requestunit=x_requestunit,
    #         x_treasurer_pid=x_economydeletemeaddress.treasurer_pid,
    #         x_economy_id=x_economydeletemeaddress.economy_id,
    #     )

    # def _apply_requestunit_to_economy(
    #     self,
    #     x_requestunit: RequestUnit,
    #     x_treasurer_pid: PersonID,
    #     x_economy_id: EconomyID,
    # ):
    #     self.set_personunit(x_treasurer_pid, replace_alert=False)
    #     x_personunit = self.get_personunit_from_memory(x_treasurer_pid)
    #     x_economyunit = x_personunit.get_economyunit(x_economy_id)
    #     x_economyunit.full_setup_clerkunit(x_treasurer_pid)
    #     x_economyunit.full_setup_clerkunit(x_requestunit._requester_pid)
    #     requester_clerkunit = x_economyunit.get_clerkunit(x_requestunit._requester_pid)
    #     requester_contract = requester_clerkunit.get_contract()

    #     # add ideas to requester_contract_agenda
    #     fix_weight = x_requestunit._fix_weight
    #     wantunit_ideas = x_requestunit._wantunit.get_issueunit_ideas(fix_weight)
    #     for x_idea in wantunit_ideas.values():
    #         # TODO ideas should not be added if they already exist. Create test, then change code
    #         requester_contract.add_idea(x_idea, parent_road=x_idea._parent_road)

    #     x_assignedunit = assigned_unit_shop()
    #     x_balancelinks = {}
    #     # for each requestee exist in economy, collect attributes for requester_contract agenda
    #     for requestee_pid in x_requestunit._requestee_pids.keys():
    #         # requestee_contract changes
    #         x_economyunit.full_setup_clerkunit(requestee_pid)
    #         requestee_clerkunit = x_economyunit.get_clerkunit(requestee_pid)
    #         requestee_contract = requestee_clerkunit.get_contract()
    #         requestee_contract.add_partyunit(
    #             x_requestunit._requester_pid,
    #             debtor_weight=fix_weight,
    #             depotlink_type="assignment",
    #         )
    #         requester_contract.add_partyunit(requestee_pid, depotlink_type="assignment")

    #     for request_group in x_requestunit._requestee_groups.keys():
    #         x_groupunit = groupunit_shop(request_group)
    #         for requestee_pid in x_requestunit._requestee_pids.keys():
    #             x_groupunit.set_partylink(partylink_shop(requestee_pid))
    #         requester_contract.set_groupunit(x_groupunit, False, False, True)

    #     if x_requestunit._requestee_groups == {}:
    #         for requestee_pid in x_requestunit._requestee_pids.keys():
    #             # requestee_contract changes
    #             x_assignedunit.set_suffgroup(requestee_pid)
    #             x_balancelinks[requestee_pid] = balancelink_shop(requestee_pid)
    #     else:
    #         for request_group in x_requestunit._requestee_groups.keys():
    #             # requestee_contract changes
    #             x_assignedunit.set_suffgroup(request_group)
    #             x_balancelinks[request_group] = balancelink_shop(request_group)

    #     # for every idea in wantunit set idea attributes to requester_contract
    #     x_isssue = x_requestunit._wantunit.isssue
    #     for x_idea in wantunit_ideas.values():
    #         idea_road = x_idea.get_road()
    #         requester_contract.edit_idea_attr(idea_road, assignedunit=x_assignedunit)
    #         for x_balancelink in x_balancelinks.values():
    #             requester_contract.edit_idea_attr(idea_road, balancelink=x_balancelink)

    #     # if idea is promise set the promise reasonunits
    #     for x_idea in wantunit_ideas.values():
    #         idea_road = x_idea.get_road()
    #         if x_idea.promise:
    #             requester_contract.edit_idea_attr(
    #                 idea_road,
    #                 reason_base=x_isssue.base,
    #                 reason_premise=x_isssue.get_1_factunit(bad=True),
    #             )

    #     requester_contract.set_belief(
    #         x_isssue.base, pick=x_isssue.get_1_factunit(bad=True)
    #     )
    #     requester_clerkunit.save_contract_agenda(requester_contract)
    #     requester_clerkunit.save_refreshed_output_to_public()

    #     # for each requestee re
    #     for requestee_pid in x_requestunit._requestee_pids.keys():
    #         requestee_clerkunit = x_economyunit.get_clerkunit(requestee_pid)
    #         requestee_clerkunit.refresh_depot_agendas()
    #         requestee_clerkunit.save_refreshed_output_to_public()

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"

    def personunit_exists(self, person_id: PersonID):
        return self._personunits.get(person_id) != None

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._personunits[personunit.pid] = personunit

    def set_personunit(
        self,
        person_id: PersonID,
        replace_personunit: bool = False,
        replace_alert: bool = True,
    ):
        x_personunit = personunit_shop(
            person_id,
            self._get_person_dir(person_id),
            _road_delimiter=self._road_delimiter,
        )
        if self.personunit_exists(x_personunit.pid) == False and not replace_personunit:
            self._set_person_in_memory(x_personunit)
        elif replace_alert:
            raise PersonExistsException(
                f"set_personunit fail: {x_personunit.pid} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def add_economy_connection(
        self,
        treasurer_pid: PersonID,
        economy_id: EconomyID,
        clerk_person_id: PersonID,
    ):
        if self.personunit_exists(treasurer_pid) == False:
            self.set_personunit(treasurer_pid)
        x_personunit = self.get_personunit_from_memory(treasurer_pid)

        if x_personunit.economyunit_exists(economy_id) == False:
            x_personunit.set_economyunit(economy_id)
        x_economy = x_personunit.get_economyunit(economy_id)

        if self.personunit_exists(clerk_person_id) == False:
            self.set_personunit(clerk_person_id)

        if x_economy.clerkunit_exists(treasurer_pid) == False:
            x_economy.add_clerkunit(treasurer_pid)
        if x_economy.clerkunit_exists(clerk_person_id) == False:
            x_economy.add_clerkunit(clerk_person_id)

    def get_priority_agenda(self, person_id: PersonID):
        x_personunit = self.get_personunit_from_memory(person_id)
        x_agenda = agendaunit_shop(person_id)
        for x_painunit in x_personunit._pains.values():
            for x_healerlink in x_painunit._healerlinks.values():
                healer_personunit = self.get_personunit_from_memory(
                    x_healerlink.person_id
                )
                for x_economylink in x_healerlink._economylinks.values():
                    x_economyunit = healer_personunit.get_economyunit(
                        x_economylink.economy_id
                    )
                    public_agenda = x_economyunit.get_public_agenda(person_id)
                    public_agenda.set_economy_id(x_agenda._economy_id)
                    x_agenda.meld(public_agenda)
        return x_agenda

    def create_person_economy(
        self,
        person_id: PersonID,
        pain_genus: PainGenus,
        healer_id: PersonID,
        economy_id: EconomyID,
    ):
        x_healerlink = healerlink_shop(healer_id)
        x_healerlink.set_economylink(economylink_shop(economy_id))
        x_painunit = painunit_shop(pain_genus)
        x_painunit.set_healerlink(x_healerlink)

        self.set_personunit(person_id, replace_personunit=False, replace_alert=False)
        x_personunit = self.get_personunit_from_memory(person_id)
        x_personunit.set_painunit(x_painunit)

        self.set_personunit(healer_id, replace_personunit=False, replace_alert=False)
        x_healerunit = self.get_personunit_from_memory(healer_id)
        x_healerunit.set_economyunit(economy_id, replace=False)
        x_economyunit = x_healerunit.get_economyunit(economy_id)
        x_economyunit.full_setup_clerkunit(healer_id)
        if healer_id != x_personunit.pid:
            self._set_partyunit(x_economyunit, x_personunit.pid, healer_id)

    def _set_partyunit(
        self, x_economyunit: EconomyUnit, person_id: PersonID, party_pid: PersonID
    ):
        x_economyunit.full_setup_clerkunit(person_id)
        person_clerkunit = x_economyunit.get_clerkunit(person_id)
        person_contract = person_clerkunit.get_contract()
        person_contract.add_partyunit(party_pid)
        person_clerkunit.save_contract_agenda(person_contract)
        person_clerkunit.save_refreshed_output_to_public()


def worldunit_shop(
    mark: WorldMark, worlds_dir: str, _road_delimiter: str = None
) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir, _personunits={})
    world_x._set_world_dirs()
    world_x._road_delimiter = default_road_delimiter_if_none(_road_delimiter)
    return world_x
