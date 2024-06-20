from src.agenda.other import OtherUnit


def allot_scale(others: OtherUnit, scale_number: float, grain_unit: float):
    """
    allots the scale_number across others with credor_weighted attributes with a resolution of the grain unit.

    :param others: Dictionary of others with 'credor_weight' attribute.
    :param scale_number: The total number to allot.
    :param grain_unit: The smallest unit of distribution.
    :raises ValueError: If the scale number is not a multiple of the grain unit.
    :return: Dictionary with alloted values.
    """
    # Check if the scale number is a multiple of the grain unit
    if scale_number % grain_unit != 0:
        raise ValueError(
            f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
        )

    # Calculate the total credor_weight
    total_credor_weight = sum(obj["credor_weight"] for obj in others.values())

    # Calculate the distribution
    for key, obj in others.items():
        # Determine the share based on credor_weight
        share = (obj["credor_weight"] / total_credor_weight) * scale_number

        # Adjust to the nearest grain unit
        alloted_value = round(share / grain_unit) * grain_unit
        others[key]["alloted_value"] = alloted_value

    return others


# # Example usage:
# others = {"obj1": {"credor_weight": 1.0}, "obj2": {"credor_weight": 2.0}, "obj3": {"credor_weight": 3.0}}
# print(f"{others=}")
# scale_number = 100
# grain_unit = 0.3

# alloted_others = allot_scale(others, scale_number, grain_unit)
# print(alloted_others)
