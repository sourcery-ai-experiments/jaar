from dataclasses import dataclass


@dataclass
class AgentLink:
    agent_desc: str
    link_type: str = None
    weight: float = None

    def set_link_type(self, link_type: str):
        if link_type not in (list(get_agentlink_types())):
            raise Exception(
                f"Agentlink '{self.agent_desc}' cannot have type '{link_type}'."
            )
        self.link_type = link_type

    def set_weight(self, weight: float):
        self.weight = weight

    def get_dict(self):
        return {
            "agent_desc": self.agent_desc,
            "link_type": self.link_type,
            "weight": self.weight,
        }


def agentlink_shop(
    agent_desc: str, link_type: str = None, weight: float = None
) -> AgentLink:
    if link_type is None:
        link_type = "blind_trust"
    if weight is None:
        weight = 1
    sl = AgentLink(agent_desc=agent_desc)
    sl.set_link_type(link_type=link_type)
    sl.set_weight(weight=weight)
    return sl


def get_agent_from_agents_dirlink_from_dict(x_dict: dict) -> AgentLink:
    agent_desc_text = "agent_desc"
    link_type_text = "link_type"
    weight_text = "weight"
    return agentlink_shop(
        agent_desc=x_dict[agent_desc_text],
        link_type=x_dict[link_type_text],
        weight=x_dict[weight_text],
    )


def get_agentlink_types() -> dict[str:None]:
    return {"blind_trust": None, "bond_filter": None, "tributary": None, "ignore": None}
