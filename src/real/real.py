from src._instrument.file import set_dir, delete_dir, dir_files
from src._road.jaar_config import get_gifts_folder
from src._road.finance import default_pixel_if_none, default_penny_if_none
from src._road.road import default_road_delimiter_if_none, OwnerID, RoadUnit, RealID
from src._world.world import WorldUnit
from src.listen.basis_worlds import get_default_live_world
from src.listen.userhub import userhub_shop, UserHub
from src.listen.listen import (
    listen_to_speaker_agenda,
    listen_to_debtors_roll_same_live,
    listen_to_debtors_roll_role_job,
    create_job_file_from_role_file,
)
from src.real.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


@dataclass
class RealUnit:
    """Data pipelines:
    pipeline1: gifts->same
    pipeline2: same->roles
    pipeline3: role->job
    pipeline4: job->live
    pipeline5: same->live (direct)
    pipeline6: same->job->live (through jobs)
    pipeline7: gifts->live (could be 5 of 6)
    """

    real_id: RealID
    reals_dir: str
    _real_dir: str = None
    _owners_dir: str = None
    _journal_db: str = None
    _gifts_dir: str = None
    _road_delimiter: str = None
    _pixel: float = None
    _penny: float = None

    # directory setup
    def _set_real_dirs(self, in_memory_journal: bool = None):
        self._real_dir = f"{self.reals_dir}/{self.real_id}"
        self._owners_dir = f"{self._real_dir}/owners"
        self._gifts_dir = f"{self._real_dir}/{get_gifts_folder()}"
        set_dir(x_path=self._real_dir)
        set_dir(x_path=self._owners_dir)
        set_dir(x_path=self._gifts_dir)
        self._create_journal_db(in_memory=in_memory_journal)

    def _get_owner_dir(self, owner_id):
        return f"{self._owners_dir}/{owner_id}"

    def _get_owner_folder_names(self) -> set:
        owners = dir_files(self._owners_dir, include_dirs=True, include_files=False)
        return set(owners.keys())

    def get_owner_userhubs(self) -> dict[OwnerID:UserHub]:
        x_owner_ids = self._get_owner_folder_names()
        return {
            x_owner_id: userhub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                owner_id=x_owner_id,
                econ_road=None,
                road_delimiter=self._road_delimiter,
                pixel=self._pixel,
            )
            for x_owner_id in x_owner_ids
        }

    # database
    def get_journal_db_path(self) -> str:
        return f"{self.reals_dir}/{self.real_id}/journal.db"

    def _create_journal_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        journal_file_new = False
        if overwrite:
            journal_file_new = True
            self._delete_journal()

        if in_memory:
            if self._journal_db is None:
                journal_file_new = True
            self._journal_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_journal_db_path())

        if journal_file_new:
            with self.get_journal_conn() as journal_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    journal_conn.execute(sqlstr)

    def _delete_journal(self):
        self._journal_db = None
        delete_dir(dir=self.get_journal_db_path())

    def get_journal_conn(self) -> Connection:
        if self._journal_db is None:
            return sqlite3_connect(self.get_journal_db_path())
        else:
            return self._journal_db

    # owner management
    def _get_userhub(self, owner_id: OwnerID) -> UserHub:
        return userhub_shop(
            owner_id=owner_id,
            real_id=self.real_id,
            reals_dir=self.reals_dir,
            econ_road=None,
            road_delimiter=self._road_delimiter,
            pixel=self._pixel,
        )

    def init_owner_econs(self, owner_id: OwnerID):
        x_userhub = self._get_userhub(owner_id)
        x_userhub.initialize_gift_same_files()
        x_userhub.initialize_live_file(self.get_owner_same_from_file(owner_id))

    def get_owner_same_from_file(self, owner_id: OwnerID) -> WorldUnit:
        return self._get_userhub(owner_id).get_same_world()

    def _set_all_healer_roles(self, owner_id: OwnerID):
        x_same = self.get_owner_same_from_file(owner_id)
        x_same.calc_world_metrics()
        for healer_id, healer_dict in x_same._healers_dict.items():
            healer_userhub = userhub_shop(
                self.reals_dir,
                self.real_id,
                healer_id,
                econ_road=None,
                # "role_job",
                road_delimiter=self._road_delimiter,
                pixel=self._pixel,
            )
            for econ_road in healer_dict.keys():
                self._set_owner_role(healer_userhub, econ_road, x_same)

    def _set_owner_role(
        self,
        healer_userhub: UserHub,
        econ_road: RoadUnit,
        same_world: WorldUnit,
    ):
        healer_userhub.econ_road = econ_road
        healer_userhub.create_treasury_db_file()
        healer_userhub.save_role_world(same_world)

    # live world management
    def generate_live_world(self, owner_id: OwnerID) -> WorldUnit:
        listener_userhub = self._get_userhub(owner_id)
        x_same = listener_userhub.get_same_world()
        x_same.calc_world_metrics()
        x_live = get_default_live_world(x_same)
        for healer_id, healer_dict in x_same._healers_dict.items():
            healer_userhub = userhub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                owner_id=healer_id,
                econ_road=None,
                # "role_job",
                road_delimiter=self._road_delimiter,
                pixel=self._pixel,
            )
            healer_userhub.create_same_treasury_db_files()
            for econ_road in healer_dict.keys():
                econ_userhub = userhub_shop(
                    reals_dir=self.reals_dir,
                    real_id=self.real_id,
                    owner_id=healer_id,
                    econ_road=econ_road,
                    # "role_job",
                    road_delimiter=self._road_delimiter,
                    pixel=self._pixel,
                )
                econ_userhub.save_role_world(x_same)
                create_job_file_from_role_file(econ_userhub, owner_id)
                x_job = econ_userhub.get_job_world(owner_id)
                listen_to_speaker_agenda(x_live, x_job)

        # if nothing has come from same->role->job->live pipeline use same->live pipeline
        x_live.calc_world_metrics()
        if len(x_live._idea_dict) == 1:
            # pipeline_same_live_text()
            listen_to_debtors_roll_same_live(listener_userhub)
            listener_userhub.open_file_live()
            x_live.calc_world_metrics()
        if len(x_live._idea_dict) == 1:
            x_live = x_same
        listener_userhub.save_live_world(x_live)

        return self.get_live_file_world(owner_id)

    def generate_all_live_worlds(self):
        for x_owner_id in self._get_owner_folder_names():
            self.generate_live_world(x_owner_id)

    def get_live_file_world(self, owner_id: OwnerID) -> WorldUnit:
        return self._get_userhub(owner_id).get_live_world()


def realunit_shop(
    real_id: RealID,
    reals_dir: str,
    in_memory_journal: bool = None,
    _road_delimiter: str = None,
    _pixel: float = None,
    _penny: float = None,
) -> RealUnit:
    real_x = RealUnit(
        real_id=real_id,
        reals_dir=reals_dir,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _pixel=default_pixel_if_none(_pixel),
        _penny=default_penny_if_none(_penny),
    )
    real_x._set_real_dirs(in_memory_journal=in_memory_journal)
    return real_x
