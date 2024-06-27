from src._road.road import OwnerID
from src._world.world import WorldUnit, get_from_json as world_get_from_json
from src._instrument.file import dir_files, open_file
from dataclasses import dataclass


@dataclass
class MeldeeOrderUnit:
    owner_id: OwnerID
    voice_rank: int
    voice_hx_lowest_rank: int
    file_name: str


def get_meldeeorderunit(
    primary_world: WorldUnit, meldee_file_name: str
) -> MeldeeOrderUnit:
    file_src_owner_id = meldee_file_name.replace(".json", "")
    primary_meldee_charunit = primary_world.get_char(file_src_owner_id)

    default_voice_rank = 0
    default_voice_hx_lowest_rank = 0
    if primary_meldee_charunit is None:
        primary_voice_rank_for_meldee = default_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank
    else:
        primary_voice_rank_for_meldee = primary_meldee_charunit._treasury_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = (
            primary_meldee_charunit._treasury_voice_hx_lowest_rank
        )
        if primary_voice_rank_for_meldee is None:
            primary_voice_rank_for_meldee = default_voice_rank
            primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank

    return MeldeeOrderUnit(
        owner_id=file_src_owner_id,
        voice_rank=primary_voice_rank_for_meldee,
        voice_hx_lowest_rank=primary_voice_hx_lowest_rank_for_meldee,
        file_name=meldee_file_name,
    )


def get_file_names_in_voice_rank_order(primary_world, meldees_dir) -> list[str]:
    world_voice_ranks = {}
    for meldee_file_name in dir_files(dir_path=meldees_dir):
        meldee_orderunit = get_meldeeorderunit(primary_world, meldee_file_name)
        world_voice_ranks[meldee_orderunit.owner_id] = meldee_orderunit
    worlds_voice_rank_ordered_list = list(world_voice_ranks.values())
    worlds_voice_rank_ordered_list.sort(
        key=lambda x: (x.voice_rank * -1, x.voice_hx_lowest_rank * -1, x.owner_id)
    )
    return [
        x_meldeeorderunit.file_name
        for x_meldeeorderunit in worlds_voice_rank_ordered_list
    ]


def get_meld_of_world_files(primary_world: WorldUnit, meldees_dir: str) -> WorldUnit:
    for x_filename in get_file_names_in_voice_rank_order(primary_world, meldees_dir):
        primary_world.meld(world_get_from_json(open_file(meldees_dir, x_filename)))
    primary_world.calc_world_metrics()
    return primary_world
