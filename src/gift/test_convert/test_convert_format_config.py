from src._instrument.file import dir_files
from src.gift.atom_config import (
    config_file_dir,
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_atom_order as q_order,
    set_mog,
    get_flattened_atom_table_build,
    get_normalized_world_table_build,
    required_args_text,
    optional_args_text,
    normal_table_name_text,
    normal_specs_text,
    sqlite_datatype_text,
    python_type_text,
    worldunit_text,
    world_charunit_text,
    world_char_beliefhold_text,
    world_ideaunit_text,
    world_idea_fiscallink_text,
    world_idea_reasonunit_text,
    world_idea_reason_premiseunit_text,
    world_idea_heldbelief_text,
    world_idea_healerhold_text,
    world_idea_factunit_text,
)
from src.gift.convert import (
    real_id_str,
    owner_id_str,
    char_id_str,
    belief_id_str,
    ideaunit_str,
    char_pool_str,
    debtor_weight_str,
    credor_weight_str,
    validate_str,
    must_be_str,
    must_be_roadnode_str,
    must_be_number_str,
    get_convert_format_dir,
    get_convert_format_filenames,
    get_convert_format_dict,
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_beliefhold_v0_0_0,
    jaar_format_0003_ideaunit_v0_0_0,
)

# from src.gift.examples.gift_env import get_codespace_gift_dir
from os.path import exists as os_path_exists


def test_str_functions_ReturnCorrectObjs():
    # GIVEN / WHEN / THEN
    assert real_id_str() == "real_id"
    assert owner_id_str() == "owner_id"
    assert char_id_str() == "char_id"
    assert char_pool_str() == "char_pool"
    assert debtor_weight_str() == "debtor_weight"
    assert credor_weight_str() == "credor_weight"
    assert jaar_format_0001_char_v0_0_0() == "jaar_format_0001_char_v0_0_0"
    x0002_convert_format = "jaar_format_0002_beliefhold_v0_0_0"
    assert jaar_format_0002_beliefhold_v0_0_0() == x0002_convert_format
    x0003_convert_format = "jaar_format_0003_ideaunit_v0_0_0"
    assert jaar_format_0003_ideaunit_v0_0_0() == x0003_convert_format


def test_get_convert_format_dir_ReturnsObj():
    # GIVEN / WHEN
    convert_format_dir = get_convert_format_dir()
    # THEN
    print(f"{convert_format_dir=}")
    assert convert_format_dir == f"{config_file_dir()}/convert_formats"


def test_get_convert_format_filenames_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_filenames = get_convert_format_filenames()
    # THEN
    print(f"{x_filenames=}")
    assert jaar_format_0001_char_v0_0_0() in x_filenames
    assert jaar_format_0002_beliefhold_v0_0_0() in x_filenames
    assert jaar_format_0003_ideaunit_v0_0_0() in x_filenames


def test_convert_format_FilesExist():
    # GIVEN
    convert_format_dir = get_convert_format_dir()

    # WHEN
    convert_format_files = dir_files(convert_format_dir, True)

    # THEN
    convert_format_filenames = set(convert_format_files.keys())
    assert convert_format_filenames == get_convert_format_filenames()
    assert len(convert_format_filenames) == len(get_convert_format_filenames())


def test_get_convert_format_dict_HasCorrectAttrs_jaar_format_0001_char_v0_0_0():
    # GIVEN
    convert_format_name = jaar_format_0001_char_v0_0_0()

    # WHEN
    convert_format_dict = get_convert_format_dict(convert_format_name)

    # THEN
    real_id_dict = convert_format_dict.get(real_id_str())
    owner_id_dict = convert_format_dict.get(owner_id_str())
    char_id_dict = convert_format_dict.get(char_id_str())
    char_pool_dict = convert_format_dict.get(char_pool_str())
    debtor_weight_dict = convert_format_dict.get(debtor_weight_str())
    credor_weight_dict = convert_format_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert char_pool_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    real_id_required = real_id_dict.get(validate_str())
    owner_id_required = owner_id_dict.get(validate_str())
    char_id_required = char_id_dict.get(validate_str())
    char_pool_required = char_pool_dict.get(validate_str())
    debtor_weight_required = debtor_weight_dict.get(validate_str())
    credor_weight_required = credor_weight_dict.get(validate_str())
    assert real_id_required == [must_be_roadnode_str()]
    assert owner_id_required == [must_be_roadnode_str()]
    assert char_id_required == [must_be_roadnode_str()]
    assert char_pool_required == [must_be_number_str()]
    assert debtor_weight_required == [must_be_number_str()]
    assert credor_weight_required == [must_be_number_str()]


def test_get_convert_format_dict_HasCorrectAttrs_jaar_format_0002_beliefhold_v0_0_0():
    # GIVEN
    convert_format_name = jaar_format_0002_beliefhold_v0_0_0()

    # WHEN
    convert_format_dict = get_convert_format_dict(convert_format_name)

    # THEN
    real_id_dict = convert_format_dict.get(real_id_str())
    owner_id_dict = convert_format_dict.get(owner_id_str())
    char_id_dict = convert_format_dict.get(char_id_str())
    belief_id_dict = convert_format_dict.get(belief_id_str())
    debtor_weight_dict = convert_format_dict.get(debtor_weight_str())
    credor_weight_dict = convert_format_dict.get(credor_weight_str())
    assert real_id_dict != None
    assert owner_id_dict != None
    assert char_id_dict != None
    assert belief_id_dict != None
    assert debtor_weight_dict != None
    assert credor_weight_dict != None
    real_id_required = real_id_dict.get(validate_str())
    owner_id_required = owner_id_dict.get(validate_str())
    char_id_required = char_id_dict.get(validate_str())
    belief_id_required = belief_id_dict.get(validate_str())
    debtor_weight_required = debtor_weight_dict.get(validate_str())
    credor_weight_required = credor_weight_dict.get(validate_str())
    assert real_id_required == [must_be_roadnode_str()]
    assert owner_id_required == [must_be_roadnode_str()]
    assert char_id_required == [must_be_roadnode_str()]
    assert belief_id_required == [must_be_str()]
    assert debtor_weight_required == [must_be_number_str()]
    assert credor_weight_required == [must_be_number_str()]


# def test_get_convert_format_dict_HasCorrectAttrs_jaar_format_0003_ideaunit_v0_0_0():
#     # GIVEN
#     convert_format_name = jaar_format_0003_ideaunit_v0_0_0()

#     # WHEN
#     convert_format_dict = get_convert_format_dict(convert_format_name)

#     # THEN
#     real_id_dict = convert_format_dict.get(real_id_str())
#     owner_id_dict = convert_format_dict.get(owner_id_str())
#     ideaunit_dict = convert_format_dict.get(ideaunit_str())
#     belief_id_dict = convert_format_dict.get(belief_id_str())
#     debtor_weight_dict = convert_format_dict.get(debtor_weight_str())
#     credor_weight_dict = convert_format_dict.get(credor_weight_str())
#     assert real_id_dict != None
#     assert owner_id_dict != None
#     assert ideaunit_dict != None
#     assert belief_id_dict != None
#     assert debtor_weight_dict != None
#     assert credor_weight_dict != None
#     real_id_required = real_id_dict.get(validate_str())
#     owner_id_required = owner_id_dict.get(validate_str())
#     char_id_required = ideaunit_dict.get(validate_str())
#     belief_id_required = belief_id_dict.get(validate_str())
#     debtor_weight_required = debtor_weight_dict.get(validate_str())
#     credor_weight_required = credor_weight_dict.get(validate_str())
#     assert real_id_required == [must_be_roadnode_str()]
#     assert owner_id_required == [must_be_roadnode_str()]
#     assert char_id_required == [must_be_roadnode_str()]
#     assert belief_id_required == [must_be_roadnode_str()]
#     assert debtor_weight_required == [must_be_number_str()]
#     assert credor_weight_required == [must_be_number_str()]

#     real_id
#     owner_id
#     road
#     fiscal_belief_id
#     fiscal_credor_weight
#     fiscal_debtor_weight
#     reason_base
#     reason_premise_true
#     reason_premise_false
#     reason_suff_idea_active


#     _cultureunit: CultureUnit = None
#     _factunits: dict[RoadUnit:FactUnit] = None
#     _healerhold: HealerHold = None
#     # _begin: float = None
#     # _close: float = None
#     # _addin: float = None
#     # _denom: int = None
#     # _numor: int = None
#     # _reest: bool = None
#     # _range_source_road: RoadUnit = None
#     # _numeric_road: RoadUnit = None
#     pledge: bool = None
#     _problem_bool: bool = None
