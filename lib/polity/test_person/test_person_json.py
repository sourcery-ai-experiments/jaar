import lib.polity.examples.example_persons as person_examples
from lib.polity.person import (
    get_from_json as get_person_from_json,
    agentlink_shop,
)
from lib.agent.x_func import x_is_json, x_get_dict
from json import loads as json_loads
from lib.polity.examples.person_env_tools import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from lib.agent.agent import AgentUnit


def test_person_receive_src_agentunit_obj_SetsCorrectInfo():
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2agent(env_dir=env_dir)
    assert len(person_x.get_agent_from_agents_dirlinks_dict()) == 2

    # WHEN
    swim_text = "swim1"
    person_x.receive_src_agentunit_obj(agent_x=AgentUnit(_desc=swim_text))
    run_text = "run1"
    person_x.receive_src_agentunit_obj(agent_x=AgentUnit(_desc=run_text))

    # THEN
    assert len(person_x.get_agent_from_agents_dirlinks_dict()) == 4


def test_person_get_agent_from_agents_dirlinks_dict_ReturnsCorrectInfo():
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2agent(env_dir=env_dir)
    assert len(person_x.get_agent_from_agents_dirlinks_dict()) == 2
    swim_text = "swim1"
    person_x.receive_src_agentunit_obj(agent_x=AgentUnit(_desc=swim_text))
    run_text = "run1"
    person_x.receive_src_agentunit_obj(agent_x=AgentUnit(_desc=run_text))

    # WHEN
    src_agentlinks_dict = person_x.get_agent_from_agents_dirlinks_dict()

    # THEN
    assert len(src_agentlinks_dict) == 4
    swim_dict = src_agentlinks_dict.get(swim_text)
    assert str(type(swim_dict)) == "<class 'dict'>"
    assert len(swim_dict) > 1
    assert swim_dict.get("agent_desc") == swim_text
    assert swim_dict.get("link_type") == "blind_trust"


def test_person_get_dict_ReturnsDictObject(person_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2agent(env_dir=env_dir)
    person_x.receive_src_agentunit_obj(agent_x=AgentUnit(_desc="swim8"))

    # WHEN
    x_dict = person_x.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["name"] == person_x.name
    assert (
        x_dict["_auto_dest_agent_to_public_agent"]
        == person_x._auto_dest_agent_to_public_agent
    )
    assert x_dict["_env_dir"] == person_x._env_dir
    assert x_dict["_public_agents_dir"] == person_x._public_agents_dir
    assert x_dict["_digest_agents_dir"] == person_x._digest_agents_dir
    print("check internal obj attributes")
    for src_agent_desc, src_agent_obj in x_dict["_src_agentlinks"].items():
        print(f"{src_agent_desc=}")

    assert x_dict["_src_agentlinks"]["A"] != None
    assert x_dict["_src_agentlinks"]["J"] != None
    assert len(x_dict["_src_agentlinks"]) == 3
    assert x_dict["_src_agentlinks"] == person_x.get_agent_from_agents_dirlinks_dict()
    assert len(person_x.get_agent_from_agents_dirlinks_dict()) == 3

    assert x_dict["_dest_agent"] == person_x._dest_agent.get_dict()


def test_person_export_to_JSON_simple_example_works(person_dir_setup_cleanup):
    x_json = None
    env_dir = get_temp_person_dir()
    x_person = person_examples.get_person_2agent(env_dir=env_dir)

    assert x_json is None
    x_json = x_person.get_json()
    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)
    # print(x_dict)
    assert x_dict["name"] == x_person.name
    assert x_dict["_env_dir"] == x_person._env_dir
    assert x_dict["_public_agents_dir"] == x_person._public_agents_dir
    assert x_dict["_digest_agents_dir"] == x_person._digest_agents_dir
    assert x_dict["_src_agentlinks"]["A"] != None
    assert x_dict["_src_agentlinks"]["J"] != None
    assert len(x_dict["_src_agentlinks"]) == 2
    assert x_dict["_src_agentlinks"] == x_person.get_agent_from_agents_dirlinks_dict()
    assert x_dict["_dest_agent"] == x_person._dest_agent.get_dict()


def test_person_get_json_CorrectlyWorksForSimpleExample(
    person_dir_setup_cleanup,
):
    # GIVEN
    x_json = None
    person_algo = person_examples.get_person_2agent(env_dir=get_temp_person_dir())

    # WHEN
    x_json = person_algo.get_json()

    # THEN
    assert x_is_json(x_json) == True

    # WHEN
    x_dict = x_get_dict(json_x=x_json)

    # THEN check x_dict

    # WHEN
    person_json = get_person_from_json(person_json=x_json)

    # THEN check json
    assert str(type(person_json)).find(".person.PersonUnit'>") > 0
    assert person_json.name != None
    assert person_json.name == person_algo.name
    assert (
        person_json._auto_dest_agent_to_public_agent
        == person_algo._auto_dest_agent_to_public_agent
    )
    assert person_json._env_dir == person_algo._env_dir
    assert person_json._public_agents_dir == person_algo._public_agents_dir
    assert person_json._digest_agents_dir == person_algo._digest_agents_dir
    assert person_json._person_dir != None
    assert len(person_json._src_agentlinks) == 2
    assert person_json._src_agentlinks.keys() == person_algo._src_agentlinks.keys()
    for algo_agentlink_x in person_algo._src_agentlinks.values():
        assert algo_agentlink_x == person_json._src_agentlinks.get(
            algo_agentlink_x.agent_desc
        )
    assert len(person_json._src_agentlinks) == len(person_algo._src_agentlinks)
    assert person_json._dest_agent == person_json._dest_agent
