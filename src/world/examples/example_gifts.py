from src.world.gift import giftunit_shop, GiftUnit


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop(_gifter="Yao", _gift_id=37, _giftees=set("Sue"))


def get_sue_giftunit() -> GiftUnit:
    return giftunit_shop(_gifter="Sue", _gift_id=37, _giftees=set("Yao"))
