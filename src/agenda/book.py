from src._road.road import (
    RoadUnit,
    get_terminus_node,
    get_parent_road,
)
from src.agenda.reason_idea import BeliefUnit, ReasonUnit
from src.agenda.party import (
    PartyLink,
    PartyID,
)
from src.agenda.group import (
    GroupUnit,
    GroupID,
)
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.agenda.atom import (
    CRUD_command,
    AgendaAtom,
    agendaatom_shop,
    change_agenda_with_agendaatom,
    InvalidAgendaAtomException,
    atom_delete,
    atom_insert,
    atom_update,
    optional_args_different,
)
from src.instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class BookUnit:
    agendaatoms: dict[CRUD_command : dict[str:AgendaAtom]] = None
    _agenda_build_validated: bool = None

    def get_crud_agendaatoms_list(self) -> dict[CRUD_command : list[AgendaAtom]]:
        return get_all_nondictionary_objs(self.agendaatoms)

    def get_agendaatoms_list(self) -> list[AgendaAtom]:
        atoms_list = []
        for crud_dict in self.get_crud_agendaatoms_list().values():
            atoms_list.extend(iter(crud_dict))
        return atoms_list

    def get_sorted_agendaatoms(self) -> list[AgendaAtom]:
        agendaatoms_list = self.get_agendaatoms_list()
        return sorted(agendaatoms_list, key=lambda x: int(x.atom_order))

    def get_edited_agenda(self, before_agenda: AgendaUnit):
        edit_agenda = copy_deepcopy(before_agenda)
        agendaatoms_by_order = self.get_crud_agendaatoms_list()

        for x_atom_order_int in sorted(agendaatoms_by_order.keys()):
            agendaatoms_list = agendaatoms_by_order.get(x_atom_order_int)
            for x_agendaatom in agendaatoms_list:
                change_agenda_with_agendaatom(edit_agenda, x_agendaatom)
        return edit_agenda

    def set_agendaatom(self, x_agendaatom: AgendaAtom):
        if x_agendaatom.is_valid() == False:
            raise InvalidAgendaAtomException(
                f"""'{x_agendaatom.category}' {x_agendaatom.crud_text} AgendaAtom is invalid
                {x_agendaatom.is_required_args_valid()=}
                {x_agendaatom.is_optional_args_valid()=}"""
            )

        x_agendaatom.set_atom_order()
        x_keylist = [
            x_agendaatom.crud_text,
            x_agendaatom.category,
            *list(x_agendaatom.required_args.values()),
        ]
        place_obj_in_dict(self.agendaatoms, x_keylist, x_agendaatom)

    def agendaatom_exists(self, x_agendaatom: AgendaAtom) -> bool:
        if x_agendaatom.is_valid() == False:
            raise InvalidAgendaAtomException(
                f"""'{x_agendaatom.category}' {x_agendaatom.crud_text} AgendaAtom is invalid
                {x_agendaatom.is_required_args_valid()=}
                {x_agendaatom.is_optional_args_valid()=}"""
            )

        x_agendaatom.set_atom_order()
        x_keylist = [
            x_agendaatom.crud_text,
            x_agendaatom.category,
            *list(x_agendaatom.required_args.values()),
        ]
        try:
            nested_agendaatom = get_nested_value(self.agendaatoms, x_keylist)
        except Exception:
            return False
        return nested_agendaatom == x_agendaatom

    def add_agendaatom(
        self,
        category: str,
        crud_text: str,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_agendaatom = agendaatom_shop(
            category=category,
            crud_text=crud_text,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_agendaatom(x_agendaatom)

    def get_agendaatom(
        self, crud_text: str, category: str, required_args: list[str]
    ) -> AgendaAtom:
        x_keylist = [crud_text, category, *required_args]
        return get_nested_value(self.agendaatoms, x_keylist)

    def add_all_agendaatoms(self, before_agenda: AgendaUnit, after_agenda: AgendaUnit):
        before_agenda.set_agenda_metrics()
        after_agenda.set_agenda_metrics()
        self.add_agendaatoms_agendaunit_simple_attrs(before_agenda, after_agenda)
        self.add_agendaatom_partyunits(before_agenda, after_agenda)
        self.add_agendaatom_groupunits(before_agenda, after_agenda)
        self.add_agendaatoms_ideas(before_agenda, after_agenda)

    def add_agendaatoms_agendaunit_simple_attrs(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        if optional_args_different("agendaunit", before_agenda, after_agenda):
            x_agendaatom = agendaatom_shop("agendaunit", atom_update())
            if (
                before_agenda._auto_output_job_to_forum
                != after_agenda._auto_output_job_to_forum
            ):
                x_agendaatom.set_optional_arg(
                    "_auto_output_job_to_forum", after_agenda._auto_output_job_to_forum
                )
            if before_agenda._max_tree_traverse != after_agenda._max_tree_traverse:
                x_agendaatom.set_optional_arg(
                    "_max_tree_traverse", after_agenda._max_tree_traverse
                )
            if before_agenda._meld_strategy != after_agenda._meld_strategy:
                x_agendaatom.set_optional_arg(
                    "_meld_strategy", after_agenda._meld_strategy
                )
            if before_agenda._money_desc != after_agenda._money_desc:
                x_agendaatom.set_optional_arg("_money_desc", after_agenda._money_desc)
            if before_agenda._party_creditor_pool != after_agenda._party_creditor_pool:
                x_agendaatom.set_optional_arg(
                    "_party_creditor_pool", after_agenda._party_creditor_pool
                )
            if before_agenda._party_debtor_pool != after_agenda._party_debtor_pool:
                x_agendaatom.set_optional_arg(
                    "_party_debtor_pool", after_agenda._party_debtor_pool
                )
            if before_agenda._weight != after_agenda._weight:
                x_agendaatom.set_optional_arg("_weight", after_agenda._weight)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_party_ids = set(before_agenda._partys.keys())
        after_party_ids = set(after_agenda._partys.keys())

        self.add_agendaatom_partyunit_inserts(
            after_agenda=after_agenda,
            insert_party_ids=after_party_ids.difference(before_party_ids),
        )
        self.add_agendaatom_partyunit_deletes(
            delete_party_ids=before_party_ids.difference(after_party_ids)
        )
        self.add_agendaatom_partyunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_party_ids=before_party_ids.intersection(after_party_ids),
        )

    def add_agendaatom_partyunit_inserts(
        self, after_agenda: AgendaUnit, insert_party_ids: set
    ):
        for insert_party_id in insert_party_ids:
            x_partyunit = after_agenda.get_party(insert_party_id)
            x_agendaatom = agendaatom_shop("agenda_partyunit", atom_insert())
            x_agendaatom.set_required_arg("party_id", x_partyunit.party_id)
            if x_partyunit.creditor_weight != None:
                x_agendaatom.set_optional_arg(
                    "creditor_weight", x_partyunit.creditor_weight
                )
            if x_partyunit.debtor_weight != None:
                x_agendaatom.set_optional_arg(
                    "debtor_weight", x_partyunit.debtor_weight
                )
            if x_partyunit.depotlink_type != None:
                x_agendaatom.set_optional_arg(
                    "depotlink_type", x_partyunit.depotlink_type
                )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_party_ids: set
    ):
        for party_id in update_party_ids:
            after_partyunit = after_agenda.get_party(party_id)
            before_partyunit = before_agenda.get_party(party_id)
            if optional_args_different(
                "agenda_partyunit", after_partyunit, before_partyunit
            ):
                x_agendaatom = agendaatom_shop("agenda_partyunit", atom_update())
                x_agendaatom.set_required_arg("party_id", after_partyunit.party_id)
                if before_partyunit.creditor_weight != after_partyunit.creditor_weight:
                    x_agendaatom.set_optional_arg(
                        "creditor_weight", after_partyunit.creditor_weight
                    )
                if before_partyunit.debtor_weight != after_partyunit.debtor_weight:
                    x_agendaatom.set_optional_arg(
                        "debtor_weight", after_partyunit.debtor_weight
                    )
                if before_partyunit.depotlink_type != after_partyunit.depotlink_type:
                    x_agendaatom.set_optional_arg(
                        "depotlink_type", after_partyunit.depotlink_type
                    )
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunit_deletes(self, delete_party_ids: set):
        for delete_party_id in delete_party_ids:
            x_agendaatom = agendaatom_shop("agenda_partyunit", atom_delete())
            x_agendaatom.set_required_arg("party_id", delete_party_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_groupunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_group_ids = {
            before_group_id
            for before_group_id in before_agenda._groups.keys()
            if before_agenda.get_groupunit(before_group_id)._party_mirror == False
        }
        after_group_ids = {
            after_group_id
            for after_group_id in after_agenda._groups.keys()
            if after_agenda.get_groupunit(after_group_id)._party_mirror == False
        }

        self.add_agendaatom_groupunit_inserts(
            after_agenda=after_agenda,
            insert_group_ids=after_group_ids.difference(before_group_ids),
        )

        self.add_agendaatom_groupunit_deletes(
            before_agenda=before_agenda,
            delete_group_ids=before_group_ids.difference(after_group_ids),
        )

        self.add_agendaatom_groupunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_group_ids=before_group_ids.intersection(after_group_ids),
        )

    def add_agendaatom_groupunit_inserts(
        self, after_agenda: AgendaUnit, insert_group_ids: set
    ):
        for insert_group_id in insert_group_ids:
            insert_groupunit = after_agenda.get_groupunit(insert_group_id)
            x_agendaatom = agendaatom_shop("agenda_groupunit", atom_insert())
            x_agendaatom.set_required_arg("group_id", insert_groupunit.group_id)
            if insert_groupunit._treasury_partylinks != None:
                x_agendaatom.set_optional_arg(
                    "_treasury_partylinks",
                    insert_groupunit._treasury_partylinks,
                )
            self.set_agendaatom(x_agendaatom)
            self.add_agendaatom_partylinks_inserts(
                after_groupunit=insert_groupunit,
                insert_partylink_party_ids=set(insert_groupunit._partys.keys()),
            )

    def add_agendaatom_groupunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_group_ids: set
    ):
        for group_id in update_group_ids:
            after_groupunit = after_agenda.get_groupunit(group_id)
            before_groupunit = before_agenda.get_groupunit(group_id)
            if optional_args_different(
                "agenda_groupunit", before_groupunit, after_groupunit
            ):
                x_agendaatom = agendaatom_shop("agenda_groupunit", atom_update())
                x_agendaatom.set_required_arg("group_id", after_groupunit.group_id)
                x_agendaatom.set_optional_arg(
                    "_treasury_partylinks",
                    after_groupunit._treasury_partylinks,
                )
                self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_groupunit_update_partylinks(
                after_groupunit=after_groupunit, before_groupunit=before_groupunit
            )

    def add_agendaatom_groupunit_update_partylinks(
        self, after_groupunit: GroupUnit, before_groupunit: GroupUnit
    ):
        after_party_ids = set(after_groupunit._partys.keys())
        before_party_ids = set(before_groupunit._partys.keys())

        self.add_agendaatom_partylinks_inserts(
            after_groupunit=after_groupunit,
            insert_partylink_party_ids=after_party_ids.difference(before_party_ids),
        )

        self.add_agendaatom_partylinks_delete(
            before_group_id=before_groupunit.group_id,
            before_party_ids=before_party_ids.difference(after_party_ids),
        )

        update_party_ids = before_party_ids.intersection(after_party_ids)
        for update_party_id in update_party_ids:
            before_partylink = before_groupunit.get_partylink(update_party_id)
            after_partylink = after_groupunit.get_partylink(update_party_id)
            if optional_args_different(
                "agenda_group_partylink", before_partylink, after_partylink
            ):
                self.add_agendaatom_partylink_update(
                    group_id=after_groupunit.group_id,
                    before_partylink=before_partylink,
                    after_partylink=after_partylink,
                )

    def add_agendaatom_groupunit_deletes(
        self, before_agenda: AgendaUnit, delete_group_ids: set
    ):
        for delete_group_id in delete_group_ids:
            x_agendaatom = agendaatom_shop("agenda_groupunit", atom_delete())
            x_agendaatom.set_required_arg("group_id", delete_group_id)
            self.set_agendaatom(x_agendaatom)

            delete_groupunit = before_agenda.get_groupunit(delete_group_id)
            self.add_agendaatom_partylinks_delete(
                delete_group_id, set(delete_groupunit._partys.keys())
            )

    def add_agendaatom_partylinks_inserts(
        self,
        after_groupunit: GroupUnit,
        insert_partylink_party_ids: list[PartyID],
    ):
        after_group_id = after_groupunit.group_id
        for insert_party_id in insert_partylink_party_ids:
            after_partylink = after_groupunit.get_partylink(insert_party_id)
            x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_insert())
            x_agendaatom.set_required_arg("group_id", after_group_id)
            x_agendaatom.set_required_arg("party_id", after_partylink.party_id)
            if after_partylink.creditor_weight != None:
                x_agendaatom.set_optional_arg(
                    "creditor_weight", after_partylink.creditor_weight
                )
            if after_partylink.debtor_weight != None:
                x_agendaatom.set_optional_arg(
                    "debtor_weight", after_partylink.debtor_weight
                )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partylink_update(
        self,
        group_id: GroupID,
        before_partylink: PartyLink,
        after_partylink: PartyLink,
    ):
        x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_update())
        x_agendaatom.set_required_arg("group_id", group_id)
        x_agendaatom.set_required_arg("party_id", after_partylink.party_id)
        if after_partylink.creditor_weight != before_partylink.creditor_weight:
            x_agendaatom.set_optional_arg(
                "creditor_weight", after_partylink.creditor_weight
            )
        if after_partylink.debtor_weight != before_partylink.debtor_weight:
            x_agendaatom.set_optional_arg(
                "debtor_weight", after_partylink.debtor_weight
            )
        self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partylinks_delete(
        self, before_group_id: GroupID, before_party_ids: PartyID
    ):
        for delete_party_id in before_party_ids:
            x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_delete())
            x_agendaatom.set_required_arg("group_id", before_group_id)
            x_agendaatom.set_required_arg("party_id", delete_party_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatoms_ideas(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_idea_roads = set(before_agenda._idea_dict.keys())
        after_idea_roads = set(after_agenda._idea_dict.keys())

        self.add_agendaatom_idea_inserts(
            after_agenda=after_agenda,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_agendaatom_idea_deletes(
            before_agenda=before_agenda,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_agendaatom_idea_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_agendaatom_idea_inserts(
        self, after_agenda: AgendaUnit, insert_idea_roads: set
    ):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_agenda.get_idea_obj(insert_idea_road)
            x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_insert())
            x_agendaatom.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_agendaatom.set_required_arg("label", insert_ideaunit._label)
            x_agendaatom.set_optional_arg("_addin", insert_ideaunit._addin)
            x_agendaatom.set_optional_arg("_begin", insert_ideaunit._begin)
            x_agendaatom.set_optional_arg("_close", insert_ideaunit._close)
            x_agendaatom.set_optional_arg("_denom", insert_ideaunit._denom)
            x_agendaatom.set_optional_arg(
                "_meld_strategy", insert_ideaunit._meld_strategy
            )
            x_agendaatom.set_optional_arg(
                "_numeric_road", insert_ideaunit._numeric_road
            )
            x_agendaatom.set_optional_arg("_numor", insert_ideaunit._numor)
            x_agendaatom.set_optional_arg(
                "_range_source_road", insert_ideaunit._range_source_road
            )
            x_agendaatom.set_optional_arg("_reest", insert_ideaunit._reest)
            x_agendaatom.set_optional_arg("_weight", insert_ideaunit._weight)
            x_agendaatom.set_optional_arg("promise", insert_ideaunit.promise)
            self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_idea_beliefunit_inserts(
                ideaunit=insert_ideaunit,
                insert_beliefunit_bases=set(insert_ideaunit._beliefunits.keys()),
            )
            self.add_agendaatom_idea_balancelink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_balancelink_group_ids=set(insert_ideaunit._balancelinks.keys()),
            )
            self.add_agendaatom_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_agendaatom_idea_suffgroup_insert(
                idea_road=insert_idea_road,
                insert_suffgroup_group_ids=insert_ideaunit._assignedunit._suffgroups.keys(),
            )

    def add_agendaatom_idea_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_agenda.get_idea_obj(idea_road)
            before_ideaunit = before_agenda.get_idea_obj(idea_road)
            if optional_args_different(
                "agenda_ideaunit", before_ideaunit, after_ideaunit
            ):
                x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_update())
                x_agendaatom.set_required_arg(
                    "parent_road", after_ideaunit._parent_road
                )
                x_agendaatom.set_required_arg("label", after_ideaunit._label)
                if before_ideaunit._addin != after_ideaunit._addin:
                    x_agendaatom.set_optional_arg("_addin", after_ideaunit._addin)
                if before_ideaunit._begin != after_ideaunit._begin:
                    x_agendaatom.set_optional_arg("_begin", after_ideaunit._begin)
                if before_ideaunit._close != after_ideaunit._close:
                    x_agendaatom.set_optional_arg("_close", after_ideaunit._close)
                if before_ideaunit._denom != after_ideaunit._denom:
                    x_agendaatom.set_optional_arg("_denom", after_ideaunit._denom)
                if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
                    x_agendaatom.set_optional_arg(
                        "_meld_strategy", after_ideaunit._meld_strategy
                    )
                if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
                    x_agendaatom.set_optional_arg(
                        "_numeric_road", after_ideaunit._numeric_road
                    )
                if before_ideaunit._numor != after_ideaunit._numor:
                    x_agendaatom.set_optional_arg("_numor", after_ideaunit._numor)
                if (
                    before_ideaunit._range_source_road
                    != after_ideaunit._range_source_road
                ):
                    x_agendaatom.set_optional_arg(
                        "_range_source_road", after_ideaunit._range_source_road
                    )
                if before_ideaunit._reest != after_ideaunit._reest:
                    x_agendaatom.set_optional_arg("_reest", after_ideaunit._reest)
                if before_ideaunit._weight != after_ideaunit._weight:
                    x_agendaatom.set_optional_arg("_weight", after_ideaunit._weight)
                if before_ideaunit.promise != after_ideaunit.promise:
                    x_agendaatom.set_optional_arg("promise", after_ideaunit.promise)
                self.set_agendaatom(x_agendaatom)

            # insert / update / delete beliefunits
            before_beliefunit_bases = set(before_ideaunit._beliefunits.keys())
            after_beliefunit_bases = set(after_ideaunit._beliefunits.keys())
            self.add_agendaatom_idea_beliefunit_inserts(
                ideaunit=after_ideaunit,
                insert_beliefunit_bases=after_beliefunit_bases.difference(
                    before_beliefunit_bases
                ),
            )
            self.add_agendaatom_idea_beliefunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_beliefunit_bases=before_beliefunit_bases.intersection(
                    after_beliefunit_bases
                ),
            )
            self.add_agendaatom_idea_beliefunit_deletes(
                idea_road=idea_road,
                delete_beliefunit_bases=before_beliefunit_bases.difference(
                    after_beliefunit_bases
                ),
            )

            # insert / update / delete balanceunits
            before_balancelinks_group_ids = set(before_ideaunit._balancelinks.keys())
            after_balancelinks_group_ids = set(after_ideaunit._balancelinks.keys())
            self.add_agendaatom_idea_balancelink_inserts(
                after_ideaunit=after_ideaunit,
                insert_balancelink_group_ids=after_balancelinks_group_ids.difference(
                    before_balancelinks_group_ids
                ),
            )
            self.add_agendaatom_idea_balancelink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_balancelink_group_ids=before_balancelinks_group_ids.intersection(
                    after_balancelinks_group_ids
                ),
            )
            self.add_agendaatom_idea_balancelink_deletes(
                idea_road=idea_road,
                delete_balancelink_group_ids=before_balancelinks_group_ids.difference(
                    after_balancelinks_group_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit._reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit._reasonunits.keys())
            self.add_agendaatom_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_agendaatom_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_agendaatom_idea_reasonunit_deletes(
                before_ideaunit=before_ideaunit,
                delete_reasonunit_bases=before_reasonunit_bases.difference(
                    after_reasonunit_bases
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete suffgroups
            before_suffgroups_group_ids = set(
                before_ideaunit._assignedunit._suffgroups.keys()
            )
            after_suffgroups_group_ids = set(
                after_ideaunit._assignedunit._suffgroups.keys()
            )
            self.add_agendaatom_idea_suffgroup_insert(
                idea_road=idea_road,
                insert_suffgroup_group_ids=after_suffgroups_group_ids.difference(
                    before_suffgroups_group_ids
                ),
            )
            self.add_agendaatom_idea_suffgroup_deletes(
                idea_road=idea_road,
                delete_suffgroup_group_ids=before_suffgroups_group_ids.difference(
                    after_suffgroups_group_ids
                ),
            )

    def add_agendaatom_idea_deletes(
        self, before_agenda: AgendaUnit, delete_idea_roads: set
    ):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_agenda._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_agenda._road_delimiter)
            x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_delete())
            x_agendaatom.set_required_arg("parent_road", x_parent_road)
            x_agendaatom.set_required_arg("label", x_label)
            self.set_agendaatom(x_agendaatom)

            delete_ideaunit = before_agenda.get_idea_obj(delete_idea_road)
            self.add_agendaatom_idea_beliefunit_deletes(
                idea_road=delete_idea_road,
                delete_beliefunit_bases=set(delete_ideaunit._beliefunits.keys()),
            )
            self.add_agendaatom_idea_balancelink_deletes(
                idea_road=delete_idea_road,
                delete_balancelink_group_ids=set(delete_ideaunit._balancelinks.keys()),
            )
            self.add_agendaatom_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_agendaatom_idea_suffgroup_deletes(
                idea_road=delete_idea_road,
                delete_suffgroup_group_ids=set(
                    delete_ideaunit._assignedunit._suffgroups.keys()
                ),
            )

    def add_agendaatom_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_insert())
            x_agendaatom.set_required_arg("road", after_ideaunit.get_road())
            x_agendaatom.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.suff_idea_active != None:
                x_agendaatom.set_optional_arg(
                    "suff_idea_active", after_reasonunit.suff_idea_active
                )
            self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_idea_reason_premiseunit_inserts(
                idea_road=after_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_agendaatom_idea_reasonunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_reasonunit_bases: set,
    ):
        for update_reasonunit_base in update_reasonunit_bases:
            before_reasonunit = before_ideaunit.get_reasonunit(update_reasonunit_base)
            after_reasonunit = after_ideaunit.get_reasonunit(update_reasonunit_base)
            if optional_args_different(
                "agenda_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_update())
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.suff_idea_active
                    != after_reasonunit.suff_idea_active
                ):
                    x_agendaatom.set_optional_arg(
                        "suff_idea_active", after_reasonunit.suff_idea_active
                    )
                self.set_agendaatom(x_agendaatom)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_agendaatom_idea_reason_premiseunit_inserts(
                idea_road=before_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_agendaatom_idea_reason_premiseunit_updates(
                idea_road=before_ideaunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_agendaatom_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_agendaatom_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_delete())
            x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
            x_agendaatom.set_required_arg("base", delete_reasonunit_base)
            self.set_agendaatom(x_agendaatom)

            before_reasonunit = before_ideaunit.get_reasonunit(delete_reasonunit_base)
            self.add_agendaatom_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_agendaatom_idea_reason_premiseunit_inserts(
        self,
        idea_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_agendaatom = agendaatom_shop(
                "agenda_idea_reason_premiseunit", atom_insert()
            )
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", after_reasonunit.base)
            x_agendaatom.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open != None:
                x_agendaatom.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh != None:
                x_agendaatom.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor != None:
                x_agendaatom.set_optional_arg("divisor", after_premiseunit.divisor)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_reason_premiseunit_updates(
        self,
        idea_road: RoadUnit,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_needs: set,
    ):
        for update_premise_need in update_premise_needs:
            before_premiseunit = before_reasonunit.get_premise(update_premise_need)
            after_premiseunit = after_reasonunit.get_premise(update_premise_need)
            if optional_args_different(
                "agenda_idea_reason_premiseunit", before_premiseunit, after_premiseunit
            ):
                x_agendaatom = agendaatom_shop(
                    "agenda_idea_reason_premiseunit", atom_update()
                )
                x_agendaatom.set_required_arg("road", idea_road)
                x_agendaatom.set_required_arg("base", before_reasonunit.base)
                x_agendaatom.set_required_arg("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_agendaatom.set_optional_arg("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_agendaatom.set_optional_arg("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_agendaatom.set_optional_arg("divisor", after_premiseunit.divisor)
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_reason_premiseunit_deletes(
        self,
        idea_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_agendaatom = agendaatom_shop(
                "agenda_idea_reason_premiseunit", atom_delete()
            )
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", reasonunit_base)
            x_agendaatom.set_required_arg("need", delete_premise_need)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_suffgroup_insert(
        self, idea_road: RoadUnit, insert_suffgroup_group_ids: set
    ):
        for insert_suffgroup_group_id in insert_suffgroup_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_suffgroup", atom_insert())
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", insert_suffgroup_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_suffgroup_deletes(
        self, idea_road: RoadUnit, delete_suffgroup_group_ids: set
    ):
        for delete_suffgroup_group_id in delete_suffgroup_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_suffgroup", atom_delete())
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", delete_suffgroup_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_inserts(
        self, after_ideaunit: IdeaUnit, insert_balancelink_group_ids: set
    ):
        for after_balancelink_group_id in insert_balancelink_group_ids:
            after_balancelink = after_ideaunit._balancelinks.get(
                after_balancelink_group_id
            )
            x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_insert())
            x_agendaatom.set_required_arg("road", after_ideaunit.get_road())
            x_agendaatom.set_required_arg("group_id", after_balancelink.group_id)
            x_agendaatom.set_optional_arg(
                "creditor_weight", after_balancelink.creditor_weight
            )
            x_agendaatom.set_optional_arg(
                "debtor_weight", after_balancelink.debtor_weight
            )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_balancelink_group_ids: set,
    ):
        for update_balancelink_group_id in update_balancelink_group_ids:
            before_balancelink = before_ideaunit._balancelinks.get(
                update_balancelink_group_id
            )
            after_balancelink = after_ideaunit._balancelinks.get(
                update_balancelink_group_id
            )
            if optional_args_different(
                "agenda_idea_balancelink", before_balancelink, after_balancelink
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_update())
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("group_id", after_balancelink.group_id)
                if (
                    before_balancelink.creditor_weight
                    != after_balancelink.creditor_weight
                ):
                    x_agendaatom.set_optional_arg(
                        "creditor_weight", after_balancelink.creditor_weight
                    )
                if before_balancelink.debtor_weight != after_balancelink.debtor_weight:
                    x_agendaatom.set_optional_arg(
                        "debtor_weight", after_balancelink.debtor_weight
                    )
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_deletes(
        self, idea_road: RoadUnit, delete_balancelink_group_ids: set
    ):
        for delete_balancelink_group_id in delete_balancelink_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_delete())
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", delete_balancelink_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_inserts(
        self, ideaunit: IdeaUnit, insert_beliefunit_bases: set
    ):
        for insert_beliefunit_base in insert_beliefunit_bases:
            insert_beliefunit = ideaunit._beliefunits.get(insert_beliefunit_base)
            x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_insert())
            x_agendaatom.set_required_arg("road", ideaunit.get_road())
            x_agendaatom.set_required_arg("base", insert_beliefunit.base)
            if insert_beliefunit.pick != None:
                x_agendaatom.set_optional_arg("pick", insert_beliefunit.pick)
            if insert_beliefunit.open != None:
                x_agendaatom.set_optional_arg("open", insert_beliefunit.open)
            if insert_beliefunit.nigh != None:
                x_agendaatom.set_optional_arg("nigh", insert_beliefunit.nigh)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_beliefunit_bases: set,
    ):
        for update_beliefunit_base in update_beliefunit_bases:
            before_beliefunit = before_ideaunit._beliefunits.get(update_beliefunit_base)
            after_beliefunit = after_ideaunit._beliefunits.get(update_beliefunit_base)
            if optional_args_different(
                "agenda_idea_beliefunit", before_beliefunit, after_beliefunit
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_update())
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("base", after_beliefunit.base)
                if before_beliefunit.pick != after_beliefunit.pick:
                    x_agendaatom.set_optional_arg("pick", after_beliefunit.pick)
                if before_beliefunit.open != after_beliefunit.open:
                    x_agendaatom.set_optional_arg("open", after_beliefunit.open)
                if before_beliefunit.nigh != after_beliefunit.nigh:
                    x_agendaatom.set_optional_arg("nigh", after_beliefunit.nigh)
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_deletes(
        self, idea_road: RoadUnit, delete_beliefunit_bases: BeliefUnit
    ):
        for delete_beliefunit_base in delete_beliefunit_bases:
            x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_delete())
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", delete_beliefunit_base)
            self.set_agendaatom(x_agendaatom)

    def get_ordered_agendaatoms(self, x_count: int = None) -> dict[int:AgendaAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_agendaatoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int:str]:
        return {
            atom_num: atom_obj.get_dict()
            for atom_num, atom_obj in self.get_ordered_agendaatoms(x_count).items()
        }

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def bookunit_shop(agendaatoms: dict[str:str] = None):
    return BookUnit(
        agendaatoms=get_empty_dict_if_none(agendaatoms),
        _agenda_build_validated=False,
    )


def validate_agenda_build_from_book(x_book: BookUnit, x_agenda: AgendaUnit = None):
    if x_agenda is None:
        x_agenda = agendaunit_shop()

    x_agenda = x_book.get_edited_agenda(x_agenda)

    try:
        x_agenda.set_agenda_metrics()
    except Exception:
        return False

    return True


def create_legible_list(x_book: BookUnit, x_agenda: AgendaUnit) -> list[str]:
    x_list = []
    insert_dict = x_book.agendaatoms.get(atom_insert())
    update_dict = x_book.agendaatoms.get(atom_update())
    delete_dict = x_book.agendaatoms.get(atom_delete())

    # if insert_dict != None:
    #     pass
    if update_dict != None:
        print(f"{update_dict.keys()=}")
        agendaunit_text = "agendaunit"
        if update_dict.get(agendaunit_text) != None:
            x_atom = update_dict.get(agendaunit_text)
            add_agendaunit_legible_list(x_list, x_atom, x_agenda)
    # if delete_dict != None:
    #     pass

    return x_list


def add_agendaunit_legible_list(
    legible_list: list[str], x_atom: AgendaAtom, x_agenda: AgendaUnit
):
    optional_args = x_atom.optional_args
    x_atom._crud_cache = None
    _weight_text = "_weight"
    _max_tree_traverse_text = "_max_tree_traverse"
    _meld_strategy_text = "_meld_strategy"
    _money_desc_text = "_money_desc"
    _party_creditor_pool_text = "_party_creditor_pool"
    _party_debtor_pool_text = "_party_debtor_pool"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _meld_strategy_value = optional_args.get(_meld_strategy_text)
    _money_desc_value = optional_args.get(_money_desc_text)
    _party_creditor_pool_value = optional_args.get(_party_creditor_pool_text)
    _party_debtor_pool_value = optional_args.get(_party_debtor_pool_text)
    _weight_value = optional_args.get(_weight_text)

    x_money_desc = x_agenda._money_desc
    if x_money_desc is None:
        x_money_desc = f"{x_agenda._worker_id}'s money"

    if _max_tree_traverse_value != None:
        legible_list.append(
            f"{x_agenda._worker_id}'s maximum number of Agenda output evaluations changed to {_max_tree_traverse_value}"
        )
    if _meld_strategy_value != None:
        legible_list.append(
            f"{x_agenda._worker_id}'s Meld strategy changed to '{_meld_strategy_value}'"
        )
    if _money_desc_value != None:
        legible_list.append(
            f"{x_agenda._worker_id}'s money is now called '{_money_desc_value}'"
        )
    if (
        _party_creditor_pool_value != None
        and _party_debtor_pool_value != None
        and _party_creditor_pool_value == _party_debtor_pool_value
    ):
        legible_list.append(
            f"{x_money_desc} total pool is now {_party_creditor_pool_value}"
        )
    elif _party_creditor_pool_value != None:
        legible_list.append(
            f"{x_money_desc} creditor pool is now {_party_creditor_pool_value}"
        )
    elif _party_debtor_pool_value != None:
        legible_list.append(
            f"{x_money_desc} debtor pool is now {_party_debtor_pool_value}"
        )
    if _weight_value != None:
        legible_list.append(
            f"{x_agenda._worker_id}'s agenda weight was changed to {_weight_value}"
        )
