from src._instrument.file import open_file, save_file
from src._instrument.python import get_json_from_dict, get_dict_from_json
from os import getcwd as os_getcwd


class CRUD_command(str):
    pass


def quark_update() -> CRUD_command:
    return "UPDATE"


def quark_insert() -> CRUD_command:
    return "INSERT"


def quark_delete() -> CRUD_command:
    return "DELETE"


def quark_hx_table_name() -> str:
    return "quark_hx"


def quark_mstr_table_name() -> str:
    return "quark_mstr"


def normal_table_name_text() -> str:
    return "normal_table_name"


def columns_text() -> str:
    return "columns"


def sqlite_datatype_text() -> str:
    return "sqlite_datatype"


def python_type_text() -> str:
    return "python_type"


def nullable_text() -> str:
    return "nullable"


def required_args_text() -> str:
    return "required_args"


def optional_args_text() -> str:
    return "optional_args"


def agendaunit_text() -> str:
    return "agendaunit"


def agenda_partyunit_text() -> str:
    return "agenda_partyunit"


def agenda_beliefunit_text() -> str:
    return "agenda_beliefunit"


def agenda_belief_partylink_text() -> str:
    return "agenda_belief_partylink"


def agenda_ideaunit_text() -> str:
    return "agenda_ideaunit"


def agenda_idea_balancelink_text() -> str:
    return "agenda_idea_balancelink"


def agenda_idea_reasonunit_text() -> str:
    return "agenda_idea_reasonunit"


def agenda_idea_reason_premiseunit_text() -> str:
    return "agenda_idea_reason_premiseunit"


def agenda_idea_suffbelief_text() -> str:
    return "agenda_idea_suffbelief"


def agenda_idea_healerhold_text() -> str:
    return "agenda_idea_healerhold"


def agenda_idea_factunit_text() -> str:
    return "agenda_idea_factunit"


def get_quark_config_file_name() -> str:
    return "quark_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/atom"


def get_quark_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_quark_config_file_name())
    )


def add_to_quark_table_columns(x_dict, quark_category, crud, arg_key, arg_value):
    x_dict[f"{quark_category}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_quark_table_build() -> dict[str:]:
    quark_table_columns = {}
    quark_config = get_quark_config_dict()
    for quark_category, category_dict in quark_config.items():
        catergory_insert = category_dict.get(quark_insert())
        catergory_update = category_dict.get(quark_update())
        catergory_delete = category_dict.get(quark_delete())
        if catergory_insert != None:
            required_args = category_dict.get(required_args_text())
            optional_args = category_dict.get(optional_args_text())
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_insert(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_insert(),
                    optional_arg,
                    x_value,
                )
        if catergory_update != None:
            required_args = category_dict.get(required_args_text())
            optional_args = category_dict.get(optional_args_text())
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_update(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_update(),
                    optional_arg,
                    x_value,
                )
        if catergory_delete != None:
            required_args = category_dict.get(required_args_text())
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_delete(),
                    required_arg,
                    x_value,
                )
    return quark_table_columns


def get_normalized_agenda_table_build() -> dict[str : dict[str:]]:
    agenda_tables = {}
    quark_config = get_quark_config_dict()
    for x_category, category_dict in quark_config.items():
        agenda_tables[x_category] = {}
        l1_dict = agenda_tables.get(x_category)
        l1_dict[normal_table_name_text()] = category_dict.get(normal_table_name_text())
        l1_dict[columns_text()] = {}
        l2_dict = l1_dict.get(columns_text())
        l2_dict["uid"] = {
            sqlite_datatype_text(): "INTEGER",
            nullable_text(): False,
            "primary_key": True,
        }
        required_args = category_dict.get(required_args_text())
        optional_args = category_dict.get(optional_args_text())
        if required_args != None:
            for required_arg, x_value in required_args.items():
                l2_dict[required_arg] = {
                    sqlite_datatype_text(): x_value.get(sqlite_datatype_text()),
                    nullable_text(): False,
                }

        if optional_args != None:
            for optional_arg, x_value in optional_args.items():
                l2_dict[optional_arg] = {
                    sqlite_datatype_text(): x_value.get(sqlite_datatype_text()),
                    nullable_text(): True,
                }
    return agenda_tables


def save_quark_config_file(quark_config_dict):
    save_file(
        dest_dir=config_file_dir(),
        file_name=get_quark_config_file_name(),
        file_text=get_json_from_dict(quark_config_dict),
    )


def category_ref() -> set:
    return get_quark_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_quark_order(
    category: str,
    crud_text: str,
    quark_order_text: str,
    expected_quark_order: int = None,
) -> int:
    quark_config_dict = get_quark_config_dict()
    category_dict = quark_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(quark_order_text)


def set_mog(
    category: str,
    crud_text: str,
    quark_order_text: str,
    quark_order_int: int,
) -> int:
    quark_config_dict = get_quark_config_dict()
    category_dict = quark_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[quark_order_text] = quark_order_int
    save_quark_config_file(quark_config_dict)


def get_category_from_dict(x_row_dict: dict) -> str:
    x_category_ref = category_ref()
    for x_columnname in x_row_dict:
        for x_category in x_category_ref:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]
