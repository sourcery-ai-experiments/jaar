from src.agenda.atom import atom_hx_table_name
from src.instrument.sqlite import check_table_column_existence
from src.world.journal_sqlstr import get_atom_hx_table_insert_sqlstr
from src.world.world import worldunit_shop
from src.world.examples.example_atoms import get_beliefunit_atom_example_01
from src.world.examples.world_env_kit import (
    get_test_world_id,
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from src.instrument.sqlite import check_connection, get_row_count
from os import path as os_path
from pytest import raises as pytest_raises


# def test_WorldUnit_get_atom_hx_table_insert_sqlstr_CorrectlyWorksInDatabase(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     music_text = "music"
#     music_world = worldunit_shop(music_text, get_test_worlds_dir())
#     # with music_world.get_journal_conn() as journal_conn:
#     #     assert check_table_column_existence({atom_hx_table_name()}, journal_conn)
#     #     assert get_row_count(journal_conn, atom_hx_table_name()) == 0

#     # WHEN
#     x_atom = get_beliefunit_atom_example_01()
#     # with music_world.get_journal_conn() as treasury_conn:
#     #     treasury_conn.execute(get_atom_hx_table_insert_sqlstr(x_atom))

#     # THEN
#     with music_world.get_journal_conn() as journal_conn:
#         assert get_row_count(journal_conn, atom_hx_table_name()) == 1

#     assert 1 == 2
