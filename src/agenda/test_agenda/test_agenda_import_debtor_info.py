from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
)
from src.agenda.party import PartyUnitExternalMetrics


def test_agenda_import_debtor_info_CorrectlyWorks():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    jane_text = "Jane Randolph"

    jane_party = x_agenda._partys.get(jane_text)
    print(f"Before Party {jane_party.handle} {jane_party._debtor_active=} ")
    assert jane_party._debtor_active is None
    assert jane_party._creditor_active is None

    assert sum(
        party_x._creditor_active is None for party_x in x_agenda._partys.values()
    ) == len(x_agenda._partys)
    assert sum(
        party_x._debtor_active is None for party_x in x_agenda._partys.values()
    ) == len(x_agenda._partys)

    # WHEN
    jane_debtor_status = True
    jane_creditor_status = True
    jane_metr = PartyUnitExternalMetrics(
        internal_handle=jane_text,
        debtor_active=jane_debtor_status,
        creditor_active=jane_creditor_status,
    )
    x_agenda.import_external_partyunit_metrics(jane_metr)

    # THEN
    assert jane_party._debtor_active == jane_debtor_status
    assert jane_party._creditor_active == jane_creditor_status

    assert (
        sum(party_x._creditor_active is None for party_x in x_agenda._partys.values())
        == len(x_agenda._partys) - 1
    )
    assert (
        sum(party_x._debtor_active is None for party_x in x_agenda._partys.values())
        == len(x_agenda._partys) - 1
    )
    assert (
        sum(party_x._creditor_active != None for party_x in x_agenda._partys.values())
        == 1
    )
    assert (
        sum(party_x._debtor_active != None for party_x in x_agenda._partys.values())
        == 1
    )
