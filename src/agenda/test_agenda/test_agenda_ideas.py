from src._road.road import get_default_real_id_roadnode
from src.agenda.idea import (
    IdeaID,
    balancelink_shop,
    ideaunit_shop,
    get_partys_relevant_ideas,
    get_party_relevant_ideas,
)
from src.agenda.party import PartyID, partyunit_shop, partylink_shop
from src.agenda.oath import oathunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import agenda_v001 as examples_agenda_v001
from pytest import raises as pytest_raises


def test_AgendaUnit_ideas_get_ideaunit_ReturnsCorrectObj():
    # GIVEN
    x_agenda = agendaunit_shop()
    swim_text = ",swimmers"
    # x_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(idea_id=swim_text))
    swim_ideas = {swim_text: ideaunit_shop(idea_id=swim_text)}
    x_agenda._ideas = swim_ideas

    # WHEN
    swim_ideaunit = x_agenda.get_ideaunit(swim_text)

    # THEN
    assert swim_ideaunit == ideaunit_shop(idea_id=swim_text)


def test_AgendaUnit_ideas_set_ideaunit_CorrectlySetAttr():
    # GIVEN
    swim_text = ",swimmers"
    x_agenda = agendaunit_shop()

    # WHEN
    x_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(idea_id=swim_text))

    # THEN
    assert len(x_agenda._ideas) == 1
    swim_ideas = {swim_text: ideaunit_shop(idea_id=swim_text)}
    assert len(x_agenda._ideas) == len(swim_ideas)
    assert x_agenda.get_ideaunit(swim_text) != None
    swim_ideaunit = x_agenda.get_ideaunit(swim_text)
    assert swim_ideaunit._partys == swim_ideas.get(swim_text)._partys
    assert x_agenda.get_ideaunit(swim_text) == swim_ideas.get(swim_text)
    assert x_agenda._ideas == swim_ideas


def test_AgendaUnit_ideas_set_ideaunit_CorrectlyReplacesIdea():
    # GIVEN
    swim_text = ",swimmers"
    x_agenda = agendaunit_shop()
    swim1_idea = ideaunit_shop(swim_text)
    bob_text = "Bob"
    swim1_idea.set_partylink(partylink_shop(bob_text))
    x_agenda.set_ideaunit(swim1_idea)
    assert len(x_agenda.get_ideaunit(swim_text)._partys) == 1

    # WHEN
    yao_text = "Yao"
    swim2_idea = ideaunit_shop(swim_text)
    swim2_idea.set_partylink(partylink_shop(bob_text))
    swim2_idea.set_partylink(partylink_shop(yao_text))
    x_agenda.set_ideaunit(swim2_idea, replace=False)

    # THEN
    assert len(x_agenda.get_ideaunit(swim_text)._partys) == 1

    # WHEN / THEN
    x_agenda.set_ideaunit(swim2_idea, replace=True)
    assert len(x_agenda.get_ideaunit(swim_text)._partys) == 2


# def test_AgendaUnit_ideas_set_ideaunit_RaisesErrorWhen_party_mirrorSubmitted():
#     # GIVEN
#     yao_agenda = agendaunit_shop("Yao")
#     bob_text = "Bob"
#     yao_agenda.set_partyunit(partyunit_shop(bob_text))
#     bob_ideaunit = yao_agenda.get_ideaunit(bob_text)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         yao_agenda.set_ideaunit(bob_ideaunit)
#     assert (
#         str(excinfo.value)
#         == f"AgendaUnit.set_ideaunit('{bob_text}') fails because idea is _party_mirror."
#     )


def test_AgendaUnit_ideas_set_ideaunit_CorrectlySets_partylinks():
    # GIVEN
    swim_text = ",swimmers"
    x_agenda = agendaunit_shop()
    swim1_idea = ideaunit_shop(swim_text)
    bob_text = "Bob"
    swim1_idea.set_partylink(partylink_shop(bob_text))
    x_agenda.set_ideaunit(swim1_idea)
    assert len(x_agenda.get_ideaunit(swim_text)._partys) == 1

    # WHEN
    yao_text = "Yao"
    swim2_idea = ideaunit_shop(swim_text)
    swim2_idea.set_partylink(partylink_shop(bob_text))
    swim2_idea.set_partylink(partylink_shop(yao_text))
    x_agenda.set_ideaunit(swim2_idea, add_partylinks=True)

    # THEN
    assert len(x_agenda.get_ideaunit(swim_text)._partys) == 2


def test_AgendaUnit_ideas_del_ideaunit_casasCorrectly():
    # GIVEN
    x_agenda = agendaunit_shop()
    swim_text = "swimmers"
    swim_idea = ideaunit_shop(idea_id=IdeaID(swim_text))
    x_agenda.set_ideaunit(y_ideaunit=swim_idea)
    assert x_agenda.get_ideaunit(swim_text) != None

    # WHEN
    x_agenda.del_ideaunit(idea_id=swim_text)
    assert x_agenda.get_ideaunit(swim_text) is None
    assert x_agenda._ideas == {}


def test_examples_agenda_v001_HasIdeas():
    # GIVEN / WHEN
    x_agenda = examples_agenda_v001()

    # THEN
    assert x_agenda._ideas != None
    assert len(x_agenda._ideas) == 34
    everyone_partys_len = None
    everyone_idea = x_agenda.get_ideaunit(",Everyone")
    everyone_partys_len = len(everyone_idea._partys)
    assert everyone_partys_len == 22

    # WHEN
    x_agenda.calc_agenda_metrics()
    oath_dict = x_agenda._oath_dict

    # THEN
    print(f"{len(oath_dict)=}")
    db_oath = oath_dict.get(x_agenda.make_l1_road("D&B"))
    print(f"{db_oath._label=} {db_oath._balancelinks=}")
    assert len(db_oath._balancelinks) == 3
    # for oath_key in oath_dict:
    #     print(f"{oath_key=}")
    #     if oath._label == "D&B":
    #         print(f"{oath._label=} {oath._balancelinks=}")
    #         db_balancelink_len = len(oath._balancelinks)
    # assert db_balancelink_len == 3


def test_AgendaUnit_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))

    assert len(sue_agenda._partys) == 3
    assert len(sue_agenda._ideas) == 3
    swim_text = "swim"
    sue_agenda.add_l1_oath(oathunit_shop(swim_text))
    balancelink_rico = balancelink_shop(idea_id=IdeaID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(idea_id=IdeaID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(idea_id=IdeaID(patr_text), credor_weight=10)
    swim_road = sue_agenda.make_l1_road(swim_text)
    sue_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_rico)
    sue_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_carm)
    sue_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_patr)

    street_text = "streets"
    sue_agenda.add_oath(oathunit_shop(street_text), parent_road=swim_road)
    assert sue_agenda._oathroot._balancelinks in (None, {})
    assert len(sue_agenda._oathroot._kids[swim_text]._balancelinks) == 3

    # WHEN
    oath_dict = sue_agenda.get_oath_dict()

    # THEN
    print(f"{oath_dict.keys()=} {get_default_real_id_roadnode()=}")
    root_oath = oath_dict.get(get_default_real_id_roadnode())
    swim_oath = oath_dict.get(swim_road)
    street_oath = oath_dict.get(sue_agenda.make_road(swim_road, street_text))

    assert len(swim_oath._balancelinks) == 3
    assert len(swim_oath._balanceheirs) == 3
    assert street_oath._balancelinks in (None, {})
    assert len(street_oath._balanceheirs) == 3

    print(f"{len(oath_dict)}")
    print(f"{swim_oath._balancelinks}")
    print(f"{swim_oath._balanceheirs}")
    print(f"{swim_oath._balanceheirs}")
    assert len(sue_agenda._oathroot._kids["swim"]._balanceheirs) == 3


def test_AgendaUnit_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))

    swim_text = "swim"
    swim_road = x_agenda.make_road(prom_text, swim_text)

    x_agenda.add_l1_oath(oathunit_shop(swim_text))
    balancelink_rico = balancelink_shop(idea_id=IdeaID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(idea_id=IdeaID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(idea_id=IdeaID(patr_text), credor_weight=10)

    swim_oath = x_agenda.get_oath_obj(swim_road)
    x_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_rico)
    x_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_carm)
    x_agenda.edit_oath_attr(road=swim_road, balancelink=balancelink_patr)

    assert len(swim_oath._balancelinks) == 3
    assert len(swim_oath._balanceheirs) == 3

    # print(f"{len(oath_list)}")
    # print(f"{oath_list[0]._balancelinks}")
    # print(f"{oath_list[0]._balanceheirs}")
    # print(f"{oath_list[1]._balanceheirs}")
    assert len(x_agenda._oathroot._kids[swim_text]._balancelinks) == 3
    assert len(x_agenda._oathroot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    x_agenda.edit_oath_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_oath = x_agenda.get_oath_obj(swim_road)
    print(f"{swim_oath._label=}")
    print(f"{swim_oath._balancelinks=}")
    print(f"{swim_oath._balanceheirs=}")

    assert len(x_agenda._oathroot._kids[swim_text]._balancelinks) == 2
    assert len(x_agenda._oathroot._kids[swim_text]._balanceheirs) == 2


def test_AgendaUnit_set_balancelink_CorrectlyCalculatesInheritedBalanceLinkAgendaImportance():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    sue_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    blink_rico = balancelink_shop(idea_id=rico_text, credor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(idea_id=carm_text, credor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(idea_id=patr_text, credor_weight=10)
    sue_agenda._oathroot.set_balancelink(balancelink=blink_rico)
    sue_agenda._oathroot.set_balancelink(balancelink=blink_carm)
    sue_agenda._oathroot.set_balancelink(balancelink=blink_patr)
    assert len(sue_agenda._oathroot._balancelinks) == 3

    # WHEN
    oath_dict = sue_agenda.get_oath_dict()

    # THEN
    print(f"{oath_dict.keys()=}")
    oath_prom = oath_dict.get(get_default_real_id_roadnode())
    assert len(oath_prom._balanceheirs) == 3

    bheir_rico = oath_prom._balanceheirs.get(rico_text)
    bheir_carm = oath_prom._balanceheirs.get(carm_text)
    bheir_patr = oath_prom._balanceheirs.get(patr_text)
    assert bheir_rico._agenda_cred == 0.5
    assert bheir_rico._agenda_debt == 0.75
    assert bheir_carm._agenda_cred == 0.25
    assert bheir_carm._agenda_debt == 0.125
    assert bheir_patr._agenda_cred == 0.25
    assert bheir_patr._agenda_debt == 0.125
    assert (
        bheir_rico._agenda_cred + bheir_carm._agenda_cred + bheir_patr._agenda_cred == 1
    )
    assert (
        bheir_rico._agenda_debt + bheir_carm._agenda_debt + bheir_patr._agenda_debt == 1
    )

    # agenda_cred_sum = 0
    # agenda_debt_sum = 0
    # for idea in x_agenda._oathroot._balanceheirs.values():
    #     print(f"{idea=}")
    #     assert idea._agenda_cred != None
    #     assert idea._agenda_cred in [0.25, 0.5]
    #     assert idea._agenda_debt != None
    #     assert idea._agenda_debt in [0.75, 0.125]
    #     agenda_cred_sum += idea._agenda_cred
    #     agenda_debt_sum += idea._agenda_debt

    # assert agenda_cred_sum == 1
    # assert agenda_debt_sum == 1


def test_AgendaUnit_get_oath_list_CorrectlyCalculates1LevelAgendaIdeaAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    blink_rico = balancelink_shop(idea_id=rico_text, credor_weight=20, debtor_weight=6)
    blink_carm = balancelink_shop(idea_id=carm_text, credor_weight=10, debtor_weight=1)
    blink_patr = balancelink_shop(idea_id=patr_text, credor_weight=10)
    x_agenda._oathroot.set_balancelink(balancelink=blink_rico)
    x_agenda._oathroot.set_balancelink(balancelink=blink_carm)
    x_agenda._oathroot.set_balancelink(balancelink=blink_patr)

    assert len(x_agenda._ideas) == 3

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    idea_rico = x_agenda.get_ideaunit(rico_text)
    idea_carm = x_agenda.get_ideaunit(carm_text)
    idea_patr = x_agenda.get_ideaunit(patr_text)
    assert idea_rico._agenda_cred == 0.5
    assert idea_rico._agenda_debt == 0.75
    assert idea_carm._agenda_cred == 0.25
    assert idea_carm._agenda_debt == 0.125
    assert idea_patr._agenda_cred == 0.25
    assert idea_patr._agenda_debt == 0.125
    assert idea_rico._agenda_cred + idea_carm._agenda_cred + idea_patr._agenda_cred == 1
    assert idea_rico._agenda_debt + idea_carm._agenda_debt + idea_patr._agenda_debt == 1

    # WHEN
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(sele_text)))
    bl_sele = balancelink_shop(idea_id=sele_text, credor_weight=37)
    x_agenda._oathroot.set_balancelink(balancelink=bl_sele)
    assert len(x_agenda._ideas) == 4
    x_agenda.calc_agenda_metrics()

    # THEN
    idea_sele = x_agenda.get_ideaunit(sele_text)
    assert idea_rico._agenda_cred != 0.5
    assert idea_rico._agenda_debt != 0.75
    assert idea_carm._agenda_cred != 0.25
    assert idea_carm._agenda_debt != 0.125
    assert idea_patr._agenda_cred != 0.25
    assert idea_patr._agenda_debt != 0.125
    assert idea_sele._agenda_cred != None
    assert idea_sele._agenda_debt != None
    assert (
        idea_rico._agenda_cred
        + idea_carm._agenda_cred
        + idea_patr._agenda_cred
        + idea_sele._agenda_cred
        == 1
    )
    assert (
        idea_rico._agenda_debt
        + idea_carm._agenda_debt
        + idea_patr._agenda_debt
        + idea_sele._agenda_debt
        == 1
    )


def test_AgendaUnit_get_oath_list_CorrectlyCalculates3levelAgendaIdeaAgendaImportance():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    swim_text = "swim"
    x_agenda.add_l1_oath(oathunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    rico_balancelink = balancelink_shop(
        idea_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        idea_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(idea_id=patr_text, credor_weight=10)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(x_agenda._ideas) == 3

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    idea_rico = x_agenda.get_ideaunit(rico_text)
    idea_carm = x_agenda.get_ideaunit(carm_text)
    idea_patr = x_agenda.get_ideaunit(patr_text)
    assert idea_rico._agenda_cred == 0.5
    assert idea_rico._agenda_debt == 0.75
    assert idea_carm._agenda_cred == 0.25
    assert idea_carm._agenda_debt == 0.125
    assert idea_patr._agenda_cred == 0.25
    assert idea_patr._agenda_debt == 0.125
    assert idea_rico._agenda_cred + idea_carm._agenda_cred + idea_patr._agenda_cred == 1
    assert idea_rico._agenda_debt + idea_carm._agenda_debt + idea_patr._agenda_debt == 1


def test_AgendaUnit_get_oath_list_CorrectlyCalculatesIdeaAgendaImportanceLWwithIdeaEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_agenda = agendaunit_shop(prom_text)
    swim_text = "swim"
    x_agenda.add_l1_oath(oathunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(rico_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(carm_text)))
    x_agenda.set_partyunit(partyunit=partyunit_shop(party_id=PartyID(patr_text)))
    rico_balancelink = balancelink_shop(
        idea_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        idea_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(idea_id=patr_text, credor_weight=10)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_agenda._oathroot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    x_agenda.add_l1_oath(oathunit_shop("hunt", _weight=3))

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_agenda._oathroot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    idea_rico = x_agenda.get_ideaunit(rico_text)
    idea_carm = x_agenda.get_ideaunit(carm_text)
    idea_patr = x_agenda.get_ideaunit(patr_text)
    assert idea_rico._agenda_cred == 0.125
    assert idea_rico._agenda_debt == 0.1875
    assert idea_carm._agenda_cred == 0.0625
    assert idea_carm._agenda_debt == 0.03125
    assert idea_patr._agenda_cred == 0.0625
    assert idea_patr._agenda_debt == 0.03125
    assert (
        idea_rico._agenda_cred + idea_carm._agenda_cred + idea_patr._agenda_cred == 0.25
    )
    assert (
        idea_rico._agenda_debt + idea_carm._agenda_debt + idea_patr._agenda_debt == 0.25
    )


def test_AgendaUnit_edit_ideaunit_idea_id_CorrectlyCreatesNewPersonID():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(party_id=rico_text)
    swim_text = ",swimmers"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    swim_idea.set_partylink(partylink=partylink_shop(party_id=rico_text))
    agenda.set_ideaunit(swim_idea)
    assert len(agenda._partys) == 1
    assert len(agenda._ideas) == 2
    assert agenda.get_ideaunit(swim_text) != None
    assert agenda.get_ideaunit(swim_text)._party_mirror is False
    assert len(agenda.get_ideaunit(swim_text)._partys) == 1

    # WHEN
    jog_text = ",jog"
    agenda.edit_ideaunit_idea_id(
        old_idea_id=swim_text, new_idea_id=jog_text, allow_idea_overwite=False
    )

    # THEN
    assert agenda.get_ideaunit(jog_text) != None
    assert agenda.get_ideaunit(swim_text) is None
    assert len(agenda._partys) == 1
    assert len(agenda._ideas) == 2
    assert agenda.get_ideaunit(jog_text)._party_mirror is False
    assert len(agenda.get_ideaunit(jog_text)._partys) == 1


def test_AgendaUnit_edit_Ideaunit_idea_id_raiseErrorNewPersonIDPreviouslyExists():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(party_id=rico_text)
    swim_text = ",swimmers"
    agenda.set_ideaunit(ideaunit_shop(idea_id=swim_text))
    jog_text = ",jog"
    agenda.set_ideaunit(ideaunit_shop(idea_id=jog_text))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        agenda.edit_ideaunit_idea_id(
            old_idea_id=swim_text,
            new_idea_id=jog_text,
            allow_idea_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Idea '{swim_text}' modify to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_AgendaUnit_edit_ideaunit_idea_id_CorrectlyMeldPersonIDs():
    # GIVEN
    agenda = agendaunit_shop("prom")
    rico_text = "rico"
    agenda.add_partyunit(party_id=rico_text)
    swim_text = ",swimmers"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    swim_idea.set_partylink(
        partylink=partylink_shop(party_id=rico_text, credor_weight=5, debtor_weight=3)
    )
    agenda.set_ideaunit(swim_idea)
    jog_text = ",jog"
    jog_idea = ideaunit_shop(idea_id=jog_text)
    jog_idea.set_partylink(
        partylink=partylink_shop(party_id=rico_text, credor_weight=7, debtor_weight=10)
    )
    agenda.set_ideaunit(jog_idea)
    print(f"{agenda.get_ideaunit(jog_text)._partys.get(rico_text)=}")
    assert agenda.get_ideaunit(jog_text) != None

    # WHEN
    agenda.edit_ideaunit_idea_id(
        old_idea_id=swim_text,
        new_idea_id=jog_text,
        allow_idea_overwite=True,
    )

    # THEN
    assert agenda.get_ideaunit(jog_text) != None
    assert agenda.get_ideaunit(swim_text) is None
    assert len(agenda._partys) == 1
    assert len(agenda._ideas) == 2
    assert agenda.get_ideaunit(jog_text)._party_mirror is False
    assert len(agenda.get_ideaunit(jog_text)._partys) == 1
    assert agenda.get_ideaunit(jog_text)._partys.get(rico_text).credor_weight == 12
    assert agenda.get_ideaunit(jog_text)._partys.get(rico_text).debtor_weight == 13


def test_AgendaUnit_edit_ideaunit_idea_id_CorrectlyModifiesBalanceLinks():
    # GIVEN
    x_agenda = agendaunit_shop("prom")
    rico_text = "rico"
    x_agenda.add_partyunit(party_id=rico_text)
    swim_text = ",swimmers"
    swim_ideaunit = ideaunit_shop(idea_id=swim_text)
    x_agenda.set_ideaunit(swim_ideaunit)
    outdoor_text = "outdoors"
    outdoor_road = x_agenda.make_road(x_agenda._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_agenda.make_road(outdoor_road, camping_text)
    x_agenda.add_oath(oathunit_shop(camping_text), parent_road=outdoor_road)

    camping_oath = x_agenda.get_oath_obj(camping_road)
    swim_balancelink = balancelink_shop(
        idea_id=swim_ideaunit.idea_id, credor_weight=5, debtor_weight=3
    )
    camping_oath.set_balancelink(swim_balancelink)
    assert camping_oath._balancelinks.get(swim_text) != None
    assert camping_oath._balancelinks.get(swim_text).credor_weight == 5
    assert camping_oath._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = ",jog"
    x_agenda.edit_ideaunit_idea_id(
        old_idea_id=swim_text, new_idea_id=jog_text, allow_idea_overwite=False
    )

    # THEN
    assert camping_oath._balancelinks.get(swim_text) is None
    assert camping_oath._balancelinks.get(jog_text) != None
    assert camping_oath._balancelinks.get(jog_text).credor_weight == 5
    assert camping_oath._balancelinks.get(jog_text).debtor_weight == 3


def test_AgendaUnit_edit_ideaunit_idea_id_CorrectlyMeldsBalanceLinesBalanceLinksBalanceHeirs():
    # GIVEN
    x_agenda = agendaunit_shop("prom")
    rico_text = "rico"
    x_agenda.add_partyunit(party_id=rico_text)
    swim_text = ",swimmers"
    swim_ideaunit = ideaunit_shop(idea_id=swim_text)
    x_agenda.set_ideaunit(swim_ideaunit)

    jog_text = ",jog"
    jog_ideaunit = ideaunit_shop(idea_id=jog_text)
    x_agenda.set_ideaunit(jog_ideaunit)

    outdoor_text = "outdoors"
    outdoor_road = x_agenda.make_road(x_agenda._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_agenda.make_road(outdoor_road, camping_text)
    x_agenda.add_oath(oathunit_shop(camping_text), parent_road=outdoor_road)

    camping_oath = x_agenda.get_oath_obj(camping_road)
    swim_balancelink = balancelink_shop(
        idea_id=swim_ideaunit.idea_id, credor_weight=5, debtor_weight=3
    )
    camping_oath.set_balancelink(swim_balancelink)
    jog_balancelink = balancelink_shop(
        idea_id=jog_ideaunit.idea_id, credor_weight=7, debtor_weight=10
    )
    camping_oath.set_balancelink(jog_balancelink)
    assert camping_oath._balancelinks.get(swim_text) != None
    assert camping_oath._balancelinks.get(swim_text).credor_weight == 5
    assert camping_oath._balancelinks.get(swim_text).debtor_weight == 3
    assert camping_oath._balancelinks.get(jog_text) != None
    assert camping_oath._balancelinks.get(jog_text).credor_weight == 7
    assert camping_oath._balancelinks.get(jog_text).debtor_weight == 10

    # WHEN
    x_agenda.edit_ideaunit_idea_id(
        old_idea_id=swim_text, new_idea_id=jog_text, allow_idea_overwite=True
    )

    # THEN
    assert camping_oath._balancelinks.get(swim_text) is None
    assert camping_oath._balancelinks.get(jog_text) != None
    assert camping_oath._balancelinks.get(jog_text).credor_weight == 12
    assert camping_oath._balancelinks.get(jog_text).debtor_weight == 13


def test_AgendaUnit_add_oath_CreatesMissingIdeas():
    # GIVEN
    bob_text = "Bob"
    x_agenda = agendaunit_shop(bob_text)
    casa_road = x_agenda.make_l1_road("casa")
    new_oath_parent_road = x_agenda.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_oath = oathunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    balancelink_z = balancelink_shop(idea_id=family_text)
    clean_cookery_oath.set_balancelink(balancelink=balancelink_z)
    assert len(x_agenda._ideas) == 0
    assert x_agenda.get_ideaunit(family_text) is None

    # WHEN
    x_agenda.add_l1_oath(clean_cookery_oath, create_missing_ideas=True)

    # THEN
    assert len(x_agenda._ideas) == 1
    assert x_agenda.get_ideaunit(family_text) != None
    assert x_agenda.get_ideaunit(family_text)._partys in (None, {})


def test_AgendaUnit__get_filtered_balancelinks_oath_CorrectlyFiltersOath_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_agenda = agendaunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_agenda.add_partyunit(party_id=xia_text)
    x1_agenda.add_partyunit(party_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_agenda.make_l1_road(swim_text)
    x1_agenda.add_l1_oath(oathunit_shop(casa_text))
    x1_agenda.add_l1_oath(oathunit_shop(swim_text))
    x1_agenda.edit_oath_attr(swim_road, balancelink=balancelink_shop(xia_text))
    x1_agenda.edit_oath_attr(swim_road, balancelink=balancelink_shop(zoa_text))
    x1_agenda_swim_oath = x1_agenda.get_oath_obj(swim_road)
    assert len(x1_agenda_swim_oath._balancelinks) == 2
    x_agenda = agendaunit_shop(noa_text)
    x_agenda.add_partyunit(party_id=xia_text)

    # WHEN
    filtered_oath = x_agenda._get_filtered_balancelinks_oath(x1_agenda_swim_oath)

    # THEN
    assert len(filtered_oath._balancelinks) == 1
    assert list(filtered_oath._balancelinks.keys()) == [xia_text]


def test_AgendaUnit_add_oath_CorrectlyFiltersOath_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_agenda = agendaunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_agenda.add_partyunit(party_id=xia_text)
    x1_agenda.add_partyunit(party_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_agenda.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_agenda.make_l1_road(swim_text)
    x1_agenda.add_l1_oath(oathunit_shop(casa_text))
    x1_agenda.add_l1_oath(oathunit_shop(swim_text))
    x1_agenda.edit_oath_attr(
        road=swim_road, balancelink=balancelink_shop(idea_id=xia_text)
    )
    x1_agenda.edit_oath_attr(
        road=swim_road, balancelink=balancelink_shop(idea_id=zoa_text)
    )
    x1_agenda_swim_oath = x1_agenda.get_oath_obj(swim_road)
    assert len(x1_agenda_swim_oath._balancelinks) == 2

    # WHEN
    x_agenda = agendaunit_shop(noa_text)
    x_agenda.add_partyunit(party_id=xia_text)
    x_agenda.add_l1_oath(x1_agenda_swim_oath, create_missing_oaths=False)

    # THEN
    x_agenda_swim_oath = x_agenda.get_oath_obj(swim_road)
    assert len(x_agenda_swim_oath._balancelinks) == 1
    assert list(x_agenda_swim_oath._balancelinks.keys()) == [xia_text]


def test_AgendaUnit_add_oath_DoesNotOverwriteIdeas():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)
    casa_road = bob_agenda.make_l1_road("casa")
    new_oath_parent_road = bob_agenda.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_oath = oathunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    balancelink_z = balancelink_shop(idea_id=family_text)
    clean_cookery_oath.set_balancelink(balancelink=balancelink_z)

    ideaunit_z = ideaunit_shop(idea_id=family_text)
    ideaunit_z.set_partylink(partylink=partylink_shop(party_id="ann1"))
    ideaunit_z.set_partylink(partylink=partylink_shop(party_id="bet1"))
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_z)

    # assert len(bob_agenda._ideas) == 0
    # assert bob_agenda.get_ideaunit(family_text) is None
    assert len(bob_agenda._ideas) == 1
    assert len(bob_agenda.get_ideaunit(family_text)._partys) == 2

    # WHEN
    bob_agenda.add_oath(
        oath_kid=clean_cookery_oath,
        parent_road=new_oath_parent_road,
        create_missing_ideas=True,
    )

    # THEN

    # assert len(bob_agenda._ideas) == 1
    # assert len(bob_agenda.get_ideaunit(family_text)._partys) == 0
    # ideaunit_z = ideaunit_shop(idea_id=family_text)
    # ideaunit_z.set_partylink(partylink=partylink_shop(party_id="ann2"))
    # ideaunit_z.set_partylink(partylink=partylink_shop(party_id="bet2"))
    # bob_agenda.set_ideaunit(y_ideaunit=ideaunit_z)

    assert len(bob_agenda._ideas) == 1
    assert len(bob_agenda.get_ideaunit(family_text)._partys) == 2


def test_AgendaUnit_set_ideaunit_create_missing_partys_DoesCreateMissingPartys():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    ideaunit_z = ideaunit_shop(idea_id=family_text)
    ideaunit_z.set_partylink(
        partylink=partylink_shop(party_id=anna_text, credor_weight=3, debtor_weight=7)
    )
    ideaunit_z.set_partylink(
        partylink=partylink_shop(party_id=beto_text, credor_weight=5, debtor_weight=11)
    )

    assert ideaunit_z._partys.get(anna_text).credor_weight == 3
    assert ideaunit_z._partys.get(anna_text).debtor_weight == 7

    assert ideaunit_z._partys.get(beto_text).credor_weight == 5
    assert ideaunit_z._partys.get(beto_text).debtor_weight == 11

    assert len(bob_agenda._partys) == 0
    assert len(bob_agenda._ideas) == 0

    # WHEN
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_z, create_missing_partys=True)

    # THEN
    assert len(bob_agenda._partys) == 2
    assert len(bob_agenda._ideas) == 3
    assert bob_agenda._partys.get(anna_text).credor_weight == 3
    assert bob_agenda._partys.get(anna_text).debtor_weight == 7

    assert bob_agenda._partys.get(beto_text).credor_weight == 5
    assert bob_agenda._partys.get(beto_text).debtor_weight == 11


def test_AgendaUnit_set_ideaunit_create_missing_partys_DoesNotReplacePartys():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    bob_agenda.set_partyunit(
        partyunit_shop(party_id=anna_text, credor_weight=17, debtor_weight=88)
    )
    bob_agenda.set_partyunit(
        partyunit_shop(party_id=beto_text, credor_weight=46, debtor_weight=71)
    )
    ideaunit_z = ideaunit_shop(idea_id=family_text)
    ideaunit_z.set_partylink(
        partylink=partylink_shop(party_id=anna_text, credor_weight=3, debtor_weight=7)
    )
    ideaunit_z.set_partylink(
        partylink=partylink_shop(party_id=beto_text, credor_weight=5, debtor_weight=11)
    )

    assert ideaunit_z._partys.get(anna_text).credor_weight == 3
    assert ideaunit_z._partys.get(anna_text).debtor_weight == 7
    assert ideaunit_z._partys.get(beto_text).credor_weight == 5
    assert ideaunit_z._partys.get(beto_text).debtor_weight == 11
    assert len(bob_agenda._partys) == 2
    assert bob_agenda._partys.get(anna_text).credor_weight == 17
    assert bob_agenda._partys.get(anna_text).debtor_weight == 88
    assert bob_agenda._partys.get(beto_text).credor_weight == 46
    assert bob_agenda._partys.get(beto_text).debtor_weight == 71

    # WHEN
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_z, create_missing_partys=True)

    # THEN
    assert len(bob_agenda._partys) == 2
    assert bob_agenda._partys.get(anna_text).credor_weight == 17
    assert bob_agenda._partys.get(anna_text).debtor_weight == 88
    assert bob_agenda._partys.get(beto_text).credor_weight == 46
    assert bob_agenda._partys.get(beto_text).debtor_weight == 71


def test_AgendaUnit_get_ideaunits_dict_ReturnsCorrectObj():
    # GIVEN
    bob_agenda = agendaunit_shop("Bob")
    swim_text = ",swimmers"
    run_text = ",runners"
    fly_text = ",flyers"
    yao_text = "Yao"
    bob_agenda.set_partyunit(partyunit_shop(yao_text))
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(idea_id=swim_text))
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(idea_id=run_text))
    bob_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(idea_id=fly_text))
    assert len(bob_agenda._ideas) == 4

    # WHEN
    x_ideaunits_dict = bob_agenda.get_ideaunits_dict()

    # THEN
    assert x_ideaunits_dict.get(fly_text) != None
    assert x_ideaunits_dict.get(run_text) != None
    assert x_ideaunits_dict.get(swim_text) != None
    assert x_ideaunits_dict.get(yao_text) is None
    assert len(x_ideaunits_dict) == 3


def test_get_partys_relevant_ideas_ReturnsEmptyDict():
    # GIVEN
    bob_text = "Bob"
    agenda_with_partys = agendaunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    agenda_with_partys.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    agenda_with_partys.set_partyunit(partyunit=partyunit_shop(party_id=sam_text))

    agenda_with_ideas = agendaunit_shop()

    # WHEN
    print(f"{len(agenda_with_partys._partys)=} {len(agenda_with_ideas._ideas)=}")
    relevant_x = get_partys_relevant_ideas(
        agenda_with_ideas._ideas, agenda_with_partys._partys
    )

    # THEN
    assert relevant_x == {}


def test_get_partys_relevant_ideas_Returns2SinglePartyIdeas():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    agenda_3ideas = agendaunit_shop(bob_text)
    agenda_3ideas.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    agenda_3ideas.set_partyunit(partyunit=partyunit_shop(party_id=sam_text))
    agenda_3ideas.set_partyunit(partyunit=partyunit_shop(party_id=wil_text))

    agenda_2partys = agendaunit_shop(bob_text)
    agenda_2partys.set_partyunit(partyunit=partyunit_shop(party_id=bob_text))
    agenda_2partys.set_partyunit(partyunit=partyunit_shop(party_id=sam_text))

    # WHEN
    print(f"{len(agenda_2partys._partys)=} {len(agenda_3ideas._ideas)=}")
    mrg_x = get_partys_relevant_ideas(agenda_3ideas._ideas, agenda_2partys._partys)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_party_relevant_ideas_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(jes_text)
    bob_text = "Bob"
    jes_agenda.set_partyunit(partyunit_shop(party_id=jes_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=bob_text))

    hike_text = "hikers"
    jes_agenda.set_ideaunit(ideaunit_shop(idea_id=hike_text))
    hike_idea = jes_agenda.get_ideaunit(hike_text)
    hike_idea.set_partylink(partylink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_party_relevant_ideas(jes_agenda._ideas, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_party_relevant_ideas_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_agenda = agendaunit_shop(jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_agenda.set_partyunit(partyunit_shop(party_id=jes_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=bob_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=noa_text))
    jes_agenda.set_partyunit(partyunit_shop(party_id=eli_text))

    swim_text = ",swimmers"
    jes_agenda.set_ideaunit(ideaunit_shop(idea_id=swim_text))
    swim_idea = jes_agenda.get_ideaunit(swim_text)
    swim_idea.set_partylink(partylink_shop(bob_text))

    hike_text = ",hikers"
    jes_agenda.set_ideaunit(ideaunit_shop(idea_id=hike_text))
    hike_idea = jes_agenda.get_ideaunit(hike_text)
    hike_idea.set_partylink(partylink_shop(bob_text))
    hike_idea.set_partylink(partylink_shop(noa_text))

    hunt_text = ",hunters"
    jes_agenda.set_ideaunit(ideaunit_shop(idea_id=hunt_text))
    hike_idea = jes_agenda.get_ideaunit(hunt_text)
    hike_idea.set_partylink(partylink_shop(noa_text))
    hike_idea.set_partylink(partylink_shop(eli_text))

    # WHEN
    print(f"{len(jes_agenda._partys)=} {len(jes_agenda._ideas)=}")
    bob_mrg = get_party_relevant_ideas(jes_agenda._ideas, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
