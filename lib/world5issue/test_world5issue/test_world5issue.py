from lib.world5issue.world5issue import World5Issue


def test_World5Issue_exists():
    new_obj = World5Issue()
    assert new_obj
    assert new_obj.issue_1_desc is None
    assert new_obj.issue_2_desc is None
    assert new_obj.issue_3_desc is None
    assert new_obj.issue_4_desc is None
    assert new_obj.issue_5_desc is None
    assert new_obj.issue_1_weight is None
    assert new_obj.issue_2_weight is None
    assert new_obj.issue_3_weight is None
    assert new_obj.issue_4_weight is None
    assert new_obj.issue_5_weight is None
    assert new_obj.adovacate_1_desc is None
    assert new_obj.adovacate_2_desc is None
    assert new_obj.adovacate_3_desc is None
    assert new_obj.adovacate_4_desc is None
    assert new_obj.adovacate_5_desc is None
    assert new_obj.adovacate_1_weight is None
    assert new_obj.adovacate_2_weight is None
    assert new_obj.adovacate_3_weight is None
    assert new_obj.adovacate_4_weight is None
    assert new_obj.adovacate_5_weight is None
