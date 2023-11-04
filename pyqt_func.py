from src.agenda.agenda import AgendaUnit, IdeaCore
from PyQt5.QtWidgets import QTreeWidgetItem
from dataclasses import dataclass


class InvalidPyQtException(Exception):
    pass


@dataclass
class PYQTTreeHolder:
    ideacore: IdeaCore
    yo_action_flag: str
    yo_goal_flag: str
    yo_complete_flag: str
    yo_acptfactunit_time_flag: str
    yo_acptfactunit_count_flag: str
    yo_acptfactheir_count_flag: str
    yo2bd_count_flag: str
    yo2bd_view_bd_flag: str
    yo2bd_view_bd_id: str
    requiredheir_count_flag: str
    required_count_flag: str
    required_view_flag: str
    required_view_handle: str
    acptfactheir_view_flag: str
    root_percent_flag: str
    source_agenda: str


def get_pyqttree(
    idearoot: IdeaCore,
    root_percent_flag: bool = None,
    yo2bd_count_flag: bool = None,
    yo2bd_view_bd_flag: bool = None,
    yo2bd_view_bd_id: bool = None,
    yo_action_flag: bool = None,
    yo_goal_flag: bool = None,
    yo_complete_flag: bool = None,
    yo_acptfactunit_time_flag: bool = None,
    yo_acptfactunit_count_flag: bool = None,
    yo_acptfactheir_count_flag: bool = None,
    requiredheir_count_flag: bool = None,
    required_count_flag: bool = None,
    required_view_flag: bool = None,
    required_view_handle: bool = None,
    acptfactheir_view_flag: bool = None,
    source_agenda: AgendaUnit = None,
) -> QTreeWidgetItem:
    pyqttree_holder = PYQTTreeHolder(
        ideacore=idearoot,
        yo_action_flag=yo_action_flag,
        yo_goal_flag=yo_goal_flag,
        yo_complete_flag=yo_complete_flag,
        yo_acptfactunit_time_flag=yo_acptfactunit_time_flag,
        yo_acptfactunit_count_flag=yo_acptfactunit_count_flag,
        yo_acptfactheir_count_flag=yo_acptfactheir_count_flag,
        yo2bd_count_flag=yo2bd_count_flag,
        yo2bd_view_bd_flag=yo2bd_view_bd_flag,
        yo2bd_view_bd_id=yo2bd_view_bd_id,
        requiredheir_count_flag=requiredheir_count_flag,
        required_count_flag=required_count_flag,
        required_view_flag=required_view_flag,
        required_view_handle=required_view_handle,
        acptfactheir_view_flag=acptfactheir_view_flag,
        root_percent_flag=root_percent_flag,
        source_agenda=source_agenda,
    )

    return _create_node(pth=pyqttree_holder)


def _create_node(pth: PYQTTreeHolder) -> QTreeWidgetItem:
    treenode_l = _create_treenode_l(pth)
    item = QTreeWidgetItem([treenode_l])
    item.setData(2, 10, pth.ideacore._label)
    item.setData(2, 11, pth.ideacore._pad)
    # item.setData(2, 12, ideacore._weight)
    # item.setData(2, 13, ideacore._begin)
    # item.setData(2, 14, ideacore._close)
    item.setData(2, 20, pth.ideacore._is_expanded)
    if pth.ideacore._requiredunits is None:
        item.setData(2, 21, 0)
    else:
        item.setData(2, 21, len(pth.ideacore._requiredunits))
    if pth.ideacore._kids is None:
        raise InvalidPyQtException(f"Idea {pth.ideacore._label} has null kids.")

    sort_ideas_list = list(pth.ideacore._kids.values())
    # print(f"{len(sort_ideas_list)=}")
    # print(f"{type(sort_ideas_list)=}")
    # print(f"{len(unsorted_ideas_list.sort(key=lambda x: x._label, reverse=False))=}")
    sort_ideas_list.sort(key=lambda x: x._label.lower(), reverse=False)
    # print(f"{len(sorted_ideas_list)=}")

    for kid_idea in sort_ideas_list:
        # for kid_idea in sort_ideas_list.sort(key=lambda x: x._agenda_importance, reverse=True):
        child_pth = PYQTTreeHolder(
            ideacore=kid_idea,
            yo_action_flag=pth.yo_action_flag,
            yo_goal_flag=pth.yo_goal_flag,
            yo_complete_flag=pth.yo_complete_flag,
            yo_acptfactunit_time_flag=pth.yo_acptfactunit_time_flag,
            yo_acptfactunit_count_flag=pth.yo_acptfactunit_count_flag,
            yo_acptfactheir_count_flag=pth.yo_acptfactheir_count_flag,
            yo2bd_count_flag=pth.yo2bd_count_flag,
            yo2bd_view_bd_flag=pth.yo2bd_view_bd_flag,
            yo2bd_view_bd_id=pth.yo2bd_view_bd_id,
            requiredheir_count_flag=pth.requiredheir_count_flag,
            required_count_flag=pth.required_count_flag,
            required_view_flag=pth.required_view_flag,
            required_view_handle=pth.required_view_handle,
            acptfactheir_view_flag=pth.acptfactheir_view_flag,
            root_percent_flag=pth.root_percent_flag,
            source_agenda=pth.source_agenda,
        )
        item.addChild(_create_node(child_pth))
    return item


def str2float(str_x: str):
    return None if not str_x or str_x is None else float(str_x)


def num2str(num_x: float):
    return "" if num_x is None else str(num_x)


def emptystr(str_x: str):
    return str_x or None


def bool_val(bool_x):
    return False if bool_x is None else bool_x


def emptystring_returns_none(str_x: str) -> str:
    # sourcery skip: swap-if-expression
    return None if not str_x else str_x


def agenda_importance_diplay(agenda_importance: float):
    if agenda_importance is None:
        return "None"
    if str(type(agenda_importance)) == "<class 'set'>":
        return f"ERROR {agenda_importance} {type(agenda_importance)=}"
    agenda_importance *= 100
    if agenda_importance == 1:
        return "100%"
    elif agenda_importance >= 10:
        return f"{agenda_importance:.1f}%"
    elif agenda_importance >= 1:
        return f"{agenda_importance:.2f}%"
    elif agenda_importance >= 0.1:
        return f"{agenda_importance:.3f}%"
    elif agenda_importance >= 0.01:
        return f"{agenda_importance:.4f}%"
    elif agenda_importance >= 0.001:
        return f"{agenda_importance:.5f}%"
    elif agenda_importance >= 0.0001:
        return f"{agenda_importance:.6f}%"
    elif agenda_importance >= 0.00001:
        return f"{agenda_importance:.7f}%"
    elif agenda_importance >= 0.000001:
        return f"{agenda_importance:.8f}%"
    elif agenda_importance == 0:
        return "0%"
    else:
        return f"{agenda_importance:.15f}%"


def _get_treenode_l_required_count(treenode_l, pth: PYQTTreeHolder) -> str:
    sufffact_count = sum(
        required.get_sufffacts_count()
        for required in pth.ideacore._requiredunits.values()
    )
    required_count = len(pth.ideacore._requiredunits)
    if required_count != 0:
        treenode_l += f" (lim {len(pth.ideacore._requiredunits)}/c{sufffact_count})"
    return treenode_l


def _get_treenode_l_required_view(treenode_l, pth: PYQTTreeHolder) -> str:
    requiredheir = pth.ideacore._requiredheirs.get(pth.required_view_handle)
    if requiredheir != None:
        # treenode_l += f"{get_terminus_node_from_road(requiredheir.base)}"
        grabed_sufffact = None
        for sufffact in requiredheir.sufffacts.values():
            grabed_sufffact = sufffact.need
        if grabed_sufffact not in [requiredheir.base, None]:
            grabed_sufffact = grabed_sufffact.replace(f"{requiredheir.base},", "")
            treenode_l += f" ({grabed_sufffact})"
    return treenode_l


def _get_treenode_l_acptfactheir_view(treenode_l, pth: PYQTTreeHolder) -> str:
    acptfactheir = pth.ideacore._acptfactheirs.get(pth.required_view_handle)
    if acptfactheir != None:
        time_road = f"{pth.source_agenda._idearoot._label},time,jajatime"
        if (
            acptfactheir.base == time_road
            and acptfactheir.open != None
            and acptfactheir.nigh != None
        ):
            hc_open_text = pth.source_agenda.get_jajatime_legible_one_time_event(
                jajatime_min=acptfactheir.open
            )
            hc_nigh_text = pth.source_agenda.get_jajatime_legible_one_time_event(
                jajatime_min=acptfactheir.nigh
            )
            # treenode_l += f"{get_terminus_node_from_road(acptfactheir.base)}"
            treenode_l += f" ({hc_open_text}-{hc_nigh_text})"
        elif (
            acptfactheir.base != time_road
            and acptfactheir.open != None
            and acptfactheir.nigh != None
        ):
            treenode_l += f" ({acptfactheir.open}-{acptfactheir.nigh})"
    return treenode_l


def _create_treenode_l(pth: PYQTTreeHolder):
    treenode_l = pth.ideacore._label

    if pth.root_percent_flag:
        treenode_l += f" ({agenda_importance_diplay(pth.ideacore._agenda_importance)})"
    elif pth.yo2bd_count_flag:
        treenode_l += f" ({len(pth.ideacore._balancelinks)})"
    elif pth.required_count_flag:
        treenode_l = _get_treenode_l_required_count(treenode_l, pth)
    elif pth.required_view_flag:
        treenode_l = _get_treenode_l_required_view(treenode_l, pth)
    elif pth.acptfactheir_view_flag and pth.ideacore._pad != "":
        treenode_l = _get_treenode_l_acptfactheir_view(treenode_l, pth)
    elif pth.yo_action_flag and pth.ideacore.promise:
        treenode_l += " (task)" if pth.ideacore._task else " (state)"
    elif pth.yo_acptfactunit_count_flag:
        treenode_l += f" ({len(pth.ideacore._acptfactunits)})"
    elif pth.yo_acptfactheir_count_flag and pth.ideacore._pad != "":
        treenode_l += f" ({len(pth.ideacore._acptfactheirs)})"

    if pth.requiredheir_count_flag and pth.ideacore._pad not in (None, ""):
        # requiredunit_count = sum(
        #     str(type(requiredheir)) == "<class 'src.agenda.required.RequiredUnit'>"
        #     for requiredheir in pth.ideacore._requiredheirs.values()
        # )
        treenode_l += f" (RequiredHeirs {len(pth.ideacore._requiredheirs)})"

    if pth.yo_acptfactunit_time_flag:
        time_road = f"{pth.source_agenda._idearoot._label},time,jajatime"
        acptfactunit_time_obj = pth.ideacore._acptfactunits.get(time_road)
        if acptfactunit_time_obj != None:
            hc_open_text = pth.source_agenda.get_jajatime_legible_one_time_event(
                jajatime_min=acptfactunit_time_obj.open
            )
            hc_nigh_text = pth.source_agenda.get_jajatime_legible_one_time_event(
                jajatime_min=acptfactunit_time_obj.nigh
            )
            # treenode_l += f" ({acptfactunit.base=} {acptfactunit.open}-{acptfactunit.nigh})"
            treenode_l += f" ({hc_open_text}-{hc_nigh_text})"

    return treenode_l
