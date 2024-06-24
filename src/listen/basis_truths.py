from src._road.road import PersonID
from src._truth.truth import TruthUnit, truthunit_shop


def _is_empty_truth(x_truth: TruthUnit) -> bool:
    empty_truth = create_empty_truth(x_truth)
    return x_truth.get_dict() == empty_truth.get_dict()


def create_empty_truth(ref_truth: TruthUnit, x_owner_id: PersonID = None) -> TruthUnit:
    if x_owner_id is None:
        x_owner_id = ref_truth._owner_id
    x_road_delimiter = ref_truth._road_delimiter
    x_pixel = ref_truth._pixel
    x_penny = ref_truth._penny
    return truthunit_shop(
        x_owner_id, ref_truth._real_id, x_road_delimiter, x_pixel, x_penny
    )


def create_listen_basis(x_role: TruthUnit) -> TruthUnit:
    x_listen = create_empty_truth(x_role, x_owner_id=x_role._owner_id)
    x_listen._others = x_role._others
    x_listen._beliefs = x_role._beliefs
    x_listen.set_monetary_desc(x_role._monetary_desc)
    x_listen.set_max_tree_traverse(x_role._max_tree_traverse)
    if x_role._other_credor_pool != None:
        x_listen.set_other_credor_pool(x_role._other_credor_pool)
    if x_role._other_debtor_pool != None:
        x_listen.set_other_debtor_pool(x_role._other_debtor_pool)
    for x_otherunit in x_listen._others.values():
        x_otherunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_live_truth(same: TruthUnit) -> TruthUnit:
    default_live_truth = create_listen_basis(same)
    default_live_truth._last_atom_id = same._last_atom_id
    default_live_truth._other_credor_pool = None
    default_live_truth._other_debtor_pool = None
    return default_live_truth
