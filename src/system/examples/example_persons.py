from src.agent.agent import AgentUnit
from src.agent.idea import IdeaKid
from src.system.person import personunit_shop
from src.agent.required import Road
from random import randrange


def get_1node_agent():
    a_text = "A"
    agent_x = AgentUnit(_desc=a_text)
    agent_x.set_agent_metrics()
    return agent_x


def get_Jnode2node_agent():
    src_text = "J"
    src_road = Road(f"{src_text}")
    agent_x = AgentUnit(_desc=src_text)
    a_text = "A"
    idea_a = IdeaKid(_desc=a_text)
    agent_x.add_idea(idea_kid=idea_a, walk=src_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_2node_agent():
    src_text = "A"
    src_road = Road(f"{src_text}")
    b_text = "B"
    agent_x = AgentUnit(_desc=src_text)
    idea_b = IdeaKid(_desc=b_text)
    agent_x.add_idea(idea_kid=idea_b, walk=src_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_3node_agent():
    a_text = "A"
    a_road = Road(a_text)
    agent_x = AgentUnit(_desc=a_text)
    b_text = "B"
    idea_b = IdeaKid(_desc=b_text)
    c_text = "C"
    idea_c = IdeaKid(_desc=c_text)
    agent_x.add_idea(idea_kid=idea_b, walk=a_road)
    agent_x.add_idea(idea_kid=idea_c, walk=a_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_3node_D_E_F_agent():
    a_text = "D"
    a_road = Road(a_text)
    agent_x = AgentUnit(_desc=a_text)
    b_text = "E"
    idea_b = IdeaKid(_desc=b_text)
    c_text = "F"
    idea_c = IdeaKid(_desc=c_text)
    agent_x.add_idea(idea_kid=idea_b, walk=a_road)
    agent_x.add_idea(idea_kid=idea_c, walk=a_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_6node_agent():
    agent_x = AgentUnit(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    agent_x.add_idea(idea_kid=idea_b, walk="A")
    agent_x.add_idea(idea_kid=idea_c, walk="A")
    agent_x.add_idea(idea_kid=idea_d, walk="A,C")
    agent_x.add_idea(idea_kid=idea_e, walk="A,C")
    agent_x.add_idea(idea_kid=idea_f, walk="A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeInsertH_agent():
    agent_x = AgentUnit(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_h = IdeaKid(_desc="H")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    agent_x.add_idea(idea_kid=idea_b, walk="A")
    agent_x.add_idea(idea_kid=idea_c, walk="A")
    agent_x.add_idea(idea_kid=idea_e, walk="A,C")
    agent_x.add_idea(idea_kid=idea_f, walk="A,C")
    agent_x.add_idea(idea_kid=idea_h, walk="A,C")
    agent_x.add_idea(idea_kid=idea_d, walk="A,C,H")
    agent_x.set_agent_metrics()
    return agent_x


def get_5nodeHG_agent():
    agent_x = AgentUnit(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_h = IdeaKid(_desc="H")
    idea_g = IdeaKid(_desc="G")
    agent_x.add_idea(idea_kid=idea_b, walk="A")
    agent_x.add_idea(idea_kid=idea_c, walk="A")
    agent_x.add_idea(idea_kid=idea_h, walk="A,C")
    agent_x.add_idea(idea_kid=idea_g, walk="A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeJRoot_agent():
    agent_x = AgentUnit(_desc="J")
    idea_a = IdeaKid(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_d = IdeaKid(_desc="D")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    agent_x.add_idea(idea_kid=idea_a, walk="J")
    agent_x.add_idea(idea_kid=idea_b, walk="J,A")
    agent_x.add_idea(idea_kid=idea_c, walk="J,A")
    agent_x.add_idea(idea_kid=idea_d, walk="J,A,C")
    agent_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    agent_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeJRootWithH_agent():
    agent_x = AgentUnit(_desc="J")
    idea_a = IdeaKid(_desc="A")
    idea_b = IdeaKid(_desc="B")
    idea_c = IdeaKid(_desc="C")
    idea_e = IdeaKid(_desc="E")
    idea_f = IdeaKid(_desc="F")
    idea_h = IdeaKid(_desc="H")
    agent_x.add_idea(idea_kid=idea_a, walk="J")
    agent_x.add_idea(idea_kid=idea_b, walk="J,A")
    agent_x.add_idea(idea_kid=idea_c, walk="J,A")
    agent_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    agent_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    agent_x.add_idea(idea_kid=idea_h, walk="J,A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_person_2agent(env_dir):
    person_name = "person1"
    wx = personunit_shop(
        name=person_name, env_dir=env_dir, _auto_dest_agent_to_public_agent=True
    )
    wx.receive_src_agentunit_obj(agent_x=get_1node_agent(), link_type="blind_trust")
    wx.receive_src_agentunit_obj(
        agent_x=get_Jnode2node_agent(), link_type="blind_trust"
    )
    return wx


def get_agent_2CleanNodesRandomWeights(_desc: str = None):
    desc_text = _desc if _desc != None else "ernie"
    agent_x = AgentUnit(_desc=desc_text)
    casa_text = "casa"
    agent_x.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    kitchen_text = "clean kitchen"
    bedroom_text = "clean bedroom"
    kitchen_idea = IdeaKid(_desc=kitchen_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    agent_x.add_idea(idea_kid=kitchen_idea, walk=casa_road)
    agent_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_agent_3CleanNodesRandomWeights(_desc: str = None):
    desc_text = _desc if _desc != None else "ernie"
    agent_x = AgentUnit(_desc=desc_text)
    casa_text = "casa"
    agent_x.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    kitchen_text = "clean kitchen"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    kitchen_idea = IdeaKid(_desc=kitchen_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = IdeaKid(_desc=hallway_text, _weight=randrange(1, 50), promise=True)
    agent_x.add_idea(idea_kid=kitchen_idea, walk=casa_road)
    agent_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    agent_x.add_idea(idea_kid=hallway_idea, walk=casa_road)
    agent_x.set_agent_metrics()
    return agent_x
