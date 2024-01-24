def get_meld_weight(
    src_weight: float,
    src_meld_strategy: str,
    other_weight: float,
    other_meld_strategy: float,
) -> float:
    output_float = 0
    if src_meld_strategy == "default" and other_meld_strategy == "override":
        output_float = other_weight
    elif src_meld_strategy != "default" or other_meld_strategy == "ignore":
        output_float = src_weight + other_weight
    else:
        output_float = src_weight
    return output_float


def get_meld_strategys() -> dict[str:None]:
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
