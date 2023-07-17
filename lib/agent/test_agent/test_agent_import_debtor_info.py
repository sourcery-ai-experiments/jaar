from lib.agent.examples.example_agents import agent_v001 as example_agents_agent_v001
from lib.agent.ally import AllyUnitExternalMetrics


def test_agent_import_debtor_info_CorrectlyWorks():
    # GIVEN
    agent_x = example_agents_agent_v001()
    jane_text = "Jane Randolph"

    jane_ally = agent_x._allys.get(jane_text)
    print(f"Before Ally {jane_ally.name} {jane_ally._debtor_active=} ")
    assert jane_ally._debtor_active is None
    assert jane_ally._creditor_active is None

    assert sum(
        ally_x._creditor_active is None for ally_x in agent_x._allys.values()
    ) == len(agent_x._allys)
    assert sum(
        ally_x._debtor_active is None for ally_x in agent_x._allys.values()
    ) == len(agent_x._allys)

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
    assert jane_ally._debtor_active == jane_debtor_status
    assert jane_ally._creditor_active == jane_creditor_status

    assert (
        sum(ally_x._creditor_active is None for ally_x in agent_x._allys.values())
        == len(agent_x._allys) - 1
    )
    assert (
        sum(ally_x._debtor_active is None for ally_x in agent_x._allys.values())
        == len(agent_x._allys) - 1
    )
    assert (
        sum(ally_x._creditor_active != None for ally_x in agent_x._allys.values()) == 1
    )
    assert sum(ally_x._debtor_active != None for ally_x in agent_x._allys.values()) == 1
