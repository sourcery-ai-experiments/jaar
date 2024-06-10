# from src.atom.quark import quark_hx_table_name
# from src._instrument.sqlite import check_table_column_existence
# from src.real.journal_sqlstr import get_quark_hx_table_insert_sqlstr
# from src.real.real import realunit_shop
# from src.real.examples.real_env import (
#     get_test_real_id,
#     get_test_reals_dir,
#     env_dir_setup_cleanup,
# )
# from src._instrument.sqlite import get_row_count
# from os.path import exists as os_path_exists
# from pytest import raises as pytest_raises


# def test_RealUnit_get_quark_hx_table_insert_sqlstr_CorrectlyInsertsIntoDatabase(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     music_text = "music"
#     music_real = realunit_shop(music_text, get_test_reals_dir())
#     # with music_real.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({quark_hx_table_name()}, journal_conn)
#     #     assert get_row_count(journal_conn, quark_hx_table_name()) == 0

#     # WHEN
#     x_quark = get_quark_example_beliefunit_knee()
#     # with music_real.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_quark_hx_table_insert_sqlstr(x_quark))

#     # THEN
#     with music_real.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, quark_hx_table_name()) == 1

#     assert 1 == 2
