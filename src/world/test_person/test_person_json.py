from src.world.person import personunit_shop, PersonUnit
from src.instrument.python import x_get_dict
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)


# def test_PersonUnit_get_dict_CorrectlyGetsDict_simple():
#     # GIVEN
#     yao_text = "Yao"
#     yao_world_dir = f"/artbitarydirectory/{yao_text}"
#     yao_artbitarydirectory = f"/artbitarydirectory/persons/{yao_text}"
#     yao_personunit = personunit_shop(
#         person_id=yao_text,
#     )

#     # WHEN
#     yao_personunit_get_dict = yao_personunit.get_dict()

#     # THEN
#     yao_personunit_x_dict = {
#         "person_id": yao_text,
#         "person_dir": yao_artbitarydirectory,
#         "_markets": {},
#         "_problems": {},
#     }
#     assert yao_personunit_x_dict == yao_personunit_get_dict


# # def test_PersonUnit_get_json_ExportsJSONWorksForSimpleExample():
# #     pass


# # def test_AgendaUnit_get_json_ExportJSONWorksForBigExample():
# #     pass


# # def test_save_file_CorrectlySavesPersonUnitJSON(env_dir_setup_cleanup):
# #     pass


# # def test_agenda_get_from_json_ReturnsCorrectObjSimpleExample():
# #     pass


# # def test_agenda_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
# #     pass
