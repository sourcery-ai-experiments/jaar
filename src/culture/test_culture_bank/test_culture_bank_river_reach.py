from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.examples.culture_env_kit import _delete_and_set_ex6
from src.culture.y_func import get_single_result

from src.culture.bank_sqlstr import (
    get_river_block_reach_base_sqlstr,
)


def test_culture_clear_river_score_CorrectlyEmptysTable(env_dir_setup_cleanup):
    # GIVEN
    ex7_text = "ex7"
    x_culture = _delete_and_set_ex6(x_handle=ex7_text)
    sal_text = "sal"
    reach_sqlstr = get_river_block_reach_base_sqlstr(sal_text)

    # WHEN
    count_reach_rows_str = f"""
SELECT COUNT(*)
FROM (
    {reach_sqlstr}
) x
"""
    count_reach_rows_num = get_single_result(
        x_culture.get_bank_conn(), count_reach_rows_str
    )

    # THEN
    assert count_reach_rows_num == 94
