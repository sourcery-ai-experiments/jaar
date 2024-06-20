from src.agenda.agenda import AgendaUnit


def get_credorledger(x_agende: AgendaUnit):
    return {
        otherunit.other_id: otherunit.credor_weight
        for otherunit in x_agende._others.values()
    }


def allot_scale(credorledger: dict, scale_number: float, grain_unit: float):
    """
    allots the scale_number across credorledgers with credor_weighted attributes with a resolution of the grain unit.

    :param credorledgers: Dictionary of credorledgers with 'credor_weight' attribute.
    :param scale_number: The total number to allot.
    :param grain_unit: The smallest unit of distribution.
    :raises ValueError: If the scale number is not a multiple of the grain unit.
    :return: Dictionary with alloted values.
    """
    # Check if the scale number is a multiple of the grain unit
    print(f"{scale_number=}")
    print(f"{grain_unit=}")
    print(f"{scale_number / grain_unit=}")
    print(f"{10 % 0.1=}")
    print(f"{scale_number % grain_unit=}")
    print(f"{1.0 % grain_unit=}")
    if scale_number % grain_unit != 0:
        raise ValueError(
            f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
        )

    # Calculate the total credor_weight
    total_credor_weight = sum(credorledger.values())

    # Calculate the distribution
    x_dict = {}
    for key, obj in credorledger.items():
        # Determine the share based on credor_weight
        share = (obj / total_credor_weight) * scale_number

        # Adjust to the nearest grain unit
        alloted_value = round(share / grain_unit) * grain_unit
        x_dict[key] = alloted_value

    return x_dict


# # Example usage:
# credorledgers = {"obj1": {"credor_weight": 1.0}, "obj2": {"credor_weight": 2.0}, "obj3": {"credor_weight": 3.0}}
# print(f"{credorledgers=}")
# scale_number = 100
# grain_unit = 0.3

# alloted_credorledgers = allot_scale(credorledgers, scale_number, grain_unit)
# print(alloted_credorledgers)
