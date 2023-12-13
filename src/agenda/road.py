class InvalidRoadException(Exception):
    pass


class RaodNode(str):
    def is_node(self, separator: str = None) -> bool:
        return self.find(get_node_separator(separator)) == -1


class Road(str):  # Created to help track the concept
    pass


def get_node_separator(separator: str) -> str:
    return separator if separator != None else ","


def change_road(current_road: Road, old_road: Road, new_road: Road) -> Road:
    if current_road is None:
        return current_road
    else:
        return current_road.replace(old_road, new_road, 1)


def is_sub_road(ref_road: Road, sub_road: Road) -> bool:
    if ref_road is None:
        ref_road = ""
    return ref_road.find(sub_road) == 0


def is_heir_road(src: Road, heir: Road, separator: str = None) -> bool:
    return src == heir or heir.find(f"{src}{get_node_separator(separator)}") == 0


def find_replace_road_key_dict(dict_x: dict, old_road: Road, new_road: Road) -> dict:
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        # rint(f"{x_key=} {old_road=} {new_road=}")
        if is_sub_road(ref_road=x_key, sub_road=old_road):
            #  or (
            #     key_is_last_node
            #     and is_sub_road(
            #         ref_road=Road(f"{x_obj._pad},{x_obj._label}"), sub_road=old_road
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


def get_all_road_nodes(road: Road, separator: str = None) -> list[RaodNode]:
    return road.split(get_node_separator(separator))


def get_terminus_node_from_road(road: Road) -> RaodNode:
    return get_all_road_nodes(road=road)[-1]


def get_pad_from_road(road: Road) -> Road:  # road without terminus node
    return get_road_from_nodes(get_all_road_nodes(road=road)[:-1])


def get_road_without_root_node(
    road: Road, separator: str = None
) -> Road:  # road without terminus node
    if road[:1] == get_node_separator(separator):
        raise InvalidRoadException(
            f"Cannot get_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = get_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f"{get_node_separator(separator)}{road_without_root_node}"


def road_validate(road: Road) -> Road:
    if road == "" or road is None:
        return Road("")
    x_root = get_all_road_nodes(road)[0]
    return (
        change_road(
            current_road=road,
            old_road=x_root,
            new_road=get_default_culture_root_label(),
        )
        if x_root != get_default_culture_root_label()
        else road
    )


def get_ancestor_roads(road: Road) -> list[Road:None]:
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


def get_forefather_roads(road: Road) -> dict[Road]:
    ancestor_roads = get_ancestor_roads(road=road)
    popped_road = ancestor_roads.pop(0)
    if popped_road != road:
        raise ForeFatherException(
            f"Incorrect road {popped_road} removed from forefather_roads"
        )
    return {a_road: None for a_road in ancestor_roads}


def get_default_culture_root_label() -> str:
    return "A"


def get_road_from_nodes(nodes: list[RaodNode], separator: str = None) -> Road:
    return get_node_separator(separator).join(nodes)


def get_road_from_road_and_node(
    pad: Road, terminus_node: RaodNode, separator: str = None
) -> Road:
    if terminus_node is None:
        return Road(pad)
    else:
        return Road(
            terminus_node
            if pad in {"", None}
            else f"{pad}{get_node_separator(separator)}{terminus_node}"
        )


def get_road(
    road_begin: Road = None,
    terminus_node: RaodNode = None,
    road_nodes: list[RaodNode] = None,
    separator: str = None,
) -> Road:
    x_road = ""
    if road_begin != None and road_nodes is None:
        x_road = road_begin
    if road_begin != None and road_nodes != None:
        x_road = get_road(
            road_begin, get_road_from_nodes(road_nodes, separator=separator)
        )
    if road_begin is None and road_nodes != None:
        x_road = get_road_from_nodes(road_nodes, separator=separator)
    if terminus_node != None:
        x_road = get_road_from_road_and_node(x_road, terminus_node, separator=separator)
    return x_road


def get_diff_road(x_road: Road, sub_road: Road, separator: str = None):
    sub_road = f"{sub_road}{get_node_separator(separator)}"
    return x_road.replace(sub_road, "")


class InvalidSepartorReplaceException(Exception):
    pass


def replace_road_node_separtor(road: Road, old_separator: str, new_separator: str):
    if road.find(new_separator) >= 0:
        raise InvalidSepartorReplaceException(
            f"Cannot replace_road_node_separtor '{old_separator}' with '{new_separator}' because the new one already exists in road '{road}'."
        )

    return road.replace(old_separator, new_separator)
