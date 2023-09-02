from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.system.person import personunit_shop
from src.calendar.required_idea import Road
from random import randrange


def get_1node_calendar():
    a_text = "A"
    calendar_x = CalendarUnit(_owner=a_text)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_Jnode2node_calendar():
    src_text = "J"
    src_road = Road(f"{src_text}")
    calendar_x = CalendarUnit(_owner=src_text)
    a_text = "A"
    idea_a = IdeaKid(_desc=a_text)
    calendar_x.add_idea(idea_kid=idea_a, walk=src_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_2node_calendar():
    src_text = "A"
    src_road = Road(f"{src_text}")
    b_text = "B"
    calendar_x = CalendarUnit(_owner=src_text)
    idea_b = IdeaKid(_desc=b_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=src_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_3node_calendar():
    a_text = "A"
    a_road = Road(a_text)
    calendar_x = CalendarUnit(_owner=a_text)
    b_text = "B"
    idea_b = IdeaKid(_desc=b_text)
    c_text = "C"
    idea_c = IdeaKid(_desc=c_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=a_road)
    calendar_x.add_idea(idea_kid=idea_c, walk=a_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_3node_D_E_F_calendar():
    a_text = "D"
    a_road = Road(a_text)
    calendar_x = CalendarUnit(_owner=a_text)
    b_text = "E"
    idea_b = IdeaKid(_desc=b_text)
    c_text = "F"
    idea_c = IdeaKid(_desc=c_text)
    calendar_x.add_idea(idea_kid=idea_b, walk=a_road)
    calendar_x.add_idea(idea_kid=idea_c, walk=a_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_6node_calendar():
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_d, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_e, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeInsertH_calendar():
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_h = IdeaKid(_desc="H")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_e, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_h, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_d, walk="A,C,H")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_5nodeHG_calendar():
    calendar_x = CalendarUnit(_owner="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_h = IdeaKid(_desc="H")
    idea_g = IdeaKid(_desc="G")
    calendar_x.add_idea(idea_kid=idea_b, walk="A")
    calendar_x.add_idea(idea_kid=idea_c, walk="A")
    calendar_x.add_idea(idea_kid=idea_h, walk="A,C")
    calendar_x.add_idea(idea_kid=idea_g, walk="A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeJRoot_calendar():
    calendar_x = CalendarUnit(_owner="J")
    idea_a = IdeaKid(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    calendar_x.add_idea(idea_kid=idea_a, walk="J")
    calendar_x.add_idea(idea_kid=idea_b, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_c, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_d, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_7nodeJRootWithH_calendar():
    calendar_x = CalendarUnit(_owner="J")
    idea_a = IdeaKid(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    idea_h = IdeaKid(_desc="H")
    calendar_x.add_idea(idea_kid=idea_a, walk="J")
    calendar_x.add_idea(idea_kid=idea_b, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_c, walk="J,A")
    calendar_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    calendar_x.add_idea(idea_kid=idea_h, walk="J,A,C")
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_person_2calendar(env_dir):
    person_name = "person1"
    wx = personunit_shop(
        name=person_name, env_dir=env_dir, _auto_dest_calendar_to_public_calendar=True
    )
    wx.receive_src_calendarunit_obj(
        calendar_x=get_1node_calendar(), link_type="blind_trust"
    )
    wx.receive_src_calendarunit_obj(
        calendar_x=get_Jnode2node_calendar(), link_type="blind_trust"
    )
    return wx


def get_calendar_2CleanNodesRandomWeights(_desc: str = None):
    desc_text = _desc if _desc != None else "ernie"
    calendar_x = CalendarUnit(_owner=desc_text)
    casa_text = "casa"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = IdeaKid(_desc=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    calendar_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    calendar_x.set_calendar_metrics()
    return calendar_x


def get_calendar_3CleanNodesRandomWeights(_desc: str = None):
    desc_text = _desc if _desc != None else "ernie"
    calendar_x = CalendarUnit(_owner=desc_text)
    casa_text = "casa"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = IdeaKid(_desc=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = IdeaKid(_desc=hallway_text, _weight=randrange(1, 50), promise=True)
    calendar_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    calendar_x.add_idea(idea_kid=hallway_idea, walk=casa_road)
    calendar_x.set_calendar_metrics()
    return calendar_x
