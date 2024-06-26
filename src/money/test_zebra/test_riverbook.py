from src._world.world import worldunit_shop
from src.listen.userhub import userhub_shop
from src.money.rivercycle import (
    RiverBook,
    riverbook_shop,
    create_riverbook,
    get_credorledger,
)


def test_RiverBook_Exists():
    # GIVEN / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert x_riverbook.owner_id is None
    assert x_riverbook.userhub is None
    assert x_riverbook._rivergrants is None


def test_riverbook_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)

    # WHEN
    bob_text = "Bob"
    bob_riverbook = riverbook_shop(yao_userhub, bob_text)

    # THEN
    assert bob_riverbook.owner_id == bob_text
    assert bob_riverbook.userhub == yao_userhub
    assert bob_riverbook._rivergrants == {}


def test_create_riverbook_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_world = worldunit_shop(yao_text)
    yao_world.add_personunit(yao_text)
    yao_world.add_personunit(sue_text)
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_book_money_amount = 500

    # WHEN
    yao_credorledger = get_credorledger(yao_world)
    yao_riverbook = create_riverbook(
        yao_userhub, yao_text, yao_credorledger, yao_book_money_amount
    )

    # THEN
    assert yao_riverbook.userhub == yao_userhub
    assert yao_riverbook.owner_id == yao_text
    assert yao_riverbook._rivergrants == {yao_text: 250, sue_text: 250}
    assert sum(yao_riverbook._rivergrants.values()) == yao_book_money_amount
