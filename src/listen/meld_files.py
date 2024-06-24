from src._road.road import OwnerID
from src._truth.truth import TruthUnit, get_from_json as truth_get_from_json
from src._instrument.file import dir_files, open_file
from dataclasses import dataclass


@dataclass
class MeldeeOrderUnit:
    owner_id: OwnerID
    voice_rank: int
    voice_hx_lowest_rank: int
    file_name: str


def get_meldeeorderunit(
    primary_truth: TruthUnit, meldee_file_name: str
) -> MeldeeOrderUnit:
    file_src_owner_id = meldee_file_name.replace(".json", "")
    primary_meldee_otherunit = primary_truth.get_other(file_src_owner_id)

    default_voice_rank = 0
    default_voice_hx_lowest_rank = 0
    if primary_meldee_otherunit is None:
        primary_voice_rank_for_meldee = default_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank
    else:
        primary_voice_rank_for_meldee = primary_meldee_otherunit._treasury_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = (
            primary_meldee_otherunit._treasury_voice_hx_lowest_rank
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


def get_file_names_in_voice_rank_order(primary_truth, meldees_dir) -> list[str]:
    truth_voice_ranks = {}
    for meldee_file_name in dir_files(dir_path=meldees_dir):
        meldee_orderunit = get_meldeeorderunit(primary_truth, meldee_file_name)
        truth_voice_ranks[meldee_orderunit.owner_id] = meldee_orderunit
    truths_voice_rank_ordered_list = list(truth_voice_ranks.values())
    truths_voice_rank_ordered_list.sort(
        key=lambda x: (x.voice_rank * -1, x.voice_hx_lowest_rank * -1, x.owner_id)
    )
    return [
        x_meldeeorderunit.file_name
        for x_meldeeorderunit in truths_voice_rank_ordered_list
    ]


def get_meld_of_truth_files(primary_truth: TruthUnit, meldees_dir: str) -> TruthUnit:
    for x_filename in get_file_names_in_voice_rank_order(primary_truth, meldees_dir):
        primary_truth.meld(truth_get_from_json(open_file(meldees_dir, x_filename)))
    primary_truth.calc_truth_metrics()
    return primary_truth
