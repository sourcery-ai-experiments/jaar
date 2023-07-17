from lib.agent.examples.example_agents import agent_v001 as example_agents_agent_v001
from lib.agent.ally import AllyUnitExternalMetrics


def test_agent_import_debtor_info_CorrectlyWorks():
    # GIVEN
    agent_x = example_agents_agent_v001()
    jane_text = "Jane Randolph"

    for ally_x in agent_x._allys.values():
        if ally_x.name == jane_text:
            print(f"Before Ally {ally_x.name} {ally_x._debtor_active=} ")
        assert ally_x._creditor_active is None
        assert ally_x._debtor_active is None
    # WHEN
    jane_debtor_status = True
    jane_creditor_status = True
    jane_metr = AllyUnitExternalMetrics(
        internal_name=jane_text,
        debtor_active=jane_debtor_status,
        creditor_active=jane_creditor_status,
    )
    agent_x.import_external_allyunit_metrics(jane_metr)

    # THEN
    for ally_x in agent_x._allys.values():
        if ally_x.name == jane_text:
            print(f"After  Ally {ally_x.name} {ally_x._debtor_active=} ")
            assert ally_x._debtor_active == jane_debtor_status
            assert ally_x._creditor_active == jane_creditor_status
        else:
            # print(f"Ally {ally_x.name} {ally_x._debtor_active=} ")
            assert ally_x._debtor_active is None
            assert ally_x._creditor_active is None
