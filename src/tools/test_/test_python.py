from src.tools.python import return1ifnone


def test_return1ifnone():
    # GIVEN / WHEN / THEN
    assert return1ifnone(None) == 1
    assert return1ifnone(2) == 2
    assert return1ifnone(-3) == -3
