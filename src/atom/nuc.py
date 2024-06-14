from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src.agenda.reason_idea import BeliefUnit, ReasonUnit
from src.agenda.party import PartyLink, PartyID
from src.agenda.group import GroupUnit, GroupID
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.atom.quark import (
    CRUD_command,
    QuarkUnit,
    quarkunit_shop,
    modify_agenda_with_quarkunit,
    InvalidQuarkUnitException,
    quark_delete,
    quark_insert,
    quark_update,
    optional_args_different,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class NucUnit:
    quarkunits: dict[CRUD_command : dict[str:QuarkUnit]] = None
    _agenda_build_validated: bool = None

    def _get_crud_quarkunits_list(self) -> dict[CRUD_command : list[QuarkUnit]]:
        return get_all_nondictionary_objs(self.quarkunits)

    def get_category_sorted_quarkunits_list(self) -> list[QuarkUnit]:
        quarks_list = []
        for crud_list in self._get_crud_quarkunits_list().values():
            quarks_list.extend(iter(crud_list))

        quark_order_key_dict = {}
        for x_quark in quarks_list:
            quark_order_list = quark_order_key_dict.get(x_quark.quark_order)
            if quark_order_list is None:
                quark_order_key_dict[x_quark.quark_order] = [x_quark]
            else:
                quark_order_list.append(x_quark)

        ordered_list = []
        for x_list in quark_order_key_dict.values():
            if x_list[0].required_args.get("parent_road") != None:
                x_list = sorted(
                    x_list, key=lambda x: x.required_args.get("parent_road")
                )
            if x_list[0].required_args.get("road") != None:
                x_list = sorted(x_list, key=lambda x: x.required_args.get("road"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_quarkunits(self) -> list[QuarkUnit]:
        quarkunits_list = self.get_category_sorted_quarkunits_list()
        return sorted(quarkunits_list, key=lambda x: x.quark_order)

    def get_edited_agenda(self, before_agenda: AgendaUnit):
        edited_agenda = copy_deepcopy(before_agenda)
        for x_quarkunit in self.get_sorted_quarkunits():
            modify_agenda_with_quarkunit(edited_agenda, x_quarkunit)
        return edited_agenda

    def set_quarkunit(self, x_quarkunit: QuarkUnit):
        if x_quarkunit.is_valid() is False:
            raise InvalidQuarkUnitException(
                f"""'{x_quarkunit.category}' {x_quarkunit.crud_text} QuarkUnit is invalid
                {x_quarkunit.is_required_args_valid()=}
                {x_quarkunit.is_optional_args_valid()=}"""
            )

        x_quarkunit.set_quark_order()
        x_keylist = [
            x_quarkunit.crud_text,
            x_quarkunit.category,
            *list(x_quarkunit.required_args.values()),
        ]
        place_obj_in_dict(self.quarkunits, x_keylist, x_quarkunit)

    def quarkunit_exists(self, x_quarkunit: QuarkUnit) -> bool:
        if x_quarkunit.is_valid() is False:
            raise InvalidQuarkUnitException(
                f"""'{x_quarkunit.category}' {x_quarkunit.crud_text} QuarkUnit is invalid
                {x_quarkunit.is_required_args_valid()=}
                {x_quarkunit.is_optional_args_valid()=}"""
            )

        x_quarkunit.set_quark_order()
        x_keylist = [
            x_quarkunit.crud_text,
            x_quarkunit.category,
            *list(x_quarkunit.required_args.values()),
        ]
        try:
            nested_quarkunit = get_nested_value(self.quarkunits, x_keylist)
        except Exception:
            return False
        return nested_quarkunit == x_quarkunit

    def add_quarkunit(
        self,
        category: str,
        crud_text: str,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_quarkunit = quarkunit_shop(
            category=category,
            crud_text=crud_text,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_quarkunit(x_quarkunit)

    def get_quarkunit(
        self, crud_text: str, category: str, required_args: list[str]
    ) -> QuarkUnit:
        x_keylist = [crud_text, category, *required_args]
        return get_nested_value(self.quarkunits, x_keylist)

    def add_all_different_quarkunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_agenda.calc_agenda_metrics()
        after_agenda.calc_agenda_metrics()
        self.add_quarkunits_agendaunit_simple_attrs(before_agenda, after_agenda)
        self.add_quarkunit_partyunits(before_agenda, after_agenda)
        self.add_quarkunit_groupunits(before_agenda, after_agenda)
        self.add_quarkunits_ideas(before_agenda, after_agenda)

    def add_quarkunits_agendaunit_simple_attrs(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        if not optional_args_different("agendaunit", before_agenda, after_agenda):
            return
        x_quarkunit = quarkunit_shop("agendaunit", quark_update())
        if before_agenda._max_tree_traverse != after_agenda._max_tree_traverse:
            x_quarkunit.set_optional_arg(
                "_max_tree_traverse", after_agenda._max_tree_traverse
            )
        if before_agenda._meld_strategy != after_agenda._meld_strategy:
            x_quarkunit.set_optional_arg("_meld_strategy", after_agenda._meld_strategy)
        if before_agenda._monetary_desc != after_agenda._monetary_desc:
            x_quarkunit.set_optional_arg("_monetary_desc", after_agenda._monetary_desc)
        if before_agenda._party_credor_pool != after_agenda._party_credor_pool:
            x_quarkunit.set_optional_arg(
                "_party_credor_pool", after_agenda._party_credor_pool
            )
        if before_agenda._party_debtor_pool != after_agenda._party_debtor_pool:
            x_quarkunit.set_optional_arg(
                "_party_debtor_pool", after_agenda._party_debtor_pool
            )
        if before_agenda._weight != after_agenda._weight:
            x_quarkunit.set_optional_arg("_weight", after_agenda._weight)
        if before_agenda._planck != after_agenda._planck:
            x_quarkunit.set_optional_arg("_planck", after_agenda._planck)
        self.set_quarkunit(x_quarkunit)

    def add_quarkunit_partyunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_party_ids = set(before_agenda._partys.keys())
        after_party_ids = set(after_agenda._partys.keys())

        self.add_quarkunit_partyunit_inserts(
            after_agenda=after_agenda,
            insert_party_ids=after_party_ids.difference(before_party_ids),
        )
        self.add_quarkunit_partyunit_deletes(
            delete_party_ids=before_party_ids.difference(after_party_ids)
        )
        self.add_quarkunit_partyunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_party_ids=before_party_ids.intersection(after_party_ids),
        )

    def add_quarkunit_partyunit_inserts(
        self, after_agenda: AgendaUnit, insert_party_ids: set
    ):
        for insert_party_id in insert_party_ids:
            x_partyunit = after_agenda.get_party(insert_party_id)
            x_quarkunit = quarkunit_shop("agenda_partyunit", quark_insert())
            x_quarkunit.set_required_arg("party_id", x_partyunit.party_id)
            if x_partyunit.credor_weight != None:
                x_quarkunit.set_optional_arg("credor_weight", x_partyunit.credor_weight)
            if x_partyunit.debtor_weight != None:
                x_quarkunit.set_optional_arg("debtor_weight", x_partyunit.debtor_weight)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_partyunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_party_ids: set
    ):
        for party_id in update_party_ids:
            after_partyunit = after_agenda.get_party(party_id)
            before_partyunit = before_agenda.get_party(party_id)
            if optional_args_different(
                "agenda_partyunit", after_partyunit, before_partyunit
            ):
                x_quarkunit = quarkunit_shop("agenda_partyunit", quark_update())
                x_quarkunit.set_required_arg("party_id", after_partyunit.party_id)
                if before_partyunit.credor_weight != after_partyunit.credor_weight:
                    x_quarkunit.set_optional_arg(
                        "credor_weight", after_partyunit.credor_weight
                    )
                if before_partyunit.debtor_weight != after_partyunit.debtor_weight:
                    x_quarkunit.set_optional_arg(
                        "debtor_weight", after_partyunit.debtor_weight
                    )
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_partyunit_deletes(self, delete_party_ids: set):
        for delete_party_id in delete_party_ids:
            x_quarkunit = quarkunit_shop("agenda_partyunit", quark_delete())
            x_quarkunit.set_required_arg("party_id", delete_party_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_groupunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_group_ids = {
            before_group_id
            for before_group_id in before_agenda._groups.keys()
            if before_agenda.get_groupunit(before_group_id)._party_mirror is False
        }
        after_group_ids = {
            after_group_id
            for after_group_id in after_agenda._groups.keys()
            if after_agenda.get_groupunit(after_group_id)._party_mirror is False
        }

        self.add_quarkunit_groupunit_inserts(
            after_agenda=after_agenda,
            insert_group_ids=after_group_ids.difference(before_group_ids),
        )

        self.add_quarkunit_groupunit_deletes(
            before_agenda=before_agenda,
            delete_group_ids=before_group_ids.difference(after_group_ids),
        )

        self.add_quarkunit_groupunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_group_ids=before_group_ids.intersection(after_group_ids),
        )

    def add_quarkunit_groupunit_inserts(
        self, after_agenda: AgendaUnit, insert_group_ids: set
    ):
        for insert_group_id in insert_group_ids:
            insert_groupunit = after_agenda.get_groupunit(insert_group_id)
            x_quarkunit = quarkunit_shop("agenda_groupunit", quark_insert())
            x_quarkunit.set_required_arg("group_id", insert_groupunit.group_id)
            self.set_quarkunit(x_quarkunit)
            self.add_quarkunit_partylinks_inserts(
                after_groupunit=insert_groupunit,
                insert_partylink_party_ids=set(insert_groupunit._partys.keys()),
            )

    def add_quarkunit_groupunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_group_ids: set
    ):
        for group_id in update_group_ids:
            after_groupunit = after_agenda.get_groupunit(group_id)
            before_groupunit = before_agenda.get_groupunit(group_id)
            if optional_args_different(
                "agenda_groupunit", before_groupunit, after_groupunit
            ):
                x_quarkunit = quarkunit_shop("agenda_groupunit", quark_update())
                x_quarkunit.set_required_arg("group_id", after_groupunit.group_id)
                self.set_quarkunit(x_quarkunit)

            self.add_quarkunit_groupunit_update_partylinks(
                after_groupunit=after_groupunit, before_groupunit=before_groupunit
            )

    def add_quarkunit_groupunit_update_partylinks(
        self, after_groupunit: GroupUnit, before_groupunit: GroupUnit
    ):
        after_party_ids = set(after_groupunit._partys.keys())
        before_party_ids = set(before_groupunit._partys.keys())

        self.add_quarkunit_partylinks_inserts(
            after_groupunit=after_groupunit,
            insert_partylink_party_ids=after_party_ids.difference(before_party_ids),
        )

        self.add_quarkunit_partylinks_delete(
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
                self.add_quarkunit_partylink_update(
                    group_id=after_groupunit.group_id,
                    before_partylink=before_partylink,
                    after_partylink=after_partylink,
                )

    def add_quarkunit_groupunit_deletes(
        self, before_agenda: AgendaUnit, delete_group_ids: set
    ):
        for delete_group_id in delete_group_ids:
            x_quarkunit = quarkunit_shop("agenda_groupunit", quark_delete())
            x_quarkunit.set_required_arg("group_id", delete_group_id)
            self.set_quarkunit(x_quarkunit)

            delete_groupunit = before_agenda.get_groupunit(delete_group_id)
            self.add_quarkunit_partylinks_delete(
                delete_group_id, set(delete_groupunit._partys.keys())
            )

    def add_quarkunit_partylinks_inserts(
        self,
        after_groupunit: GroupUnit,
        insert_partylink_party_ids: list[PartyID],
    ):
        after_group_id = after_groupunit.group_id
        for insert_party_id in insert_partylink_party_ids:
            after_partylink = after_groupunit.get_partylink(insert_party_id)
            x_quarkunit = quarkunit_shop("agenda_group_partylink", quark_insert())
            x_quarkunit.set_required_arg("group_id", after_group_id)
            x_quarkunit.set_required_arg("party_id", after_partylink.party_id)
            if after_partylink.credor_weight != None:
                x_quarkunit.set_optional_arg(
                    "credor_weight", after_partylink.credor_weight
                )
            if after_partylink.debtor_weight != None:
                x_quarkunit.set_optional_arg(
                    "debtor_weight", after_partylink.debtor_weight
                )
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_partylink_update(
        self,
        group_id: GroupID,
        before_partylink: PartyLink,
        after_partylink: PartyLink,
    ):
        x_quarkunit = quarkunit_shop("agenda_group_partylink", quark_update())
        x_quarkunit.set_required_arg("group_id", group_id)
        x_quarkunit.set_required_arg("party_id", after_partylink.party_id)
        if after_partylink.credor_weight != before_partylink.credor_weight:
            x_quarkunit.set_optional_arg("credor_weight", after_partylink.credor_weight)
        if after_partylink.debtor_weight != before_partylink.debtor_weight:
            x_quarkunit.set_optional_arg("debtor_weight", after_partylink.debtor_weight)
        self.set_quarkunit(x_quarkunit)

    def add_quarkunit_partylinks_delete(
        self, before_group_id: GroupID, before_party_ids: PartyID
    ):
        for delete_party_id in before_party_ids:
            x_quarkunit = quarkunit_shop("agenda_group_partylink", quark_delete())
            x_quarkunit.set_required_arg("group_id", before_group_id)
            x_quarkunit.set_required_arg("party_id", delete_party_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunits_ideas(self, before_agenda: AgendaUnit, after_agenda: AgendaUnit):
        before_idea_roads = set(before_agenda._idea_dict.keys())
        after_idea_roads = set(after_agenda._idea_dict.keys())

        self.add_quarkunit_idea_inserts(
            after_agenda=after_agenda,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_quarkunit_idea_deletes(
            before_agenda=before_agenda,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_quarkunit_idea_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_quarkunit_idea_inserts(
        self, after_agenda: AgendaUnit, insert_idea_roads: set
    ):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_agenda.get_idea_obj(insert_idea_road)
            x_quarkunit = quarkunit_shop("agenda_ideaunit", quark_insert())
            x_quarkunit.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_quarkunit.set_required_arg("label", insert_ideaunit._label)
            x_quarkunit.set_optional_arg("_addin", insert_ideaunit._addin)
            x_quarkunit.set_optional_arg("_begin", insert_ideaunit._begin)
            x_quarkunit.set_optional_arg("_close", insert_ideaunit._close)
            x_quarkunit.set_optional_arg("_denom", insert_ideaunit._denom)
            x_quarkunit.set_optional_arg(
                "_meld_strategy", insert_ideaunit._meld_strategy
            )
            x_quarkunit.set_optional_arg("_numeric_road", insert_ideaunit._numeric_road)
            x_quarkunit.set_optional_arg("_numor", insert_ideaunit._numor)
            x_quarkunit.set_optional_arg(
                "_range_source_road", insert_ideaunit._range_source_road
            )
            x_quarkunit.set_optional_arg("_reest", insert_ideaunit._reest)
            x_quarkunit.set_optional_arg("_weight", insert_ideaunit._weight)
            x_quarkunit.set_optional_arg("pledge", insert_ideaunit.pledge)
            self.set_quarkunit(x_quarkunit)

            self.add_quarkunit_idea_beliefunit_inserts(
                ideaunit=insert_ideaunit,
                insert_beliefunit_bases=set(insert_ideaunit._beliefunits.keys()),
            )
            self.add_quarkunit_idea_balancelink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_balancelink_group_ids=set(insert_ideaunit._balancelinks.keys()),
            )
            self.add_quarkunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_quarkunit_idea_suffgroup_insert(
                idea_road=insert_idea_road,
                insert_suffgroup_group_ids=insert_ideaunit._assignedunit._suffgroups.keys(),
            )

    def add_quarkunit_idea_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_agenda.get_idea_obj(idea_road)
            before_ideaunit = before_agenda.get_idea_obj(idea_road)
            if optional_args_different(
                "agenda_ideaunit", before_ideaunit, after_ideaunit
            ):
                x_quarkunit = quarkunit_shop("agenda_ideaunit", quark_update())
                x_quarkunit.set_required_arg("parent_road", after_ideaunit._parent_road)
                x_quarkunit.set_required_arg("label", after_ideaunit._label)
                if before_ideaunit._addin != after_ideaunit._addin:
                    x_quarkunit.set_optional_arg("_addin", after_ideaunit._addin)
                if before_ideaunit._begin != after_ideaunit._begin:
                    x_quarkunit.set_optional_arg("_begin", after_ideaunit._begin)
                if before_ideaunit._close != after_ideaunit._close:
                    x_quarkunit.set_optional_arg("_close", after_ideaunit._close)
                if before_ideaunit._denom != after_ideaunit._denom:
                    x_quarkunit.set_optional_arg("_denom", after_ideaunit._denom)
                if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
                    x_quarkunit.set_optional_arg(
                        "_meld_strategy", after_ideaunit._meld_strategy
                    )
                if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
                    x_quarkunit.set_optional_arg(
                        "_numeric_road", after_ideaunit._numeric_road
                    )
                if before_ideaunit._numor != after_ideaunit._numor:
                    x_quarkunit.set_optional_arg("_numor", after_ideaunit._numor)
                if (
                    before_ideaunit._range_source_road
                    != after_ideaunit._range_source_road
                ):
                    x_quarkunit.set_optional_arg(
                        "_range_source_road", after_ideaunit._range_source_road
                    )
                if before_ideaunit._reest != after_ideaunit._reest:
                    x_quarkunit.set_optional_arg("_reest", after_ideaunit._reest)
                if before_ideaunit._weight != after_ideaunit._weight:
                    x_quarkunit.set_optional_arg("_weight", after_ideaunit._weight)
                if before_ideaunit.pledge != after_ideaunit.pledge:
                    x_quarkunit.set_optional_arg("pledge", after_ideaunit.pledge)
                self.set_quarkunit(x_quarkunit)

            # insert / update / delete beliefunits
            before_beliefunit_bases = set(before_ideaunit._beliefunits.keys())
            after_beliefunit_bases = set(after_ideaunit._beliefunits.keys())
            self.add_quarkunit_idea_beliefunit_inserts(
                ideaunit=after_ideaunit,
                insert_beliefunit_bases=after_beliefunit_bases.difference(
                    before_beliefunit_bases
                ),
            )
            self.add_quarkunit_idea_beliefunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_beliefunit_bases=before_beliefunit_bases.intersection(
                    after_beliefunit_bases
                ),
            )
            self.add_quarkunit_idea_beliefunit_deletes(
                idea_road=idea_road,
                delete_beliefunit_bases=before_beliefunit_bases.difference(
                    after_beliefunit_bases
                ),
            )

            # insert / update / delete balanceunits
            before_balancelinks_group_ids = set(before_ideaunit._balancelinks.keys())
            after_balancelinks_group_ids = set(after_ideaunit._balancelinks.keys())
            self.add_quarkunit_idea_balancelink_inserts(
                after_ideaunit=after_ideaunit,
                insert_balancelink_group_ids=after_balancelinks_group_ids.difference(
                    before_balancelinks_group_ids
                ),
            )
            self.add_quarkunit_idea_balancelink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_balancelink_group_ids=before_balancelinks_group_ids.intersection(
                    after_balancelinks_group_ids
                ),
            )
            self.add_quarkunit_idea_balancelink_deletes(
                idea_road=idea_road,
                delete_balancelink_group_ids=before_balancelinks_group_ids.difference(
                    after_balancelinks_group_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit._reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit._reasonunits.keys())
            self.add_quarkunit_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_quarkunit_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_quarkunit_idea_reasonunit_deletes(
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
            self.add_quarkunit_idea_suffgroup_insert(
                idea_road=idea_road,
                insert_suffgroup_group_ids=after_suffgroups_group_ids.difference(
                    before_suffgroups_group_ids
                ),
            )
            self.add_quarkunit_idea_suffgroup_deletes(
                idea_road=idea_road,
                delete_suffgroup_group_ids=before_suffgroups_group_ids.difference(
                    after_suffgroups_group_ids
                ),
            )

    def add_quarkunit_idea_deletes(
        self, before_agenda: AgendaUnit, delete_idea_roads: set
    ):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_agenda._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_agenda._road_delimiter)
            x_quarkunit = quarkunit_shop("agenda_ideaunit", quark_delete())
            x_quarkunit.set_required_arg("parent_road", x_parent_road)
            x_quarkunit.set_required_arg("label", x_label)
            self.set_quarkunit(x_quarkunit)

            delete_ideaunit = before_agenda.get_idea_obj(delete_idea_road)
            self.add_quarkunit_idea_beliefunit_deletes(
                idea_road=delete_idea_road,
                delete_beliefunit_bases=set(delete_ideaunit._beliefunits.keys()),
            )
            self.add_quarkunit_idea_balancelink_deletes(
                idea_road=delete_idea_road,
                delete_balancelink_group_ids=set(delete_ideaunit._balancelinks.keys()),
            )
            self.add_quarkunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_quarkunit_idea_suffgroup_deletes(
                idea_road=delete_idea_road,
                delete_suffgroup_group_ids=set(
                    delete_ideaunit._assignedunit._suffgroups.keys()
                ),
            )

    def add_quarkunit_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_quarkunit = quarkunit_shop("agenda_idea_reasonunit", quark_insert())
            x_quarkunit.set_required_arg("road", after_ideaunit.get_road())
            x_quarkunit.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.suff_idea_active != None:
                x_quarkunit.set_optional_arg(
                    "suff_idea_active", after_reasonunit.suff_idea_active
                )
            self.set_quarkunit(x_quarkunit)

            self.add_quarkunit_idea_reason_premiseunit_inserts(
                idea_road=after_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_quarkunit_idea_reasonunit_updates(
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
                x_quarkunit = quarkunit_shop("agenda_idea_reasonunit", quark_update())
                x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
                x_quarkunit.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.suff_idea_active
                    != after_reasonunit.suff_idea_active
                ):
                    x_quarkunit.set_optional_arg(
                        "suff_idea_active", after_reasonunit.suff_idea_active
                    )
                self.set_quarkunit(x_quarkunit)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_quarkunit_idea_reason_premiseunit_inserts(
                idea_road=before_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_quarkunit_idea_reason_premiseunit_updates(
                idea_road=before_ideaunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_quarkunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_quarkunit_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_quarkunit = quarkunit_shop("agenda_idea_reasonunit", quark_delete())
            x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
            x_quarkunit.set_required_arg("base", delete_reasonunit_base)
            self.set_quarkunit(x_quarkunit)

            before_reasonunit = before_ideaunit.get_reasonunit(delete_reasonunit_base)
            self.add_quarkunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_quarkunit_idea_reason_premiseunit_inserts(
        self,
        idea_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_quarkunit = quarkunit_shop(
                "agenda_idea_reason_premiseunit", quark_insert()
            )
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("base", after_reasonunit.base)
            x_quarkunit.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open != None:
                x_quarkunit.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh != None:
                x_quarkunit.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor != None:
                x_quarkunit.set_optional_arg("divisor", after_premiseunit.divisor)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_reason_premiseunit_updates(
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
                x_quarkunit = quarkunit_shop(
                    "agenda_idea_reason_premiseunit", quark_update()
                )
                x_quarkunit.set_required_arg("road", idea_road)
                x_quarkunit.set_required_arg("base", before_reasonunit.base)
                x_quarkunit.set_required_arg("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_quarkunit.set_optional_arg("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_quarkunit.set_optional_arg("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_quarkunit.set_optional_arg("divisor", after_premiseunit.divisor)
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_reason_premiseunit_deletes(
        self,
        idea_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_quarkunit = quarkunit_shop(
                "agenda_idea_reason_premiseunit", quark_delete()
            )
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("base", reasonunit_base)
            x_quarkunit.set_required_arg("need", delete_premise_need)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_suffgroup_insert(
        self, idea_road: RoadUnit, insert_suffgroup_group_ids: set
    ):
        for insert_suffgroup_group_id in insert_suffgroup_group_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_suffgroup", quark_insert())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("group_id", insert_suffgroup_group_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_suffgroup_deletes(
        self, idea_road: RoadUnit, delete_suffgroup_group_ids: set
    ):
        for delete_suffgroup_group_id in delete_suffgroup_group_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_suffgroup", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("group_id", delete_suffgroup_group_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_balancelink_inserts(
        self, after_ideaunit: IdeaUnit, insert_balancelink_group_ids: set
    ):
        for after_balancelink_group_id in insert_balancelink_group_ids:
            after_balancelink = after_ideaunit._balancelinks.get(
                after_balancelink_group_id
            )
            x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_insert())
            x_quarkunit.set_required_arg("road", after_ideaunit.get_road())
            x_quarkunit.set_required_arg("group_id", after_balancelink.group_id)
            x_quarkunit.set_optional_arg(
                "credor_weight", after_balancelink.credor_weight
            )
            x_quarkunit.set_optional_arg(
                "debtor_weight", after_balancelink.debtor_weight
            )
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_balancelink_updates(
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
                x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_update())
                x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
                x_quarkunit.set_required_arg("group_id", after_balancelink.group_id)
                if before_balancelink.credor_weight != after_balancelink.credor_weight:
                    x_quarkunit.set_optional_arg(
                        "credor_weight", after_balancelink.credor_weight
                    )
                if before_balancelink.debtor_weight != after_balancelink.debtor_weight:
                    x_quarkunit.set_optional_arg(
                        "debtor_weight", after_balancelink.debtor_weight
                    )
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_balancelink_deletes(
        self, idea_road: RoadUnit, delete_balancelink_group_ids: set
    ):
        for delete_balancelink_group_id in delete_balancelink_group_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("group_id", delete_balancelink_group_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_beliefunit_inserts(
        self, ideaunit: IdeaUnit, insert_beliefunit_bases: set
    ):
        for insert_beliefunit_base in insert_beliefunit_bases:
            insert_beliefunit = ideaunit._beliefunits.get(insert_beliefunit_base)
            x_quarkunit = quarkunit_shop("agenda_idea_beliefunit", quark_insert())
            x_quarkunit.set_required_arg("road", ideaunit.get_road())
            x_quarkunit.set_required_arg("base", insert_beliefunit.base)
            if insert_beliefunit.pick != None:
                x_quarkunit.set_optional_arg("pick", insert_beliefunit.pick)
            if insert_beliefunit.open != None:
                x_quarkunit.set_optional_arg("open", insert_beliefunit.open)
            if insert_beliefunit.nigh != None:
                x_quarkunit.set_optional_arg("nigh", insert_beliefunit.nigh)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_beliefunit_updates(
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
                x_quarkunit = quarkunit_shop("agenda_idea_beliefunit", quark_update())
                x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
                x_quarkunit.set_required_arg("base", after_beliefunit.base)
                if before_beliefunit.pick != after_beliefunit.pick:
                    x_quarkunit.set_optional_arg("pick", after_beliefunit.pick)
                if before_beliefunit.open != after_beliefunit.open:
                    x_quarkunit.set_optional_arg("open", after_beliefunit.open)
                if before_beliefunit.nigh != after_beliefunit.nigh:
                    x_quarkunit.set_optional_arg("nigh", after_beliefunit.nigh)
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_beliefunit_deletes(
        self, idea_road: RoadUnit, delete_beliefunit_bases: BeliefUnit
    ):
        for delete_beliefunit_base in delete_beliefunit_bases:
            x_quarkunit = quarkunit_shop("agenda_idea_beliefunit", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("base", delete_beliefunit_base)
            self.set_quarkunit(x_quarkunit)

    def get_ordered_quarkunits(self, x_count: int = None) -> dict[int:QuarkUnit]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_quark in self.get_sorted_quarkunits():
            x_dict[x_count] = x_quark
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int:str]:
        return {
            quark_num: quark_obj.get_dict()
            for quark_num, quark_obj in self.get_ordered_quarkunits(x_count).items()
        }

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def nucunit_shop(quarkunits: dict[str:str] = None):
    return NucUnit(
        quarkunits=get_empty_dict_if_none(quarkunits),
        _agenda_build_validated=False,
    )


def validate_agenda_build_from_nuc(x_nuc: NucUnit, x_agenda: AgendaUnit = None):
    if x_agenda is None:
        x_agenda = agendaunit_shop()

    x_agenda = x_nuc.get_edited_agenda(x_agenda)

    try:
        x_agenda.calc_agenda_metrics()
    except Exception:
        return False

    return True


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_nested_value(
        x_dict=x_dict, x_keylist=x_keylist, if_missing_return_None=True
    )


def create_legible_list(x_nuc: NucUnit, x_agenda: AgendaUnit) -> list[str]:
    quarks_dict = x_nuc.quarkunits
    agendaunit_quark = get_leg_obj(quarks_dict, [quark_update(), "agendaunit"])

    partyunit_insert_dict = get_leg_obj(
        quarks_dict, [quark_insert(), "agenda_partyunit"]
    )
    partyunit_update_dict = get_leg_obj(
        quarks_dict, [quark_update(), "agenda_partyunit"]
    )
    partyunit_delete_dict = get_leg_obj(
        quarks_dict, [quark_delete(), "agenda_partyunit"]
    )

    groupunit_insert_dict = get_leg_obj(
        quarks_dict, [quark_insert(), "agenda_groupunit"]
    )
    groupunit_update_dict = get_leg_obj(
        quarks_dict, [quark_update(), "agenda_groupunit"]
    )
    groupunit_delete_dict = get_leg_obj(
        quarks_dict, [quark_delete(), "agenda_groupunit"]
    )

    x_list = [quark_insert(), "agenda_group_partylink"]
    group_partylink_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_group_partylink"]
    group_partylink_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_group_partylink"]
    group_partylink_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_ideaunit"]
    agenda_ideaunit_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_ideaunit"]
    agenda_ideaunit_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_ideaunit"]
    agenda_ideaunit_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_balancelink"]
    agenda_idea_balancelink_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_idea_balancelink"]
    agenda_idea_balancelink_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_balancelink"]
    agenda_idea_balancelink_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_reasonunit"]
    agenda_idea_reasonunit_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_idea_reasonunit"]
    agenda_idea_reasonunit_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_reasonunit"]
    agenda_idea_reasonunit_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_reason_premiseunit"]
    agenda_idea_reason_premiseunit_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_idea_reason_premiseunit"]
    agenda_idea_reason_premiseunit_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_reason_premiseunit"]
    agenda_idea_reason_premiseunit_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_suffgroup"]
    agenda_idea_suffgroup_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_suffgroup"]
    agenda_idea_suffgroup_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_healerhold"]
    agenda_idea_healerhold_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_healerhold"]
    agenda_idea_healerhold_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_beliefunit"]
    agenda_idea_beliefunit_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_idea_beliefunit"]
    agenda_idea_beliefunit_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_beliefunit"]
    agenda_idea_beliefunit_delete_dict = get_leg_obj(quarks_dict, x_list)

    leg_list = []
    if agendaunit_quark != None:
        add_agendaunit_legible_list(leg_list, agendaunit_quark, x_agenda)
    if partyunit_insert_dict != None:
        add_agenda_partyunit_insert_to_legible_list(
            leg_list, partyunit_insert_dict, x_agenda
        )
    if partyunit_update_dict != None:
        add_agenda_partyunit_update_to_legible_list(
            leg_list, partyunit_update_dict, x_agenda
        )
    if partyunit_delete_dict != None:
        add_agenda_partyunit_delete_to_legible_list(
            leg_list, partyunit_delete_dict, x_agenda
        )

    if groupunit_insert_dict != None:
        add_agenda_groupunit_insert_to_legible_list(
            leg_list, groupunit_insert_dict, x_agenda
        )
    if groupunit_update_dict != None:
        add_agenda_groupunit_update_to_legible_list(
            leg_list, groupunit_update_dict, x_agenda
        )
    if groupunit_delete_dict != None:
        add_agenda_groupunit_delete_to_legible_list(
            leg_list, groupunit_delete_dict, x_agenda
        )

    if group_partylink_insert_dict != None:
        add_agenda_group_partylink_insert_to_legible_list(
            leg_list, group_partylink_insert_dict, x_agenda
        )
    if group_partylink_update_dict != None:
        add_agenda_group_partylink_update_to_legible_list(
            leg_list, group_partylink_update_dict, x_agenda
        )
    if group_partylink_delete_dict != None:
        add_agenda_group_partylink_delete_to_legible_list(
            leg_list, group_partylink_delete_dict, x_agenda
        )

    if agenda_ideaunit_insert_dict != None:
        add_agenda_ideaunit_insert_to_legible_list(
            leg_list, agenda_ideaunit_insert_dict, x_agenda
        )
    if agenda_ideaunit_update_dict != None:
        add_agenda_ideaunit_update_to_legible_list(
            leg_list, agenda_ideaunit_update_dict, x_agenda
        )
    if agenda_ideaunit_delete_dict != None:
        add_agenda_ideaunit_delete_to_legible_list(
            leg_list, agenda_ideaunit_delete_dict, x_agenda
        )

    if agenda_idea_balancelink_insert_dict != None:
        add_agenda_idea_balancelink_insert_to_legible_list(
            leg_list, agenda_idea_balancelink_insert_dict, x_agenda
        )
    if agenda_idea_balancelink_update_dict != None:
        add_agenda_idea_balancelink_update_to_legible_list(
            leg_list, agenda_idea_balancelink_update_dict, x_agenda
        )
    if agenda_idea_balancelink_delete_dict != None:
        add_agenda_idea_balancelink_delete_to_legible_list(
            leg_list, agenda_idea_balancelink_delete_dict, x_agenda
        )

    if agenda_idea_reasonunit_insert_dict != None:
        add_agenda_idea_reasonunit_insert_to_legible_list(
            leg_list, agenda_idea_reasonunit_insert_dict, x_agenda
        )
    if agenda_idea_reasonunit_update_dict != None:
        add_agenda_idea_reasonunit_update_to_legible_list(
            leg_list, agenda_idea_reasonunit_update_dict, x_agenda
        )
    if agenda_idea_reasonunit_delete_dict != None:
        add_agenda_idea_reasonunit_delete_to_legible_list(
            leg_list, agenda_idea_reasonunit_delete_dict, x_agenda
        )

    if agenda_idea_reason_premiseunit_insert_dict != None:
        add_agenda_reason_premiseunit_insert_to_legible_list(
            leg_list, agenda_idea_reason_premiseunit_insert_dict, x_agenda
        )
    if agenda_idea_reason_premiseunit_update_dict != None:
        add_agenda_reason_premiseunit_update_to_legible_list(
            leg_list, agenda_idea_reason_premiseunit_update_dict, x_agenda
        )
    if agenda_idea_reason_premiseunit_delete_dict != None:
        add_agenda_reason_premiseunit_delete_to_legible_list(
            leg_list, agenda_idea_reason_premiseunit_delete_dict, x_agenda
        )

    if agenda_idea_suffgroup_insert_dict != None:
        add_agenda_idea_suffgroup_insert_to_legible_list(
            leg_list, agenda_idea_suffgroup_insert_dict, x_agenda
        )
    if agenda_idea_suffgroup_delete_dict != None:
        add_agenda_idea_suffgroup_delete_to_legible_list(
            leg_list, agenda_idea_suffgroup_delete_dict, x_agenda
        )

    if agenda_idea_healerhold_insert_dict != None:
        add_agenda_idea_healerhold_insert_to_legible_list(
            leg_list, agenda_idea_healerhold_insert_dict, x_agenda
        )
    if agenda_idea_healerhold_delete_dict != None:
        add_agenda_idea_healerhold_delete_to_legible_list(
            leg_list, agenda_idea_healerhold_delete_dict, x_agenda
        )

    if agenda_idea_beliefunit_insert_dict != None:
        add_agenda_idea_beliefunit_insert_to_legible_list(
            leg_list, agenda_idea_beliefunit_insert_dict, x_agenda
        )
    if agenda_idea_beliefunit_update_dict != None:
        add_agenda_idea_beliefunit_update_to_legible_list(
            leg_list, agenda_idea_beliefunit_update_dict, x_agenda
        )
    if agenda_idea_beliefunit_delete_dict != None:
        add_agenda_idea_beliefunit_delete_to_legible_list(
            leg_list, agenda_idea_beliefunit_delete_dict, x_agenda
        )

    return leg_list


def add_agendaunit_legible_list(
    legible_list: list[str], x_quark: QuarkUnit, x_agenda: AgendaUnit
):
    optional_args = x_quark.optional_args
    _weight_text = "_weight"
    _max_tree_traverse_text = "_max_tree_traverse"
    _meld_strategy_text = "_meld_strategy"
    _monetary_desc_text = "_monetary_desc"
    _party_credor_pool_text = "_party_credor_pool"
    _party_debtor_pool_text = "_party_debtor_pool"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _meld_strategy_value = optional_args.get(_meld_strategy_text)
    _monetary_desc_value = optional_args.get(_monetary_desc_text)
    _party_credor_pool_value = optional_args.get(_party_credor_pool_text)
    _party_debtor_pool_value = optional_args.get(_party_debtor_pool_text)
    _weight_value = optional_args.get(_weight_text)

    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = f"{x_agenda._owner_id}'s monetary_desc"

    if _max_tree_traverse_value != None:
        legible_list.append(
            f"{x_agenda._owner_id}'s maximum number of Agenda output evaluations transited to {_max_tree_traverse_value}"
        )
    if _meld_strategy_value != None:
        legible_list.append(
            f"{x_agenda._owner_id}'s Meld strategy transited to '{_meld_strategy_value}'"
        )
    if _monetary_desc_value != None:
        legible_list.append(
            f"{x_agenda._owner_id}'s monetary_desc is now called '{_monetary_desc_value}'"
        )
    if (
        _party_credor_pool_value != None
        and _party_debtor_pool_value != None
        and _party_credor_pool_value == _party_debtor_pool_value
    ):
        legible_list.append(
            f"{x_monetary_desc} total pool is now {_party_credor_pool_value}"
        )
    elif _party_credor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} credor pool is now {_party_credor_pool_value}"
        )
    elif _party_debtor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} debtor pool is now {_party_debtor_pool_value}"
        )
    if _weight_value != None:
        legible_list.append(
            f"{x_agenda._owner_id}'s agenda weight was transited to {_weight_value}"
        )


def add_agenda_partyunit_insert_to_legible_list(
    legible_list: list[str], partyunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for partyunit_quark in partyunit_dict.values():
        party_id = partyunit_quark.get_value("party_id")
        credor_weight_value = partyunit_quark.get_value("credor_weight")
        debtor_weight_value = partyunit_quark.get_value("debtor_weight")
        x_str = f"{party_id} was added with {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_agenda_partyunit_update_to_legible_list(
    legible_list: list[str], partyunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for partyunit_quark in partyunit_dict.values():
        party_id = partyunit_quark.get_value("party_id")
        credor_weight_value = partyunit_quark.get_value("credor_weight")
        debtor_weight_value = partyunit_quark.get_value("debtor_weight")
        if credor_weight_value != None and debtor_weight_value != None:
            x_str = f"{party_id} now has {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt."
        elif credor_weight_value != None and debtor_weight_value is None:
            x_str = f"{party_id} now has {credor_weight_value} {x_monetary_desc} cred."
        elif credor_weight_value is None and debtor_weight_value != None:
            x_str = f"{party_id} now has {debtor_weight_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_agenda_partyunit_delete_to_legible_list(
    legible_list: list[str], partyunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for partyunit_quark in partyunit_dict.values():
        party_id = partyunit_quark.get_value("party_id")
        x_str = f"{party_id} was removed from {x_monetary_desc} partys."
        legible_list.append(x_str)


def add_agenda_groupunit_insert_to_legible_list(
    legible_list: list[str], groupunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    for groupunit_quark in groupunit_dict.values():
        group_id = groupunit_quark.get_value("group_id")
        x_str = f"The group '{group_id}' was created"
        x_str += "."
        legible_list.append(x_str)


def add_agenda_groupunit_update_to_legible_list(
    legible_list: list[str], groupunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    for groupunit_quark in groupunit_dict.values():
        group_id = groupunit_quark.get_value("group_id")
        x_str = f"The group '{group_id}'"
        x_str += "."
        legible_list.append(x_str)


def add_agenda_groupunit_delete_to_legible_list(
    legible_list: list[str], groupunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for groupunit_quark in groupunit_dict.values():
        group_id = groupunit_quark.get_value("group_id")
        x_str = f"The group '{group_id}' was deleted."
        legible_list.append(x_str)


def add_agenda_group_partylink_insert_to_legible_list(
    legible_list: list[str], group_partylink_insert_dict: dict, x_agenda: AgendaUnit
):
    for group_partylink_dict in group_partylink_insert_dict.values():
        for group_partylink_quark in group_partylink_dict.values():
            group_id = group_partylink_quark.get_value("group_id")
            party_id = group_partylink_quark.get_value("party_id")
            credor_weight_value = group_partylink_quark.get_value("credor_weight")
            debtor_weight_value = group_partylink_quark.get_value("debtor_weight")
            x_str = f"Group '{group_id}' has new member {party_id} with group_cred={credor_weight_value} and group_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_group_partylink_update_to_legible_list(
    legible_list: list[str], group_partylink_update_dict: dict, x_agenda: AgendaUnit
):
    for group_partylink_dict in group_partylink_update_dict.values():
        for group_partylink_quark in group_partylink_dict.values():
            group_id = group_partylink_quark.get_value("group_id")
            party_id = group_partylink_quark.get_value("party_id")
            credor_weight_value = group_partylink_quark.get_value("credor_weight")
            debtor_weight_value = group_partylink_quark.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Group '{group_id}' member {party_id} has new group_cred={credor_weight_value} and group_debt={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Group '{group_id}' member {party_id} has new group_cred={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Group '{group_id}' member {party_id} has new group_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_group_partylink_delete_to_legible_list(
    legible_list: list[str], group_partylink_delete_dict: dict, x_agenda: AgendaUnit
):
    for group_partylink_dict in group_partylink_delete_dict.values():
        for group_partylink_quark in group_partylink_dict.values():
            group_id = group_partylink_quark.get_value("group_id")
            party_id = group_partylink_quark.get_value("party_id")
            x_str = f"Group '{group_id}' no longer has member {party_id}."
            legible_list.append(x_str)


def add_agenda_ideaunit_insert_to_legible_list(
    legible_list: list[str], ideaunit_insert_dict: dict, x_agenda: AgendaUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_insert_dict.values():
        for ideaunit_quark in parent_road_dict.values():
            label_value = ideaunit_quark.get_value(label_text)
            parent_road_value = ideaunit_quark.get_value(parent_road_text)
            _addin_value = ideaunit_quark.get_value(_addin_text)
            _begin_value = ideaunit_quark.get_value(_begin_text)
            _close_value = ideaunit_quark.get_value(_close_text)
            _denom_value = ideaunit_quark.get_value(_denom_text)
            _meld_strategy_value = ideaunit_quark.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_quark.get_value(_numeric_road_text)
            _numor_value = ideaunit_quark.get_value(_numor_text)
            _problem_bool_value = ideaunit_quark.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_quark.get_value(_range_source_road_text)
            _reest_value = ideaunit_quark.get_value(_reest_text)
            _weight_value = ideaunit_quark.get_value(_weight_text)
            pledge_value = ideaunit_quark.get_value(pledge_text)
            x_str = (
                f"Created Idea '{label_value}' with parent_road {parent_road_value}. "
            )
            if _addin_value != None:
                x_str += f"_addin={_addin_value}."
            if _begin_value != None:
                x_str += f"_begin={_begin_value}."
            if _close_value != None:
                x_str += f"_close={_close_value}."
            if _denom_value != None:
                x_str += f"_denom={_denom_value}."
            if _meld_strategy_value != None:
                x_str += f"_meld_strategy={_meld_strategy_value}."
            if _numeric_road_value != None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value != None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value != None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value != None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value != None:
                x_str += f"_reest={_reest_value}."
            if _weight_value != None:
                x_str += f"_weight={_weight_value}."
            if pledge_value != None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_agenda_ideaunit_update_to_legible_list(
    legible_list: list[str], ideaunit_update_dict: dict, x_agenda: AgendaUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    pledge_text = "pledge"
    for parent_road_dict in ideaunit_update_dict.values():
        for ideaunit_quark in parent_road_dict.values():
            label_value = ideaunit_quark.get_value(label_text)
            parent_road_value = ideaunit_quark.get_value(parent_road_text)
            _addin_value = ideaunit_quark.get_value(_addin_text)
            _begin_value = ideaunit_quark.get_value(_begin_text)
            _close_value = ideaunit_quark.get_value(_close_text)
            _denom_value = ideaunit_quark.get_value(_denom_text)
            _meld_strategy_value = ideaunit_quark.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_quark.get_value(_numeric_road_text)
            _numor_value = ideaunit_quark.get_value(_numor_text)
            _problem_bool_value = ideaunit_quark.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_quark.get_value(_range_source_road_text)
            _reest_value = ideaunit_quark.get_value(_reest_text)
            _weight_value = ideaunit_quark.get_value(_weight_text)
            pledge_value = ideaunit_quark.get_value(pledge_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} transited these attributes: "
            if _addin_value != None:
                x_str += f"_addin={_addin_value}."
            if _begin_value != None:
                x_str += f"_begin={_begin_value}."
            if _close_value != None:
                x_str += f"_close={_close_value}."
            if _denom_value != None:
                x_str += f"_denom={_denom_value}."
            if _meld_strategy_value != None:
                x_str += f"_meld_strategy={_meld_strategy_value}."
            if _numeric_road_value != None:
                x_str += f"_numeric_road={_numeric_road_value}."
            if _numor_value != None:
                x_str += f"_numor={_numor_value}."
            if _problem_bool_value != None:
                x_str += f"_problem_bool={_problem_bool_value}."
            if _range_source_road_value != None:
                x_str += f"_range_source_road={_range_source_road_value}."
            if _reest_value != None:
                x_str += f"_reest={_reest_value}."
            if _weight_value != None:
                x_str += f"_weight={_weight_value}."
            if pledge_value != None:
                x_str += f"pledge={pledge_value}."

            legible_list.append(x_str)


def add_agenda_ideaunit_delete_to_legible_list(
    legible_list: list[str], ideaunit_delete_dict: dict, x_agenda: AgendaUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    for parent_road_dict in ideaunit_delete_dict.values():
        for ideaunit_quark in parent_road_dict.values():
            label_value = ideaunit_quark.get_value(label_text)
            parent_road_value = ideaunit_quark.get_value(parent_road_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_agenda_idea_balancelink_insert_to_legible_list(
    legible_list: list[str], idea_balancelink_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_balancelink_insert_dict.values():
        for idea_balancelink_quark in road_dict.values():
            group_id_value = idea_balancelink_quark.get_value("group_id")
            road_value = idea_balancelink_quark.get_value("road")
            credor_weight_value = idea_balancelink_quark.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_quark.get_value("debtor_weight")
            x_str = f"Balancelink created for group {group_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_idea_balancelink_update_to_legible_list(
    legible_list: list[str], idea_balancelink_update_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_balancelink_update_dict.values():
        for idea_balancelink_quark in road_dict.values():
            group_id_value = idea_balancelink_quark.get_value("group_id")
            road_value = idea_balancelink_quark.get_value("road")
            credor_weight_value = idea_balancelink_quark.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_quark.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for group {group_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Balancelink has been transited for group {group_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for group {group_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_idea_balancelink_delete_to_legible_list(
    legible_list: list[str], idea_balancelink_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_balancelink_delete_dict.values():
        for idea_balancelink_quark in road_dict.values():
            group_id_value = idea_balancelink_quark.get_value("group_id")
            road_value = idea_balancelink_quark.get_value("road")
            x_str = f"Balancelink for group {group_id_value}, idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_agenda_idea_reasonunit_insert_to_legible_list(
    legible_list: list[str], idea_reasonunit_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_reasonunit_insert_dict.values():
        for idea_reasonunit_quark in road_dict.values():
            road_value = idea_reasonunit_quark.get_value("road")
            base_value = idea_reasonunit_quark.get_value("base")
            suff_idea_active_value = idea_reasonunit_quark.get_value("suff_idea_active")
            x_str = (
                f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
            )
            if suff_idea_active_value != None:
                x_str += f" suff_idea_active={suff_idea_active_value}."
            legible_list.append(x_str)


def add_agenda_idea_reasonunit_update_to_legible_list(
    legible_list: list[str], idea_reasonunit_update_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_reasonunit_update_dict.values():
        for idea_reasonunit_quark in road_dict.values():
            road_value = idea_reasonunit_quark.get_value("road")
            base_value = idea_reasonunit_quark.get_value("base")
            suff_idea_active_value = idea_reasonunit_quark.get_value("suff_idea_active")
            if suff_idea_active_value != None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with suff_idea_active={suff_idea_active_value}."
            elif suff_idea_active_value is None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
            legible_list.append(x_str)


def add_agenda_idea_reasonunit_delete_to_legible_list(
    legible_list: list[str], idea_reasonunit_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_reasonunit_delete_dict.values():
        for idea_reasonunit_quark in road_dict.values():
            road_value = idea_reasonunit_quark.get_value("road")
            base_value = idea_reasonunit_quark.get_value("base")
            x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_agenda_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_insert_dict: dict,
    x_agenda: AgendaUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_insert_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_quark in base_dict.values():
                road_value = idea_reason_premiseunit_quark.get_value(road_text)
                base_value = idea_reason_premiseunit_quark.get_value(base_text)
                need_value = idea_reason_premiseunit_quark.get_value(need_text)
                divisor_value = idea_reason_premiseunit_quark.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_quark.get_value(nigh_text)
                open_value = idea_reason_premiseunit_quark.get_value(open_text)
                x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for idea '{road_value}'."
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_agenda_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_update_dict: dict,
    x_agenda: AgendaUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_update_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_quark in base_dict.values():
                road_value = idea_reason_premiseunit_quark.get_value(road_text)
                base_value = idea_reason_premiseunit_quark.get_value(base_text)
                need_value = idea_reason_premiseunit_quark.get_value(need_text)
                divisor_value = idea_reason_premiseunit_quark.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_quark.get_value(nigh_text)
                open_value = idea_reason_premiseunit_quark.get_value(open_text)
                x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for idea '{road_value}'."
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_agenda_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_delete_dict: dict,
    x_agenda: AgendaUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    for road_dict in idea_reason_premiseunit_delete_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_quark in base_dict.values():
                road_value = idea_reason_premiseunit_quark.get_value(road_text)
                base_value = idea_reason_premiseunit_quark.get_value(base_text)
                need_value = idea_reason_premiseunit_quark.get_value(need_text)
                x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for idea '{road_value}'."
                legible_list.append(x_str)


def add_agenda_idea_suffgroup_insert_to_legible_list(
    legible_list: list[str], idea_suffgroup_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_suffgroup_insert_dict.values():
        for idea_suffgroup_quark in road_dict.values():
            group_id_value = idea_suffgroup_quark.get_value("group_id")
            road_value = idea_suffgroup_quark.get_value("road")
            x_str = f"Suffgroup '{group_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_suffgroup_delete_to_legible_list(
    legible_list: list[str], idea_suffgroup_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_suffgroup_delete_dict.values():
        for idea_suffgroup_quark in road_dict.values():
            group_id_value = idea_suffgroup_quark.get_value("group_id")
            road_value = idea_suffgroup_quark.get_value("road")
            x_str = f"Suffgroup '{group_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_healerhold_insert_to_legible_list(
    legible_list: list[str], idea_healerhold_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_healerhold_insert_dict.values():
        for idea_healerhold_quark in road_dict.values():
            group_id_value = idea_healerhold_quark.get_value("group_id")
            road_value = idea_healerhold_quark.get_value("road")
            x_str = f"Healerhold '{group_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_healerhold_delete_to_legible_list(
    legible_list: list[str], idea_healerhold_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_healerhold_delete_dict.values():
        for idea_healerhold_quark in road_dict.values():
            group_id_value = idea_healerhold_quark.get_value("group_id")
            road_value = idea_healerhold_quark.get_value("road")
            x_str = f"Healerhold '{group_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_beliefunit_insert_to_legible_list(
    legible_list: list[str], idea_beliefunit_insert_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_beliefunit_insert_dict.values():
        for idea_beliefunit_quark in road_dict.values():
            road_value = idea_beliefunit_quark.get_value(road_text)
            base_value = idea_beliefunit_quark.get_value(base_text)
            pick_value = idea_beliefunit_quark.get_value(pick_text)
            nigh_value = idea_beliefunit_quark.get_value(nigh_text)
            open_value = idea_beliefunit_quark.get_value(open_text)
            x_str = f"BeliefUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_agenda_idea_beliefunit_update_to_legible_list(
    legible_list: list[str], idea_beliefunit_update_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_beliefunit_update_dict.values():
        for idea_beliefunit_quark in road_dict.values():
            road_value = idea_beliefunit_quark.get_value(road_text)
            base_value = idea_beliefunit_quark.get_value(base_text)
            pick_value = idea_beliefunit_quark.get_value(pick_text)
            nigh_value = idea_beliefunit_quark.get_value(nigh_text)
            open_value = idea_beliefunit_quark.get_value(open_text)
            x_str = f"BeliefUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_agenda_idea_beliefunit_delete_to_legible_list(
    legible_list: list[str], idea_beliefunit_delete_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    for road_dict in idea_beliefunit_delete_dict.values():
        for idea_beliefunit_quark in road_dict.values():
            road_value = idea_beliefunit_quark.get_value(road_text)
            base_value = idea_beliefunit_quark.get_value(base_text)
            pick_value = idea_beliefunit_quark.get_value(pick_text)
            x_str = f"BeliefUnit '{pick_value}' deleted from base '{base_value}' for idea '{road_value}'."
            legible_list.append(x_str)
