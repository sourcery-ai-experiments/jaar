from lib.agent.agent import AgentUnit
from lib.agent.idea import IdeaCore
from PyQt5.QtWidgets import QTreeWidgetItem
from lib.agent.road import get_terminus_node_from_road


class InvalidPyQtException(Exception):
    pass


def get_pyqttree(
    idearoot: IdeaCore,
    root_percent_flag: bool = None,
    yo2bd_count_flag: bool = None,
    yo2bd_view_bd_flag: bool = None,
    yo2bd_view_bd_id: bool = None,
    yo_action_flag: bool = None,
    yo_agenda_flag: bool = None,
    yo_complete_flag: bool = None,
    yo_acptfactunit_time_flag: bool = None,
    yo_acptfactunit_count_flag: bool = None,
    yo_acptfactheir_count_flag: bool = None,
    requiredheir_count_flag: bool = None,
    required_count_flag: bool = None,
    required_view_flag: bool = None,
    required_view_name: bool = None,
    acptfactheir_view_flag: bool = None,
    src_agent: AgentUnit = None,
) -> QTreeWidgetItem:
    return _create_node(
        idea_core=idearoot,
        yo_agenda_flag=yo_agenda_flag,
        yo_action_flag=yo_action_flag,
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
        required_view_name=required_view_name,
        acptfactheir_view_flag=acptfactheir_view_flag,
        root_percent_flag=root_percent_flag,
        src_agent=src_agent,
    )


def _create_node(
    idea_core: IdeaCore,
    root_percent_flag: bool = None,
    yo2bd_count_flag: bool = None,
    yo2bd_view_bd_flag: bool = None,
    yo2bd_view_bd_id: bool = None,
    yo_action_flag: bool = None,
    yo_agenda_flag: bool = None,
    yo_complete_flag: bool = None,
    yo_acptfactunit_time_flag: bool = None,
    yo_acptfactunit_count_flag: bool = None,
    yo_acptfactheir_count_flag: bool = None,
    requiredheir_count_flag: bool = None,
    required_count_flag: bool = None,
    required_view_flag: bool = None,
    required_view_name: bool = None,
    acptfactheir_view_flag: bool = None,
    src_agent: AgentUnit = None,
) -> QTreeWidgetItem:
    treenode_label = _create_treenode_label(
        idea_core=idea_core,
        root_percent_flag=root_percent_flag,
        yo2bd_count_flag=yo2bd_count_flag,
        yo2bd_view_bd_flag=yo2bd_view_bd_flag,
        yo2bd_view_bd_id=yo2bd_view_bd_id,
        yo_action_flag=yo_action_flag,
        yo_agenda_flag=yo_agenda_flag,
        yo_complete_flag=yo_complete_flag,
        yo_acptfactunit_time_flag=yo_acptfactunit_time_flag,
        yo_acptfactunit_count_flag=yo_acptfactunit_count_flag,
        yo_acptfactheir_count_flag=yo_acptfactheir_count_flag,
        requiredheir_count_flag=requiredheir_count_flag,
        required_count_flag=required_count_flag,
        required_view_flag=required_view_flag,
        required_view_name=required_view_name,
        acptfactheir_view_flag=acptfactheir_view_flag,
        src_agent=src_agent,
    )
    item = QTreeWidgetItem([treenode_label])
    item.setData(2, 10, idea_core._desc)
    item.setData(2, 11, idea_core._walk)
    # item.setData(2, 12, idea_core._weight)
    # item.setData(2, 13, idea_core._begin)
    # item.setData(2, 14, idea_core._close)
    item.setData(2, 20, idea_core._is_expanded)
    if idea_core._requiredunits is None:
        item.setData(2, 21, 0)
    else:
        item.setData(2, 21, len(idea_core._requiredunits))
    if idea_core._kids is None:
        raise InvalidPyQtException(f"Idea {idea_core._desc} has null kids.")

    sort_ideas_list = list(idea_core._kids.values())
    # print(f"{len(sort_ideas_list)=}")
    # print(f"{type(sort_ideas_list)=}")
    # print(f"{len(unsorted_ideas_list.sort(key=lambda x: x._desc, reverse=False))=}")
    sort_ideas_list.sort(key=lambda x: x._desc.lower(), reverse=False)
    # print(f"{len(sorted_ideas_list)=}")

    for kid_idea in sort_ideas_list:
        # for kid_idea in sort_ideas_list.sort(key=lambda x: x._agent_importance, reverse=True):
        item.addChild(
            _create_node(
                idea_core=kid_idea,
                yo_agenda_flag=yo_agenda_flag,
                yo_action_flag=yo_action_flag,
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
                required_view_name=required_view_name,
                acptfactheir_view_flag=acptfactheir_view_flag,
                root_percent_flag=root_percent_flag,
                src_agent=src_agent,
            )
        )
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


def lw_diplay(agent_importance: float):
    if agent_importance is None:
        return "None"
    if str(type(agent_importance)) == "<class 'set'>":
        return f"ERROR {agent_importance} {type(agent_importance)=}"
    agent_importance *= 100
    if agent_importance == 1:
        return "100%"
    elif agent_importance >= 10:
        return f"{agent_importance:.1f}%"
    elif agent_importance >= 1:
        return f"{agent_importance:.2f}%"
    elif agent_importance >= 0.1:
        return f"{agent_importance:.3f}%"
    elif agent_importance >= 0.01:
        return f"{agent_importance:.4f}%"
    elif agent_importance >= 0.001:
        return f"{agent_importance:.5f}%"
    elif agent_importance >= 0.0001:
        return f"{agent_importance:.6f}%"
    elif agent_importance >= 0.00001:
        return f"{agent_importance:.7f}%"
    elif agent_importance >= 0.000001:
        return f"{agent_importance:.8f}%"
    elif agent_importance == 0:
        return "0%"
    else:
        return f"{agent_importance:.15f}%"


def _create_treenode_label(
    idea_core: IdeaCore,
    yo_action_flag: bool,
    yo_agenda_flag: bool,
    yo_complete_flag: bool,
    yo_acptfactunit_time_flag: bool,
    yo_acptfactunit_count_flag: bool,
    yo_acptfactheir_count_flag: bool,
    yo2bd_count_flag: bool,
    yo2bd_view_bd_flag: bool,
    yo2bd_view_bd_id: bool,
    requiredheir_count_flag: bool,
    required_count_flag: bool,
    required_view_flag: bool,
    required_view_name: bool,
    acptfactheir_view_flag: bool,
    root_percent_flag: bool,
    src_agent: AgentUnit,
):
    treenode_label = idea_core._desc

    if root_percent_flag:
        treenode_label += f" ({lw_diplay(idea_core._agent_importance)})"
    elif yo2bd_count_flag:
        treenode_label += f" ({len(idea_core._brandlinks)})"
    elif required_count_flag:
        sufffact_count = sum(
            required.get_sufffacts_count()
            for required in idea_core._requiredunits.values()
        )
        required_count = len(idea_core._requiredunits)
        if required_count != 0:
            treenode_label += (
                f" (lim {len(idea_core._requiredunits)}/c{sufffact_count})"
            )
    elif required_view_flag:
        requiredheir = idea_core._requiredheirs.get(required_view_name)
        if requiredheir != None:
            # treenode_label += f"{get_terminus_node_from_road(requiredheir.base)}"
            grabed_sufffact = None
            for sufffact in requiredheir.sufffacts.values():
                grabed_sufffact = sufffact.need
            if grabed_sufffact not in [requiredheir.base, None]:
                grabed_sufffact = grabed_sufffact.replace(f"{requiredheir.base},", "")
                treenode_label += f" ({grabed_sufffact})"
    elif acptfactheir_view_flag and idea_core._walk != "":
        acptfactheir = idea_core._acptfactheirs.get(required_view_name)
        time_road = f"{src_agent._idearoot._desc},time,jajatime"
        if acptfactheir != None:
            if (
                acptfactheir.base == time_road
                and acptfactheir.open != None
                and acptfactheir.nigh != None
            ):
                hc_open_str = src_agent.get_jajatime_readable_one_time_event(
                    jajatime_min=acptfactheir.open
                )
                hc_nigh_str = src_agent.get_jajatime_readable_one_time_event(
                    jajatime_min=acptfactheir.nigh
                )
                # treenode_label += f"{get_terminus_node_from_road(acptfactheir.base)}"
                treenode_label += f" ({hc_open_str}-{hc_nigh_str})"
            elif (
                acptfactheir.base != time_road
                and acptfactheir.open != None
                and acptfactheir.nigh != None
            ):
                treenode_label += f" ({acptfactheir.open}-{acptfactheir.nigh})"

    elif yo_action_flag and idea_core.action:
        treenode_label += " (task)" if idea_core._task else " (state)"
    elif yo_acptfactunit_count_flag:
        treenode_label += f" ({len(idea_core._acptfactunits)})"
    elif yo_acptfactheir_count_flag and idea_core._walk != "":
        treenode_label += f" ({len(idea_core._acptfactheirs)})"

    if requiredheir_count_flag and idea_core._walk not in (None, ""):
        requiredunit_count = sum(
            str(type(requiredheir)) == "<class 'lib.agent.required.RequiredUnit'>"
            for requiredheir in idea_core._requiredheirs.values()
        )
        treenode_label += f" (RequiredHeirs {len(idea_core._requiredheirs)})"

    if yo_acptfactunit_time_flag:
        acptfactunit_time_obj = idea_core._acptfactunits.get(time_road)
        time_road = f"{src_agent._idearoot._desc},time,jajatime"
        if acptfactunit_time_obj != None:
            hc_open_str = src_agent.get_jajatime_readable_one_time_event(
                jajatime_min=acptfactunit_time_obj.open
            )
            hc_nigh_str = src_agent.get_jajatime_readable_one_time_event(
                jajatime_min=acptfactunit_time_obj.nigh
            )
            # treenode_label += f" ({acptfactunit.base=} {acptfactunit.open}-{acptfactunit.nigh})"
            treenode_label += f" ({hc_open_str}-{hc_nigh_str})"

    return treenode_label
