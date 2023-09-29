import dataclasses
from src.contract.required_idea import RequiredUnit, Road
from src.contract.group import GroupLink, GroupBrand, GroupMetrics


@dataclasses.dataclass
class TreeMetrics:
    node_count: int = None
    level_count: dict[int:int] = None
    required_bases: dict[Road:int] = None
    grouplinks_metrics: dict[GroupBrand:GroupMetrics] = None
    uid_max: int = None
    uid_dict: dict[int:int] = None
    all_idea_uids_are_unique: bool = None
    bond_promise_count: int = None
    an_promise_idea_road: Road = None

    def __init__(self):
        if self.node_count is None:
            self.node_count = 0
        if self.level_count is None:
            self.level_count = {}
        if self.required_bases is None:
            self.required_bases = {}
        self.set_grouplinks_empty_if_null()
        if self.uid_max is None:
            self.uid_max = 0
        self.set_uid_dict_emtpy_if_null()
        self.all_idea_uids_are_unique = True

    def set_grouplinks_empty_if_null(self):
        if self.grouplinks_metrics is None:
            self.grouplinks_metrics = {}

    def evaluate_node(
        self,
        level: int,
        requireds: dict[Road:RequiredUnit],
        grouplinks: dict[GroupBrand:GroupLink],
        uid: int,
        promise: bool,
        idea_road: Road,
    ):
        self.node_count += 1
        self.evaluate_action(promise=promise, idea_road=idea_road)
        self.evaluate_level(level=level)
        self.evaluate_requiredunits(requireds=requireds)
        self.evaluate_grouplinks(grouplinks=grouplinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_action(self, promise: bool, idea_road: Road):
        if self.bond_promise_count is None and promise:
            self.bond_promise_count = 1
        elif self.bond_promise_count != None and promise:
            self.bond_promise_count += 1

        if promise:
            self.an_promise_idea_road = idea_road

    def evaluate_level(self, level):
        if self.level_count.get(level) is None:
            self.level_count[level] = 1
        else:
            self.level_count[level] = self.level_count[level] + 1

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

    def evaluate_grouplinks(self, grouplinks: dict[GroupBrand:GroupLink]):
        if grouplinks != None:
            for grouplink in grouplinks.values():
                self.grouplinks_metrics[grouplink.brand] = grouplink

    def set_uid_dict_emtpy_if_null(self):
        if self.uid_dict is None:
            self.uid_dict = {}

    def evaluate_uid_max(self, uid):
        if uid != None and self.uid_max < uid:
            self.uid_max = uid

        if self.uid_dict.get(uid) is None:
            self.uid_dict[uid] = 1
        else:
            self.uid_dict[uid] += 1
            self.all_idea_uids_are_unique = False
