from src._prime.road import create_road, create_economyaddress
from src.world.deal import dealunit_shop, DealUnit, dueunit_shop
from src.world.examples.example_topics import get_no_topiclinks_dueunit


def get_no_topiclinks_dealunit() -> DealUnit:
    yao_sue_dealunit = dealunit_shop("Yao", "Sue")
    yao_sue_dealunit.set_dueunit(dueunit_shop(author_weight=12, reader_weight=7))
    yao_sue_dealunit.set_dueunit(dueunit_shop(author_weight=28, reader_weight=28))
    return yao_sue_dealunit
