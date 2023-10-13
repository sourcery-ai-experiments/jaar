class InvalidRoadException(Exception):
    pass


class Road(str):
    pass


def change_road(current_road: Road, old_road: Road, new_road: Road):
    if current_road is None:
        return current_road
    else:
        return current_road.replace(old_road, new_road, 1)


def is_sub_road(ref_road: Road, sub_road: Road):
    if ref_road is None:
        ref_road = ""
    return ref_road.find(sub_road) == 0


def find_replace_road_key_dict(dict_x: dict, old_road: Road, new_road: Road):
    keys_to_delete = []
    objs_to_add = []
    for x_key, x_obj in dict_x.items():
        # rint(f"{x_key=} {old_road=} {new_road=}")
        if is_sub_road(ref_road=x_key, sub_road=old_road):
            #  or (
            #     key_is_last_node
            #     and is_sub_road(
            #         ref_road=Road(f"{x_obj._walk},{x_obj._label}"), sub_road=old_road
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


def get_all_road_nodes(road: Road):
    return road.split(",")


def get_terminus_node_from_road(road: Road):
    return get_all_road_nodes(road=road)[-1]


def get_walk_from_road(road: Road):  # road without terminus node
    return get_road_from_nodes(get_all_road_nodes(road=road)[:-1])


def get_road_without_root_node(road: Road):  # road without terminus node
    if road[:1] == ",":
        raise InvalidRoadException(
            f"Cannot get_road_without_root_node of '{road}' because it has no root node."
        )
    road_without_root_node = get_road_from_nodes(get_all_road_nodes(road=road)[1:])
    return f",{road_without_root_node}"


def road_validate(road: Road) -> Road:
    if road == "" or road is None:
        return Road("")
    x_root = get_all_road_nodes(road)[0]
    return (
        change_road(
            current_road=road,
            old_road=x_root,
            new_road=get_default_goal_root_label(),
        )
        if x_root != get_default_goal_root_label()
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
            temp_road = f"{temp_road},{nodes.pop(0)}"
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


def get_default_goal_root_label() -> str:
    return "A"


def get_road_from_nodes(nodes: list) -> Road:
    return ",".join(nodes)
