from lib.polity.test_polity.env_tools import (
    _delete_and_set_ex3,
    _delete_and_set_ex4,
    _delete_and_set_ex5,
    _delete_and_set_ex6,
)


def test_polity_delete_and_set_ex3_andOthersRunWithOutError():
    # WHEN/THEN
    assert _delete_and_set_ex3() == None
    assert _delete_and_set_ex4() == None
    assert _delete_and_set_ex5() == None
    assert _delete_and_set_ex6() == None
