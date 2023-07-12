from lib.polity.agentlink import (
    agentlink_shop,
    get_agent_from_agents_dirlink_from_dict,
)
from pytest import raises as pytest_raises


def test_agentlink_exists():
    # GIVEN
    agent_text = "test1"
    blind_text = "blind_trust"
    weight_float = 42
    # WHEN
    slx = agentlink_shop(
        agent_desc=agent_text, link_type=blind_text, weight=weight_float
    )
    # THEN
    assert slx != None
    assert slx.agent_desc == agent_text
    assert slx.link_type == blind_text
    assert slx.weight == weight_float


def test_agentlink_shop_ifAttrNoneAutoFill():
    # GIVEN
    agent_text = "test1"
    blind_text = "blind_trust"

    # WHEN
    slx = agentlink_shop(agent_desc=agent_text, link_type=None, weight=None)

    # THEN
    assert slx != None
    assert slx.agent_desc == agent_text
    assert slx.link_type == blind_text
    assert slx.weight == 1


def test_agentlink_shop_checkAllowed_link_types():
    # GIVEN
    agent_text = "test1"
    link_types = {
        "blind_trust": None,
        "bond_filter": None,
        "tributary": None,
        "ignore": None,
    }

    # WHEN/THEN
    for link_type_x in link_types.keys():
        print(f"{link_type_x=} assert attempted.")
        assert agentlink_shop(agent_text, link_type_x).link_type == link_type_x
        print(f"{link_type_x=} assert succeeded.")


def test_agentlink_shop_raisesErrorIfByTypeIsEntered():
    # GIVEN
    agent_text = "test1"
    bad_type_text = "bad"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        agentlink_shop(agent_desc=agent_text, link_type=bad_type_text)
    assert (
        str(excinfo.value)
        == f"Agentlink '{agent_text}' cannot have type '{bad_type_text}'."
    )


def test_agentlink_get_dict_ReturnsDictObject():
    # GIVEN
    agent_text = "test1"
    blind_text = "blind_trust"
    weight_float = 29
    clx = agentlink_shop(
        agent_desc=agent_text, link_type=blind_text, weight=weight_float
    )

    # WHEN
    x_dict = clx.get_dict()

    # THEN
    assert x_dict == {
        "agent_desc": agent_text,
        "link_type": blind_text,
        "weight": weight_float,
    }


def test_get_agent_from_agents_dirlink_from_dict_ReturnsAgentLinkObject():
    # GIVEN
    agent_desc_title = "agent_desc"
    link_type_title = "link_type"
    weight_title = "weight"

    test1_desc_text = "test1"
    test1_link_text = "blind_trust"
    test1_weight_float = 12.4

    agentlink_dict = {
        agent_desc_title: test1_desc_text,
        link_type_title: test1_link_text,
        weight_title: test1_weight_float,
    }

    # WHEN
    x_obj = get_agent_from_agents_dirlink_from_dict(x_dict=agentlink_dict)

    # THEN
    assert x_obj.agent_desc == test1_desc_text
    assert x_obj.link_type == test1_link_text
    assert x_obj.weight == test1_weight_float
