from src._road.road import PersonID, OtherID
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import UserHub, userhub_shop
from src.money.river_cycle import get_credorledger


def example_yao_userhub() -> UserHub:
    return userhub_shop(None, None, "Yao")


def example_yao_credorledger() -> dict[str:float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 7
    bob_credor_weight = 3
    zia_credor_weight = 10
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text, yao_credor_weight)
    yao_agenda.add_otherunit(bob_text, bob_credor_weight)
    yao_agenda.add_otherunit(zia_text, zia_credor_weight)
    return get_credorledger(yao_agenda)


def example_bob_credorledger() -> dict[str:float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 1
    bob_credor_weight = 7
    zia_credor_weight = 42
    bob_agenda = agendaunit_shop(bob_text)
    bob_agenda.add_otherunit(yao_text, yao_credor_weight)
    bob_agenda.add_otherunit(bob_text, bob_credor_weight)
    bob_agenda.add_otherunit(zia_text, zia_credor_weight)
    return get_credorledger(bob_agenda)


def example_zia_credorledger() -> dict[str:float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 89
    bob_credor_weight = 150
    zia_credor_weight = 61
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_otherunit(yao_text, yao_credor_weight)
    zia_agenda.add_otherunit(bob_text, bob_credor_weight)
    zia_agenda.add_otherunit(zia_text, zia_credor_weight)
    return get_credorledger(zia_agenda)


def example_yao_bob_zia_credorledgers() -> dict[PersonID : dict[OtherID:float]]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    return {
        yao_text: example_yao_credorledger,
        bob_text: example_bob_credorledger,
        zia_text: example_zia_credorledger,
    }


def example_yao_bob_zia_taxledger() -> dict[OtherID:float]:
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_sum = sum(example_yao_credorledger().values())
    bob_sum = sum(example_bob_credorledger().values())
    zia_sum = sum(example_zia_credorledger().values())

    return {
        yao_text: yao_sum - 60000,
        bob_text: bob_sum - 500000,
        zia_text: zia_sum - 4000,
    }
