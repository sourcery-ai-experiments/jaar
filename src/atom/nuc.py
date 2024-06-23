from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src.agenda.reason_idea import FactUnit, ReasonUnit
from src.agenda.other import OtherLink, OtherID
from src.agenda.belief import BeliefUnit, BeliefID
from src.agenda.idea import IdeaUnit
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.atom.quark_config import CRUD_command
from src.atom.quark import (
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
        self.add_quarkunit_otherunits(before_agenda, after_agenda)
        self.add_quarkunit_beliefunits(before_agenda, after_agenda)
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
        if before_agenda._other_credor_pool != after_agenda._other_credor_pool:
            x_quarkunit.set_optional_arg(
                "_other_credor_pool", after_agenda._other_credor_pool
            )
        if before_agenda._other_debtor_pool != after_agenda._other_debtor_pool:
            x_quarkunit.set_optional_arg(
                "_other_debtor_pool", after_agenda._other_debtor_pool
            )
        if before_agenda._weight != after_agenda._weight:
            x_quarkunit.set_optional_arg("_weight", after_agenda._weight)
        if before_agenda._pixel != after_agenda._pixel:
            x_quarkunit.set_optional_arg("_pixel", after_agenda._pixel)
        self.set_quarkunit(x_quarkunit)

    def add_quarkunit_otherunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_other_ids = set(before_agenda._others.keys())
        after_other_ids = set(after_agenda._others.keys())

        self.add_quarkunit_otherunit_inserts(
            after_agenda=after_agenda,
            insert_other_ids=after_other_ids.difference(before_other_ids),
        )
        self.add_quarkunit_otherunit_deletes(
            delete_other_ids=before_other_ids.difference(after_other_ids)
        )
        self.add_quarkunit_otherunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_other_ids=before_other_ids.intersection(after_other_ids),
        )

    def add_quarkunit_otherunit_inserts(
        self, after_agenda: AgendaUnit, insert_other_ids: set
    ):
        for insert_other_id in insert_other_ids:
            x_otherunit = after_agenda.get_other(insert_other_id)
            x_quarkunit = quarkunit_shop("agenda_otherunit", quark_insert())
            x_quarkunit.set_required_arg("other_id", x_otherunit.other_id)
            if x_otherunit.credor_weight != None:
                x_quarkunit.set_optional_arg("credor_weight", x_otherunit.credor_weight)
            if x_otherunit.debtor_weight != None:
                x_quarkunit.set_optional_arg("debtor_weight", x_otherunit.debtor_weight)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_otherunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_other_ids: set
    ):
        for other_id in update_other_ids:
            after_otherunit = after_agenda.get_other(other_id)
            before_otherunit = before_agenda.get_other(other_id)
            if optional_args_different(
                "agenda_otherunit", after_otherunit, before_otherunit
            ):
                x_quarkunit = quarkunit_shop("agenda_otherunit", quark_update())
                x_quarkunit.set_required_arg("other_id", after_otherunit.other_id)
                if before_otherunit.credor_weight != after_otherunit.credor_weight:
                    x_quarkunit.set_optional_arg(
                        "credor_weight", after_otherunit.credor_weight
                    )
                if before_otherunit.debtor_weight != after_otherunit.debtor_weight:
                    x_quarkunit.set_optional_arg(
                        "debtor_weight", after_otherunit.debtor_weight
                    )
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_otherunit_deletes(self, delete_other_ids: set):
        for delete_other_id in delete_other_ids:
            x_quarkunit = quarkunit_shop("agenda_otherunit", quark_delete())
            x_quarkunit.set_required_arg("other_id", delete_other_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_beliefunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_belief_ids = {
            before_belief_id
            for before_belief_id in before_agenda._beliefs.keys()
            if before_agenda.get_beliefunit(before_belief_id)._other_mirror is False
        }
        after_belief_ids = {
            after_belief_id
            for after_belief_id in after_agenda._beliefs.keys()
            if after_agenda.get_beliefunit(after_belief_id)._other_mirror is False
        }

        self.add_quarkunit_beliefunit_inserts(
            after_agenda=after_agenda,
            insert_belief_ids=after_belief_ids.difference(before_belief_ids),
        )

        self.add_quarkunit_beliefunit_deletes(
            before_agenda=before_agenda,
            delete_belief_ids=before_belief_ids.difference(after_belief_ids),
        )

        self.add_quarkunit_beliefunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_belief_ids=before_belief_ids.intersection(after_belief_ids),
        )

    def add_quarkunit_beliefunit_inserts(
        self, after_agenda: AgendaUnit, insert_belief_ids: set
    ):
        for insert_belief_id in insert_belief_ids:
            insert_beliefunit = after_agenda.get_beliefunit(insert_belief_id)
            x_quarkunit = quarkunit_shop("agenda_beliefunit", quark_insert())
            x_quarkunit.set_required_arg("belief_id", insert_beliefunit.belief_id)
            self.set_quarkunit(x_quarkunit)
            self.add_quarkunit_otherlinks_inserts(
                after_beliefunit=insert_beliefunit,
                insert_otherlink_other_ids=set(insert_beliefunit._others.keys()),
            )

    def add_quarkunit_beliefunit_updates(
        self,
        before_agenda: AgendaUnit,
        after_agenda: AgendaUnit,
        update_belief_ids: set,
    ):
        for belief_id in update_belief_ids:
            after_beliefunit = after_agenda.get_beliefunit(belief_id)
            before_beliefunit = before_agenda.get_beliefunit(belief_id)
            if optional_args_different(
                "agenda_beliefunit", before_beliefunit, after_beliefunit
            ):
                x_quarkunit = quarkunit_shop("agenda_beliefunit", quark_update())
                x_quarkunit.set_required_arg("belief_id", after_beliefunit.belief_id)
                self.set_quarkunit(x_quarkunit)

            self.add_quarkunit_beliefunit_update_otherlinks(
                after_beliefunit=after_beliefunit, before_beliefunit=before_beliefunit
            )

    def add_quarkunit_beliefunit_update_otherlinks(
        self, after_beliefunit: BeliefUnit, before_beliefunit: BeliefUnit
    ):
        after_other_ids = set(after_beliefunit._others.keys())
        before_other_ids = set(before_beliefunit._others.keys())

        self.add_quarkunit_otherlinks_inserts(
            after_beliefunit=after_beliefunit,
            insert_otherlink_other_ids=after_other_ids.difference(before_other_ids),
        )

        self.add_quarkunit_otherlinks_delete(
            before_belief_id=before_beliefunit.belief_id,
            before_other_ids=before_other_ids.difference(after_other_ids),
        )

        update_other_ids = before_other_ids.intersection(after_other_ids)
        for update_other_id in update_other_ids:
            before_otherlink = before_beliefunit.get_otherlink(update_other_id)
            after_otherlink = after_beliefunit.get_otherlink(update_other_id)
            if optional_args_different(
                "agenda_belief_otherlink", before_otherlink, after_otherlink
            ):
                self.add_quarkunit_otherlink_update(
                    belief_id=after_beliefunit.belief_id,
                    before_otherlink=before_otherlink,
                    after_otherlink=after_otherlink,
                )

    def add_quarkunit_beliefunit_deletes(
        self, before_agenda: AgendaUnit, delete_belief_ids: set
    ):
        for delete_belief_id in delete_belief_ids:
            x_quarkunit = quarkunit_shop("agenda_beliefunit", quark_delete())
            x_quarkunit.set_required_arg("belief_id", delete_belief_id)
            self.set_quarkunit(x_quarkunit)

            delete_beliefunit = before_agenda.get_beliefunit(delete_belief_id)
            self.add_quarkunit_otherlinks_delete(
                delete_belief_id, set(delete_beliefunit._others.keys())
            )

    def add_quarkunit_otherlinks_inserts(
        self,
        after_beliefunit: BeliefUnit,
        insert_otherlink_other_ids: list[OtherID],
    ):
        after_belief_id = after_beliefunit.belief_id
        for insert_other_id in insert_otherlink_other_ids:
            after_otherlink = after_beliefunit.get_otherlink(insert_other_id)
            x_quarkunit = quarkunit_shop("agenda_belief_otherlink", quark_insert())
            x_quarkunit.set_required_arg("belief_id", after_belief_id)
            x_quarkunit.set_required_arg("other_id", after_otherlink.other_id)
            if after_otherlink.credor_weight != None:
                x_quarkunit.set_optional_arg(
                    "credor_weight", after_otherlink.credor_weight
                )
            if after_otherlink.debtor_weight != None:
                x_quarkunit.set_optional_arg(
                    "debtor_weight", after_otherlink.debtor_weight
                )
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_otherlink_update(
        self,
        belief_id: BeliefID,
        before_otherlink: OtherLink,
        after_otherlink: OtherLink,
    ):
        x_quarkunit = quarkunit_shop("agenda_belief_otherlink", quark_update())
        x_quarkunit.set_required_arg("belief_id", belief_id)
        x_quarkunit.set_required_arg("other_id", after_otherlink.other_id)
        if after_otherlink.credor_weight != before_otherlink.credor_weight:
            x_quarkunit.set_optional_arg("credor_weight", after_otherlink.credor_weight)
        if after_otherlink.debtor_weight != before_otherlink.debtor_weight:
            x_quarkunit.set_optional_arg("debtor_weight", after_otherlink.debtor_weight)
        self.set_quarkunit(x_quarkunit)

    def add_quarkunit_otherlinks_delete(
        self, before_belief_id: BeliefID, before_other_ids: OtherID
    ):
        for delete_other_id in before_other_ids:
            x_quarkunit = quarkunit_shop("agenda_belief_otherlink", quark_delete())
            x_quarkunit.set_required_arg("belief_id", before_belief_id)
            x_quarkunit.set_required_arg("other_id", delete_other_id)
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

            self.add_quarkunit_idea_factunit_inserts(
                ideaunit=insert_ideaunit,
                insert_factunit_bases=set(insert_ideaunit._factunits.keys()),
            )
            self.add_quarkunit_idea_balancelink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_balancelink_belief_ids=set(insert_ideaunit._balancelinks.keys()),
            )
            self.add_quarkunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_quarkunit_idea_suffbelief_insert(
                idea_road=insert_idea_road,
                insert_suffbelief_belief_ids=insert_ideaunit._assignedunit._suffbeliefs.keys(),
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

            # insert / update / delete factunits
            before_factunit_bases = set(before_ideaunit._factunits.keys())
            after_factunit_bases = set(after_ideaunit._factunits.keys())
            self.add_quarkunit_idea_factunit_inserts(
                ideaunit=after_ideaunit,
                insert_factunit_bases=after_factunit_bases.difference(
                    before_factunit_bases
                ),
            )
            self.add_quarkunit_idea_factunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_factunit_bases=before_factunit_bases.intersection(
                    after_factunit_bases
                ),
            )
            self.add_quarkunit_idea_factunit_deletes(
                idea_road=idea_road,
                delete_factunit_bases=before_factunit_bases.difference(
                    after_factunit_bases
                ),
            )

            # insert / update / delete balanceunits
            before_balancelinks_belief_ids = set(before_ideaunit._balancelinks.keys())
            after_balancelinks_belief_ids = set(after_ideaunit._balancelinks.keys())
            self.add_quarkunit_idea_balancelink_inserts(
                after_ideaunit=after_ideaunit,
                insert_balancelink_belief_ids=after_balancelinks_belief_ids.difference(
                    before_balancelinks_belief_ids
                ),
            )
            self.add_quarkunit_idea_balancelink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_balancelink_belief_ids=before_balancelinks_belief_ids.intersection(
                    after_balancelinks_belief_ids
                ),
            )
            self.add_quarkunit_idea_balancelink_deletes(
                idea_road=idea_road,
                delete_balancelink_belief_ids=before_balancelinks_belief_ids.difference(
                    after_balancelinks_belief_ids
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

            # insert / update / delete suffbeliefs
            before_suffbeliefs_belief_ids = set(
                before_ideaunit._assignedunit._suffbeliefs.keys()
            )
            after_suffbeliefs_belief_ids = set(
                after_ideaunit._assignedunit._suffbeliefs.keys()
            )
            self.add_quarkunit_idea_suffbelief_insert(
                idea_road=idea_road,
                insert_suffbelief_belief_ids=after_suffbeliefs_belief_ids.difference(
                    before_suffbeliefs_belief_ids
                ),
            )
            self.add_quarkunit_idea_suffbelief_deletes(
                idea_road=idea_road,
                delete_suffbelief_belief_ids=before_suffbeliefs_belief_ids.difference(
                    after_suffbeliefs_belief_ids
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
            self.add_quarkunit_idea_factunit_deletes(
                idea_road=delete_idea_road,
                delete_factunit_bases=set(delete_ideaunit._factunits.keys()),
            )
            self.add_quarkunit_idea_balancelink_deletes(
                idea_road=delete_idea_road,
                delete_balancelink_belief_ids=set(delete_ideaunit._balancelinks.keys()),
            )
            self.add_quarkunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_quarkunit_idea_suffbelief_deletes(
                idea_road=delete_idea_road,
                delete_suffbelief_belief_ids=set(
                    delete_ideaunit._assignedunit._suffbeliefs.keys()
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

    def add_quarkunit_idea_suffbelief_insert(
        self, idea_road: RoadUnit, insert_suffbelief_belief_ids: set
    ):
        for insert_suffbelief_belief_id in insert_suffbelief_belief_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_suffbelief", quark_insert())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("belief_id", insert_suffbelief_belief_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_suffbelief_deletes(
        self, idea_road: RoadUnit, delete_suffbelief_belief_ids: set
    ):
        for delete_suffbelief_belief_id in delete_suffbelief_belief_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_suffbelief", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("belief_id", delete_suffbelief_belief_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_balancelink_inserts(
        self, after_ideaunit: IdeaUnit, insert_balancelink_belief_ids: set
    ):
        for after_balancelink_belief_id in insert_balancelink_belief_ids:
            after_balancelink = after_ideaunit._balancelinks.get(
                after_balancelink_belief_id
            )
            x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_insert())
            x_quarkunit.set_required_arg("road", after_ideaunit.get_road())
            x_quarkunit.set_required_arg("belief_id", after_balancelink.belief_id)
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
        update_balancelink_belief_ids: set,
    ):
        for update_balancelink_belief_id in update_balancelink_belief_ids:
            before_balancelink = before_ideaunit._balancelinks.get(
                update_balancelink_belief_id
            )
            after_balancelink = after_ideaunit._balancelinks.get(
                update_balancelink_belief_id
            )
            if optional_args_different(
                "agenda_idea_balancelink", before_balancelink, after_balancelink
            ):
                x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_update())
                x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
                x_quarkunit.set_required_arg("belief_id", after_balancelink.belief_id)
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
        self, idea_road: RoadUnit, delete_balancelink_belief_ids: set
    ):
        for delete_balancelink_belief_id in delete_balancelink_belief_ids:
            x_quarkunit = quarkunit_shop("agenda_idea_balancelink", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("belief_id", delete_balancelink_belief_id)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = ideaunit._factunits.get(insert_factunit_base)
            x_quarkunit = quarkunit_shop("agenda_idea_factunit", quark_insert())
            x_quarkunit.set_required_arg("road", ideaunit.get_road())
            x_quarkunit.set_required_arg("base", insert_factunit.base)
            if insert_factunit.pick != None:
                x_quarkunit.set_optional_arg("pick", insert_factunit.pick)
            if insert_factunit.open != None:
                x_quarkunit.set_optional_arg("open", insert_factunit.open)
            if insert_factunit.nigh != None:
                x_quarkunit.set_optional_arg("nigh", insert_factunit.nigh)
            self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_factunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_factunit_bases: set,
    ):
        for update_factunit_base in update_factunit_bases:
            before_factunit = before_ideaunit._factunits.get(update_factunit_base)
            after_factunit = after_ideaunit._factunits.get(update_factunit_base)
            if optional_args_different(
                "agenda_idea_factunit", before_factunit, after_factunit
            ):
                x_quarkunit = quarkunit_shop("agenda_idea_factunit", quark_update())
                x_quarkunit.set_required_arg("road", before_ideaunit.get_road())
                x_quarkunit.set_required_arg("base", after_factunit.base)
                if before_factunit.pick != after_factunit.pick:
                    x_quarkunit.set_optional_arg("pick", after_factunit.pick)
                if before_factunit.open != after_factunit.open:
                    x_quarkunit.set_optional_arg("open", after_factunit.open)
                if before_factunit.nigh != after_factunit.nigh:
                    x_quarkunit.set_optional_arg("nigh", after_factunit.nigh)
                self.set_quarkunit(x_quarkunit)

    def add_quarkunit_idea_factunit_deletes(
        self, idea_road: RoadUnit, delete_factunit_bases: FactUnit
    ):
        for delete_factunit_base in delete_factunit_bases:
            x_quarkunit = quarkunit_shop("agenda_idea_factunit", quark_delete())
            x_quarkunit.set_required_arg("road", idea_road)
            x_quarkunit.set_required_arg("base", delete_factunit_base)
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

    otherunit_insert_dict = get_leg_obj(
        quarks_dict, [quark_insert(), "agenda_otherunit"]
    )
    otherunit_update_dict = get_leg_obj(
        quarks_dict, [quark_update(), "agenda_otherunit"]
    )
    otherunit_delete_dict = get_leg_obj(
        quarks_dict, [quark_delete(), "agenda_otherunit"]
    )

    beliefunit_insert_dict = get_leg_obj(
        quarks_dict, [quark_insert(), "agenda_beliefunit"]
    )
    beliefunit_update_dict = get_leg_obj(
        quarks_dict, [quark_update(), "agenda_beliefunit"]
    )
    beliefunit_delete_dict = get_leg_obj(
        quarks_dict, [quark_delete(), "agenda_beliefunit"]
    )

    x_list = [quark_insert(), "agenda_belief_otherlink"]
    belief_otherlink_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_belief_otherlink"]
    belief_otherlink_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_belief_otherlink"]
    belief_otherlink_delete_dict = get_leg_obj(quarks_dict, x_list)

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

    x_list = [quark_insert(), "agenda_idea_suffbelief"]
    agenda_idea_suffbelief_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_suffbelief"]
    agenda_idea_suffbelief_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_healerhold"]
    agenda_idea_healerhold_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_healerhold"]
    agenda_idea_healerhold_delete_dict = get_leg_obj(quarks_dict, x_list)

    x_list = [quark_insert(), "agenda_idea_factunit"]
    agenda_idea_factunit_insert_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_update(), "agenda_idea_factunit"]
    agenda_idea_factunit_update_dict = get_leg_obj(quarks_dict, x_list)
    x_list = [quark_delete(), "agenda_idea_factunit"]
    agenda_idea_factunit_delete_dict = get_leg_obj(quarks_dict, x_list)

    leg_list = []
    if agendaunit_quark != None:
        add_agendaunit_legible_list(leg_list, agendaunit_quark, x_agenda)
    if otherunit_insert_dict != None:
        add_agenda_otherunit_insert_to_legible_list(
            leg_list, otherunit_insert_dict, x_agenda
        )
    if otherunit_update_dict != None:
        add_agenda_otherunit_update_to_legible_list(
            leg_list, otherunit_update_dict, x_agenda
        )
    if otherunit_delete_dict != None:
        add_agenda_otherunit_delete_to_legible_list(
            leg_list, otherunit_delete_dict, x_agenda
        )

    if beliefunit_insert_dict != None:
        add_agenda_beliefunit_insert_to_legible_list(
            leg_list, beliefunit_insert_dict, x_agenda
        )
    if beliefunit_update_dict != None:
        add_agenda_beliefunit_update_to_legible_list(
            leg_list, beliefunit_update_dict, x_agenda
        )
    if beliefunit_delete_dict != None:
        add_agenda_beliefunit_delete_to_legible_list(
            leg_list, beliefunit_delete_dict, x_agenda
        )

    if belief_otherlink_insert_dict != None:
        add_agenda_belief_otherlink_insert_to_legible_list(
            leg_list, belief_otherlink_insert_dict, x_agenda
        )
    if belief_otherlink_update_dict != None:
        add_agenda_belief_otherlink_update_to_legible_list(
            leg_list, belief_otherlink_update_dict, x_agenda
        )
    if belief_otherlink_delete_dict != None:
        add_agenda_belief_otherlink_delete_to_legible_list(
            leg_list, belief_otherlink_delete_dict, x_agenda
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

    if agenda_idea_suffbelief_insert_dict != None:
        add_agenda_idea_suffbelief_insert_to_legible_list(
            leg_list, agenda_idea_suffbelief_insert_dict, x_agenda
        )
    if agenda_idea_suffbelief_delete_dict != None:
        add_agenda_idea_suffbelief_delete_to_legible_list(
            leg_list, agenda_idea_suffbelief_delete_dict, x_agenda
        )

    if agenda_idea_healerhold_insert_dict != None:
        add_agenda_idea_healerhold_insert_to_legible_list(
            leg_list, agenda_idea_healerhold_insert_dict, x_agenda
        )
    if agenda_idea_healerhold_delete_dict != None:
        add_agenda_idea_healerhold_delete_to_legible_list(
            leg_list, agenda_idea_healerhold_delete_dict, x_agenda
        )

    if agenda_idea_factunit_insert_dict != None:
        add_agenda_idea_factunit_insert_to_legible_list(
            leg_list, agenda_idea_factunit_insert_dict, x_agenda
        )
    if agenda_idea_factunit_update_dict != None:
        add_agenda_idea_factunit_update_to_legible_list(
            leg_list, agenda_idea_factunit_update_dict, x_agenda
        )
    if agenda_idea_factunit_delete_dict != None:
        add_agenda_idea_factunit_delete_to_legible_list(
            leg_list, agenda_idea_factunit_delete_dict, x_agenda
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
    _other_credor_pool_text = "_other_credor_pool"
    _other_debtor_pool_text = "_other_debtor_pool"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _meld_strategy_value = optional_args.get(_meld_strategy_text)
    _monetary_desc_value = optional_args.get(_monetary_desc_text)
    _other_credor_pool_value = optional_args.get(_other_credor_pool_text)
    _other_debtor_pool_value = optional_args.get(_other_debtor_pool_text)
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
        _other_credor_pool_value != None
        and _other_debtor_pool_value != None
        and _other_credor_pool_value == _other_debtor_pool_value
    ):
        legible_list.append(
            f"{x_monetary_desc} total pool is now {_other_credor_pool_value}"
        )
    elif _other_credor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} credor pool is now {_other_credor_pool_value}"
        )
    elif _other_debtor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} debtor pool is now {_other_debtor_pool_value}"
        )
    if _weight_value != None:
        legible_list.append(
            f"{x_agenda._owner_id}'s agenda weight was transited to {_weight_value}"
        )


def add_agenda_otherunit_insert_to_legible_list(
    legible_list: list[str], otherunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for otherunit_quark in otherunit_dict.values():
        other_id = otherunit_quark.get_value("other_id")
        credor_weight_value = otherunit_quark.get_value("credor_weight")
        debtor_weight_value = otherunit_quark.get_value("debtor_weight")
        x_str = f"{other_id} was added with {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_agenda_otherunit_update_to_legible_list(
    legible_list: list[str], otherunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for otherunit_quark in otherunit_dict.values():
        other_id = otherunit_quark.get_value("other_id")
        credor_weight_value = otherunit_quark.get_value("credor_weight")
        debtor_weight_value = otherunit_quark.get_value("debtor_weight")
        if credor_weight_value != None and debtor_weight_value != None:
            x_str = f"{other_id} now has {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt."
        elif credor_weight_value != None and debtor_weight_value is None:
            x_str = f"{other_id} now has {credor_weight_value} {x_monetary_desc} cred."
        elif credor_weight_value is None and debtor_weight_value != None:
            x_str = f"{other_id} now has {debtor_weight_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_agenda_otherunit_delete_to_legible_list(
    legible_list: list[str], otherunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for otherunit_quark in otherunit_dict.values():
        other_id = otherunit_quark.get_value("other_id")
        x_str = f"{other_id} was removed from {x_monetary_desc} others."
        legible_list.append(x_str)


def add_agenda_beliefunit_insert_to_legible_list(
    legible_list: list[str], beliefunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    for beliefunit_quark in beliefunit_dict.values():
        belief_id = beliefunit_quark.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was created"
        x_str += "."
        legible_list.append(x_str)


def add_agenda_beliefunit_update_to_legible_list(
    legible_list: list[str], beliefunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    for beliefunit_quark in beliefunit_dict.values():
        belief_id = beliefunit_quark.get_value("belief_id")
        x_str = f"The belief '{belief_id}'"
        x_str += "."
        legible_list.append(x_str)


def add_agenda_beliefunit_delete_to_legible_list(
    legible_list: list[str], beliefunit_dict: QuarkUnit, x_agenda: AgendaUnit
):
    x_monetary_desc = x_agenda._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for beliefunit_quark in beliefunit_dict.values():
        belief_id = beliefunit_quark.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was deleted."
        legible_list.append(x_str)


def add_agenda_belief_otherlink_insert_to_legible_list(
    legible_list: list[str], belief_otherlink_insert_dict: dict, x_agenda: AgendaUnit
):
    for belief_otherlink_dict in belief_otherlink_insert_dict.values():
        for belief_otherlink_quark in belief_otherlink_dict.values():
            belief_id = belief_otherlink_quark.get_value("belief_id")
            other_id = belief_otherlink_quark.get_value("other_id")
            credor_weight_value = belief_otherlink_quark.get_value("credor_weight")
            debtor_weight_value = belief_otherlink_quark.get_value("debtor_weight")
            x_str = f"Belief '{belief_id}' has new member {other_id} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_belief_otherlink_update_to_legible_list(
    legible_list: list[str], belief_otherlink_update_dict: dict, x_agenda: AgendaUnit
):
    for belief_otherlink_dict in belief_otherlink_update_dict.values():
        for belief_otherlink_quark in belief_otherlink_dict.values():
            belief_id = belief_otherlink_quark.get_value("belief_id")
            other_id = belief_otherlink_quark.get_value("other_id")
            credor_weight_value = belief_otherlink_quark.get_value("credor_weight")
            debtor_weight_value = belief_otherlink_quark.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {other_id} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Belief '{belief_id}' member {other_id} has new belief_cred={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {other_id} has new belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_belief_otherlink_delete_to_legible_list(
    legible_list: list[str], belief_otherlink_delete_dict: dict, x_agenda: AgendaUnit
):
    for belief_otherlink_dict in belief_otherlink_delete_dict.values():
        for belief_otherlink_quark in belief_otherlink_dict.values():
            belief_id = belief_otherlink_quark.get_value("belief_id")
            other_id = belief_otherlink_quark.get_value("other_id")
            x_str = f"Belief '{belief_id}' no longer has member {other_id}."
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
            belief_id_value = idea_balancelink_quark.get_value("belief_id")
            road_value = idea_balancelink_quark.get_value("road")
            credor_weight_value = idea_balancelink_quark.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_quark.get_value("debtor_weight")
            x_str = f"Balancelink created for belief {belief_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_idea_balancelink_update_to_legible_list(
    legible_list: list[str], idea_balancelink_update_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_balancelink_update_dict.values():
        for idea_balancelink_quark in road_dict.values():
            belief_id_value = idea_balancelink_quark.get_value("belief_id")
            road_value = idea_balancelink_quark.get_value("road")
            credor_weight_value = idea_balancelink_quark.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_quark.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_agenda_idea_balancelink_delete_to_legible_list(
    legible_list: list[str], idea_balancelink_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_balancelink_delete_dict.values():
        for idea_balancelink_quark in road_dict.values():
            belief_id_value = idea_balancelink_quark.get_value("belief_id")
            road_value = idea_balancelink_quark.get_value("road")
            x_str = f"Balancelink for belief {belief_id_value}, idea '{road_value}' has been deleted."
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


def add_agenda_idea_suffbelief_insert_to_legible_list(
    legible_list: list[str], idea_suffbelief_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_suffbelief_insert_dict.values():
        for idea_suffbelief_quark in road_dict.values():
            belief_id_value = idea_suffbelief_quark.get_value("belief_id")
            road_value = idea_suffbelief_quark.get_value("road")
            x_str = f"Suffbelief '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_suffbelief_delete_to_legible_list(
    legible_list: list[str], idea_suffbelief_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_suffbelief_delete_dict.values():
        for idea_suffbelief_quark in road_dict.values():
            belief_id_value = idea_suffbelief_quark.get_value("belief_id")
            road_value = idea_suffbelief_quark.get_value("road")
            x_str = f"Suffbelief '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_healerhold_insert_to_legible_list(
    legible_list: list[str], idea_healerhold_insert_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_healerhold_insert_dict.values():
        for idea_healerhold_quark in road_dict.values():
            belief_id_value = idea_healerhold_quark.get_value("belief_id")
            road_value = idea_healerhold_quark.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_healerhold_delete_to_legible_list(
    legible_list: list[str], idea_healerhold_delete_dict: dict, x_agenda: AgendaUnit
):
    for road_dict in idea_healerhold_delete_dict.values():
        for idea_healerhold_quark in road_dict.values():
            belief_id_value = idea_healerhold_quark.get_value("belief_id")
            road_value = idea_healerhold_quark.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_agenda_idea_factunit_insert_to_legible_list(
    legible_list: list[str], idea_factunit_insert_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_insert_dict.values():
        for idea_factunit_quark in road_dict.values():
            road_value = idea_factunit_quark.get_value(road_text)
            base_value = idea_factunit_quark.get_value(base_text)
            pick_value = idea_factunit_quark.get_value(pick_text)
            nigh_value = idea_factunit_quark.get_value(nigh_text)
            open_value = idea_factunit_quark.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_agenda_idea_factunit_update_to_legible_list(
    legible_list: list[str], idea_factunit_update_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_update_dict.values():
        for idea_factunit_quark in road_dict.values():
            road_value = idea_factunit_quark.get_value(road_text)
            base_value = idea_factunit_quark.get_value(base_text)
            pick_value = idea_factunit_quark.get_value(pick_text)
            nigh_value = idea_factunit_quark.get_value(nigh_text)
            open_value = idea_factunit_quark.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_agenda_idea_factunit_delete_to_legible_list(
    legible_list: list[str], idea_factunit_delete_dict: dict, x_agenda: AgendaUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    for road_dict in idea_factunit_delete_dict.values():
        for idea_factunit_quark in road_dict.values():
            road_value = idea_factunit_quark.get_value(road_text)
            base_value = idea_factunit_quark.get_value(base_text)
            pick_value = idea_factunit_quark.get_value(pick_text)
            x_str = f"FactUnit '{pick_value}' deleted from base '{base_value}' for idea '{road_value}'."
            legible_list.append(x_str)
