import dataclasses
from lib.agent.required import RequiredUnit, Road
from lib.agent.brand import BrandLink, BrandName, BrandMetrics


@dataclasses.dataclass
class TreeMetrics:
    nodeCount: int = None
    levelCount: dict[int:int] = None
    required_bases: dict[Road:int] = None
    brandlinks_metrics: dict[BrandName:BrandMetrics] = None
    uid_max: int = None
    uid_dict: dict[int:int] = None
    all_idea_uids_are_unique: bool = None
    bond_promise_count: int = None
    an_promise_idea_road: Road = None

    def __init__(self):
        if self.nodeCount is None:
            self.nodeCount = 0
        if self.levelCount is None:
            self.levelCount = {}
        if self.required_bases is None:
            self.required_bases = {}
        self.set_brandlinks_empty_if_null()
        if self.uid_max is None:
            self.uid_max = 0
        self.set_uid_dict_emtpy_if_null()
        self.all_idea_uids_are_unique = True

    def set_brandlinks_empty_if_null(self):
        if self.brandlinks_metrics is None:
            self.brandlinks_metrics = {}

    def evaluate_node(
        self,
        level: int,
        requireds: dict[Road:RequiredUnit],
        brandlinks: dict[BrandName:BrandLink],
        uid: int,
        promise: bool,
        idea_road: Road,
    ):
        self.nodeCount += 1
        self.evaluate_action(promise=promise, idea_road=idea_road)
        self.evaluate_level(level=level)
        self.evaluate_requiredunits(requireds=requireds)
        self.evaluate_brandlinks(brandlinks=brandlinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_action(self, promise: bool, idea_road: Road):
        if self.bond_promise_count is None and promise:
            self.bond_promise_count = 1
        elif self.bond_promise_count != None and promise:
            self.bond_promise_count += 1

        if promise:
            self.an_promise_idea_road = idea_road

    def evaluate_level(self, level):
        if self.levelCount.get(level) is None:
            self.levelCount[level] = 1
        else:
            self.levelCount[level] = self.levelCount[level] + 1

    def evaluate_requiredunits(self, requireds: dict[Road:RequiredUnit]):
        if requireds is None:
            requireds = {}
        for required in requireds.values():
            if self.required_bases.get(required.base) is None:
                self.required_bases[required.base] = 1
            else:
                self.required_bases[required.base] = (
                    self.required_bases[required.base] + 1
                )

    def evaluate_brandlinks(self, brandlinks: dict[BrandName:BrandLink]):
        if brandlinks != None:
            for brandlink in brandlinks.values():
                self.brandlinks_metrics[brandlink.name] = brandlink

    def set_uid_dict_emtpy_if_null(self):
        if self.uid_dict is None:
            self.uid_dict = {}

    def evaluate_uid_max(self, uid):
        try:
            if self.uid_max < uid:
                self.uid_max = uid
        except:
            pass

        if self.uid_dict.get(uid) is None:
            self.uid_dict[uid] = 1
        else:
            self.uid_dict[uid] += 1
            self.all_idea_uids_are_unique = False
