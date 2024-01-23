from src.tools.python import get_1_if_None


def test_get_1_if_None():
    # GIVEN / WHEN / THEN
    assert get_1_if_None(None) == 1
    assert get_1_if_None(2) == 2
    assert get_1_if_None(-3) == -3
