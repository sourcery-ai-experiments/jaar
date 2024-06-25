from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
    get_0_if_None,
)
from src._road.road import RoadUnit, get_terminus_node, get_parent_road
from src._world.reason_idea import FactUnit, ReasonUnit
from src._world.person import BeliefLink, PersonID
from src._world.belief import BeliefUnit, BeliefID
from src._world.idea import IdeaUnit
from src._world.world import WorldUnit, worldunit_shop
from src.gift.atom_config import CRUD_command
from src.gift.atom import (
    AtomUnit,
    atomunit_shop,
    modify_world_with_atomunit,
    InvalidAtomUnitException,
    atom_delete,
    atom_insert,
    atom_update,
    optional_args_different,
)
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class ChangeUnit:
    atomunits: dict[CRUD_command : dict[str:AtomUnit]] = None
    _world_build_validated: bool = None

    def _get_crud_atomunits_list(self) -> dict[CRUD_command : list[AtomUnit]]:
        return get_all_nondictionary_objs(self.atomunits)

    def get_category_sorted_atomunits_list(self) -> list[AtomUnit]:
        atoms_list = []
        for crud_list in self._get_crud_atomunits_list().values():
            atoms_list.extend(iter(crud_list))

        atom_order_key_dict = {}
        for x_atom in atoms_list:
            atom_order_list = atom_order_key_dict.get(x_atom.atom_order)
            if atom_order_list is None:
                atom_order_key_dict[x_atom.atom_order] = [x_atom]
            else:
                atom_order_list.append(x_atom)

        ordered_list = []
        for x_list in atom_order_key_dict.values():
            if x_list[0].required_args.get("parent_road") != None:
                x_list = sorted(
                    x_list, key=lambda x: x.required_args.get("parent_road")
                )
            if x_list[0].required_args.get("road") != None:
                x_list = sorted(x_list, key=lambda x: x.required_args.get("road"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_atomunits(self) -> list[AtomUnit]:
        atomunits_list = self.get_category_sorted_atomunits_list()
        return sorted(atomunits_list, key=lambda x: x.atom_order)

    def get_edited_world(self, before_world: WorldUnit):
        edited_world = copy_deepcopy(before_world)
        for x_atomunit in self.get_sorted_atomunits():
            modify_world_with_atomunit(edited_world, x_atomunit)
        return edited_world

    def set_atomunit(self, x_atomunit: AtomUnit):
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_text} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_text,
            x_atomunit.category,
            *list(x_atomunit.required_args.values()),
        ]
        place_obj_in_dict(self.atomunits, x_keylist, x_atomunit)

    def atomunit_exists(self, x_atomunit: AtomUnit) -> bool:
        if x_atomunit.is_valid() is False:
            raise InvalidAtomUnitException(
                f"""'{x_atomunit.category}' {x_atomunit.crud_text} AtomUnit is invalid
                {x_atomunit.is_required_args_valid()=}
                {x_atomunit.is_optional_args_valid()=}"""
            )

        x_atomunit.set_atom_order()
        x_keylist = [
            x_atomunit.crud_text,
            x_atomunit.category,
            *list(x_atomunit.required_args.values()),
        ]
        try:
            nested_atomunit = get_nested_value(self.atomunits, x_keylist)
        except Exception:
            return False
        return nested_atomunit == x_atomunit

    def add_atomunit(
        self,
        category: str,
        crud_text: str,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_atomunit = atomunit_shop(
            category=category,
            crud_text=crud_text,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_atomunit(x_atomunit)

    def get_atomunit(
        self, crud_text: str, category: str, required_args: list[str]
    ) -> AtomUnit:
        x_keylist = [crud_text, category, *required_args]
        return get_nested_value(self.atomunits, x_keylist)

    def add_all_different_atomunits(
        self, before_world: WorldUnit, after_world: WorldUnit
    ):
        before_world.calc_world_metrics()
        after_world.calc_world_metrics()
        self.add_atomunits_worldunit_simple_attrs(before_world, after_world)
        self.add_atomunit_personunits(before_world, after_world)
        self.add_atomunit_beliefunits(before_world, after_world)
        self.add_atomunits_ideas(before_world, after_world)

    def add_atomunits_worldunit_simple_attrs(
        self, before_world: WorldUnit, after_world: WorldUnit
    ):
        if not optional_args_different("worldunit", before_world, after_world):
            return
        x_atomunit = atomunit_shop("worldunit", atom_update())
        if before_world._max_tree_traverse != after_world._max_tree_traverse:
            x_atomunit.set_optional_arg(
                "_max_tree_traverse", after_world._max_tree_traverse
            )
        if before_world._meld_strategy != after_world._meld_strategy:
            x_atomunit.set_optional_arg("_meld_strategy", after_world._meld_strategy)
        if before_world._monetary_desc != after_world._monetary_desc:
            x_atomunit.set_optional_arg("_monetary_desc", after_world._monetary_desc)
        if before_world._person_credor_pool != after_world._person_credor_pool:
            x_atomunit.set_optional_arg(
                "_person_credor_pool", after_world._person_credor_pool
            )
        if before_world._person_debtor_pool != after_world._person_debtor_pool:
            x_atomunit.set_optional_arg(
                "_person_debtor_pool", after_world._person_debtor_pool
            )
        if before_world._weight != after_world._weight:
            x_atomunit.set_optional_arg("_weight", after_world._weight)
        if before_world._pixel != after_world._pixel:
            x_atomunit.set_optional_arg("_pixel", after_world._pixel)
        self.set_atomunit(x_atomunit)

    def add_atomunit_personunits(self, before_world: WorldUnit, after_world: WorldUnit):
        before_person_ids = set(before_world._persons.keys())
        after_person_ids = set(after_world._persons.keys())

        self.add_atomunit_personunit_inserts(
            after_world=after_world,
            insert_person_ids=after_person_ids.difference(before_person_ids),
        )
        self.add_atomunit_personunit_deletes(
            delete_person_ids=before_person_ids.difference(after_person_ids)
        )
        self.add_atomunit_personunit_updates(
            before_world=before_world,
            after_world=after_world,
            update_person_ids=before_person_ids.intersection(after_person_ids),
        )

    def add_atomunit_personunit_inserts(
        self, after_world: WorldUnit, insert_person_ids: set
    ):
        for insert_person_id in insert_person_ids:
            x_personunit = after_world.get_person(insert_person_id)
            x_atomunit = atomunit_shop("world_personunit", atom_insert())
            x_atomunit.set_required_arg("person_id", x_personunit.person_id)
            if x_personunit.credor_weight != None:
                x_atomunit.set_optional_arg("credor_weight", x_personunit.credor_weight)
            if x_personunit.debtor_weight != None:
                x_atomunit.set_optional_arg("debtor_weight", x_personunit.debtor_weight)
            self.set_atomunit(x_atomunit)

    def add_atomunit_personunit_updates(
        self, before_world: WorldUnit, after_world: WorldUnit, update_person_ids: set
    ):
        for person_id in update_person_ids:
            after_personunit = after_world.get_person(person_id)
            before_personunit = before_world.get_person(person_id)
            if optional_args_different(
                "world_personunit", after_personunit, before_personunit
            ):
                x_atomunit = atomunit_shop("world_personunit", atom_update())
                x_atomunit.set_required_arg("person_id", after_personunit.person_id)
                if before_personunit.credor_weight != after_personunit.credor_weight:
                    x_atomunit.set_optional_arg(
                        "credor_weight", after_personunit.credor_weight
                    )
                if before_personunit.debtor_weight != after_personunit.debtor_weight:
                    x_atomunit.set_optional_arg(
                        "debtor_weight", after_personunit.debtor_weight
                    )
                self.set_atomunit(x_atomunit)

    def add_atomunit_personunit_deletes(self, delete_person_ids: set):
        for delete_person_id in delete_person_ids:
            x_atomunit = atomunit_shop("world_personunit", atom_delete())
            x_atomunit.set_required_arg("person_id", delete_person_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_beliefunits(self, before_world: WorldUnit, after_world: WorldUnit):
        before_belief_ids = {
            before_belief_id
            for before_belief_id in before_world._beliefs.keys()
            if before_world.get_beliefunit(before_belief_id)._person_mirror is False
        }
        after_belief_ids = {
            after_belief_id
            for after_belief_id in after_world._beliefs.keys()
            if after_world.get_beliefunit(after_belief_id)._person_mirror is False
        }

        self.add_atomunit_beliefunit_inserts(
            after_world=after_world,
            insert_belief_ids=after_belief_ids.difference(before_belief_ids),
        )

        self.add_atomunit_beliefunit_deletes(
            before_world=before_world,
            delete_belief_ids=before_belief_ids.difference(after_belief_ids),
        )

        self.add_atomunit_beliefunit_updates(
            before_world=before_world,
            after_world=after_world,
            update_belief_ids=before_belief_ids.intersection(after_belief_ids),
        )

    def add_atomunit_beliefunit_inserts(
        self, after_world: WorldUnit, insert_belief_ids: set
    ):
        for insert_belief_id in insert_belief_ids:
            insert_beliefunit = after_world.get_beliefunit(insert_belief_id)
            x_atomunit = atomunit_shop("world_beliefunit", atom_insert())
            x_atomunit.set_required_arg("belief_id", insert_beliefunit.belief_id)
            self.set_atomunit(x_atomunit)
            self.add_atomunit_belieflinks_inserts(
                after_beliefunit=insert_beliefunit,
                insert_belieflink_person_ids=set(insert_beliefunit._persons.keys()),
            )

    def add_atomunit_beliefunit_updates(
        self,
        before_world: WorldUnit,
        after_world: WorldUnit,
        update_belief_ids: set,
    ):
        for belief_id in update_belief_ids:
            after_beliefunit = after_world.get_beliefunit(belief_id)
            before_beliefunit = before_world.get_beliefunit(belief_id)
            if optional_args_different(
                "world_beliefunit", before_beliefunit, after_beliefunit
            ):
                x_atomunit = atomunit_shop("world_beliefunit", atom_update())
                x_atomunit.set_required_arg("belief_id", after_beliefunit.belief_id)
                self.set_atomunit(x_atomunit)

            self.add_atomunit_beliefunit_update_belieflinks(
                after_beliefunit=after_beliefunit, before_beliefunit=before_beliefunit
            )

    def add_atomunit_beliefunit_update_belieflinks(
        self, after_beliefunit: BeliefUnit, before_beliefunit: BeliefUnit
    ):
        after_person_ids = set(after_beliefunit._persons.keys())
        before_person_ids = set(before_beliefunit._persons.keys())

        self.add_atomunit_belieflinks_inserts(
            after_beliefunit=after_beliefunit,
            insert_belieflink_person_ids=after_person_ids.difference(before_person_ids),
        )

        self.add_atomunit_belieflinks_delete(
            before_belief_id=before_beliefunit.belief_id,
            before_person_ids=before_person_ids.difference(after_person_ids),
        )

        update_person_ids = before_person_ids.intersection(after_person_ids)
        for update_person_id in update_person_ids:
            before_belieflink = before_beliefunit.get_belieflink(update_person_id)
            after_belieflink = after_beliefunit.get_belieflink(update_person_id)
            if optional_args_different(
                "world_belief_belieflink", before_belieflink, after_belieflink
            ):
                self.add_atomunit_belieflink_update(
                    belief_id=after_beliefunit.belief_id,
                    before_belieflink=before_belieflink,
                    after_belieflink=after_belieflink,
                )

    def add_atomunit_beliefunit_deletes(
        self, before_world: WorldUnit, delete_belief_ids: set
    ):
        for delete_belief_id in delete_belief_ids:
            x_atomunit = atomunit_shop("world_beliefunit", atom_delete())
            x_atomunit.set_required_arg("belief_id", delete_belief_id)
            self.set_atomunit(x_atomunit)

            delete_beliefunit = before_world.get_beliefunit(delete_belief_id)
            self.add_atomunit_belieflinks_delete(
                delete_belief_id, set(delete_beliefunit._persons.keys())
            )

    def add_atomunit_belieflinks_inserts(
        self,
        after_beliefunit: BeliefUnit,
        insert_belieflink_person_ids: list[PersonID],
    ):
        after_belief_id = after_beliefunit.belief_id
        for insert_person_id in insert_belieflink_person_ids:
            after_belieflink = after_beliefunit.get_belieflink(insert_person_id)
            x_atomunit = atomunit_shop("world_belief_belieflink", atom_insert())
            x_atomunit.set_required_arg("belief_id", after_belief_id)
            x_atomunit.set_required_arg("person_id", after_belieflink.person_id)
            if after_belieflink.credor_weight != None:
                x_atomunit.set_optional_arg(
                    "credor_weight", after_belieflink.credor_weight
                )
            if after_belieflink.debtor_weight != None:
                x_atomunit.set_optional_arg(
                    "debtor_weight", after_belieflink.debtor_weight
                )
            self.set_atomunit(x_atomunit)

    def add_atomunit_belieflink_update(
        self,
        belief_id: BeliefID,
        before_belieflink: BeliefLink,
        after_belieflink: BeliefLink,
    ):
        x_atomunit = atomunit_shop("world_belief_belieflink", atom_update())
        x_atomunit.set_required_arg("belief_id", belief_id)
        x_atomunit.set_required_arg("person_id", after_belieflink.person_id)
        if after_belieflink.credor_weight != before_belieflink.credor_weight:
            x_atomunit.set_optional_arg("credor_weight", after_belieflink.credor_weight)
        if after_belieflink.debtor_weight != before_belieflink.debtor_weight:
            x_atomunit.set_optional_arg("debtor_weight", after_belieflink.debtor_weight)
        self.set_atomunit(x_atomunit)

    def add_atomunit_belieflinks_delete(
        self, before_belief_id: BeliefID, before_person_ids: PersonID
    ):
        for delete_person_id in before_person_ids:
            x_atomunit = atomunit_shop("world_belief_belieflink", atom_delete())
            x_atomunit.set_required_arg("belief_id", before_belief_id)
            x_atomunit.set_required_arg("person_id", delete_person_id)
            self.set_atomunit(x_atomunit)

    def add_atomunits_ideas(self, before_world: WorldUnit, after_world: WorldUnit):
        before_idea_roads = set(before_world._idea_dict.keys())
        after_idea_roads = set(after_world._idea_dict.keys())

        self.add_atomunit_idea_inserts(
            after_world=after_world,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_atomunit_idea_deletes(
            before_world=before_world,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_atomunit_idea_updates(
            before_world=before_world,
            after_world=after_world,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_atomunit_idea_inserts(self, after_world: WorldUnit, insert_idea_roads: set):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_world.get_idea_obj(insert_idea_road)
            x_atomunit = atomunit_shop("world_ideaunit", atom_insert())
            x_atomunit.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_atomunit.set_required_arg("label", insert_ideaunit._label)
            x_atomunit.set_optional_arg("_addin", insert_ideaunit._addin)
            x_atomunit.set_optional_arg("_begin", insert_ideaunit._begin)
            x_atomunit.set_optional_arg("_close", insert_ideaunit._close)
            x_atomunit.set_optional_arg("_denom", insert_ideaunit._denom)
            x_atomunit.set_optional_arg(
                "_meld_strategy", insert_ideaunit._meld_strategy
            )
            x_atomunit.set_optional_arg("_numeric_road", insert_ideaunit._numeric_road)
            x_atomunit.set_optional_arg("_numor", insert_ideaunit._numor)
            x_atomunit.set_optional_arg(
                "_range_source_road", insert_ideaunit._range_source_road
            )
            x_atomunit.set_optional_arg("_reest", insert_ideaunit._reest)
            x_atomunit.set_optional_arg("_weight", insert_ideaunit._weight)
            x_atomunit.set_optional_arg("pledge", insert_ideaunit.pledge)
            self.set_atomunit(x_atomunit)

            self.add_atomunit_idea_factunit_inserts(
                ideaunit=insert_ideaunit,
                insert_factunit_bases=set(insert_ideaunit._factunits.keys()),
            )
            self.add_atomunit_idea_balancelink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_balancelink_belief_ids=set(insert_ideaunit._balancelinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_suffbelief_insert(
                idea_road=insert_idea_road,
                insert_suffbelief_belief_ids=insert_ideaunit._assignedunit._suffbeliefs.keys(),
            )

    def add_atomunit_idea_updates(
        self, before_world: WorldUnit, after_world: WorldUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_world.get_idea_obj(idea_road)
            before_ideaunit = before_world.get_idea_obj(idea_road)
            if optional_args_different(
                "world_ideaunit", before_ideaunit, after_ideaunit
            ):
                x_atomunit = atomunit_shop("world_ideaunit", atom_update())
                x_atomunit.set_required_arg("parent_road", after_ideaunit._parent_road)
                x_atomunit.set_required_arg("label", after_ideaunit._label)
                if before_ideaunit._addin != after_ideaunit._addin:
                    x_atomunit.set_optional_arg("_addin", after_ideaunit._addin)
                if before_ideaunit._begin != after_ideaunit._begin:
                    x_atomunit.set_optional_arg("_begin", after_ideaunit._begin)
                if before_ideaunit._close != after_ideaunit._close:
                    x_atomunit.set_optional_arg("_close", after_ideaunit._close)
                if before_ideaunit._denom != after_ideaunit._denom:
                    x_atomunit.set_optional_arg("_denom", after_ideaunit._denom)
                if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
                    x_atomunit.set_optional_arg(
                        "_meld_strategy", after_ideaunit._meld_strategy
                    )
                if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
                    x_atomunit.set_optional_arg(
                        "_numeric_road", after_ideaunit._numeric_road
                    )
                if before_ideaunit._numor != after_ideaunit._numor:
                    x_atomunit.set_optional_arg("_numor", after_ideaunit._numor)
                if (
                    before_ideaunit._range_source_road
                    != after_ideaunit._range_source_road
                ):
                    x_atomunit.set_optional_arg(
                        "_range_source_road", after_ideaunit._range_source_road
                    )
                if before_ideaunit._reest != after_ideaunit._reest:
                    x_atomunit.set_optional_arg("_reest", after_ideaunit._reest)
                if before_ideaunit._weight != after_ideaunit._weight:
                    x_atomunit.set_optional_arg("_weight", after_ideaunit._weight)
                if before_ideaunit.pledge != after_ideaunit.pledge:
                    x_atomunit.set_optional_arg("pledge", after_ideaunit.pledge)
                self.set_atomunit(x_atomunit)

            # insert / update / delete factunits
            before_factunit_bases = set(before_ideaunit._factunits.keys())
            after_factunit_bases = set(after_ideaunit._factunits.keys())
            self.add_atomunit_idea_factunit_inserts(
                ideaunit=after_ideaunit,
                insert_factunit_bases=after_factunit_bases.difference(
                    before_factunit_bases
                ),
            )
            self.add_atomunit_idea_factunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_factunit_bases=before_factunit_bases.intersection(
                    after_factunit_bases
                ),
            )
            self.add_atomunit_idea_factunit_deletes(
                idea_road=idea_road,
                delete_factunit_bases=before_factunit_bases.difference(
                    after_factunit_bases
                ),
            )

            # insert / update / delete balanceunits
            before_balancelinks_belief_ids = set(before_ideaunit._balancelinks.keys())
            after_balancelinks_belief_ids = set(after_ideaunit._balancelinks.keys())
            self.add_atomunit_idea_balancelink_inserts(
                after_ideaunit=after_ideaunit,
                insert_balancelink_belief_ids=after_balancelinks_belief_ids.difference(
                    before_balancelinks_belief_ids
                ),
            )
            self.add_atomunit_idea_balancelink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_balancelink_belief_ids=before_balancelinks_belief_ids.intersection(
                    after_balancelinks_belief_ids
                ),
            )
            self.add_atomunit_idea_balancelink_deletes(
                idea_road=idea_road,
                delete_balancelink_belief_ids=before_balancelinks_belief_ids.difference(
                    after_balancelinks_belief_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit._reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit._reasonunits.keys())
            self.add_atomunit_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_atomunit_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_atomunit_idea_reasonunit_deletes(
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
            self.add_atomunit_idea_suffbelief_insert(
                idea_road=idea_road,
                insert_suffbelief_belief_ids=after_suffbeliefs_belief_ids.difference(
                    before_suffbeliefs_belief_ids
                ),
            )
            self.add_atomunit_idea_suffbelief_deletes(
                idea_road=idea_road,
                delete_suffbelief_belief_ids=before_suffbeliefs_belief_ids.difference(
                    after_suffbeliefs_belief_ids
                ),
            )

    def add_atomunit_idea_deletes(
        self, before_world: WorldUnit, delete_idea_roads: set
    ):
        for delete_idea_road in delete_idea_roads:
            x_parent_road = get_parent_road(
                delete_idea_road, before_world._road_delimiter
            )
            x_label = get_terminus_node(delete_idea_road, before_world._road_delimiter)
            x_atomunit = atomunit_shop("world_ideaunit", atom_delete())
            x_atomunit.set_required_arg("parent_road", x_parent_road)
            x_atomunit.set_required_arg("label", x_label)
            self.set_atomunit(x_atomunit)

            delete_ideaunit = before_world.get_idea_obj(delete_idea_road)
            self.add_atomunit_idea_factunit_deletes(
                idea_road=delete_idea_road,
                delete_factunit_bases=set(delete_ideaunit._factunits.keys()),
            )
            self.add_atomunit_idea_balancelink_deletes(
                idea_road=delete_idea_road,
                delete_balancelink_belief_ids=set(delete_ideaunit._balancelinks.keys()),
            )
            self.add_atomunit_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_atomunit_idea_suffbelief_deletes(
                idea_road=delete_idea_road,
                delete_suffbelief_belief_ids=set(
                    delete_ideaunit._assignedunit._suffbeliefs.keys()
                ),
            )

    def add_atomunit_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_atomunit = atomunit_shop("world_idea_reasonunit", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.suff_idea_active != None:
                x_atomunit.set_optional_arg(
                    "suff_idea_active", after_reasonunit.suff_idea_active
                )
            self.set_atomunit(x_atomunit)

            self.add_atomunit_idea_reason_premiseunit_inserts(
                idea_road=after_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_atomunit_idea_reasonunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_reasonunit_bases: set,
    ):
        for update_reasonunit_base in update_reasonunit_bases:
            before_reasonunit = before_ideaunit.get_reasonunit(update_reasonunit_base)
            after_reasonunit = after_ideaunit.get_reasonunit(update_reasonunit_base)
            if optional_args_different(
                "world_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_atomunit = atomunit_shop("world_idea_reasonunit", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.suff_idea_active
                    != after_reasonunit.suff_idea_active
                ):
                    x_atomunit.set_optional_arg(
                        "suff_idea_active", after_reasonunit.suff_idea_active
                    )
                self.set_atomunit(x_atomunit)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_atomunit_idea_reason_premiseunit_inserts(
                idea_road=before_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_atomunit_idea_reason_premiseunit_updates(
                idea_road=before_ideaunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_atomunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_atomunit_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_atomunit = atomunit_shop("world_idea_reasonunit", atom_delete())
            x_atomunit.set_required_arg("road", before_ideaunit.get_road())
            x_atomunit.set_required_arg("base", delete_reasonunit_base)
            self.set_atomunit(x_atomunit)

            before_reasonunit = before_ideaunit.get_reasonunit(delete_reasonunit_base)
            self.add_atomunit_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_atomunit_idea_reason_premiseunit_inserts(
        self,
        idea_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", after_reasonunit.base)
            x_atomunit.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open != None:
                x_atomunit.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh != None:
                x_atomunit.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor != None:
                x_atomunit.set_optional_arg("divisor", after_premiseunit.divisor)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_reason_premiseunit_updates(
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
                "world_idea_reason_premiseunit", before_premiseunit, after_premiseunit
            ):
                x_atomunit = atomunit_shop(
                    "world_idea_reason_premiseunit", atom_update()
                )
                x_atomunit.set_required_arg("road", idea_road)
                x_atomunit.set_required_arg("base", before_reasonunit.base)
                x_atomunit.set_required_arg("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_atomunit.set_optional_arg("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_atomunit.set_optional_arg("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_atomunit.set_optional_arg("divisor", after_premiseunit.divisor)
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_reason_premiseunit_deletes(
        self,
        idea_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_atomunit = atomunit_shop("world_idea_reason_premiseunit", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", reasonunit_base)
            x_atomunit.set_required_arg("need", delete_premise_need)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_suffbelief_insert(
        self, idea_road: RoadUnit, insert_suffbelief_belief_ids: set
    ):
        for insert_suffbelief_belief_id in insert_suffbelief_belief_ids:
            x_atomunit = atomunit_shop("world_idea_suffbelief", atom_insert())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", insert_suffbelief_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_suffbelief_deletes(
        self, idea_road: RoadUnit, delete_suffbelief_belief_ids: set
    ):
        for delete_suffbelief_belief_id in delete_suffbelief_belief_ids:
            x_atomunit = atomunit_shop("world_idea_suffbelief", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", delete_suffbelief_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_balancelink_inserts(
        self, after_ideaunit: IdeaUnit, insert_balancelink_belief_ids: set
    ):
        for after_balancelink_belief_id in insert_balancelink_belief_ids:
            after_balancelink = after_ideaunit._balancelinks.get(
                after_balancelink_belief_id
            )
            x_atomunit = atomunit_shop("world_idea_balancelink", atom_insert())
            x_atomunit.set_required_arg("road", after_ideaunit.get_road())
            x_atomunit.set_required_arg("belief_id", after_balancelink.belief_id)
            x_atomunit.set_optional_arg(
                "credor_weight", after_balancelink.credor_weight
            )
            x_atomunit.set_optional_arg(
                "debtor_weight", after_balancelink.debtor_weight
            )
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_balancelink_updates(
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
                "world_idea_balancelink", before_balancelink, after_balancelink
            ):
                x_atomunit = atomunit_shop("world_idea_balancelink", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("belief_id", after_balancelink.belief_id)
                if before_balancelink.credor_weight != after_balancelink.credor_weight:
                    x_atomunit.set_optional_arg(
                        "credor_weight", after_balancelink.credor_weight
                    )
                if before_balancelink.debtor_weight != after_balancelink.debtor_weight:
                    x_atomunit.set_optional_arg(
                        "debtor_weight", after_balancelink.debtor_weight
                    )
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_balancelink_deletes(
        self, idea_road: RoadUnit, delete_balancelink_belief_ids: set
    ):
        for delete_balancelink_belief_id in delete_balancelink_belief_ids:
            x_atomunit = atomunit_shop("world_idea_balancelink", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("belief_id", delete_balancelink_belief_id)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_inserts(
        self, ideaunit: IdeaUnit, insert_factunit_bases: set
    ):
        for insert_factunit_base in insert_factunit_bases:
            insert_factunit = ideaunit._factunits.get(insert_factunit_base)
            x_atomunit = atomunit_shop("world_idea_factunit", atom_insert())
            x_atomunit.set_required_arg("road", ideaunit.get_road())
            x_atomunit.set_required_arg("base", insert_factunit.base)
            if insert_factunit.pick != None:
                x_atomunit.set_optional_arg("pick", insert_factunit.pick)
            if insert_factunit.open != None:
                x_atomunit.set_optional_arg("open", insert_factunit.open)
            if insert_factunit.nigh != None:
                x_atomunit.set_optional_arg("nigh", insert_factunit.nigh)
            self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_factunit_bases: set,
    ):
        for update_factunit_base in update_factunit_bases:
            before_factunit = before_ideaunit._factunits.get(update_factunit_base)
            after_factunit = after_ideaunit._factunits.get(update_factunit_base)
            if optional_args_different(
                "world_idea_factunit", before_factunit, after_factunit
            ):
                x_atomunit = atomunit_shop("world_idea_factunit", atom_update())
                x_atomunit.set_required_arg("road", before_ideaunit.get_road())
                x_atomunit.set_required_arg("base", after_factunit.base)
                if before_factunit.pick != after_factunit.pick:
                    x_atomunit.set_optional_arg("pick", after_factunit.pick)
                if before_factunit.open != after_factunit.open:
                    x_atomunit.set_optional_arg("open", after_factunit.open)
                if before_factunit.nigh != after_factunit.nigh:
                    x_atomunit.set_optional_arg("nigh", after_factunit.nigh)
                self.set_atomunit(x_atomunit)

    def add_atomunit_idea_factunit_deletes(
        self, idea_road: RoadUnit, delete_factunit_bases: FactUnit
    ):
        for delete_factunit_base in delete_factunit_bases:
            x_atomunit = atomunit_shop("world_idea_factunit", atom_delete())
            x_atomunit.set_required_arg("road", idea_road)
            x_atomunit.set_required_arg("base", delete_factunit_base)
            self.set_atomunit(x_atomunit)

    def get_ordered_atomunits(self, x_count: int = None) -> dict[int:AtomUnit]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_atomunits():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int:str]:
        return {
            atom_num: atom_obj.get_dict()
            for atom_num, atom_obj in self.get_ordered_atomunits(x_count).items()
        }

    def get_json(self, x_count: int = None) -> str:
        x_dict = self.get_ordered_dict(x_count)
        return get_json_from_dict(x_dict)


def changeunit_shop(atomunits: dict[str:str] = None):
    return ChangeUnit(
        atomunits=get_empty_dict_if_none(atomunits),
        _world_build_validated=False,
    )


def validate_world_build_from_change(x_change: ChangeUnit, x_world: WorldUnit = None):
    if x_world is None:
        x_world = worldunit_shop()

    x_world = x_change.get_edited_world(x_world)

    try:
        x_world.calc_world_metrics()
    except Exception:
        return False

    return True


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_nested_value(
        x_dict=x_dict, x_keylist=x_keylist, if_missing_return_None=True
    )


def create_legible_list(x_change: ChangeUnit, x_world: WorldUnit) -> list[str]:
    atoms_dict = x_change.atomunits
    worldunit_atom = get_leg_obj(atoms_dict, [atom_update(), "worldunit"])

    personunit_insert_dict = get_leg_obj(
        atoms_dict, [atom_insert(), "world_personunit"]
    )
    personunit_update_dict = get_leg_obj(
        atoms_dict, [atom_update(), "world_personunit"]
    )
    personunit_delete_dict = get_leg_obj(
        atoms_dict, [atom_delete(), "world_personunit"]
    )

    beliefunit_insert_dict = get_leg_obj(
        atoms_dict, [atom_insert(), "world_beliefunit"]
    )
    beliefunit_update_dict = get_leg_obj(
        atoms_dict, [atom_update(), "world_beliefunit"]
    )
    beliefunit_delete_dict = get_leg_obj(
        atoms_dict, [atom_delete(), "world_beliefunit"]
    )

    x_list = [atom_insert(), "world_belief_belieflink"]
    belief_belieflink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_belief_belieflink"]
    belief_belieflink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_belief_belieflink"]
    belief_belieflink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_ideaunit"]
    world_ideaunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_ideaunit"]
    world_ideaunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_ideaunit"]
    world_ideaunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_balancelink"]
    world_idea_balancelink_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_balancelink"]
    world_idea_balancelink_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_balancelink"]
    world_idea_balancelink_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_reasonunit"]
    world_idea_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_reasonunit"]
    world_idea_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_reasonunit"]
    world_idea_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_reason_premiseunit"]
    world_idea_reason_premiseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_suffbelief"]
    world_idea_suffbelief_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_suffbelief"]
    world_idea_suffbelief_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_healerhold"]
    world_idea_healerhold_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_healerhold"]
    world_idea_healerhold_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = [atom_insert(), "world_idea_factunit"]
    world_idea_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_update(), "world_idea_factunit"]
    world_idea_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = [atom_delete(), "world_idea_factunit"]
    world_idea_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if worldunit_atom != None:
        add_worldunit_legible_list(leg_list, worldunit_atom, x_world)
    if personunit_insert_dict != None:
        add_world_personunit_insert_to_legible_list(
            leg_list, personunit_insert_dict, x_world
        )
    if personunit_update_dict != None:
        add_world_personunit_update_to_legible_list(
            leg_list, personunit_update_dict, x_world
        )
    if personunit_delete_dict != None:
        add_world_personunit_delete_to_legible_list(
            leg_list, personunit_delete_dict, x_world
        )

    if beliefunit_insert_dict != None:
        add_world_beliefunit_insert_to_legible_list(
            leg_list, beliefunit_insert_dict, x_world
        )
    if beliefunit_update_dict != None:
        add_world_beliefunit_update_to_legible_list(
            leg_list, beliefunit_update_dict, x_world
        )
    if beliefunit_delete_dict != None:
        add_world_beliefunit_delete_to_legible_list(
            leg_list, beliefunit_delete_dict, x_world
        )

    if belief_belieflink_insert_dict != None:
        add_world_belief_belieflink_insert_to_legible_list(
            leg_list, belief_belieflink_insert_dict, x_world
        )
    if belief_belieflink_update_dict != None:
        add_world_belief_belieflink_update_to_legible_list(
            leg_list, belief_belieflink_update_dict, x_world
        )
    if belief_belieflink_delete_dict != None:
        add_world_belief_belieflink_delete_to_legible_list(
            leg_list, belief_belieflink_delete_dict, x_world
        )

    if world_ideaunit_insert_dict != None:
        add_world_ideaunit_insert_to_legible_list(
            leg_list, world_ideaunit_insert_dict, x_world
        )
    if world_ideaunit_update_dict != None:
        add_world_ideaunit_update_to_legible_list(
            leg_list, world_ideaunit_update_dict, x_world
        )
    if world_ideaunit_delete_dict != None:
        add_world_ideaunit_delete_to_legible_list(
            leg_list, world_ideaunit_delete_dict, x_world
        )

    if world_idea_balancelink_insert_dict != None:
        add_world_idea_balancelink_insert_to_legible_list(
            leg_list, world_idea_balancelink_insert_dict, x_world
        )
    if world_idea_balancelink_update_dict != None:
        add_world_idea_balancelink_update_to_legible_list(
            leg_list, world_idea_balancelink_update_dict, x_world
        )
    if world_idea_balancelink_delete_dict != None:
        add_world_idea_balancelink_delete_to_legible_list(
            leg_list, world_idea_balancelink_delete_dict, x_world
        )

    if world_idea_reasonunit_insert_dict != None:
        add_world_idea_reasonunit_insert_to_legible_list(
            leg_list, world_idea_reasonunit_insert_dict, x_world
        )
    if world_idea_reasonunit_update_dict != None:
        add_world_idea_reasonunit_update_to_legible_list(
            leg_list, world_idea_reasonunit_update_dict, x_world
        )
    if world_idea_reasonunit_delete_dict != None:
        add_world_idea_reasonunit_delete_to_legible_list(
            leg_list, world_idea_reasonunit_delete_dict, x_world
        )

    if world_idea_reason_premiseunit_insert_dict != None:
        add_world_reason_premiseunit_insert_to_legible_list(
            leg_list, world_idea_reason_premiseunit_insert_dict, x_world
        )
    if world_idea_reason_premiseunit_update_dict != None:
        add_world_reason_premiseunit_update_to_legible_list(
            leg_list, world_idea_reason_premiseunit_update_dict, x_world
        )
    if world_idea_reason_premiseunit_delete_dict != None:
        add_world_reason_premiseunit_delete_to_legible_list(
            leg_list, world_idea_reason_premiseunit_delete_dict, x_world
        )

    if world_idea_suffbelief_insert_dict != None:
        add_world_idea_suffbelief_insert_to_legible_list(
            leg_list, world_idea_suffbelief_insert_dict, x_world
        )
    if world_idea_suffbelief_delete_dict != None:
        add_world_idea_suffbelief_delete_to_legible_list(
            leg_list, world_idea_suffbelief_delete_dict, x_world
        )

    if world_idea_healerhold_insert_dict != None:
        add_world_idea_healerhold_insert_to_legible_list(
            leg_list, world_idea_healerhold_insert_dict, x_world
        )
    if world_idea_healerhold_delete_dict != None:
        add_world_idea_healerhold_delete_to_legible_list(
            leg_list, world_idea_healerhold_delete_dict, x_world
        )

    if world_idea_factunit_insert_dict != None:
        add_world_idea_factunit_insert_to_legible_list(
            leg_list, world_idea_factunit_insert_dict, x_world
        )
    if world_idea_factunit_update_dict != None:
        add_world_idea_factunit_update_to_legible_list(
            leg_list, world_idea_factunit_update_dict, x_world
        )
    if world_idea_factunit_delete_dict != None:
        add_world_idea_factunit_delete_to_legible_list(
            leg_list, world_idea_factunit_delete_dict, x_world
        )

    return leg_list


def add_worldunit_legible_list(
    legible_list: list[str], x_atom: AtomUnit, x_world: WorldUnit
):
    optional_args = x_atom.optional_args
    _weight_text = "_weight"
    _max_tree_traverse_text = "_max_tree_traverse"
    _meld_strategy_text = "_meld_strategy"
    _monetary_desc_text = "_monetary_desc"
    _person_credor_pool_text = "_person_credor_pool"
    _person_debtor_pool_text = "_person_debtor_pool"

    _max_tree_traverse_value = optional_args.get(_max_tree_traverse_text)
    _meld_strategy_value = optional_args.get(_meld_strategy_text)
    _monetary_desc_value = optional_args.get(_monetary_desc_text)
    _person_credor_pool_value = optional_args.get(_person_credor_pool_text)
    _person_debtor_pool_value = optional_args.get(_person_debtor_pool_text)
    _weight_value = optional_args.get(_weight_text)

    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = f"{x_world._owner_id}'s monetary_desc"

    if _max_tree_traverse_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s maximum number of World output evaluations transited to {_max_tree_traverse_value}"
        )
    if _meld_strategy_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s Meld strategy transited to '{_meld_strategy_value}'"
        )
    if _monetary_desc_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s monetary_desc is now called '{_monetary_desc_value}'"
        )
    if (
        _person_credor_pool_value != None
        and _person_debtor_pool_value != None
        and _person_credor_pool_value == _person_debtor_pool_value
    ):
        legible_list.append(
            f"{x_monetary_desc} total pool is now {_person_credor_pool_value}"
        )
    elif _person_credor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} credor pool is now {_person_credor_pool_value}"
        )
    elif _person_debtor_pool_value != None:
        legible_list.append(
            f"{x_monetary_desc} debtor pool is now {_person_debtor_pool_value}"
        )
    if _weight_value != None:
        legible_list.append(
            f"{x_world._owner_id}'s world weight was transited to {_weight_value}"
        )


def add_world_personunit_insert_to_legible_list(
    legible_list: list[str], personunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for personunit_atom in personunit_dict.values():
        person_id = personunit_atom.get_value("person_id")
        credor_weight_value = personunit_atom.get_value("credor_weight")
        debtor_weight_value = personunit_atom.get_value("debtor_weight")
        x_str = f"{person_id} was added with {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt"
        legible_list.append(x_str)


def add_world_personunit_update_to_legible_list(
    legible_list: list[str], personunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for personunit_atom in personunit_dict.values():
        person_id = personunit_atom.get_value("person_id")
        credor_weight_value = personunit_atom.get_value("credor_weight")
        debtor_weight_value = personunit_atom.get_value("debtor_weight")
        if credor_weight_value != None and debtor_weight_value != None:
            x_str = f"{person_id} now has {credor_weight_value} {x_monetary_desc} cred and {debtor_weight_value} {x_monetary_desc} debt."
        elif credor_weight_value != None and debtor_weight_value is None:
            x_str = f"{person_id} now has {credor_weight_value} {x_monetary_desc} cred."
        elif credor_weight_value is None and debtor_weight_value != None:
            x_str = f"{person_id} now has {debtor_weight_value} {x_monetary_desc} debt."
        legible_list.append(x_str)


def add_world_personunit_delete_to_legible_list(
    legible_list: list[str], personunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for personunit_atom in personunit_dict.values():
        person_id = personunit_atom.get_value("person_id")
        x_str = f"{person_id} was removed from {x_monetary_desc} persons."
        legible_list.append(x_str)


def add_world_beliefunit_insert_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was created"
        x_str += "."
        legible_list.append(x_str)


def add_world_beliefunit_update_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}'"
        x_str += "."
        legible_list.append(x_str)


def add_world_beliefunit_delete_to_legible_list(
    legible_list: list[str], beliefunit_dict: AtomUnit, x_world: WorldUnit
):
    x_monetary_desc = x_world._monetary_desc
    if x_monetary_desc is None:
        x_monetary_desc = "monetary_desc"
    for beliefunit_atom in beliefunit_dict.values():
        belief_id = beliefunit_atom.get_value("belief_id")
        x_str = f"The belief '{belief_id}' was deleted."
        legible_list.append(x_str)


def add_world_belief_belieflink_insert_to_legible_list(
    legible_list: list[str], belief_belieflink_insert_dict: dict, x_world: WorldUnit
):
    for belief_belieflink_dict in belief_belieflink_insert_dict.values():
        for belief_belieflink_atom in belief_belieflink_dict.values():
            belief_id = belief_belieflink_atom.get_value("belief_id")
            person_id = belief_belieflink_atom.get_value("person_id")
            credor_weight_value = belief_belieflink_atom.get_value("credor_weight")
            debtor_weight_value = belief_belieflink_atom.get_value("debtor_weight")
            x_str = f"Belief '{belief_id}' has new member {person_id} with belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_belief_belieflink_update_to_legible_list(
    legible_list: list[str], belief_belieflink_update_dict: dict, x_world: WorldUnit
):
    for belief_belieflink_dict in belief_belieflink_update_dict.values():
        for belief_belieflink_atom in belief_belieflink_dict.values():
            belief_id = belief_belieflink_atom.get_value("belief_id")
            person_id = belief_belieflink_atom.get_value("person_id")
            credor_weight_value = belief_belieflink_atom.get_value("credor_weight")
            debtor_weight_value = belief_belieflink_atom.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {person_id} has new belief_cred={credor_weight_value} and belief_debt={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Belief '{belief_id}' member {person_id} has new belief_cred={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Belief '{belief_id}' member {person_id} has new belief_debt={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_belief_belieflink_delete_to_legible_list(
    legible_list: list[str], belief_belieflink_delete_dict: dict, x_world: WorldUnit
):
    for belief_belieflink_dict in belief_belieflink_delete_dict.values():
        for belief_belieflink_atom in belief_belieflink_dict.values():
            belief_id = belief_belieflink_atom.get_value("belief_id")
            person_id = belief_belieflink_atom.get_value("person_id")
            x_str = f"Belief '{belief_id}' no longer has member {person_id}."
            legible_list.append(x_str)


def add_world_ideaunit_insert_to_legible_list(
    legible_list: list[str], ideaunit_insert_dict: dict, x_world: WorldUnit
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
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _meld_strategy_value = ideaunit_atom.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _weight_value = ideaunit_atom.get_value(_weight_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
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


def add_world_ideaunit_update_to_legible_list(
    legible_list: list[str], ideaunit_update_dict: dict, x_world: WorldUnit
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
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            _addin_value = ideaunit_atom.get_value(_addin_text)
            _begin_value = ideaunit_atom.get_value(_begin_text)
            _close_value = ideaunit_atom.get_value(_close_text)
            _denom_value = ideaunit_atom.get_value(_denom_text)
            _meld_strategy_value = ideaunit_atom.get_value(_meld_strategy_text)
            _numeric_road_value = ideaunit_atom.get_value(_numeric_road_text)
            _numor_value = ideaunit_atom.get_value(_numor_text)
            _problem_bool_value = ideaunit_atom.get_value(_problem_bool_text)
            _range_source_road_value = ideaunit_atom.get_value(_range_source_road_text)
            _reest_value = ideaunit_atom.get_value(_reest_text)
            _weight_value = ideaunit_atom.get_value(_weight_text)
            pledge_value = ideaunit_atom.get_value(pledge_text)
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


def add_world_ideaunit_delete_to_legible_list(
    legible_list: list[str], ideaunit_delete_dict: dict, x_world: WorldUnit
):
    label_text = "label"
    parent_road_text = "parent_road"
    for parent_road_dict in ideaunit_delete_dict.values():
        for ideaunit_atom in parent_road_dict.values():
            label_value = ideaunit_atom.get_value(label_text)
            parent_road_value = ideaunit_atom.get_value(parent_road_text)
            x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
            legible_list.append(x_str)


def add_world_idea_balancelink_insert_to_legible_list(
    legible_list: list[str], idea_balancelink_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_balancelink_insert_dict.values():
        for idea_balancelink_atom in road_dict.values():
            belief_id_value = idea_balancelink_atom.get_value("belief_id")
            road_value = idea_balancelink_atom.get_value("road")
            credor_weight_value = idea_balancelink_atom.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_atom.get_value("debtor_weight")
            x_str = f"Balancelink created for belief {belief_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_idea_balancelink_update_to_legible_list(
    legible_list: list[str], idea_balancelink_update_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_balancelink_update_dict.values():
        for idea_balancelink_atom in road_dict.values():
            belief_id_value = idea_balancelink_atom.get_value("belief_id")
            road_value = idea_balancelink_atom.get_value("road")
            credor_weight_value = idea_balancelink_atom.get_value("credor_weight")
            debtor_weight_value = idea_balancelink_atom.get_value("debtor_weight")
            if credor_weight_value != None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
            elif credor_weight_value != None and debtor_weight_value is None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
            elif credor_weight_value is None and debtor_weight_value != None:
                x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
            legible_list.append(x_str)


def add_world_idea_balancelink_delete_to_legible_list(
    legible_list: list[str], idea_balancelink_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_balancelink_delete_dict.values():
        for idea_balancelink_atom in road_dict.values():
            belief_id_value = idea_balancelink_atom.get_value("belief_id")
            road_value = idea_balancelink_atom.get_value("road")
            x_str = f"Balancelink for belief {belief_id_value}, idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_world_idea_reasonunit_insert_to_legible_list(
    legible_list: list[str], idea_reasonunit_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_reasonunit_insert_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            suff_idea_active_value = idea_reasonunit_atom.get_value("suff_idea_active")
            x_str = (
                f"ReasonUnit created for idea '{road_value}' with base '{base_value}'."
            )
            if suff_idea_active_value != None:
                x_str += f" suff_idea_active={suff_idea_active_value}."
            legible_list.append(x_str)


def add_world_idea_reasonunit_update_to_legible_list(
    legible_list: list[str], idea_reasonunit_update_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_reasonunit_update_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            suff_idea_active_value = idea_reasonunit_atom.get_value("suff_idea_active")
            if suff_idea_active_value != None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' transited with suff_idea_active={suff_idea_active_value}."
            elif suff_idea_active_value is None:
                x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' and no longer checks base active mode."
            legible_list.append(x_str)


def add_world_idea_reasonunit_delete_to_legible_list(
    legible_list: list[str], idea_reasonunit_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_reasonunit_delete_dict.values():
        for idea_reasonunit_atom in road_dict.values():
            road_value = idea_reasonunit_atom.get_value("road")
            base_value = idea_reasonunit_atom.get_value("base")
            x_str = f"ReasonUnit base='{base_value}' for idea '{road_value}' has been deleted."
            legible_list.append(x_str)


def add_world_reason_premiseunit_insert_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_insert_dict: dict,
    x_world: WorldUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_insert_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_text)
                open_value = idea_reason_premiseunit_atom.get_value(open_text)
                x_str = f"PremiseUnit '{need_value}' created for reason '{base_value}' for idea '{road_value}'."
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_world_reason_premiseunit_update_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_update_dict: dict,
    x_world: WorldUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    divisor_text = "divisor"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_reason_premiseunit_update_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                divisor_value = idea_reason_premiseunit_atom.get_value(divisor_text)
                nigh_value = idea_reason_premiseunit_atom.get_value(nigh_text)
                open_value = idea_reason_premiseunit_atom.get_value(open_text)
                x_str = f"PremiseUnit '{need_value}' updated for reason '{base_value}' for idea '{road_value}'."
                if open_value != None:
                    x_str += f" Open={open_value}."
                if nigh_value != None:
                    x_str += f" Nigh={nigh_value}."
                if divisor_value != None:
                    x_str += f" Divisor={divisor_value}."
                legible_list.append(x_str)


def add_world_reason_premiseunit_delete_to_legible_list(
    legible_list: list[str],
    idea_reason_premiseunit_delete_dict: dict,
    x_world: WorldUnit,
):
    road_text = "road"
    base_text = "base"
    need_text = "need"
    for road_dict in idea_reason_premiseunit_delete_dict.values():
        for base_dict in road_dict.values():
            for idea_reason_premiseunit_atom in base_dict.values():
                road_value = idea_reason_premiseunit_atom.get_value(road_text)
                base_value = idea_reason_premiseunit_atom.get_value(base_text)
                need_value = idea_reason_premiseunit_atom.get_value(need_text)
                x_str = f"PremiseUnit '{need_value}' deleted from reason '{base_value}' for idea '{road_value}'."
                legible_list.append(x_str)


def add_world_idea_suffbelief_insert_to_legible_list(
    legible_list: list[str], idea_suffbelief_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_suffbelief_insert_dict.values():
        for idea_suffbelief_atom in road_dict.values():
            belief_id_value = idea_suffbelief_atom.get_value("belief_id")
            road_value = idea_suffbelief_atom.get_value("road")
            x_str = f"Suffbelief '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_suffbelief_delete_to_legible_list(
    legible_list: list[str], idea_suffbelief_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_suffbelief_delete_dict.values():
        for idea_suffbelief_atom in road_dict.values():
            belief_id_value = idea_suffbelief_atom.get_value("belief_id")
            road_value = idea_suffbelief_atom.get_value("road")
            x_str = f"Suffbelief '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_healerhold_insert_to_legible_list(
    legible_list: list[str], idea_healerhold_insert_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_healerhold_insert_dict.values():
        for idea_healerhold_atom in road_dict.values():
            belief_id_value = idea_healerhold_atom.get_value("belief_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' created for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_healerhold_delete_to_legible_list(
    legible_list: list[str], idea_healerhold_delete_dict: dict, x_world: WorldUnit
):
    for road_dict in idea_healerhold_delete_dict.values():
        for idea_healerhold_atom in road_dict.values():
            belief_id_value = idea_healerhold_atom.get_value("belief_id")
            road_value = idea_healerhold_atom.get_value("road")
            x_str = f"Healerhold '{belief_id_value}' deleted for idea '{road_value}'."
            legible_list.append(x_str)


def add_world_idea_factunit_insert_to_legible_list(
    legible_list: list[str], idea_factunit_insert_dict: dict, x_world: WorldUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_insert_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            nigh_value = idea_factunit_atom.get_value(nigh_text)
            open_value = idea_factunit_atom.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' created for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_world_idea_factunit_update_to_legible_list(
    legible_list: list[str], idea_factunit_update_dict: dict, x_world: WorldUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    nigh_text = "nigh"
    open_text = "open"
    for road_dict in idea_factunit_update_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            nigh_value = idea_factunit_atom.get_value(nigh_text)
            open_value = idea_factunit_atom.get_value(open_text)
            x_str = f"FactUnit '{pick_value}' updated for base '{base_value}' for idea '{road_value}'."
            if open_value != None:
                x_str += f" Open={open_value}."
            if nigh_value != None:
                x_str += f" Nigh={nigh_value}."
            legible_list.append(x_str)


def add_world_idea_factunit_delete_to_legible_list(
    legible_list: list[str], idea_factunit_delete_dict: dict, x_world: WorldUnit
):
    road_text = "road"
    base_text = "base"
    pick_text = "pick"
    for road_dict in idea_factunit_delete_dict.values():
        for idea_factunit_atom in road_dict.values():
            road_value = idea_factunit_atom.get_value(road_text)
            base_value = idea_factunit_atom.get_value(base_text)
            pick_value = idea_factunit_atom.get_value(pick_text)
            x_str = f"FactUnit '{pick_value}' deleted from base '{base_value}' for idea '{road_value}'."
            legible_list.append(x_str)
