from src._road.jaar_config import get_test_reals_dir
from src._road.road import (
    RoadUnit,
    create_road_from_nodes,
    get_default_real_id_roadnode as root_label,
)
from src._instrument.file import delete_dir
from src.listen.userhub import userhub_shop, UserHub
from src.money.money import OtherMoneyReport
from pytest import fixture as pytest_fixture


@pytest_fixture()
def env_dir_setup_cleanup():
    x_env_dir = get_test_reals_dir()
    delete_dir(dir=x_env_dir)
    yield x_env_dir
    delete_dir(dir=x_env_dir)


def get_bob_othermoneyreport():
    bob_other_id = "Bob"
    bob_grant_count = 333
    bob_grant_amount = 333111
    bob_grant_rank_num = 22
    bob_grant_rank_percent = 0.668
    bob_tax_due_count = 444
    bob_tax_due_amount = 444111
    bob_tax_due_rank_num = 55
    bob_tax_due_rank_percent = 0.1111
    bob_tax_paid_amount = 77777
    bob_tax_paid_bool = True
    bob_tax_paid_rank_num = 111
    bob_tax_paid_rank_percent = 0.22222
    bob_transactions_count = 888888
    bob_transactions_magnitude = 9696
    bob_transactions_rank_num = 100
    bob_transactions_rank_percent = 0.99

    # WHEN
    return OtherMoneyReport(
        other_id=bob_other_id,
        grant_count=bob_grant_count,
        grant_amount=bob_grant_amount,
        grant_rank_num=bob_grant_rank_num,
        grant_rank_percent=bob_grant_rank_percent,
        tax_due_count=bob_tax_due_count,
        tax_due_amount=bob_tax_due_amount,
        tax_due_rank_num=bob_tax_due_rank_num,
        tax_due_rank_percent=bob_tax_due_rank_percent,
        tax_paid_amount=bob_tax_paid_amount,
        tax_paid_bool=bob_tax_paid_bool,
        tax_paid_rank_num=bob_tax_paid_rank_num,
        tax_paid_rank_percent=bob_tax_paid_rank_percent,
        transactions_count=bob_transactions_count,
        transactions_magnitude=bob_transactions_magnitude,
        transactions_rank_num=bob_transactions_rank_num,
        transactions_rank_percent=bob_transactions_rank_percent,
    )


def get_texas_road() -> RoadUnit:
    naton_text = "nation-state"
    usa_text = "usa"
    texas_text = "texas"
    return create_road_from_nodes([naton_text, usa_text, texas_text])


def get_sue_texas_userhub() -> UserHub:
    return userhub_shop(get_test_reals_dir(), root_label(), "Sue", get_texas_road())
