from lib.agent.agent import AgentUnit, get_from_json as get_agent_from_json
from lib.polity.person import (
    PersonUnit,
    personunit_shop,
    get_from_json as get_person_from_json,
)
from lib.polity.agentlink import AgentLink
from dataclasses import dataclass
from lib.agent.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from sqlite3 import connect as sqlite3_connect, Connection
from lib.polity.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tally_table_delete_sqlstr,
    get_river_tally_table_insert_sqlstr,
    get_river_tally_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_agent_table_insert_sqlstr,
    get_river_ledger_unit,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    RiverTallyUnit,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    BrandUnitCatalog,
    get_brandunit_catalog_table_insert_sqlstr,
    get_brandunit_catalog_dict,
)


@dataclass
class PolityUnit:
    name: str
    politys_dir: str
    _personunits: dict[str:PersonUnit] = None
    _bank_db = None

    # figure out who is paying taxes and how much
    def set_river_sphere_for_agent(self, agent_name: str, max_flows_count: int = None):
        self._clear_all_source_river_data(agent_name)
        general_bucket = [self._get_root_river_ledger_unit(agent_name)]

        if max_flows_count is None:
            max_flows_count = 40

        flows_count = 0
        while flows_count < max_flows_count and general_bucket != []:
            parent_agent_ledger = general_bucket.pop(0)

            parent_range = parent_agent_ledger.get_range()
            parent_close = parent_agent_ledger.currency_cease
            curr_onset = parent_agent_ledger.currency_onset

            ledgers_len = len(parent_agent_ledger._ledgers.values())
            ledgers_count = 0
            for led_x in parent_agent_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * led_x._agent_agenda_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_agent_name=agent_name,
                    src_name=led_x.agent_name,
                    dst_name=led_x.ally_name,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_agent_ledger.flow_num,
                    river_tree_level=parent_agent_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

        self._set_river_tallys_buckets(agent_name)

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, agent_name: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(agent_name)
            mstr_s = get_river_tally_table_delete_sqlstr(agent_name)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, agent_name: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_agent_name=agent_name,
            src_name=None,
            dst_name=agent_name,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tallys_buckets(self, agent_name: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tally_table_insert_sqlstr(agent_name))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(agent_name))

            sal_river_tallys = get_river_tally_dict(bank_conn, agent_name)
            agent_x = self.get_agent_from_agents_dir(_desc=agent_name)
            agent_x.set_banking_attr_allyunits(sal_river_tallys)
            self.save_agentunit_obj_to_agents_dir(agent_x=agent_x)

    def get_river_tallys(self, agent_name: str) -> dict[str:RiverTallyUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tallys = get_river_tally_dict(bank_conn, agent_name)
        return river_tallys

    def refresh_bank_metrics(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        # Go to each agent file in agents dir
        # Load agent,
        # agent: run "set_agent_metrics"
        # grab agent relevant metrics
        for file_name in self.get_agents_dir_file_names_list():
            agent_json = x_func_open_file(self.get_agents_dir(), file_name)
            agentunit_x = get_agent_from_json(lw_json=agent_json)
            agentunit_x.set_agent_metrics()

            self._bank_insert_agentunit(agentunit_x)
            self._bank_insert_allyunit(agentunit_x)
            self._bank_insert_brandunit(agentunit_x)
            self._bank_insert_ideaunit(agentunit_x)
            self._bank_insert_acptfact(agentunit_x)

        for buc in get_brandunit_catalog_dict(self.get_bank_conn()).values():
            if buc.allylinks_set_by_polity_road != None:
                print(f"{buc.allylinks_set_by_polity_road=}")
            print(f"{buc=}")

    def _bank_insert_agentunit(self, agentunit_x: AgentUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_agent_table_insert_sqlstr(agent_x=agentunit_x))

    def _bank_insert_allyunit(self, agentunit_x: AgentUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for allyunit_x in agentunit_x._allys.values():
                sqlstr = get_ledger_table_insert_sqlstr(agentunit_x, allyunit_x)
                cur.execute(sqlstr)

    def _bank_insert_brandunit(self, agentunit_x: AgentUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for brandunit_x in agentunit_x._brands.values():
                brandunit_catalog_x = BrandUnitCatalog(
                    agent_name=agentunit_x._desc,
                    brandunit_name=brandunit_x.name,
                    allylinks_set_by_polity_road=brandunit_x._allylinks_set_by_polity_road,
                )
                sqlstr = get_brandunit_catalog_table_insert_sqlstr(brandunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, agentunit_x: AgentUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in agentunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(agentunit_x._desc, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, agentunit_x: AgentUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in agentunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    agent_name=agentunit_x._desc,
                    base=acptfact_x.base,
                    pick=acptfact_x.pick,
                )
                sqlstr = get_acptfact_catalog_table_insert_sqlstr(acptfact_catalog_x)
                cur.execute(sqlstr)

    def get_bank_conn(self) -> Connection:
        if self._bank_db is None:
            return sqlite3_connect(self.get_bank_db_path())
        else:
            return self._bank_db

    def _create_bank_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        if overwrite:
            self._delete_bank()

        bank_file_new = True
        if in_memory:
            self._bank_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_bank_db_path())

        if bank_file_new:
            with self.get_bank_conn() as bank_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    bank_conn.execute(sqlstr)

    def _delete_bank(self):
        self._bank_db = None
        x_func_delete_dir(dir=self.get_bank_db_path())

    def set_polityunit_name(self, name: str):
        self.name = name

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.politys_dir}/{self.name}"

    def _create_main_file_if_null(self, x_dir):
        polity_file_name = "polity.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_name=polity_file_name,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        polity_dir = self.get_object_root_dir()
        agents_dir = self.get_agents_dir()
        persons_dir = self.get_persons_dir()
        single_dir_create_if_null(x_path=polity_dir)
        single_dir_create_if_null(x_path=agents_dir)
        single_dir_create_if_null(x_path=persons_dir)
        self._create_main_file_if_null(x_dir=polity_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # PersonUnit management
    def get_persons_dir(self):
        return f"{self.get_object_root_dir()}/persons"

    def get_person_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_persons_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_personunits_empty_if_null(self):
        if self._personunits is None:
            self._personunits = {}

    def create_new_personunit(self, person_name: str):
        self.set_personunits_empty_if_null()
        px = personunit_shop(name=person_name, env_dir=self.get_object_root_dir())
        px.create_core_dir_and_files()
        self._personunits[px.name] = px

    def get_person_obj_from_polity(self, name: str) -> PersonUnit:
        return None if self._personunits.get(name) is None else self._personunits[name]

    def get_person_obj_from_file(self, name: str) -> PersonUnit:
        person_json = x_func_open_file(
            dest_dir=f"{self.get_persons_dir()}/{name}", file_name=f"{name}.json"
        )
        return get_person_from_json(person_json=person_json)

    def load_personunit(self, name: str):
        person_x = self.get_person_obj_from_file(name=name)
        self.set_personunits_empty_if_null()
        self.set_personunit_to_polity(person_x)

    def set_personunit_to_polity(self, person: PersonUnit):
        self._personunits[person.name] = person
        self.save_person_file(person_name=person.name)

    def save_person_file(self, person_name: str):
        person_x = self.get_person_obj_from_polity(name=person_name)
        x_func_save_file(
            dest_dir=person_x._person_dir,
            file_name=person_x.get_person_file_name(),
            file_text=person_x.get_json(),
        )

    def rename_personunit(self, old_name: str, new_name: str):
        person_x = self.get_person_obj_from_polity(name=old_name)
        old_person_dir = person_x._person_dir
        person_x.set_person_name(new_name=new_name)
        self.set_personunit_to_polity(person=person_x)
        x_func_delete_dir(old_person_dir)
        self.del_person_from_polity(person_name=old_name)

    def del_person_from_polity(self, person_name):
        self._personunits.pop(person_name)

    def del_person_dir(self, person_name: str):
        x_func_delete_dir(f"{self.get_persons_dir()}/{person_name}")

    # agents_dir management
    def get_agents_dir(self):
        return f"{self.get_object_root_dir()}/agents"

    def get_ignores_dir(self, person_name: str):
        return f"{self.get_persons_dir()}/{person_name}/ignores"

    def get_agent_from_agents_dir(self, _desc: str) -> AgentUnit:
        return get_agent_from_json(
            x_func_open_file(dest_dir=self.get_agents_dir(), file_name=f"{_desc}.json")
        )

    def get_agent_from_ignores_dir(self, person_name: str, _desc: str) -> AgentUnit:
        return get_agent_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(person_name=person_name),
                file_name=f"{_desc}.json",
            )
        )

    def set_ignore_agent_file(self, person_name: str, agent_obj: AgentUnit):
        person_x = self.get_person_obj_from_polity(name=person_name)
        person_x.set_ignore_agent_file(
            agentunit=agent_obj, src_agent_desc=agent_obj._desc
        )

    def rename_agent_in_agents_dir(self, old_desc: str, new_desc: str):
        agent_x = self.get_agent_from_agents_dir(_desc=old_desc)
        agent_x.agent_and_idearoot_desc_edit(new_desc=new_desc)
        self.save_agentunit_obj_to_agents_dir(agent_x=agent_x)
        self.del_agentunit_from_agents_dir(agent_x_desc=old_desc)

    def del_agentunit_from_agents_dir(self, agent_x_desc: str):
        x_func_delete_dir(f"{self.get_agents_dir()}/{agent_x_desc}.json")

    def save_agentunit_obj_to_agents_dir(self, agent_x: AgentUnit):
        x_func_save_file(
            dest_dir=self.get_agents_dir(),
            file_name=f"{agent_x._desc}.json",
            file_text=agent_x.get_json(),
        )

    def reload_all_persons_src_agentunits(self):
        for person_x in self._personunits.values():
            person_x.receive_all_src_agentunit_files()

    def get_agents_dir_file_names_list(self):
        return list(x_func_dir_files(dir_path=self.get_agents_dir()).keys())

    def get_agents_dir_list_of_obj(self):
        agents_list = []

        for file_name in self.get_agents_dir_file_names_list():
            agent_json = x_func_open_file(
                dest_dir=self.get_agents_dir(), file_name=file_name
            )
            agents_list.append(get_agent_from_json(lw_json=agent_json))

        return agents_list

    # agents_dir to person_agents_dir management
    def _person_receive_src_agentunit_obj(
        self,
        personunit: PersonUnit,
        agentunit: AgentUnit,
        link_type: str = None,
        weight: float = None,
        ignore_agent: AgentUnit = None,
    ):
        personunit.receive_src_agentunit_obj(
            agent_x=agentunit, link_type=link_type, agentlink_weight=weight
        )
        if link_type == "ignore" and ignore_agent != None:
            personunit.set_ignore_agent_file(
                agentunit=ignore_agent, src_agent_desc=agentunit._desc
            )

    def _person_delete_src_agentunit_obj(
        self, personunit: PersonUnit, agentunit_desc: str
    ):
        personunit.delete_agentlink(agent_desc=agentunit_desc)

    def create_agentlink_to_saved_agent(
        self,
        person_name: str,
        agent_desc: str,
        link_type: str = None,
        weight: float = None,
        ignore_agent: AgentUnit = None,
    ):
        person_x = self.get_person_obj_from_polity(name=person_name)
        agent_x = self.get_agent_from_agents_dir(_desc=agent_desc)
        self._person_receive_src_agentunit_obj(
            personunit=person_x,
            agentunit=agent_x,
            link_type=link_type,
            weight=weight,
            ignore_agent=ignore_agent,
        )

    def create_agentlink_to_generated_agent(
        self,
        person_name: str,
        agent_desc: str,
        link_type: str = None,
        weight: float = None,
    ):
        person_x = self.get_person_obj_from_polity(name=person_name)
        agent_x = AgentUnit(_desc=agent_desc)
        self._person_receive_src_agentunit_obj(
            personunit=person_x, agentunit=agent_x, link_type=link_type, weight=weight
        )

    def update_agentlink(self, person_name: str, agentlink: AgentLink):
        person_x = self.get_person_obj_from_polity(name=person_name)
        agent_x = self.get_agent_from_agents_dir(_desc=agentlink.agent_desc)
        self._person_receive_src_agentunit_obj(
            personunit=person_x,
            agentunit=agent_x,
            link_type=agentlink.link_type,
            weight=agentlink.weight,
        )

    def del_agentlink(self, person_name: str, agentunit_desc: str):
        person_x = self.get_person_obj_from_polity(name=person_name)
        agent_x = self.get_agent_from_agents_dir(_desc=agentunit_desc)
        self._person_delete_src_agentunit_obj(
            personunit=person_x,
            agentunit_desc=agentunit_desc,
        )

    # Person dest_agent
    def get_person_dest_agent_from_digest_agent_files(
        self, person_name: str
    ) -> AgentUnit:
        person_x = self.get_person_obj_from_polity(name=person_name)
        return person_x.get_dest_agent_from_digest_agent_files()
