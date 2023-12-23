from dataclasses import dataclass


class InvalidRoadUnitException(Exception):
    pass


class RoadNode(str):
    def is_node(self, delimiter: str = None) -> bool:
        return self.find(get_node_delimiter(delimiter)) == -1
        # return is_string_in_road(string=delimiter, road=self.__str__())


class RoadUnit(str):  # Created to help track the concept
    pass


def get_node_delimiter(delimiter: str = None) -> str:
    return delimiter if delimiter != None else ","


def change_road(
    current_road: RoadUnit, old_road: RoadUnit, new_road: RoadUnit
) -> RoadUnit:
    if current_road is None:
        return current_road
    else:
        return current_road.replace(old_road, new_road, 1)


def is_sub_road(ref_road: RoadUnit, sub_road: RoadUnit) -> bool:
    if ref_road is None:
        ref_road = ""
    return ref_road.find(sub_road) == 0


def is_heir_road(src: RoadUnit, heir: RoadUnit, delimiter: str = None) -> bool:
    return src == heir or heir.find(f"{src}{get_node_delimiter(delimiter)}") == 0


def find_replace_road_key_dict(
    dict_x: dict, old_road: RoadUnit, new_road: RoadUnit
) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        # rint(f"{x_key=} {old_road=} {new_road=}")
        if is_sub_road(ref_road=x_key, sub_road=old_road):
            #  or (
            #     key_is_last_node
            #     and is_sub_road(
            #         ref_road=RoadUnit(f"{x_obj._pad},{x_obj._label}"), sub_road=old_road
            #     )
            # changed_road = change_road(
            #     current_road=x_key, old_road=old_road, new_road=new_road
            # )
            x_obj.find_replace_road(old_road=old_road, new_road=new_road)
            objs_to_add.append(x_obj)

            keys_to_delete.append(x_key)
            # rint(f"{changed_road=} {keys_to_delete=} {len(objs_to_add)=}")

    for x_obj in objs_to_add:
        dict_x[x_obj.get_key_road()] = x_obj

    for x_key in keys_to_delete:
        dict_x.pop(x_key)

    return dict_x


def get_all_road_nodes(road: RoadUnit, delimiter: str = None) -> list[RoadNode]:
    return road.split(get_node_delimiter(delimiter))


def get_terminus_node_from_road(road: RoadUnit) -> RoadNode:
    return get_all_road_nodes(road=road)[-1]


def get_pad_from_road(road: RoadUnit) -> RoadUnit:  # road without terminus node
    return get_road_from_nodes(get_all_road_nodes(road=road)[:-1])


def get_road_without_root_node(
    road: RoadUnit, delimiter: str = None
) -> RoadUnit:  # road without terminus node
    if road[:1] == get_node_delimiter(delimiter):
        raise InvalidRoadUnitException(
            f"Cannot get_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = get_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f"{get_node_delimiter(delimiter)}{road_without_root_node}"


def road_validate(road: RoadUnit, delimiter: str, root_node: RoadNode) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_all_road_nodes(road, delimiter)[0]
    return (
        change_road(
            current_road=road,
            old_road=x_root,
            new_road=root_node,
        )
        if x_root != root_node
        else road
    )


def get_ancestor_roads(road: RoadUnit) -> list[RoadUnit:None]:
    if road is None:
        return []
    nodes = get_all_road_nodes(road)
    temp_road = nodes.pop(0)

    temp_roads = [temp_road]
    if nodes != []:
        while nodes != []:
            temp_road = get_road(temp_road, nodes.pop(0))
            temp_roads.append(temp_road)

    x_roads = []
    while temp_roads != []:
        x_roads.append(temp_roads.pop(len(temp_roads) - 1))
    return x_roads


class ForeFatherException(Exception):
    pass


def get_forefather_roads(road: RoadUnit) -> dict[RoadUnit]:
    ancestor_roads = get_ancestor_roads(road=road)
    popped_road = ancestor_roads.pop(0)
    if popped_road != road:
        raise ForeFatherException(
            f"Incorrect road {popped_road} removed from forefather_roads"
        )
    return {a_road: None for a_road in ancestor_roads}


def get_default_economy_root_label() -> str:
    return "A"


def get_road_from_nodes(nodes: list[RoadNode], delimiter: str = None) -> RoadUnit:
    return get_node_delimiter(delimiter).join(nodes)


def get_road_from_road_and_node(
    pad: RoadUnit, terminus_node: RoadNode, delimiter: str = None
) -> RoadUnit:
    if terminus_node is None:
        return RoadUnit(pad)
    else:
        return RoadUnit(
            terminus_node
            if pad in {"", None}
            else f"{pad}{get_node_delimiter(delimiter)}{terminus_node}"
        )


def get_road(
    road_begin: RoadUnit = None,
    terminus_node: RoadNode = None,
    road_nodes: list[RoadNode] = None,
    delimiter: str = None,
) -> RoadUnit:
    x_road = ""
    if road_begin != None and road_nodes in (None, []):
        x_road = road_begin
    if road_begin != None and road_nodes not in (None, []):
        x_road = get_road(
            road_begin=road_begin,
            terminus_node=get_road_from_nodes(road_nodes, delimiter),
            delimiter=delimiter,
        )
    if road_begin is None and road_nodes not in (None, []):
        x_road = get_road_from_nodes(road_nodes, delimiter=delimiter)
    if terminus_node != None:
        x_road = get_road_from_road_and_node(x_road, terminus_node, delimiter=delimiter)
    return x_road


def get_diff_road(x_road: RoadUnit, sub_road: RoadUnit, delimiter: str = None):
    sub_road = f"{sub_road}{get_node_delimiter(delimiter)}"
    return x_road.replace(sub_road, "")


class InvaliddelimiterReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadUnit) -> bool:
    return road.find(string) >= 0


def replace_road_node_delimiter(road: RoadUnit, old_delimiter: str, new_delimiter: str):
    if is_string_in_road(string=new_delimiter, road=road):
        raise InvaliddelimiterReplaceException(
            f"Cannot replace_road_node_delimiter '{old_delimiter}' with '{new_delimiter}' because the new one already exists in road '{road}'."
        )
    return road.replace(old_delimiter, new_delimiter)


class NoneZeroAffectException(Exception):
    pass


class ForkSubRoadUnitException(Exception):
    pass


@dataclass
class ForkUnit:
    base: RoadUnit = None
    descendents: dict[RoadUnit:float] = None
    delimiter: str = None

    def is_dialectic(self):
        return (
            len(self.get_good_descendents()) > 0 and len(self.get_bad_descendents()) > 0
        )

    def set_descendents_empty_if_none(self):
        if self.descendents is None:
            self.descendents = {}

    def set_descendent(self, descendent: RoadUnit, affect: float):
        if affect in {None, 0}:
            raise NoneZeroAffectException(
                f"set_descendent affect parameter {affect} must be Non-zero number"
            )
        if is_sub_road(descendent, self.base) == False:
            raise ForkSubRoadUnitException(
                f"ForkUnit cannot set descendent '{descendent}' because base road is '{self.base}'."
            )
        self.descendents[descendent] = affect

    def del_descendent(self, descendent: RoadUnit):
        self.descendents.pop(descendent)

    def get_good_descendents(self) -> dict[RoadUnit:int]:
        return {
            x_road: x_affect
            for x_road, x_affect in self.get_descendents().items()
            if x_affect > 0
        }

    def get_bad_descendents(self) -> dict[RoadUnit:int]:
        return {
            x_road: x_affect
            for x_road, x_affect in self.get_descendents().items()
            if x_affect < 0
        }

    def get_descendents(self) -> dict[RoadUnit:int]:
        return self.descendents

    def get_all_roads(self) -> dict[RoadUnit:int]:
        x_dict = dict(self.get_descendents().items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_good(self):
        return list(self.get_good_descendents())[0]

    def get_1_bad(self):
        return list(self.get_bad_descendents())[0]


def forkunit_shop(
    base: RoadUnit, descendents: dict[RoadUnit:float] = None, delimiter: str = None
):
    delimiter = get_node_delimiter(delimiter)
    x_forkunit = ForkUnit(base=base, descendents=descendents, delimiter=delimiter)
    x_forkunit.set_descendents_empty_if_none()
    return x_forkunit


def create_forkunit(
    base: RoadUnit, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_forkunit = forkunit_shop(base=base)
    x_forkunit.set_descendent(get_road(base, good, delimiter=delimiter), 1)
    x_forkunit.set_descendent(get_road(base, bad, delimiter=delimiter), -1)
    if x_forkunit.is_dialectic():
        return x_forkunit
