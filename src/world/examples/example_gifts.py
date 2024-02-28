from src._road.road import PersonRoad, create_road_from_nodes as roadnodes
from src.world.gift import giftunit_shop, GiftUnit


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop("Yao", "Sue")
