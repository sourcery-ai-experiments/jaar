from src._road.road import OwnerID
from src._world.world import WorldUnit, worldunit_shop


def _is_empty_world(x_world: WorldUnit) -> bool:
    empty_world = create_empty_world(x_world)
    return x_world.get_dict() == empty_world.get_dict()


def create_empty_world(ref_world: WorldUnit, x_owner_id: OwnerID = None) -> WorldUnit:
    if x_owner_id is None:
        x_owner_id = ref_world._owner_id
    x_road_delimiter = ref_world._road_delimiter
    x_pixel = ref_world._pixel
    x_penny = ref_world._penny
    return worldunit_shop(
        x_owner_id, ref_world._real_id, x_road_delimiter, x_pixel, x_penny
    )


def create_listen_basis(x_role: WorldUnit) -> WorldUnit:
    x_listen = create_empty_world(x_role, x_owner_id=x_role._owner_id)
    x_listen._chars = x_role._chars
    x_listen._beliefs = x_role._beliefs
    x_listen.set_monetary_desc(x_role._monetary_desc)
    x_listen.set_max_tree_traverse(x_role._max_tree_traverse)
    if x_role._char_credor_pool != None:
        x_listen.set_char_credor_pool(x_role._char_credor_pool)
    if x_role._char_debtor_pool != None:
        x_listen.set_char_debtor_pool(x_role._char_debtor_pool)
    for x_charunit in x_listen._chars.values():
        x_charunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_live_world(same: WorldUnit) -> WorldUnit:
    default_live_world = create_listen_basis(same)
    default_live_world._last_gift_id = same._last_gift_id
    default_live_world._char_credor_pool = None
    default_live_world._char_debtor_pool = None
    return default_live_world
