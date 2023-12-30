from src.world.lobby import (
    economyaddress_shop,
    create_concernunit,
    create_requestunit,
)


def get_farm_concernunit():
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    food_text = "food"
    good_text = "farm food"
    bad_text = "cheap food"
    farm_text = "cultivate"
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    return create_concernunit(
        economyaddress=texas_economyaddress,
        issue=food_text,
        good=good_text,
        bad=bad_text,
        fix=farm_text,
        positive=well_text,
        negative=poor_text,
    )


def get_farm_requestunit():
    bob_text = "Bob"
    real_text = "Real Farmers"
    farm_requestunit = create_requestunit(
        get_farm_concernunit(), bob_text, requestee_group=real_text
    )
    yao_text = "Yao"
    farm_requestunit.add_requestee_pid(yao_text)
    return farm_requestunit
