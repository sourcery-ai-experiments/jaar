from dataclasses import dataclass
from src.agenda.y_func import get_empty_dict_if_none


class InvalidRoadUnitException(Exception):
    pass


class RoadNode(str):
    def is_node(self, delimiter: str = None) -> bool:
        return self.find(default_road_delimiter_if_none(delimiter)) == -1
        # return is_string_in_road(string=delimiter, road=self.__str__())


class RoadUnit(str):  # Created to help track the concept
    pass


def default_road_delimiter_if_none(delimiter: str = None) -> str:
    return delimiter if delimiter != None else ","


def change_road(
    current_road: RoadUnit, old_road: RoadUnit, new_road: RoadUnit
) -> RoadUnit:
    if current_road is None:
        return current_road
    elif is_sub_road(current_road, old_road):
        return current_road.replace(old_road, new_road, 1)
    else:
        return current_road


def is_sub_road(ref_road: RoadUnit, sub_road: RoadUnit) -> bool:
    if ref_road is None:
        ref_road = ""
    return ref_road.find(sub_road) == 0


def is_heir_road(src: RoadUnit, heir: RoadUnit, delimiter: str = None) -> bool:
    return (
        src == heir
        or heir.find(f"{src}{default_road_delimiter_if_none(delimiter)}") == 0
    )


def find_replace_road_key_dict(
    dict_x: dict, old_road: RoadUnit, new_road: RoadUnit
) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        if old_road != new_road and is_sub_road(ref_road=x_key, sub_road=old_road):
            x_obj.find_replace_road(old_road=old_road, new_road=new_road)
            objs_to_add.append(x_obj)
            keys_to_delete.append(x_key)

    for x_obj in objs_to_add:
        dict_x[x_obj.get_key_road()] = x_obj

    for x_key in keys_to_delete:
        dict_x.pop(x_key)

    return dict_x


def get_all_road_nodes(road: RoadUnit, delimiter: str = None) -> list[RoadNode]:
    return road.split(default_road_delimiter_if_none(delimiter))


def get_terminus_node_from_road(road: RoadUnit, delimiter: str = None) -> RoadNode:
    return get_all_road_nodes(road=road, delimiter=delimiter)[-1]


def get_pad_from_road(road: RoadUnit) -> RoadUnit:  # road without terminus node
    return create_road_from_nodes(get_all_road_nodes(road=road)[:-1])


def create_road_without_root_node(
    road: RoadUnit, delimiter: str = None
) -> RoadUnit:  # road without terminus nodef
    if road[:1] == default_road_delimiter_if_none(delimiter):
        raise InvalidRoadUnitException(
            f"Cannot create_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = create_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f"{default_road_delimiter_if_none(delimiter)}{road_without_root_node}"


def get_root_node_from_road(road: RoadUnit, delimiter: str = None) -> RoadNode:
    return get_all_road_nodes(road=road, delimiter=delimiter)[0]


def road_validate(road: RoadUnit, delimiter: str, root_node: RoadNode) -> RoadUnit:
    if road == "" or road is None:
        return RoadUnit("")
    x_root = get_root_node_from_road(road, delimiter)
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
            temp_road = create_road(temp_road, nodes.pop(0))
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


def create_road_from_nodes(nodes: list[RoadNode], delimiter: str = None) -> RoadUnit:
    return default_road_delimiter_if_none(delimiter).join(nodes)


def create_road(
    pad: RoadUnit, terminus_node: RoadNode = None, delimiter: str = None
) -> RoadUnit:
    if terminus_node is None:
        return RoadUnit(pad)
    else:
        return RoadUnit(
            terminus_node
            if pad in {"", None}
            else f"{pad}{default_road_delimiter_if_none(delimiter)}{terminus_node}"
        )


def get_diff_road(x_road: RoadUnit, sub_road: RoadUnit, delimiter: str = None):
    sub_road = f"{sub_road}{default_road_delimiter_if_none(delimiter)}"
    return x_road.replace(sub_road, "")


class InvaliddelimiterReplaceException(Exception):
    pass


def is_string_in_road(string: str, road: RoadUnit) -> bool:
    return road.find(string) >= 0


def replace_road_delimiter(road: RoadUnit, old_delimiter: str, new_delimiter: str):
    if is_string_in_road(string=new_delimiter, road=road):
        raise InvaliddelimiterReplaceException(
            f"Cannot replace_road_delimiter '{old_delimiter}' with '{new_delimiter}' because the new one already exists in road '{road}'."
        )
    return road.replace(old_delimiter, new_delimiter)
