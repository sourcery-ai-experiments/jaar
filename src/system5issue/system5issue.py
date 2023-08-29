from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


@dataclass
class System5Issue:
    issue_1_desc: str = None
    issue_2_desc: str = None
    issue_3_desc: str = None
    issue_4_desc: str = None
    issue_5_desc: str = None
    issue_1_weight: str = None
    issue_2_weight: str = None
    issue_3_weight: str = None
    issue_4_weight: str = None
    issue_5_weight: str = None
    adovacate_1_desc: str = None
    adovacate_2_desc: str = None
    adovacate_3_desc: str = None
    adovacate_4_desc: str = None
    adovacate_5_desc: str = None
    adovacate_1_weight: str = None
    adovacate_2_weight: str = None
    adovacate_3_weight: str = None
    adovacate_4_weight: str = None
    adovacate_5_weight: str = None

    def test(self):
        pass
