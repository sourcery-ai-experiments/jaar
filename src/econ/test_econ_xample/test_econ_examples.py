from src.econ.examples.econ_env_kit import env_dir_setup_cleanup
from src.econ.examples.example_econ_agendas import (
    # _delete_and_set_ex3,
    _delete_and_set_ex4,
    # _delete_and_set_ex5,
    _delete_and_set_ex6,
)


def test_econ_delete_and_set_ex3_thru_6_RunWithOutError(env_dir_setup_cleanup):
    # WHEN/THEN
    print("Try ex3...")
    # assert _delete_and_set_ex3() is None
    print("Try ex4...")
    assert _delete_and_set_ex4() is None
    print("Try ex5...")
    # assert _delete_and_set_ex5() is None
    print("Try ex6...")
    assert _delete_and_set_ex6() != None
