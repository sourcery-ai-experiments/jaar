from src.culture.examples.culture_env_kit import (
    _delete_and_set_ex3,
    _delete_and_set_ex4,
    _delete_and_set_ex5,
    _delete_and_set_ex6,
)


def test_culture_delete_and_set_ex3_thru_6_RunWithOutError():
    # WHEN/THEN
    assert _delete_and_set_ex3() is None
    assert _delete_and_set_ex4() is None
    assert _delete_and_set_ex5() is None
    assert _delete_and_set_ex6() != None
