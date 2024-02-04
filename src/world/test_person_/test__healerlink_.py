from src.world.problem import HealerLink, healerlink_shop


def test_HealerLink_exists():
    # GIVEN
    yao_text = "yao"
    yao_weight = 3
    yao_in_tribe = True

    # WHEN
    yao_healerlink = HealerLink(healer_id=yao_text, weight=3, in_tribe=yao_in_tribe)

    # THEN
    assert yao_healerlink.healer_id == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._economylinks is None
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_clout is None


def test_healerlink_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_in_tribe = False

    # WHEN
    yao_healerlink = healerlink_shop(
        healer_id=yao_text, weight=yao_weight, in_tribe=yao_in_tribe
    )

    # THEN
    assert yao_healerlink.healer_id == yao_text
    assert yao_healerlink.weight == yao_weight
    assert yao_healerlink.in_tribe == yao_in_tribe
    assert yao_healerlink._economylinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_clout is None


def test_HealerLink_shop_ReturnsCorrectObj_EmptyWeight():
    # GIVEN
    yao_text = "yao"

    # WHEN
    yao_healerlink = healerlink_shop(healer_id=yao_text)

    # THEN
    assert yao_healerlink.healer_id == yao_text
    assert yao_healerlink.weight == 1
    assert yao_healerlink.in_tribe is None
    assert yao_healerlink._economylinks == {}
    assert yao_healerlink._relative_weight is None
    assert yao_healerlink._person_clout is None


def test_HealerLink_set_relative_weight_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    assert yao_healerlink._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    yao_healerlink.set_relative_weight(x_relative_weight)

    # THEN
    assert yao_healerlink._relative_weight == x_relative_weight


def test_HealerLink_set_person_clout_SetsCorrectly():
    # GIVEN
    yao_text = "Yao"
    yao_healerlink = healerlink_shop(healer_id=yao_text)
    assert yao_healerlink._person_clout is None

    # WHEN
    x_person_clout = 0.45
    yao_healerlink.set_person_clout(x_person_clout)

    # THEN
    assert yao_healerlink._person_clout == x_person_clout
