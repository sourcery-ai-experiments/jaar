from src._road.jaar_config import duty_str, work_str


def test_duty_str():
    assert duty_str() == "duty"


def test_work_str():
    assert work_str() == "work"
