from src._instrument.file import set_dir, delete_dir, dir_files
from src._road.jaar_config import get_gifts_folder
from src._road.finance import default_pixel_if_none, default_penny_if_none
from src._road.road import default_road_delimiter_if_none, OwnerID, RoadUnit, RealID
from src._world.world import WorldUnit
from src.listen.basis_worlds import get_default_being_world
from src.listen.hubunit import hubunit_shop, HubUnit
from src.listen.listen import (
    listen_to_speaker_agenda,
    listen_to_debtors_roll_suis_being,
    listen_to_debtors_roll_duty_job,
    create_job_file_from_duty_file,
)
from src.real.journal_sqlstr import get_create_table_if_not_exist_sqlstrs
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


@dataclass
class RealUnit:
    """Data pipelines:
    pipeline1: gifts->suis
    pipeline2: suis->dutys
    pipeline3: duty->job
    pipeline4: job->being
    pipeline5: suis->being (direct)
    pipeline6: suis->job->being (through jobs)
    pipeline7: gifts->being (could be 5 of 6)
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

    def get_owner_hubunits(self) -> dict[OwnerID:HubUnit]:
        x_owner_ids = self._get_owner_folder_names()
        return {
            x_owner_id: hubunit_shop(
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
    def _get_hubunit(self, owner_id: OwnerID) -> HubUnit:
        return hubunit_shop(
            owner_id=owner_id,
            real_id=self.real_id,
            reals_dir=self.reals_dir,
            econ_road=None,
            road_delimiter=self._road_delimiter,
            pixel=self._pixel,
        )

    def init_owner_econs(self, owner_id: OwnerID):
        x_hubunit = self._get_hubunit(owner_id)
        x_hubunit.initialize_gift_suis_files()
        x_hubunit.initialize_being_file(self.get_owner_suis_from_file(owner_id))

    def get_owner_suis_from_file(self, owner_id: OwnerID) -> WorldUnit:
        return self._get_hubunit(owner_id).get_suis_world()

    def _set_all_healer_dutys(self, owner_id: OwnerID):
        x_suis = self.get_owner_suis_from_file(owner_id)
        x_suis.calc_world_metrics()
        for healer_id, healer_dict in x_suis._healers_dict.items():
            healer_hubunit = hubunit_shop(
                self.reals_dir,
                self.real_id,
                healer_id,
                econ_road=None,
                # "duty_job",
                road_delimiter=self._road_delimiter,
                pixel=self._pixel,
            )
            for econ_road in healer_dict.keys():
                self._set_owner_duty(healer_hubunit, econ_road, x_suis)

    def _set_owner_duty(
        self,
        healer_hubunit: HubUnit,
        econ_road: RoadUnit,
        suis_world: WorldUnit,
    ):
        healer_hubunit.econ_road = econ_road
        healer_hubunit.create_treasury_db_file()
        healer_hubunit.save_duty_world(suis_world)

    # being world management
    def generate_being_world(self, owner_id: OwnerID) -> WorldUnit:
        listener_hubunit = self._get_hubunit(owner_id)
        x_suis = listener_hubunit.get_suis_world()
        x_suis.calc_world_metrics()
        x_being = get_default_being_world(x_suis)
        for healer_id, healer_dict in x_suis._healers_dict.items():
            healer_hubunit = hubunit_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                owner_id=healer_id,
                econ_road=None,
                # "duty_job",
                road_delimiter=self._road_delimiter,
                pixel=self._pixel,
            )
            healer_hubunit.create_suis_treasury_db_files()
            for econ_road in healer_dict.keys():
                econ_hubunit = hubunit_shop(
                    reals_dir=self.reals_dir,
                    real_id=self.real_id,
                    owner_id=healer_id,
                    econ_road=econ_road,
                    # "duty_job",
                    road_delimiter=self._road_delimiter,
                    pixel=self._pixel,
                )
                econ_hubunit.save_duty_world(x_suis)
                create_job_file_from_duty_file(econ_hubunit, owner_id)
                x_job = econ_hubunit.get_job_world(owner_id)
                listen_to_speaker_agenda(x_being, x_job)

        # if nothing has come from suis->duty->job->being pipeline use suis->being pipeline
        x_being.calc_world_metrics()
        if len(x_being._idea_dict) == 1:
            # pipeline_suis_being_text()
            listen_to_debtors_roll_suis_being(listener_hubunit)
            listener_hubunit.open_file_being()
            x_being.calc_world_metrics()
        if len(x_being._idea_dict) == 1:
            x_being = x_suis
        listener_hubunit.save_being_world(x_being)

        return self.get_being_file_world(owner_id)

    def generate_all_being_worlds(self):
        for x_owner_id in self._get_owner_folder_names():
            self.generate_being_world(x_owner_id)

    def get_being_file_world(self, owner_id: OwnerID) -> WorldUnit:
        return self._get_hubunit(owner_id).get_being_world()


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
