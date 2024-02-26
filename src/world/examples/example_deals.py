from src._road.road import PersonRoad, create_road_from_nodes as roadnodes
from src.world.deal import dealunit_shop, DealUnit


def yao_sue_dealunit() -> DealUnit:
    return dealunit_shop("Yao", "Sue")
