import dataclasses
from src.agent.required import RequiredUnit, Road
from src.agent.group import GroupLink, GroupName, GroupMetrics


@dataclasses.dataclass
class TreeMetrics:
    nodeCount: int = None
    levelCount: dict[int:int] = None
    required_bases: dict[Road:int] = None
    grouplinks_metrics: dict[GroupName:GroupMetrics] = None
    uid_max: int = None
    uid_dict: dict[int:int] = None
    all_tool_uids_are_unique: bool = None
    bond_promise_count: int = None
    an_promise_tool_road: Road = None

    def __init__(self):
        if self.nodeCount is None:
            self.nodeCount = 0
        if self.levelCount is None:
            self.levelCount = {}
        if self.required_bases is None:
            self.required_bases = {}
        self.set_grouplinks_empty_if_null()
        if self.uid_max is None:
            self.uid_max = 0
        self.set_uid_dict_emtpy_if_null()
        self.all_tool_uids_are_unique = True

    def set_grouplinks_empty_if_null(self):
        if self.grouplinks_metrics is None:
            self.grouplinks_metrics = {}

    def evaluate_node(
        self,
        level: int,
        requireds: dict[Road:RequiredUnit],
        grouplinks: dict[GroupName:GroupLink],
        uid: int,
        promise: bool,
        tool_road: Road,
    ):
        self.nodeCount += 1
        self.evaluate_action(promise=promise, tool_road=tool_road)
        self.evaluate_level(level=level)
        self.evaluate_requiredunits(requireds=requireds)
        self.evaluate_grouplinks(grouplinks=grouplinks)
        self.evaluate_uid_max(uid=uid)

    def evaluate_action(self, promise: bool, tool_road: Road):
        if self.bond_promise_count is None and promise:
            self.bond_promise_count = 1
        elif self.bond_promise_count != None and promise:
            self.bond_promise_count += 1

        if promise:
            self.an_promise_tool_road = tool_road

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

    def evaluate_grouplinks(self, grouplinks: dict[GroupName:GroupLink]):
        if grouplinks != None:
            for grouplink in grouplinks.values():
                self.grouplinks_metrics[grouplink.name] = grouplink

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
            self.all_tool_uids_are_unique = False
