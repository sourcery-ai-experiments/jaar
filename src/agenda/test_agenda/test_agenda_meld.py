from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.belief import beliefunit_shop
from src.agenda.guy import guyunit_shop, guylink_shop
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
    bob1_agenda.meld(exterior_agenda=bob2_agenda)

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
    bob1_agenda.meld(exterior_agenda=bob2_agenda)

    # THEN
    assert bob1_agenda._weight == 3


def test_AgendaUnit_meld_GuyUnits():
    # GIVEN
    yao_text = "Yao"
    yao_guyunit = guyunit_shop(guy_id=yao_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_guyunit(yao_guyunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_guyunit(yao_guyunit)
    zia_text = "Zia"
    zia_guyunit = guyunit_shop(guy_id=zia_text)
    bob2_agenda.set_guyunit(zia_guyunit)
    assert len(bob1_agenda._guys) == 1
    assert bob1_agenda.guy_exists(yao_text)
    assert bob1_agenda.guy_exists(zia_text) is False

    # WHEN
    bob1_agenda.meld(exterior_agenda=bob2_agenda)

    # THEN
    assert len(bob1_agenda._guys) == 2
    assert bob1_agenda.guy_exists(yao_text)
    assert bob1_agenda.guy_exists(zia_text)


def test_AgendaUnit_meld_GuyUnits_ignore_guyunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_guyunit = guyunit_shop(guy_id=yao_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_guyunit(yao_guyunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_guyunit(yao_guyunit)
    zia_text = "Zia"
    zia_guyunit = guyunit_shop(guy_id=zia_text)
    bob2_agenda.set_guyunit(zia_guyunit)
    assert len(bob1_agenda._guys) == 1
    assert bob1_agenda.guy_exists(yao_text)
    assert bob1_agenda.guy_exists(zia_text) is False

    # WHEN
    bob1_agenda.meld(exterior_agenda=bob2_agenda, ignore_guyunits=True)

    # THEN
    assert len(bob1_agenda._guys) == 1
    assert bob1_agenda.guy_exists(yao_text)
    assert bob1_agenda.guy_exists(zia_text) is False


def test_AgendaUnit_meld_BeliefUnits_WhereBeliefUnitIsMissing():
    # GIVEN
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(belief_id=run_text)

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob1_agenda.set_beliefunit(run_beliefunit)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.set_beliefunit(run_beliefunit)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    bob2_agenda.set_beliefunit(swim_beliefunit)
    assert len(bob1_agenda._beliefs) == 1
    assert bob1_agenda.get_beliefunit(run_text) != None
    assert bob1_agenda.get_beliefunit(swim_text) is None

    # WHEN
    bob1_agenda.meld(exterior_agenda=bob2_agenda)

    # THEN
    # for x_belief_id in bob1_agenda._beliefs.values():
    #     print(f"bob1_agenda {x_belief_id.guy_id=}")

    assert len(bob1_agenda._beliefs) == 2
    assert bob1_agenda.get_beliefunit(run_text) != None
    assert bob1_agenda.get_beliefunit(swim_text) != None


def test_AgendaUnit_meld_BeliefUnits_WhereBeliefUnitMembershipIsDifferent():
    # GIVEN

    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    sue_text = "Sue"
    bob1_agenda.set_guyunit(guyunit_shop(sue_text))

    run_text = ",runners"
    bob1_agenda.set_beliefunit(beliefunit_shop(run_text))
    bob1_agenda.get_beliefunit(run_text).set_guylink(guylink_shop(sue_text))

    bob2_agenda = agendaunit_shop(bob_text)
    yao_text = "Yao"
    bob2_agenda.set_guyunit(guyunit_shop(yao_text))
    bob2_agenda.set_guyunit(guyunit_shop(sue_text))
    bob2_agenda.set_beliefunit(beliefunit_shop(run_text))
    bob2_agenda.get_beliefunit(run_text).set_guylink(guylink_shop(yao_text))
    bob2_agenda.get_beliefunit(run_text).set_guylink(guylink_shop(sue_text))
    assert len(bob1_agenda._beliefs) == 2
    assert len(bob1_agenda.get_beliefunit(run_text)._guys) == 1

    # WHEN
    bob1_agenda.meld(exterior_agenda=bob2_agenda)

    # THEN
    assert len(bob1_agenda._beliefs) == 3
    assert len(bob1_agenda.get_beliefunit(run_text)._guys) == 2


def test_AgendaUnit_idearoot_meld_idearoot_AttrCorrectlyMelded():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda._idearoot._uid = 4
    assert bob1_agenda._idearoot._uid == 1
    assert bob2_agenda._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob1_agenda.meld(bob2_agenda)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={bob1_agenda._real_id} _uid:1 with {bob2_agenda._real_id} _uid:4"
    )


def test_AgendaUnit_idearoot_meld_Add4IdeasScenario():
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
    bob2_agenda.add_l1_idea(ideaunit_shop(tech_text))
    bob2_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    assert len(bob1_agenda.get_idea_dict()) == 1
    assert bob1_agenda.idea_exists(tech_road) is False
    assert bob1_agenda.idea_exists(bowl_road) is False
    assert bob1_agenda.idea_exists(swim_road) is False
    assert bob1_agenda.idea_exists(free_road) is False

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_agenda.get_idea_dict()) == 5
    assert bob1_agenda.idea_exists(tech_road)
    assert bob1_agenda.idea_exists(bowl_road)
    assert bob1_agenda.idea_exists(swim_road)
    assert bob1_agenda.idea_exists(free_road)
    assert bob1_agenda.get_idea_obj(tech_road)._label == tech_text
    assert bob1_agenda.get_idea_obj(bowl_road)._label == bowl_text
    assert bob1_agenda.get_idea_obj(swim_road)._label == swim_text
    assert bob1_agenda.get_idea_obj(free_road)._label == free_text


def test_AgendaUnit_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    yao_text = "Yao"
    yao1_agenda = agendaunit_shop(yao_text)
    tech_text = "tech"
    tech_road = yao1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = yao1_agenda.make_road(tech_road, bowl_text)

    yao1_agenda.add_l1_idea(ideaunit_shop(tech_text))
    yao1_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)

    yao2_agenda = agendaunit_shop(yao_text)
    yao2_agenda.add_l1_idea(ideaunit_shop(tech_text))
    yao2_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    assert yao1_agenda.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_agenda.get_idea_dict()) == 3

    # WHEN
    yao1_agenda.meld(yao2_agenda)

    # THEN
    assert yao1_agenda.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_agenda.get_idea_dict()) == 3


def test_AgendaUnit_factunits_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_agenda.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_agenda.make_road(tech_road, bowl_text)

    bob1_agenda.add_l1_idea(ideaunit_shop(tech_text))
    bob1_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_agenda.set_fact(base=tech_road, pick=bowl_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_l1_idea(ideaunit_shop(tech_text))
    bob2_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.set_fact(base=tech_road, pick=bowl_road)
    bob1_idearoot = bob1_agenda._idearoot
    bob2_idearoot = bob2_agenda._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_AgendaUnit_factunits_meld_ReturnsCorrectObj_2FactUnits():
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

    bob1_agenda.add_l1_idea(ideaunit_shop(tech_text))
    bob1_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob1_agenda.set_fact(base=tech_road, pick=bowl_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_l1_idea(ideaunit_shop(tech_text))
    bob2_agenda.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_fact(base=tech_road, pick=bowl_road)
    bob2_agenda.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_agenda._idearoot
    bob2_idearoot = bob2_agenda._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_idearoot._factunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_idearoot._factunits) == 2
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_AgendaUnit_factunits_meld_IdeasMeldedBeforeFacts():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_agenda._idearoot
    bob2_idearoot = bob2_agenda._idearoot
    assert len(bob1_idearoot._factunits) == 0
    assert bob1_agenda.idea_exists(swim_road) is False
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_agenda._idearoot._factunits

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_agenda.get_idea_obj(swim_road)._label == swim_text
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_agenda._idearoot._factunits


def test_AgendaUnit_meld_BeliefsMeldedBefore_Guys():
    # GIVEN
    yao_text = "Yao"
    yao1_agenda = agendaunit_shop(yao_text)
    yao2_agenda = agendaunit_shop(yao_text)
    bob_text = "Bob"
    yao2_agenda.set_guyunit(guyunit_shop(bob_text))
    assert yao2_agenda.get_beliefunit(bob_text) != None
    yao2_agenda.set_beliefunit(beliefunit_shop(bob_text, _guy_mirror=True))

    # WHEN/THEN
    assert yao1_agenda.meld(yao2_agenda) is None  # No error raised


def test_AgendaUnit_factunits_meld_FactsAttributeCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob1_agenda = agendaunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_agenda.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_agenda.make_l1_road(free_text)
    bob1_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    bob2_agenda = agendaunit_shop(bob_text)
    bob2_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_agenda.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    bob1_idearoot = bob1_agenda._idearoot
    assert len(bob1_idearoot._factunits) == 0

    # WHEN
    bob1_agenda.meld(bob2_agenda)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_idearoot._factunits[swim_road].base == swim_road
    assert bob1_idearoot._factunits[swim_road].pick == free_road
    assert bob1_idearoot._factunits[swim_road].open == 23
    assert bob1_idearoot._factunits[swim_road].nigh == 27


def test_AgendaUnit_meld_ReturnsCorrectObj_LargeExample():
    # GIVEN
    bob_text = "Bob"
    bob_agenda = agendaunit_shop(bob_text, "music")
    bob_idearoot = bob_agenda._idearoot
    bob_idearoot._uid = 1
    yao_agenda = agenda_v001()

    yao_idearoot = yao_agenda._idearoot
    yao_agendar_bl = yao_idearoot._balancelines
    family_text = ",Family"
    yao_family_bl = yao_agendar_bl.get(family_text)

    print(f"Before {yao_family_bl._agenda_cred=} {yao_idearoot._kids_total_weight=}")
    print(f"Before   {yao_family_bl._agenda_debt=} {yao_idearoot._kids_total_weight=}")

    # WHEN
    bob_agenda.meld(yao_agenda)
    bob_agenda.get_tree_metrics()

    # THEN
    print(f"After  {yao_family_bl._agenda_cred=} {yao_idearoot._kids_total_weight=}")
    print(f"After    {yao_family_bl._agenda_debt=} {yao_idearoot._kids_total_weight=}")
    assert bob_agenda._weight == yao_agenda._weight
    assert bob_idearoot._kids == yao_idearoot._kids
    assert bob_idearoot._uid == yao_idearoot._uid
    assert bob_idearoot._factunits == yao_idearoot._factunits
    assert bob_agenda._beliefs == yao_agenda._beliefs
    assert bob_agenda._guys == yao_agenda._guys

    assert len(bob_idearoot._factunits) == 2
    assert len(bob_idearoot._factunits) == len(yao_idearoot._factunits)
    assert bob_agenda._owner_id != yao_agenda._owner_id
    print(f"{len(bob_agenda._beliefs.items())=}")
    # for bob_agenda_belief_key, bob_agenda_belief_obj in bob_agenda._beliefs.items():
    #     print(f"{bob_agenda_belief_key=}")
    #     assert bob_agenda_belief_obj.uid == yao_agenda._beliefs[bob_agenda_belief_key].uid
    #     assert bob_agenda_belief_obj == yao_agenda._beliefs[bob_agenda_belief_key]
    assert bob_agenda._beliefs == yao_agenda._beliefs
    assert len(bob_agenda.get_idea_dict()) == len(yao_agenda.get_idea_dict())

    bob_agendar_bl = bob_idearoot._balancelines
    bob_family_bl = bob_agendar_bl.get(family_text)
    print("Melded")

    assert bob_family_bl != None
    # assert bob_family_bl == yao_family_bl
    # assert bob_family_bl.agenda_cred == yao_family_bl .agenda_cred
    print(f"{bob_family_bl._agenda_cred=} {bob_idearoot._kids_total_weight=}")
    print(f"{yao_family_bl._agenda_cred=} {bob_idearoot._kids_total_weight=}")
    print(f"  {bob_family_bl._agenda_debt=} {bob_idearoot._kids_total_weight=}")
    print(f"  {yao_family_bl._agenda_debt=} {bob_idearoot._kids_total_weight=}")
    assert abs(bob_family_bl._agenda_cred - yao_family_bl._agenda_cred) < 0.0001
    assert abs(bob_family_bl._agenda_debt - yao_family_bl._agenda_debt) < 0.0001

    # for balanceline in bob_agendar_bl.values():
    #     if balanceline.guy_id != fam_text:
    #         assert balanceline == yao_agendar_bl.get(balanceline.guy_id)
    assert bob_agendar_bl == yao_agendar_bl
    # assert x_agenda1._idearoot._balancelines == bob2_agenda._idearoot._balancelines
    # assert x_agenda1._idearoot == bob2_agenda._idearoot


def test_AgendaUnit__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_agenda = agendaunit_shop(bob_text)
    assert len(bob_agenda._originunit._links) == 0

    # WHEN
    bob_agenda._meld_originlinks(guy_id=sue_text, guy_weight=sue_weight)

    # THEN
    assert len(bob_agenda._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(guy_id=sue_text, weight=sue_weight)
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
    bob_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    sue_text = "Sue"
    sue_weight = 4
    sue_x_agenda = agendaunit_shop(sue_text)
    sue_x_agenda.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    sue_x_agenda.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_agenda.add_idea(ideaunit_shop(back_text), parent_road=swim_road)
    assert len(bob_agenda._originunit._links) == 0

    # WHEN
    bob_agenda.meld(sue_x_agenda, guy_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(guy_id=sue_text, weight=sue_weight)
    assert len(bob_agenda._originunit._links) == 1
    assert bob_agenda._originunit == sue_originunit
    bob_free_idea = bob_agenda.get_idea_obj(free_road)
    bob_back_idea = bob_agenda.get_idea_obj(back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
