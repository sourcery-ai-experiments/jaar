from src.agenda.oath import oathunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises
from src.agenda.examples.example_agendas import agenda_v001


def test_AgendaUnit_meld_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob2_agenda = agendaunit_shop(bob_text)
    assert bob1_agenda
    assert bob1_agenda._owner_id == bob_text

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # THEN
    assert bob1_agenda
    assert bob1_agenda._owner_id == bob_text


def test_AgendaUnit_meld_WeightDoesNotCombine():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda._weight = 3
    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda._weight = 5
    assert bob1_agenda._weight == 3

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # THEN
    assert bob1_agenda._weight == 3


def test_AgendaUnit_meld_PartyUnits():
    # GIVEN
    yao_text = "Yao"
    yao_partyunit = partyunit_shop(party_id=yao_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_partyunit(yao_partyunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_partyunit(yao_partyunit)
    zia_text = "Zia"
    zia_partyunit = partyunit_shop(party_id=zia_text)
    bob2_agenda.set_partyunit(zia_partyunit)
    assert len(bob1_agenda._partys) == 1
    assert bob1_agenda.party_exists(yao_text)
    assert bob1_agenda.party_exists(zia_text) is False

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # THEN
    assert len(bob1_agenda._partys) == 2
    assert bob1_agenda.party_exists(yao_text)
    assert bob1_agenda.party_exists(zia_text)


def test_AgendaUnit_meld_PartyUnits_ignore_partyunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_partyunit = partyunit_shop(party_id=yao_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_partyunit(yao_partyunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_partyunit(yao_partyunit)
    zia_text = "Zia"
    zia_partyunit = partyunit_shop(party_id=zia_text)
    bob2_agenda.set_partyunit(zia_partyunit)
    assert len(bob1_agenda._partys) == 1
    assert bob1_agenda.party_exists(yao_text)
    assert bob1_agenda.party_exists(zia_text) is False

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda, ignore_partyunits=True)

    # THEN
    assert len(bob1_agenda._partys) == 1
    assert bob1_agenda.party_exists(yao_text)
    assert bob1_agenda.party_exists(zia_text) is False


def test_AgendaUnit_meld_IdeaUnits_WhereIdeaUnitIsMissing():
    # GIVEN
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(idea_id=run_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_ideaunit(run_ideaunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_ideaunit(run_ideaunit)
    swim_text = ",swimmers"
    swim_ideaunit = ideaunit_shop(idea_id=swim_text)
    bob2_agenda.set_ideaunit(swim_ideaunit)
    assert len(bob1_agenda._ideas) == 1
    assert bob1_agenda.get_ideaunit(run_text) != None
    assert bob1_agenda.get_ideaunit(swim_text) is None

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # THEN
    # for x_idea_id in bob1_agenda._ideas.values():
    #     print(f"bob1_agenda {x_idea_id.party_id=}")

    assert len(bob1_agenda._ideas) == 2
    assert bob1_agenda.get_ideaunit(run_text) != None
    assert bob1_agenda.get_ideaunit(swim_text) != None


def test_AgendaUnit_meld_IdeaUnits_WhereIdeaUnitMembershipIsDifferent():
    # GIVEN

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    sue_text = "Sue"
    bob1_agenda.set_partyunit(partyunit_shop(sue_text))

    run_text = ",runners"
    bob1_agenda.set_ideaunit(ideaunit_shop(run_text))
    bob1_agenda.get_ideaunit(run_text).set_partylink(partylink_shop(sue_text))

    bob2_agenda = agendaunit_shop(bob_text)
    yao_text = "Yao"
    bob2_agenda.set_partyunit(partyunit_shop(yao_text))
    bob2_agenda.set_partyunit(partyunit_shop(sue_text))
    bob2_agenda.set_ideaunit(ideaunit_shop(run_text))
    bob2_agenda.get_ideaunit(run_text).set_partylink(partylink_shop(yao_text))
    bob2_agenda.get_ideaunit(run_text).set_partylink(partylink_shop(sue_text))
    assert len(bob1_agenda._ideas) == 2
    assert len(bob1_agenda.get_ideaunit(run_text)._partys) == 1

    # WHEN
    bob1_agenda.meld(other_agenda=bob2_agenda)

    # THEN
    assert len(bob1_agenda._ideas) == 3
    assert len(bob1_agenda.get_ideaunit(run_text)._partys) == 2


def test_AgendaUnit_oathroot_meld_oathroot_AttrCorrectlyMelded():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda._oathroot._uid = 4
    assert bob1_agenda._oathroot._uid == 1
    assert bob2_agenda._oathroot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob1_agenda.meld(bob2_agenda)
    assert (
        str(excinfo.value)
        == f"Meld fail oath={bob1_agenda._real_id} _uid:1 with {bob2_agenda._real_id} _uid:4"
    )


def test_AgendaUnit_oathroot_meld_Add4OathsScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)

    tech_text = "tech"
    tech_road = bob1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_agenda.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_agenda.make_road(swim_road, free_text)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_l1_oath(oathunit_shop(tech_text))
    bob2_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    assert len(bob1_agenda.get_oath_dict()) == 1
    assert bob1_agenda.oath_exists(tech_road) is False
    assert bob1_agenda.oath_exists(bowl_road) is False
    assert bob1_agenda.oath_exists(swim_road) is False
    assert bob1_agenda.oath_exists(free_road) is False

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_agenda.get_oath_dict()) == 5
    assert bob1_agenda.oath_exists(tech_road)
    assert bob1_agenda.oath_exists(bowl_road)
    assert bob1_agenda.oath_exists(swim_road)
    assert bob1_agenda.oath_exists(free_road)
    assert bob1_agenda.get_oath_obj(tech_road)._label == tech_text
    assert bob1_agenda.get_oath_obj(bowl_road)._label == bowl_text
    assert bob1_agenda.get_oath_obj(swim_road)._label == swim_text
    assert bob1_agenda.get_oath_obj(free_road)._label == free_text


def test_AgendaUnit_oathroot_meld_2SameOathsScenario():
    # GIVEN
    yao_text = "Yao"
    yao1_agenda = agendaunit_shop(yao_text)
    tech_text = "tech"
    tech_road = yao1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = yao1_agenda.make_road(tech_road, bowl_text)

    yao1_agenda.add_l1_oath(oathunit_shop(tech_text))
    yao1_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)

    yao2_agenda = agendaunit_shop(yao_text)
    yao2_agenda.add_l1_oath(oathunit_shop(tech_text))
    yao2_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    assert yao1_agenda.get_oath_obj(bowl_road)._weight == 1
    assert len(yao1_agenda.get_oath_dict()) == 3

    # WHEN
    yao1_agenda.meld(yao2_agenda)

    # THEN
    assert yao1_agenda.get_oath_obj(bowl_road)._weight == 1
    assert len(yao1_agenda.get_oath_dict()) == 3


def test_AgendaUnit_beliefunits_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_agenda.make_road(tech_road, bowl_text)

    bob1_agenda.add_l1_oath(oathunit_shop(tech_text))
    bob1_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    bob1_agenda.set_belief(base=tech_road, pick=bowl_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_l1_oath(oathunit_shop(tech_text))
    bob2_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.set_belief(base=tech_road, pick=bowl_road)
    bob1_oathroot = bob1_agenda._oathroot
    bob2_oathroot = bob2_agenda._oathroot
    assert len(bob1_oathroot._beliefunits) == 1
    assert len(bob1_oathroot._beliefunits) == len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits == bob2_oathroot._beliefunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_oathroot._beliefunits) == 1
    assert len(bob1_oathroot._beliefunits) == len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits == bob2_oathroot._beliefunits


def test_AgendaUnit_beliefunits_meld_ReturnsCorrectObj_2BeliefUnits():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_agenda.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"

    bob1_agenda.add_l1_oath(oathunit_shop(tech_text))
    bob1_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    bob1_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    bob1_agenda.set_belief(base=tech_road, pick=bowl_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_l1_oath(oathunit_shop(tech_text))
    bob2_agenda.add_oath(oathunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_belief(base=tech_road, pick=bowl_road)
    bob2_agenda.set_belief(base=swim_road, pick=swim_road)
    bob1_oathroot = bob1_agenda._oathroot
    bob2_oathroot = bob2_agenda._oathroot
    assert len(bob1_oathroot._beliefunits) == 1
    assert len(bob1_oathroot._beliefunits) != len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits != bob2_oathroot._beliefunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_oathroot._beliefunits) == 2
    assert len(bob1_oathroot._beliefunits) == len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits == bob2_oathroot._beliefunits


def test_AgendaUnit_beliefunits_meld_OathsMeldedBeforeBeliefs():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_belief(base=swim_road, pick=swim_road)
    bob1_oathroot = bob1_agenda._oathroot
    bob2_oathroot = bob2_agenda._oathroot
    assert len(bob1_oathroot._beliefunits) == 0
    assert bob1_agenda.oath_exists(swim_road) is False
    assert len(bob1_oathroot._beliefunits) != len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits != bob2_agenda._oathroot._beliefunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_oathroot._beliefunits) == 1
    assert bob1_agenda.get_oath_obj(swim_road)._label == swim_text
    assert len(bob1_oathroot._beliefunits) == len(bob2_oathroot._beliefunits)
    assert bob1_oathroot._beliefunits == bob2_agenda._oathroot._beliefunits


def test_AgendaUnit_meld_IdeasMeldedBefore_Partys():
    # GIVEN
    yao_text = "Yao"
    yao1_agenda = agendaunit_shop(yao_text)
    yao2_agenda = agendaunit_shop(yao_text)
    bob_text = "Bob"
    yao2_agenda.set_partyunit(partyunit_shop(bob_text))
    assert yao2_agenda.get_ideaunit(bob_text) != None
    yao2_agenda.set_ideaunit(ideaunit_shop(bob_text, _party_mirror=True))

    # WHEN/THEN
    assert yao1_agenda.meld(yao2_agenda) is None  # No error raised


def test_AgendaUnit_beliefunits_meld_BeliefsAttributeCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_agenda.make_l1_road(free_text)
    bob1_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_belief(base=swim_road, pick=free_road, open=23, nigh=27)
    bob1_oathroot = bob1_agenda._oathroot
    assert len(bob1_oathroot._beliefunits) == 0

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_oathroot._beliefunits) == 1
    assert bob1_oathroot._beliefunits[swim_road].base == swim_road
    assert bob1_oathroot._beliefunits[swim_road].pick == free_road
    assert bob1_oathroot._beliefunits[swim_road].open == 23
    assert bob1_oathroot._beliefunits[swim_road].nigh == 27


def test_AgendaUnit_meld_ReturnsCorrectObj_LargeExample():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text, "music")
    bob_oathroot = bob_agenda._oathroot
    bob_oathroot._uid = 1
    yao_agenda = agenda_v001()

    yao_oathroot = yao_agenda._oathroot
    yao_agendar_bl = yao_oathroot._balancelines
    family_text = ",Family"
    yao_family_bl = yao_agendar_bl.get(family_text)

    print(f"Before {yao_family_bl._agenda_cred=} {yao_oathroot._kids_total_weight=}")
    print(f"Before   {yao_family_bl._agenda_debt=} {yao_oathroot._kids_total_weight=}")

    # WHEN
    bob_agenda.meld(yao_agenda)
    bob_agenda.get_tree_metrics()

    # THEN
    print(f"After  {yao_family_bl._agenda_cred=} {yao_oathroot._kids_total_weight=}")
    print(f"After    {yao_family_bl._agenda_debt=} {yao_oathroot._kids_total_weight=}")
    assert bob_agenda._weight == yao_agenda._weight
    assert bob_oathroot._kids == yao_oathroot._kids
    assert bob_oathroot._uid == yao_oathroot._uid
    assert bob_oathroot._beliefunits == yao_oathroot._beliefunits
    assert bob_agenda._ideas == yao_agenda._ideas
    assert bob_agenda._partys == yao_agenda._partys

    assert len(bob_oathroot._beliefunits) == 2
    assert len(bob_oathroot._beliefunits) == len(yao_oathroot._beliefunits)
    assert bob_agenda._owner_id != yao_agenda._owner_id
    print(f"{len(bob_agenda._ideas.items())=}")
    # for bob_agenda_idea_key, bob_agenda_idea_obj in bob_agenda._ideas.items():
    #     print(f"{bob_agenda_idea_key=}")
    #     assert bob_agenda_idea_obj.uid == yao_agenda._ideas[bob_agenda_idea_key].uid
    #     assert bob_agenda_idea_obj == yao_agenda._ideas[bob_agenda_idea_key]
    assert bob_agenda._ideas == yao_agenda._ideas
    assert len(bob_agenda.get_oath_dict()) == len(yao_agenda.get_oath_dict())

    bob_agendar_bl = bob_oathroot._balancelines
    bob_family_bl = bob_agendar_bl.get(family_text)
    print("Melded")

    assert bob_family_bl != None
    # assert bob_family_bl == yao_family_bl
    # assert bob_family_bl.agenda_cred == yao_family_bl .agenda_cred
    print(f"{bob_family_bl._agenda_cred=} {bob_oathroot._kids_total_weight=}")
    print(f"{yao_family_bl._agenda_cred=} {bob_oathroot._kids_total_weight=}")
    print(f"  {bob_family_bl._agenda_debt=} {bob_oathroot._kids_total_weight=}")
    print(f"  {yao_family_bl._agenda_debt=} {bob_oathroot._kids_total_weight=}")
    assert abs(bob_family_bl._agenda_cred - yao_family_bl._agenda_cred) < 0.0001
    assert abs(bob_family_bl._agenda_debt - yao_family_bl._agenda_debt) < 0.0001

    # for balanceline in bob_agendar_bl.values():
    #     if balanceline.party_id != fam_text:
    #         assert balanceline == yao_agendar_bl.get(balanceline.party_id)
    assert bob_agendar_bl == yao_agendar_bl
    # assert x_agenda1._oathroot._balancelines == bob2_agenda._oathroot._balancelines
    # assert x_agenda1._oathroot == bob2_agenda._oathroot


def test_AgendaUnit__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_agenda = agendaunit_shop(bob_text)
    assert len(bob_agenda._originunit._links) == 0

    # WHEN
    bob_agenda._meld_originlinks(party_id=sue_text, party_weight=sue_weight)

    # THEN
    assert len(bob_agenda._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(party_id=sue_text, weight=sue_weight)
    assert bob_agenda._originunit == bob_sue_originunit


def test_AgendaUnit_meld_OriginUnitsCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob_agenda.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob_agenda.make_road(swim_road, free_text)
    back_text = "backstroke"
    back_road = bob_agenda.make_road(swim_road, back_text)
    bob_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)

    sue_text = "Sue"
    sue_weight = 4
    sue_x_agenda = agendaunit_shop(sue_text)
    sue_x_agenda.add_oath(oathunit_shop(free_text), parent_road=swim_road)
    sue_x_agenda.set_belief(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_agenda.add_oath(oathunit_shop(back_text), parent_road=swim_road)
    assert len(bob_agenda._originunit._links) == 0

    # WHEN
    bob_agenda.meld(sue_x_agenda, party_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(party_id=sue_text, weight=sue_weight)
    assert len(bob_agenda._originunit._links) == 1
    assert bob_agenda._originunit == sue_originunit
    bob_free_oath = bob_agenda.get_oath_obj(free_road)
    bob_back_oath = bob_agenda.get_oath_obj(back_road)
    print(f"{bob_free_oath._originunit=}")
    print(f"{bob_back_oath._originunit=}")
    assert bob_free_oath._originunit != None
    assert bob_free_oath._originunit != originunit_shop()
    assert bob_free_oath._originunit == sue_originunit
    assert bob_back_oath._originunit != None
    assert bob_back_oath._originunit != originunit_shop()
    assert bob_back_oath._originunit == sue_originunit
