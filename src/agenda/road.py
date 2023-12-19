from dataclasses import dataclass


class InvalidRoadPathException(Exception):
    pass


class RoadNode(str):
    def is_node(self, delimiter: str = None) -> bool:
        return self.find(get_node_delimiter(delimiter)) == -1
        # return is_string_in_road(string=delimiter, road=self.__str__())


class RoadPath(str):  # Created to help track the concept
    pass


def get_node_delimiter(delimiter: str = None) -> str:
    return delimiter if delimiter != None else ","


def change_road(
    current_road: RoadPath, old_road: RoadPath, new_road: RoadPath
) -> RoadPath:
    if current_road is None:
        return current_road
    else:
        return current_road.replace(old_road, new_road, 1)


def is_sub_road(ref_road: RoadPath, sub_road: RoadPath) -> bool:
    if ref_road is None:
        ref_road = ""
    return ref_road.find(sub_road) == 0


def is_heir_road(src: RoadPath, heir: RoadPath, delimiter: str = None) -> bool:
    return src == heir or heir.find(f"{src}{get_node_delimiter(delimiter)}") == 0


def find_replace_road_key_dict(
    dict_x: dict, old_road: RoadPath, new_road: RoadPath
) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        # rint(f"{x_key=} {old_road=} {new_road=}")
        if is_sub_road(ref_road=x_key, sub_road=old_road):
            #  or (
            #     key_is_last_node
            #     and is_sub_road(
            #         ref_road=RoadPath(f"{x_obj._pad},{x_obj._label}"), sub_road=old_road
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


def get_all_road_nodes(road: RoadPath, delimiter: str = None) -> list[RoadNode]:
    return road.split(get_node_delimiter(delimiter))


def get_terminus_node_from_road(road: RoadPath) -> RoadNode:
    return get_all_road_nodes(road=road)[-1]


def get_pad_from_road(road: RoadPath) -> RoadPath:  # road without terminus node
    return get_road_from_nodes(get_all_road_nodes(road=road)[:-1])


def get_road_without_root_node(
    road: RoadPath, delimiter: str = None
) -> RoadPath:  # road without terminus node
    if road[:1] == get_node_delimiter(delimiter):
        raise InvalidRoadPathException(
            f"Cannot get_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = get_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f"{get_node_delimiter(delimiter)}{road_without_root_node}"


def road_validate(road: RoadPath, delimiter: str, root_node: RoadNode) -> RoadPath:
    if road == "" or road is None:
        return RoadPath("")
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


def get_ancestor_roads(road: RoadPath) -> list[RoadPath:None]:
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


def get_forefather_roads(road: RoadPath) -> dict[RoadPath]:
    ancestor_roads = get_ancestor_roads(road=road)
    popped_road = ancestor_roads.pop(0)
    if popped_road != road:
        raise ForeFatherException(
            f"Incorrect road {popped_road} removed from forefather_roads"
        )
    return {a_road: None for a_road in ancestor_roads}


def get_default_culture_root_label() -> str:
    return "A"


def get_road_from_nodes(nodes: list[RoadNode], delimiter: str = None) -> RoadPath:
    return get_node_delimiter(delimiter).join(nodes)


def get_road_from_road_and_node(
    pad: RoadPath, terminus_node: RoadNode, delimiter: str = None
) -> RoadPath:
    if terminus_node is None:
        return RoadPath(pad)
    else:
        return RoadPath(
            terminus_node
            if pad in {"", None}
            else f"{pad}{get_node_delimiter(delimiter)}{terminus_node}"
        )


def get_road(
    road_begin: RoadPath = None,
    terminus_node: RoadNode = None,
    road_nodes: list[RoadNode] = None,
    delimiter: str = None,
) -> RoadPath:
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


def get_diff_road(x_road: RoadPath, sub_road: RoadPath, delimiter: str = None):
    sub_road = f"{sub_road}{get_node_delimiter(delimiter)}"
    return x_road.replace(sub_road, "")


class InvaliddelimiterReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadPath) -> bool:
    return road.find(string) >= 0


def replace_road_node_delimiter(road: RoadPath, old_delimiter: str, new_delimiter: str):
    if is_string_in_road(string=new_delimiter, road=road):
        raise InvaliddelimiterReplaceException(
            f"Cannot replace_road_node_delimiter '{old_delimiter}' with '{new_delimiter}' because the new one already exists in road '{road}'."
        )
    return road.replace(old_delimiter, new_delimiter)


class NoneZeroSwayException(Exception):
    pass


class ForkSubRoadPathException(Exception):
    pass


@dataclass
class ForkUnit:
    base: RoadPath = None
    descendents: dict[RoadPath:float] = None
    delimiter: str = None

    def set_descendents_empty_if_none(self):
        if self.descendents is None:
            self.descendents = {}

    def set_descendent(self, descendent: RoadNode, sway: float):
        if sway in {None, 0}:
            raise NoneZeroSwayException(
                f"set_descendent sway parameter {sway} must be Non-zero number"
            )
        if is_sub_road(descendent, self.base) == False:
            raise ForkSubRoadPathException(
                f"ForkUnit cannot set descendent '{descendent}' because base road is '{self.base}'."
            )
        self.descendents[descendent] = sway

    def get_good_descendents(self):
        return {
            x_road: x_sway for x_road, x_sway in self.descendents.items() if x_sway > 0
        }

    def get_bad_descendents(self):
        return {
            x_road: x_sway for x_road, x_sway in self.descendents.items() if x_sway < 0
        }

    def get_1_good(self):
        return list(self.get_good_descendents())[0]

    def get_1_bad(self):
        return list(self.get_bad_descendents())[0]


def forkunit_shop(
    base: RoadPath, descendents: dict[RoadPath:float] = None, delimiter: str = None
):
    delimiter = get_node_delimiter(delimiter)
    x_forkunit = ForkUnit(base=base, descendents=descendents, delimiter=delimiter)
    x_forkunit.set_descendents_empty_if_none()
    return x_forkunit


def create_forkunit(
    base: RoadPath, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_forkunit = forkunit_shop(base=base)
    x_forkunit.set_descendent(get_road(base, good, delimiter=delimiter), 1)
    x_forkunit.set_descendent(get_road(base, bad, delimiter=delimiter), -1)
    return x_forkunit
