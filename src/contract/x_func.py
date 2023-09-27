from json import loads as json_loads, dumps as json_dumps
from src.contract.road import Road
from os import (
    path as os_path,
    makedirs as os_makedirs,
    rename as os_rename,
    remove as os_remove,
    scandir as os_scandir,
    listdir as os_listdir,
)
from shutil import rmtree as shutil_rmtree, copytree as shutil_copytree


def single_dir_create_if_null(x_path: str):
    if not os_path.exists(x_path):
        os_makedirs(x_path)


def delete_dir(dir: str):
    if os_path.exists(dir):
        if os_path.isdir(dir):
            shutil_rmtree(path=dir)
        elif os_path.isfile(dir):
            os_remove(path=dir)


def rename_dir(src, dst):
    os_rename(src=src, dst=dst)


class InvalidFileCopyException(Exception):
    pass


def copy_dir(src_dir: str, dest_dir: str):
    if os_path.exists(dest_dir):
        raise InvalidFileCopyException(
            f"Cannot copy '{src_dir}' to '{dest_dir}' since '{dest_dir}' exists"
        )
    else:
        shutil_copytree(src=src_dir, dst=dest_dir)


def save_file(dest_dir: str, file_name: str, file_text: str, replace: bool = None):
    # print(f"{dest_dir=} {file_name=} {replace=}")
    if replace is None:
        replace = True

    if not os_path.exists(path=dest_dir):
        os_makedirs(dest_dir)

    file_path = f"{dest_dir}/{file_name}"
    if (os_path.exists(path=file_path) and replace) or os_path.exists(
        path=file_path
    ) == False:
        with open(file_path, "w") as f:
            f.write(file_text)
            f.close()


def open_file(dest_dir: str, file_name: str):
    # sourcery skip: raise-specific-error
    file_path = dest_dir if file_name is None else f"{dest_dir}/{file_name}"
    text_x = ""
    try:
        with open(file_path, "r") as f:
            text_x = f.read()
            f.close()
    except Exception as e:
        raise Exception(f"Could not load file {file_path} {e.args}") from e
    return text_x


def count_files(dir_path: str) -> int:
    return (
        sum(bool(path_x.is_file()) for path_x in os_scandir(dir_path))
        if os_path.exists(path=dir_path)
        else None
    )


def dir_files(
    dir_path: str, remove_extensions: bool = None, include_dirs=None, include_files=None
) -> dict[str:str]:
    if include_dirs is None:
        include_dirs = True
    if include_files is None:
        include_files = True

    dict_x = {}
    for obj_name in os_listdir(dir_path):
        dict_key = None
        file_name = None
        file_path = None
        file_text = None
        obj_path = f"{dir_path}/{obj_name}"
        if os_path.isfile(obj_path) and include_files:
            file_name = obj_name
            file_path = f"{dir_path}/{file_name}"
            # print(f" {os_path.isdir(file_path)=}")
            file_text = open_file(dest_dir=dir_path, file_name=file_name)
            dict_key = (
                os_path.splitext(file_name)[0] if remove_extensions else file_name
            )
            dict_x[dict_key] = file_text

        if os_path.isdir(obj_path) and include_dirs:
            dict_key = obj_name
            file_text = True
            dict_x[dict_key] = file_text
    return dict_x


# class XFunc:
def x_is_json(json_x: str):
    try:
        json_loads(json_x)
    except ValueError as e:
        return False
    return True


def x_get_json(dict_x: dict) -> str:
    return json_dumps(obj=dict_x)


def x_get_dict(json_x: str) -> dict:
    return json_loads(json_x)


# class YR:
def from_list_get_active_status(
    road: Road, idea_list: list, asse_bool: bool = None
) -> bool:
    active_status = None
    temp_idea = None

    active_true_count = 0
    active_false_count = 0
    for idea in idea_list:
        if idea.get_road() == road:
            temp_idea = idea
            print(
                f"searched for IdeaKid {temp_idea.get_road()} found {temp_idea._active_status=}"
            )

        if idea._active_status:
            active_true_count += 1
        elif idea._active_status == False:
            active_false_count += 1

    active_status = temp_idea._active_status
    print(
        f"Set Active_status: {idea._label=} {active_status} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active_status != asse_bool:
            yr_explanation(temp_idea)

        assert active_status == asse_bool
    else:
        yr_explanation(temp_idea)
    return active_status


def yr_print_idea_base_info(idea, filter: bool):
    for l in idea._requiredheirs.values():
        if l._status == filter:
            print(
                f"  RequiredHeir '{l.base}' Base LH:{l._status} W:{len(l.sufffacts)}"  # \t_task {l._task}"
            )
            if str(type(idea)).find(".idea.IdeaKid'>") > 0:
                yr_print_acptfact(
                    lh_base=l.base,
                    lh_status=l._status,
                    sufffacts=l.sufffacts,
                    acptfactheirs=idea._acptfactheirs,
                )


def yr_explanation(idea):
    str1 = f"'{yr_d(idea._walk)}' idea"
    str2 = f" has RequiredU:{yr_x(idea._requiredunits)} LH:{yr_x(idea._requiredheirs)}"
    str3 = f" {str(type(idea))}"
    str4 = " "
    if str(type(idea)).find(".idea.IdeaKid'>") > 0:
        str3 = f" AcptFacts:{yr_x(idea._acptfactheirs)} Status: {idea._active_status}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_required = []
        for hh in idea._acptfactheirs.values():
            hh_wo_matched_required = []
            try:
                idea._requiredheirs[hh.base]
            except Exception:
                hh_wo_matched_required.append(hh.base)

        for base in hh_wo_matched_required:
            print(f"AcptFacts that don't matter to this Idea: {base}")

    # if idea._requiredunits != None:
    #     for lu in idea._requiredunits.values():
    #         print(f"  RequiredUnit   '{lu.base}' sufffacts: {len(lu.sufffacts)} ")
    if idea._requiredheirs != None:
        filter_x = True
        yr_print_idea_base_info(idea=idea, filter=True)

        filter_x = False
        print("\nRequireds that failed:")

        for l in idea._requiredheirs.values():
            if l._status == filter_x:
                print(
                    f"  RequiredHeir '{l.base}' Base LH:{l._status} W:{len(l.sufffacts)}"  # \t_task {l._task}"
                )
                if str(type(idea)).find(".idea.IdeaKid'>") > 0:
                    yr_print_acptfact(
                        lh_base=l.base,
                        lh_status=l._status,
                        sufffacts=l.sufffacts,
                        acptfactheirs=idea._acptfactheirs,
                    )
                print("")
    # print(idea._acptfactheirs)
    # print(f"{(idea._acptfactheirs != None)=}")
    # print(f"{len(idea._acptfactheirs)=} ")

    print("")


def yr_print_acptfact(lh_base, lh_status, sufffacts, acptfactheirs):
    for ww in sufffacts.values():
        ww_open = ""
        ww_open = f"\topen:{ww.open}" if ww.open != None else ""
        ww_nigh = ""
        ww_nigh = f"\tnigh:{ww.nigh}" if ww.nigh != None else ""
        ww_task = f" Task: {ww._task}"
        hh_open = ""
        hh_nigh = ""
        hh_pick = ""
        print(
            f"\t    '{lh_base}' SuffFact LH:{lh_status} W:{ww._status}\tneed:{ww.need}{ww_open}{ww_nigh}"
        )

        for hh in acptfactheirs.values():
            if hh.base == lh_base:
                if hh.open != None:
                    hh_open = f"\topen:{hh.open}"
                if hh.nigh != None:
                    hh_nigh = f"\tnigh:{hh.nigh}"
                hh_pick = hh.pick
                # if hh_pick != "":
                print(
                    f"\t    '{hh.base}' AcptFact LH:{lh_status} W:{ww._status}\tAcptFact:{hh_pick}{hh_open}{hh_nigh}"
                )
        if hh_pick == "":
            print(f"\t    Base: No AcptFact")


def yr_d(self):
    return "no road" if self is None else self[self.find(",") + 1 :]


def yr_x(self):
    return 0 if self is None else len(self)


def get_on_meld_weight_actions() -> dict[str:None]:
    # match: melder and meldee will have
    #  equal weight or error thrown
    # sum: melder and meldee sum weights
    # ignore: melder ignores weight from meldee
    # override: meldee overwrites melder weight (only works on meldee=default)
    # default: meldee ignores meldee unless meldee is override
    return {
        "default": None,
        "match": None,
        "sum": None,
        "accept": None,
        "override": None,
    }


def get_meld_weight(
    src_weight: float,
    src_on_meld_weight_action: str,
    other_weight: float,
    other_on_meld_weight_action: float,
) -> float:
    if (
        src_on_meld_weight_action != "default"
        or other_on_meld_weight_action == "ignore"
    ):
        src_weight += other_weight
    return src_weight


def return1ifnone(x_obj):
    return 1 if x_obj is None else x_obj
