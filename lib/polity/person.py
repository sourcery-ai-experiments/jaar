from lib.polity.agentlink import (
    agentlink_shop,
    get_agent_from_agents_dirlink_from_dict,
    AgentLink,
    get_agentlink_types,
)
from lib.agent.agent import (
    get_from_json as agentunit_get_from_json,
    get_dict_of_agent_from_dict,
    get_meld_of_agent_files,
)
from lib.agent.idea import IdeaRoot
from lib.agent.road import Road
from lib.agent.agent import AgentUnit, get_from_json as agentunit_get_from_json
from lib.agent.x_func import (
    x_get_json,
    single_dir_create_if_null,
    rename_dir,
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


class InvalidPersonException(Exception):
    pass


@dataclass
class PersonUnit:
    name: str
    _env_dir: str = None
    _person_dir: str = None
    _public_agents_dir: str = None
    _person_agents_dir: str = None
    _ignore_agents_dir: str = None
    _bond_agents_dir: str = None
    _digest_agents_dir: str = None
    _person_file_path: str = None
    _src_agentlinks: dict[str:AgentUnit] = None
    _dest_agent: AgentUnit = None
    _auto_dest_agent_to_public_agent: bool = None

    # dir methods
    def _set_env_dir(self, env_dir: str):
        self._env_dir = env_dir
        self._set_person_dir()
        self._set_agents_dir()

    def _set_agents_dir(self):
        self._public_agents_dir = f"{self._env_dir}/agents"

    def _set_person_dir(self):
        self._person_dir = f"{self._env_dir}/persons/{self.name}"
        self._set_person_agents_dir()
        self._set_digest_agents_dir()
        self._set_ignore_agents_dir()
        self._set_bond_agents_dir()
        self._set_person_file_path()

    def _set_person_agents_dir(self):
        self._person_agents_dir = f"{self._person_dir}/agents"

    def get_starting_digest_agent_file_name(self):
        return "starting_digest_agent.json"

    def _set_digest_agents_dir(self):
        self._digest_agents_dir = f"{self._person_dir}/digests"

    def _set_ignore_agents_dir(self):
        self._ignore_agents_dir = f"{self._person_dir}/ignores"

    def _set_bond_agents_dir(self):
        self._bond_agents_dir = f"{self._person_dir}/bonds"

    def _set_person_file_path(self) -> str:
        self._person_file_path = f"{self._person_dir}/{self.get_person_file_name()}"

    def get_person_file_name(self) -> str:
        return f"{self.name}.json"

    def create_core_dir_and_files(self):
        single_dir_create_if_null(x_path=self._person_dir)
        single_dir_create_if_null(x_path=self._public_agents_dir)
        single_dir_create_if_null(x_path=self._person_agents_dir)
        single_dir_create_if_null(x_path=self._digest_agents_dir)
        single_dir_create_if_null(x_path=self._ignore_agents_dir)
        single_dir_create_if_null(x_path=self._bond_agents_dir)
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name=self.get_person_file_name(),
            file_text=self.get_json(),
            replace=False,
        )

    def set_person_name(self, new_name: str):
        old_name = self.name
        old_person_dir = self._person_dir
        self.name = new_name
        self._set_person_dir()
        old_person_dir_file_path = f"{self._person_dir}/{old_name}.json"

        rename_dir(src=old_person_dir, dst=self._person_dir)
        rename_dir(src=old_person_dir_file_path, dst=self._person_file_path)

    def receive_src_agentunit_obj(
        self, agent_x: AgentUnit, link_type: str = None, agentlink_weight: float = None
    ):
        x_func_save_file(
            dest_dir=self._person_agents_dir,
            file_name=f"{agent_x._desc}.json",
            file_text=agent_x.get_json(),
        )
        self._set_src_agentlinks(
            agent_desc=agent_x._desc, link_type=link_type, weight=agentlink_weight
        )

    def receive_src_agentunit_file(
        self, agent_json: str, link_type: str = None, weight: float = None
    ):
        agent_x = agentunit_get_from_json(lw_json=agent_json)
        self.receive_src_agentunit_obj(
            agent_x=agent_x, link_type=link_type, agentlink_weight=weight
        )

    def receive_all_src_agentunit_files(self):
        for agentlink_obj in self._src_agentlinks.values():
            file_name_x = f"{agentlink_obj.agent_desc}.json"
            agent_json = x_func_open_file(self._public_agents_dir, file_name_x)
            self.receive_src_agentunit_file(
                agent_json=agent_json,
                link_type=agentlink_obj.link_type,
                weight=agentlink_obj.weight,
            )

    def _set_src_agentlinks(
        self, agent_desc: str, link_type: str = None, weight: float = None
    ):
        self._set_src_agentlinks_empty_if_null()
        cx_file_name = f"{agent_desc}.json"
        cx_file_path = f"{self._person_agents_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidPersonException(
                f"Person {self.name} cannot find agent {agent_desc}"
            )

        # if not agentlink_x.link_type in list(get_agentlink_types().keys()):
        #     raise Exception(f"{agentlink_x.link_type=} not allowed.")
        agentlink_x = agentlink_shop(
            agent_desc=agent_desc, link_type=link_type, weight=weight
        )

        # if self._src_agentlinks.get(agent_desc) is None:
        #     self._src_agentlinks[agent_desc] = agentlink_x
        # elif self._src_agentlinks.get(agent_desc) != None:
        #     self._src_agentlinks[agent_desc] = agentlink_x
        self._src_agentlinks[agent_desc] = agentlink_x

        if agentlink_x.link_type == "blind_trust":
            cx_json = x_func_open_file(self._person_agents_dir, cx_file_name)
            cx_obj = agentunit_get_from_json(lw_json=cx_json)
            self._save_digest_agent_file(agentunit=cx_obj, src_agent_desc=cx_obj._desc)
        elif agentlink_x.link_type == "ignore":
            new_cx_obj = AgentUnit(_desc=agent_desc)
            self.set_ignore_agent_file(new_cx_obj, new_cx_obj._desc)

    def _set_src_agentlinks_empty_if_null(self):
        if self._src_agentlinks is None:
            self._src_agentlinks = {}

    def delete_agentlink(self, agent_desc: str):
        self._src_agentlinks.pop(agent_desc)
        x_func_delete_dir(dir=f"{self._person_agents_dir}/{agent_desc}.json")
        x_func_delete_dir(dir=f"{self._digest_agents_dir}/{agent_desc}.json")

    def _set_auto_dest_agent_to_public_agent(
        self, _auto_dest_agent_to_public_agent: bool
    ):
        self._auto_dest_agent_to_public_agent = _auto_dest_agent_to_public_agent

    def _set_emtpy_dest_agent(self):
        self._dest_agent = AgentUnit(_desc="")

    def get_dest_agent_from_digest_agent_files(self) -> AgentUnit:
        return get_meld_of_agent_files(
            agentunit=self.get_starting_digest_agent(),
            dir=self._digest_agents_dir,
        )

    def set_dest_agent_to_public_agent(self):
        dest_agent = self.get_dest_agent_from_digest_agent_files()
        self._save_public_agent_file(agentunit=dest_agent)

    def get_ignore_agent_from_ignore_agent_files(self, _desc: str) -> AgentUnit:
        file_name_x = f"{_desc}.json"
        agent_json = x_func_open_file(self._ignore_agents_dir, file_name_x)
        agent_obj = agentunit_get_from_json(lw_json=agent_json)
        agent_obj.set_agent_metrics()
        return agent_obj

    def set_ignore_agent_file(self, agentunit: AgentUnit, src_agent_desc: str):
        self._save_ignore_agent_file(agentunit, src_agent_desc)
        cx_file_name = f"{src_agent_desc}.json"
        cx_2_json = x_func_open_file(self._ignore_agents_dir, cx_file_name)
        cx_2_obj = agentunit_get_from_json(lw_json=cx_2_json)
        self._save_digest_agent_file(agentunit=cx_2_obj, src_agent_desc=src_agent_desc)

    def _save_ignore_agent_file(self, agentunit: AgentUnit, src_agent_desc: str):
        file_name = f"{src_agent_desc}.json"
        x_func_save_file(
            dest_dir=self._ignore_agents_dir,
            file_name=file_name,
            file_text=agentunit.get_json(),
            replace=True,
        )

    def _save_digest_agent_file(self, agentunit: AgentUnit, src_agent_desc: str):
        file_name = f"{src_agent_desc}.json"
        x_func_save_file(
            dest_dir=self._digest_agents_dir,
            file_name=file_name,
            file_text=agentunit.get_json(),
            replace=True,
        )

        if self._auto_dest_agent_to_public_agent:
            self.set_dest_agent_to_public_agent()

    def _save_public_agent_file(self, agentunit: AgentUnit):
        file_name = f"{agentunit._desc}.json"
        x_func_save_file(
            dest_dir=self._public_agents_dir,
            file_name=file_name,
            file_text=agentunit.get_json(),
            replace=True,
        )

    def get_starting_digest_agent(self) -> AgentUnit:
        cx = None
        try:
            ct = x_func_open_file(self._person_dir, "starting_digest_agent.json")
            cx = agentunit_get_from_json(lw_json=ct)
            empty_cx = self._get_empty_starting_digest_agent()
            cx.agent_and_idearoot_desc_edit(new_desc=empty_cx._desc)
            cx.set_agent_metrics()
        except Exception:
            cx = self._get_empty_starting_digest_agent()
            cx.set_agent_metrics()
        return cx

    def _get_empty_starting_digest_agent(self):
        return AgentUnit(_desc=self.name, _weight=0)

    def set_starting_digest_agent(self, agentunit: AgentUnit):
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name="starting_digest_agent.json",
            file_text=agentunit.get_json(),
            replace=True,
        )

    def del_starting_digest_agent_file(self):
        file_path = f"{self._person_dir}/{self.get_starting_digest_agent_file_name()}"
        x_func_delete_dir(dir=file_path)

    def get_dict(self):
        return {
            "name": self.name,
            "_env_dir": self._env_dir,
            "_person_dir": self._person_dir,
            "_public_agents_dir": self._public_agents_dir,
            "_digest_agents_dir": self._digest_agents_dir,
            "_src_agentlinks": self.get_agent_from_agents_dirlinks_dict(),
            "_dest_agent": self._dest_agent.get_dict(),
            "_auto_dest_agent_to_public_agent": self._auto_dest_agent_to_public_agent,
        }

    def get_agent_from_agents_dirlinks_dict(self) -> dict[str:dict]:
        src_agentlinks_dict = {}
        for agentlink_x in self._src_agentlinks.values():
            single_x_dict = agentlink_x.get_dict()
            src_agentlinks_dict[single_x_dict["agent_desc"]] = single_x_dict
        return src_agentlinks_dict

    def get_json(self):
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)


def get_from_json(person_json: str) -> PersonUnit:
    return get_from_dict(person_dict=json_loads(person_json))


def get_from_dict(person_dict: dict) -> PersonUnit:
    wx = personunit_shop(
        name=person_dict["name"],
        env_dir=person_dict["_env_dir"],
        _auto_dest_agent_to_public_agent=person_dict[
            "_auto_dest_agent_to_public_agent"
        ],
    )
    wx._src_agentlinks = get_agent_from_agents_dirlinks_from_dict(
        person_dict["_src_agentlinks"]
    )
    return wx


def get_agent_from_agents_dirlinks_from_dict(x_dict: dict) -> dict[str:AgentLink]:
    _src_agentlinks = {}

    for agentlink_dict in x_dict.values():
        agentlink_obj = get_agent_from_agents_dirlink_from_dict(x_dict=agentlink_dict)
        _src_agentlinks[agentlink_obj.agent_desc] = agentlink_obj
    return _src_agentlinks


def personunit_shop(
    name: str, env_dir: str, _auto_dest_agent_to_public_agent: bool = None
) -> PersonUnit:
    person_x = PersonUnit(name=name)
    person_x._set_env_dir(env_dir=env_dir)
    person_x._set_auto_dest_agent_to_public_agent(_auto_dest_agent_to_public_agent)
    person_x._set_src_agentlinks_empty_if_null()
    person_x._set_emtpy_dest_agent()
    return person_x
