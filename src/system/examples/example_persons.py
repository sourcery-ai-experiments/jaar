from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.required_assign import assigned_unit_shop
from src.system.person import personunit_shop, PersonUnit
from src.calendar.road import Road, get_global_root_label as root_label
from random import randrange


def get_1node_calendar() -> CalendarUnit:
    a_text = "A"
    calendar_x = CalendarUnit(_owner=a_text)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_Jnode2node_calendar() -> CalendarUnit:
    owner_text = "J"
    calendar_x = CalendarUnit(_owner=owner_text)
    a_text = "A"
    idea_a = IdeaKid(_label=a_text)
    calendar_x.add_idea(idea_kid=idea_a, walk=root_label())
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_2node_calendar() -> CalendarUnit:
    owner_text = "A"
    b_text = "B"
    calendar_x = CalendarUnit(_owner=owner_text)
    idea_b = IdeaKid(_label=b_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=root_label())
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_3node_calendar() -> CalendarUnit:
    a_text = "A"
    a_road = Road(a_text)
    calendar_x = CalendarUnit(_owner=a_text)
    b_text = "B"
    idea_b = IdeaKid(_label=b_text)
    c_text = "C"
    idea_c = IdeaKid(_label=c_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=a_road)
    calendar_x.add_idea(idea_kid=idea_c, walk=a_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_3node_D_E_F_calendar() -> CalendarUnit:
    d_text = "D"
    d_road = Road(d_text)
    calendar_x = CalendarUnit(_owner=d_text)
    b_text = "E"
    idea_b = IdeaKid(_label=b_text)
    c_text = "F"
    idea_c = IdeaKid(_label=c_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=d_road)
    calendar_x.add_idea(idea_kid=idea_c, walk=d_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_6node_calendar() -> CalendarUnit:
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_d, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_e, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeInsertH_calendar() -> CalendarUnit:
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_e, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_h, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_d, walk="A,C,H")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_5nodeHG_calendar() -> CalendarUnit:
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_g = IdeaKid(_label="G")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_h, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_g, walk="A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeJRoot_calendar() -> CalendarUnit:
    calendar_x = CalendarUnit(_owner="J")
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    calendar_x.add_idea(idea_kid=idea_a, walk="J")
    calendar_x.add_idea(idea_kid=idea_b, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_c, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_d, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeJRootWithH_calendar() -> CalendarUnit:
    calendar_x = CalendarUnit(_owner="J")
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    idea_h = IdeaKid(_label="H")
    calendar_x.add_idea(idea_kid=idea_a, walk="J")
    calendar_x.add_idea(idea_kid=idea_b, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_c, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_h, walk="J,A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_person_2calendar(env_dir) -> PersonUnit:
    yao_text = "Yao"
    yao_per = personunit_shop(yao_text, env_dir=env_dir, _auto_output_to_public=True)
    yao_per.set_depot_calendar(get_1node_calendar(), depotlink_type="blind_trust")
    yao_per.set_depot_calendar(get_Jnode2node_calendar(), depotlink_type="blind_trust")
    return yao_per


def get_calendar_2CleanNodesRandomWeights(_owner: str = None) -> CalendarUnit:
    label_text = _owner if _owner != None else "ernie"
    calendar_x = CalendarUnit(_owner=label_text)
    casa_text = "casa"
    calendar_x.add_idea(idea_kid=IdeaKid(_label=casa_text), walk="")
    casa_road = Road(f"{label_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    calendar_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_calendar_3CleanNodesRandomWeights(_owner: str = None) -> CalendarUnit:
    label_text = _owner if _owner != None else "ernie"
    calendar_x = CalendarUnit(_owner=label_text)
    casa_text = "casa"
    calendar_x.add_idea(idea_kid=IdeaKid(_label=casa_text), walk="")
    casa_road = Road(f"{label_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = IdeaKid(_label=hallway_text, _weight=randrange(1, 50), promise=True)
    calendar_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=hallway_idea, walk=casa_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_calendar_assignment_laundry_example1() -> CalendarUnit:
    america_text = "America"
    cx = CalendarUnit(_owner=america_text)
    joachim_text = "Joachim"
    cx.add_memberunit(america_text)
    cx.add_memberunit(joachim_text)

    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    cx.add_idea(IdeaKid(_label=casa_text), walk=root_label())

    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    cx.add_idea(IdeaKid(_label=basket_text), walk=casa_road)

    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    cx.add_idea(IdeaKid(_label=basket_text), walk=casa_road)

    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    cx.add_idea(IdeaKid(_label=basket_text), walk=casa_road)

    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    cx.add_idea(IdeaKid(_label=b_bare_text), walk=casa_road)

    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    cx.add_idea(IdeaKid(_label=b_fine_text), walk=casa_road)

    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    cx.add_idea(IdeaKid(_label=b_half_text), walk=casa_road)

    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    cx.add_idea(IdeaKid(_label=laundry_task_text, promise=True), walk=casa_road)

    # make laundry requirement
    cx.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_full_road
    )
    # make laundry requirement
    cx.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_smel_road
    )
    # assign Joachim to task
    joachim_assignunit = assigned_unit_shop()
    joachim_assignunit.set_suffgroup(joachim_text)
    cx.edit_idea_attr(road=laundry_task_road, assignedunit=joachim_assignunit)

    return cx
