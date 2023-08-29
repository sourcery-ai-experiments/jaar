from src.agent.agent import AgentUnit
from src.agent.tool import ToolKid
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
    tool_a = ToolKid(_desc=a_text)
    agent_x.add_tool(tool_kid=tool_a, walk=src_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_2node_agent():
    src_text = "A"
    src_road = Road(f"{src_text}")
    b_text = "B"
    agent_x = AgentUnit(_desc=src_text)
    tool_b = ToolKid(_desc=b_text)
    agent_x.add_tool(tool_kid=tool_b, walk=src_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_3node_agent():
    a_text = "A"
    a_road = Road(a_text)
    agent_x = AgentUnit(_desc=a_text)
    b_text = "B"
    tool_b = ToolKid(_desc=b_text)
    c_text = "C"
    tool_c = ToolKid(_desc=c_text)
    agent_x.add_tool(tool_kid=tool_b, walk=a_road)
    agent_x.add_tool(tool_kid=tool_c, walk=a_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_3node_D_E_F_agent():
    a_text = "D"
    a_road = Road(a_text)
    agent_x = AgentUnit(_desc=a_text)
    b_text = "E"
    tool_b = ToolKid(_desc=b_text)
    c_text = "F"
    tool_c = ToolKid(_desc=c_text)
    agent_x.add_tool(tool_kid=tool_b, walk=a_road)
    agent_x.add_tool(tool_kid=tool_c, walk=a_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_6node_agent():
    agent_x = AgentUnit(_desc="A")
    tool_b = ToolKid(_desc="B")
    tool_c = ToolKid(_desc="C")
    tool_d = ToolKid(_desc="D")
    tool_e = ToolKid(_desc="E")
    tool_f = ToolKid(_desc="F")
    agent_x.add_tool(tool_kid=tool_b, walk="A")
    agent_x.add_tool(tool_kid=tool_c, walk="A")
    agent_x.add_tool(tool_kid=tool_d, walk="A,C")
    agent_x.add_tool(tool_kid=tool_e, walk="A,C")
    agent_x.add_tool(tool_kid=tool_f, walk="A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeInsertH_agent():
    agent_x = AgentUnit(_desc="A")
    tool_b = ToolKid(_desc="B")
    tool_c = ToolKid(_desc="C")
    tool_h = ToolKid(_desc="H")
    tool_d = ToolKid(_desc="D")
    tool_e = ToolKid(_desc="E")
    tool_f = ToolKid(_desc="F")
    agent_x.add_tool(tool_kid=tool_b, walk="A")
    agent_x.add_tool(tool_kid=tool_c, walk="A")
    agent_x.add_tool(tool_kid=tool_e, walk="A,C")
    agent_x.add_tool(tool_kid=tool_f, walk="A,C")
    agent_x.add_tool(tool_kid=tool_h, walk="A,C")
    agent_x.add_tool(tool_kid=tool_d, walk="A,C,H")
    agent_x.set_agent_metrics()
    return agent_x


def get_5nodeHG_agent():
    agent_x = AgentUnit(_desc="A")
    tool_b = ToolKid(_desc="B")
    tool_c = ToolKid(_desc="C")
    tool_h = ToolKid(_desc="H")
    tool_g = ToolKid(_desc="G")
    agent_x.add_tool(tool_kid=tool_b, walk="A")
    agent_x.add_tool(tool_kid=tool_c, walk="A")
    agent_x.add_tool(tool_kid=tool_h, walk="A,C")
    agent_x.add_tool(tool_kid=tool_g, walk="A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeJRoot_agent():
    agent_x = AgentUnit(_desc="J")
    tool_a = ToolKid(_desc="A")
    tool_b = ToolKid(_desc="B")
    tool_c = ToolKid(_desc="C")
    tool_d = ToolKid(_desc="D")
    tool_e = ToolKid(_desc="E")
    tool_f = ToolKid(_desc="F")
    agent_x.add_tool(tool_kid=tool_a, walk="J")
    agent_x.add_tool(tool_kid=tool_b, walk="J,A")
    agent_x.add_tool(tool_kid=tool_c, walk="J,A")
    agent_x.add_tool(tool_kid=tool_d, walk="J,A,C")
    agent_x.add_tool(tool_kid=tool_e, walk="J,A,C")
    agent_x.add_tool(tool_kid=tool_f, walk="J,A,C")
    agent_x.set_agent_metrics()
    return agent_x


def get_7nodeJRootWithH_agent():
    agent_x = AgentUnit(_desc="J")
    tool_a = ToolKid(_desc="A")
    tool_b = ToolKid(_desc="B")
    tool_c = ToolKid(_desc="C")
    tool_e = ToolKid(_desc="E")
    tool_f = ToolKid(_desc="F")
    tool_h = ToolKid(_desc="H")
    agent_x.add_tool(tool_kid=tool_a, walk="J")
    agent_x.add_tool(tool_kid=tool_b, walk="J,A")
    agent_x.add_tool(tool_kid=tool_c, walk="J,A")
    agent_x.add_tool(tool_kid=tool_e, walk="J,A,C")
    agent_x.add_tool(tool_kid=tool_f, walk="J,A,C")
    agent_x.add_tool(tool_kid=tool_h, walk="J,A,C")
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
    agent_x.add_tool(tool_kid=ToolKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_tool = ToolKid(_desc=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_tool = ToolKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    agent_x.add_tool(tool_kid=cookery_tool, walk=casa_road)
    agent_x.add_tool(tool_kid=bedroom_tool, walk=casa_road)
    agent_x.set_agent_metrics()
    return agent_x


def get_agent_3CleanNodesRandomWeights(_desc: str = None):
    desc_text = _desc if _desc != None else "ernie"
    agent_x = AgentUnit(_desc=desc_text)
    casa_text = "casa"
    agent_x.add_tool(tool_kid=ToolKid(_desc=casa_text), walk="")
    casa_road = Road(f"{desc_text},{casa_text}")
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_tool = ToolKid(_desc=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_tool = ToolKid(_desc=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_tool = ToolKid(_desc=hallway_text, _weight=randrange(1, 50), promise=True)
    agent_x.add_tool(tool_kid=cookery_tool, walk=casa_road)
    agent_x.add_tool(tool_kid=bedroom_tool, walk=casa_road)
    agent_x.add_tool(tool_kid=hallway_tool, walk=casa_road)
    agent_x.set_agent_metrics()
    return agent_x
