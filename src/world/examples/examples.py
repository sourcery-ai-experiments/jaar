from src.world.concern import create_cultureaddress, create_concernunit, create_urgeunit


def get_farm_concernunit():
    luca_text = "Luca"
    texas_text = "Texas"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_text = "food"
    good_text = "good food"
    bad_text = "bad food"
    farm_text = "farm"
    well_text = "farm well"
    poor_text = "farm poorly"
    return create_concernunit(
        cultureaddress=texas_cultureaddress,
        concern=food_text,
        good=good_text,
        bad=bad_text,
        action=farm_text,
        positive=well_text,
        negative=poor_text,
    )


def get_farm_urgeunit():
    bob_text = "Bob"
    real_text = "Real Farmers"
    farm_urgeunit = create_urgeunit(
        get_farm_concernunit(), bob_text, actor_group=real_text
    )
    yao_text = "Yao"
    farm_urgeunit.add_actor_pid(yao_text)
    return farm_urgeunit
