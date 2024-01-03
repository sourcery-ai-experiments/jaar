def get_meld_weight(
    src_weight: float,
    src_on_meld_weight_action: str,
    other_weight: float,
    other_on_meld_weight_action: float,
) -> float:
    if (
        src_on_meld_weight_action != "default"
        or other_on_meld_weight_action == "ignore"
    ):
        src_weight += other_weight
    return src_weight


def get_on_meld_weight_actions() -> dict[str:None]:
    """
    match: melder and meldee will have equal weight or error thrown
    sum: melder and meldee sum weights
    ignore: melder ignores weight from meldee
    override: meldee overwrites melder weight (only works on meldee=default)
    default: meldee ignores meldee unless meldee is override
    """
    return {
        "default": None,
        "match": None,
        "sum": None,
        "accept": None,
        "override": None,
    }
