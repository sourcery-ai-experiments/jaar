from src.culture.culture import cultureunit_shop, get_river_ledger_unit
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


# def test_culture_river_block_reach_base_sqlstr_CorrectlySelectsDataSet(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     ex7_text = "ex7"
#     x_culture = _delete_and_set_ex6(x_handle=ex7_text)
#     sal_text = "sal"
#     # x_culture = _delete_and_set_ex6()
#     # # x_culture.set_manager_name(sal_text)
#     # ex6_text = "ex6"
#     # x_culture = cultureunit_shop(handle=ex6_text, cultures_dir=get_test_cultures_dir())
#     # x_culture.set_manager_name(sal_text)
#     # x_culture.set_credit_flow_for_agenda(sal_text, max_blocks_count=100)

#     # WHEN
#     reach_sqlstr = get_river_block_reach_base_sqlstr(sal_text)
#     reach_count_sqlstr = f"""SELECT COUNT(*) FROM ({reach_sqlstr}) x;"""
#     reach_rows_num = get_single_result(x_culture.get_bank_conn(), reach_count_sqlstr)

#     # THEN
#     assert reach_rows_num == 94


# def test_culture_clear_river_score_CorrectlyEmptysTable(env_dir_setup_cleanup):
#     pass
