from src.pact.examples.example_pacts import (
    pact_v001 as example_pacts_pact_v001,
)
from src.pact.party import PartyUnitExternalMetrics


def test_pact_import_debtor_info_CorrectlyWorks():
    # GIVEN
    x_pact = example_pacts_pact_v001()
    jane_text = "Jane Randolph"

    jane_party = x_pact._partys.get(jane_text)
    print(f"Before Party {jane_party.title} {jane_party._debtor_active=} ")
    assert jane_party._debtor_active is None
    assert jane_party._creditor_active is None

    assert sum(
        party_x._creditor_active is None for party_x in x_pact._partys.values()
    ) == len(x_pact._partys)
    assert sum(
        party_x._debtor_active is None for party_x in x_pact._partys.values()
    ) == len(x_pact._partys)

    # WHEN
    jane_debtor_status = True
    jane_creditor_status = True
    jane_metr = PartyUnitExternalMetrics(
        internal_title=jane_text,
        debtor_active=jane_debtor_status,
        creditor_active=jane_creditor_status,
    )
    x_pact.import_external_partyunit_metrics(jane_metr)

    # THEN
    assert jane_party._debtor_active == jane_debtor_status
    assert jane_party._creditor_active == jane_creditor_status

    assert (
        sum(party_x._creditor_active is None for party_x in x_pact._partys.values())
        == len(x_pact._partys) - 1
    )
    assert (
        sum(party_x._debtor_active is None for party_x in x_pact._partys.values())
        == len(x_pact._partys) - 1
    )
    assert (
        sum(party_x._creditor_active != None for party_x in x_pact._partys.values())
        == 1
    )
    assert (
        sum(party_x._debtor_active != None for party_x in x_pact._partys.values()) == 1
    )
