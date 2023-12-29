from src.agenda.idea import idea_kid_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.party import partyunit_shop
from src.agenda.origin import originunit_shop
from pytest import raises as pytest_raises
from src.agenda.examples.example_agendas import agenda_v001
from src.agenda.x_func import get_on_meld_weight_actions


def test_agenda_meld_BaseScenario():
    # GIVEN
    agenda_text = "x_agenda"
    x_agenda1 = agendaunit_shop(_healer=agenda_text)
    x_agenda2 = agendaunit_shop(_healer=agenda_text)

    # WHEN
    x_agenda1.meld(other_agenda=x_agenda2)

    # THEN
    assert x_agenda1
    assert x_agenda1._healer == agenda_text


def test_agenda_meld_WeightDoesNotCombine():
    # GIVEN
    agenda_text = "x_agenda"
    x_agenda1 = agendaunit_shop(_healer=agenda_text)
    x_agenda1._weight = 3
    x_agenda2 = agendaunit_shop(_healer=agenda_text)
    x_agenda2._weight = 5

    # WHEN
    x_agenda1.meld(other_agenda=x_agenda2)

    # THEN
    assert x_agenda1._weight == 3


def test_agenda_meld_PartyUnits():
    # GIVEN
    x1_pid = "x1_party"
    x1_party = partyunit_shop(pid=x1_pid)

    agenda_text = "x_agenda"
    x_agenda1 = agendaunit_shop(_healer=agenda_text)
    x_agenda1.set_partyunit(partyunit=x1_party)

    x_agenda2 = agendaunit_shop(_healer=agenda_text)
    x_agenda2.set_partyunit(partyunit=x1_party)
    x2_pid = "x2_party"
    x2_party = partyunit_shop(pid=x2_pid)
    x_agenda2.set_partyunit(partyunit=x2_party)
    assert len(x_agenda1._partys) == 1

    # WHEN
    x_agenda1.meld(other_agenda=x_agenda2)

    # THEN
    assert len(x_agenda1._partys) == 2
    assert x_agenda1._partys.get(x1_pid) != None
    assert x_agenda1._partys.get(x2_pid) != None


def test_agenda_meld_GroupUnits():
    # GIVEN
    x1_pid = "x1_group"
    x1_group = groupunit_shop(brand=x1_pid)

    agenda_text = "x_agenda"
    x_agenda1 = agendaunit_shop(_healer=agenda_text)
    x_agenda1.set_groupunit(y_groupunit=x1_group)

    x_agenda2 = agendaunit_shop(_healer=agenda_text)
    x_agenda2.set_groupunit(y_groupunit=x1_group)
    x2_pid = "x2_group"
    x2_group = groupunit_shop(brand=x2_pid, uid=5)
    x_agenda2.set_groupunit(y_groupunit=x2_group)
    assert len(x_agenda1._groups) == 1

    # WHEN
    x_agenda1.meld(other_agenda=x_agenda2)

    # THEN
    # for group_pid in x_agenda1._groups.values():
    #     print(f"x_agenda1 {group_pid.pid=}")

    assert len(x_agenda1._groups) == 2
    assert x_agenda1._groups.get(x1_pid) != None
    assert x_agenda1._groups.get(x2_pid) != None
    # assert x_agenda1._groups.get(x2_pid).uid == 5


def test_agenda_idearoot_meld_idearoot_AttrCorrectlyMelded():
    # GIVEN
    x_agenda1 = agendaunit_shop(_healer="spirit")
    x_agenda2 = agendaunit_shop(_healer="spirit")
    x_agenda2._idearoot._uid = 4
    assert x_agenda1._idearoot._uid == 1
    assert x_agenda2._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_agenda1.meld(x_agenda2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={x_agenda1._economy_id} _uid:1 with {x_agenda2._economy_id} _uid:4"
    )


def test_agenda_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    spirit_text = "spirit"
    x_agenda1 = agendaunit_shop(_healer=spirit_text)

    tech_text = "tech"
    tech_road = x_agenda1.make_road(x_agenda1._economy_id, tech_text)
    bowl_text = "bowl"
    bowl_road = x_agenda1.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    free_text = "freestyle"
    free_road = x_agenda1.make_road(swim_road, free_text)

    x_agenda2 = agendaunit_shop(_healer=spirit_text)
    x_agenda2.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda2._economy_id)
    x_agenda2.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)
    x_agenda2.add_idea(idea_kid_shop(free_text), parent_road=swim_road)

    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    assert len(x_agenda1.get_idea_list()) == 5
    assert x_agenda1.get_idea_obj(tech_road)._label == tech_text
    assert x_agenda1.get_idea_obj(bowl_road)._label == bowl_text
    assert x_agenda1.get_idea_obj(swim_road)._label == swim_text
    assert x_agenda1.get_idea_obj(free_road)._label == free_text


def test_agenda_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    healer_text = "Yoa"
    x_agenda1 = agendaunit_shop(_healer=healer_text)
    tech_text = "tech"
    tech_road = x_agenda1.make_road(x_agenda1._economy_id, tech_text)
    bowl_text = "bowl"
    bowl_road = x_agenda1.make_road(tech_road, bowl_text)

    x_agenda1.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda1._economy_id)
    x_agenda1.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)

    x_agenda2 = agendaunit_shop(_healer=healer_text)
    x_agenda2.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda2._economy_id)
    x_agenda2.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)

    assert x_agenda1.get_idea_obj(bowl_road)._weight == 1
    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    assert x_agenda1.get_idea_obj(bowl_road)._weight == 1
    assert len(x_agenda1.get_idea_list()) == 3


def test_agenda_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    x_agenda1 = agendaunit_shop(_healer="test7")
    tech_text = "tech"
    tech_road = x_agenda1.make_road(x_agenda1._economy_id, tech_text)
    bowl_text = "bowl"
    bowl_road = x_agenda1.make_road(tech_road, bowl_text)

    x_agenda1.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda1._economy_id)
    x_agenda1.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)
    x_agenda1.set_acptfact(base=tech_road, pick=bowl_road)

    x_agenda2 = agendaunit_shop(_healer="test7")
    x_agenda2.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda2._economy_id)
    x_agenda2.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)
    x_agenda2.set_acptfact(base=tech_road, pick=bowl_road)

    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    assert len(x_agenda1._idearoot._acptfactunits) == 1
    assert len(x_agenda1._idearoot._acptfactunits) == len(
        x_agenda2._idearoot._acptfactunits
    )
    assert x_agenda1._idearoot._acptfactunits == x_agenda2._idearoot._acptfactunits


def test_agenda_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    x_agenda1 = agendaunit_shop(_healer="test7")
    tech_text = "tech"
    tech_road = x_agenda1.make_road(x_agenda1._economy_id, tech_text)
    bowl_text = "bowl"
    bowl_road = x_agenda1.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    free_text = "freestyle"

    x_agenda1.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda1._economy_id)
    x_agenda1.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)
    x_agenda1.add_idea(idea_kid_shop(free_text), parent_road=swim_road)
    x_agenda1.set_acptfact(base=tech_road, pick=bowl_road)

    x_agenda2 = agendaunit_shop(_healer="test7")
    x_agenda2.add_idea(idea_kid_shop(tech_text), parent_road=x_agenda2._economy_id)
    x_agenda2.add_idea(idea_kid_shop(bowl_text), parent_road=tech_road)
    x_agenda2.add_idea(idea_kid_shop(free_text), parent_road=swim_road)
    x_agenda2.set_acptfact(base=tech_road, pick=bowl_road)
    x_agenda2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    assert len(x_agenda1._idearoot._acptfactunits) == 2
    assert len(x_agenda1._idearoot._acptfactunits) == len(
        x_agenda2._idearoot._acptfactunits
    )
    assert x_agenda1._idearoot._acptfactunits == x_agenda2._idearoot._acptfactunits


def test_agenda_acptfactunits_meld_IdeasMeldedBeforeAcptFacts():
    # GIVEN
    x_agenda1 = agendaunit_shop(_healer="test7")

    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    free_text = "freestyle"

    x_agenda2 = agendaunit_shop(_healer="test7")
    x_agenda2.add_idea(idea_kid_shop(free_text), parent_road=swim_road)
    x_agenda2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    print()
    assert len(x_agenda1._idearoot._acptfactunits) == 1
    assert x_agenda1.get_idea_obj(swim_road)._label == swim_text
    assert x_agenda1._idearoot._kids[swim_text]._label == swim_text
    assert len(x_agenda1._idearoot._acptfactunits) == len(
        x_agenda2._idearoot._acptfactunits
    )
    assert x_agenda1._idearoot._acptfactunits == x_agenda2._idearoot._acptfactunits


def test_agenda_acptfactunits_meld_GroupsMeldedBefore_Partys():
    # GIVEN
    healer_text = "Yoa"
    x_agenda1 = agendaunit_shop(_healer=healer_text)
    x_agenda2 = agendaunit_shop(_healer=healer_text)
    bob = "bob"
    x_agenda2.set_partyunit(partyunit_shop(pid=bob))
    assert x_agenda2._groups.get(bob) != None
    assert x_agenda2._groups.get(bob).uid is None
    x_agenda2.set_groupunit(groupunit_shop(brand=bob, uid=13))
    assert x_agenda2._groups.get(bob).uid == 13

    # WHEN/THEN
    assert x_agenda1.meld(x_agenda2) is None  # No error raised
    # with pytest_raises(Exception) as excinfo:
    #     x_agenda1.meld(x_agenda2)
    # assert (
    #     str(excinfo.value)
    #     == f"Meld fail GroupUnit bob .uid='None' not the same as .uid='13"
    # )


def test_agenda_acptfactunits_meld_AcptFactsAttributeCorrectlySet():
    # GIVEN
    x_agenda1 = agendaunit_shop(_healer="test7")

    swim_text = "swim"
    swim_road = x_agenda1.make_road(x_agenda1._economy_id, swim_text)
    free_text = "freestyle"
    free_road = x_agenda1.make_road(x_agenda1._economy_id, free_text)
    x_agenda1.add_idea(idea_kid_shop(free_text), parent_road=swim_road)

    x_agenda2 = agendaunit_shop(_healer="test7")
    x_agenda2.add_idea(idea_kid_shop(free_text), parent_road=swim_road)
    x_agenda2.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)

    # WHEN
    x_agenda1.meld(x_agenda2)

    # THEN
    print()
    assert len(x_agenda1._idearoot._acptfactunits) == 1
    assert x_agenda1._idearoot._acptfactunits[swim_road].base == swim_road
    assert x_agenda1._idearoot._acptfactunits[swim_road].pick == free_road
    assert x_agenda1._idearoot._acptfactunits[swim_road].open == 23
    assert x_agenda1._idearoot._acptfactunits[swim_road].nigh == 27


def test_agenda_meld_worksCorrectlyForLargeExample():
    # GIVEN
    healer_text = "TlME"
    x_agenda1 = agendaunit_shop(_healer=healer_text)
    x_agenda1._idearoot._uid = 1
    x_agenda2 = agenda_v001()

    x_agenda2r_bl = x_agenda2._idearoot._balancelines
    fam_text = "Family"

    print(
        f"Before {x_agenda2r_bl.get(fam_text)._agenda_credit=} {x_agenda2._idearoot._kids_total_weight=}"
    )

    # WHEN
    x_agenda1.meld(x_agenda2)
    x_agenda1.get_tree_metrics()

    # THEN
    print(
        f"After    {x_agenda2r_bl.get(fam_text)._agenda_debt=} {x_agenda2._idearoot._kids_total_weight=}"
    )
    assert x_agenda1._weight == x_agenda2._weight
    assert x_agenda1._idearoot._kids == x_agenda2._idearoot._kids
    assert x_agenda1._idearoot._uid == x_agenda2._idearoot._uid
    assert x_agenda1._idearoot._acptfactunits == x_agenda2._idearoot._acptfactunits
    assert x_agenda1._groups == x_agenda2._groups
    assert x_agenda1._partys == x_agenda2._partys

    assert len(x_agenda1._idearoot._acptfactunits) == 2
    assert len(x_agenda1._idearoot._acptfactunits) == len(
        x_agenda2._idearoot._acptfactunits
    )
    assert x_agenda1._healer != x_agenda2._healer
    print(f"{len(x_agenda1._groups.items())=}")
    # for x_agenda1_group_key, x_agenda1_group_obj in x_agenda1._groups.items():
    #     print(f"{x_agenda1_group_key=}")
    #     assert x_agenda1_group_obj.uid == x_agenda2._groups[x_agenda1_group_key].uid
    #     assert x_agenda1_group_obj == x_agenda2._groups[x_agenda1_group_key]
    assert x_agenda1._groups == x_agenda2._groups
    assert len(x_agenda1.get_idea_list()) == len(x_agenda2.get_idea_list())

    x_agenda1r_bl = x_agenda1._idearoot._balancelines
    print(
        f"Melded   {x_agenda1r_bl.get(fam_text)._agenda_debt=} {x_agenda1._idearoot._kids_total_weight=}"
    )

    assert x_agenda1r_bl.get(fam_text) != None
    # assert x_agenda1r_bl.get(fam_text) == x_agenda2r_bl.get(fam_text)
    # assert x_agenda1r_bl.get(fam_text).agenda_credit == x_agenda2r_bl.get(fam_text).agenda_credit
    print(
        f"{x_agenda1r_bl.get(fam_text)._agenda_credit=} {x_agenda1._idearoot._kids_total_weight=}"
    )
    print(
        f"{x_agenda2r_bl.get(fam_text)._agenda_credit=} {x_agenda1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {x_agenda1r_bl.get(fam_text)._agenda_debt=} {x_agenda1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {x_agenda2r_bl.get(fam_text)._agenda_debt=} {x_agenda1._idearoot._kids_total_weight=}"
    )
    assert (
        abs(
            x_agenda1r_bl.get(fam_text)._agenda_credit
            - x_agenda2r_bl.get(fam_text)._agenda_credit
        )
        < 0.0001
    )
    assert (
        abs(
            x_agenda1r_bl.get(fam_text)._agenda_debt
            - x_agenda2r_bl.get(fam_text)._agenda_debt
        )
        < 0.0001
    )

    # for balanceline in x_agenda1r_bl.values():
    #     if balanceline.pid != fam_text:
    #         assert balanceline == x_agenda2r_bl.get(balanceline.pid)
    assert x_agenda1r_bl == x_agenda2r_bl
    # assert x_agenda1._idearoot._balancelines == x_agenda2._idearoot._balancelines
    # assert x_agenda1._idearoot == x_agenda2._idearoot


def test_get_on_meld_weight_actions_HasCorrectItems():
    assert len(get_on_meld_weight_actions()) == 5
    assert get_on_meld_weight_actions() == {
        "accept": None,
        "default": None,
        "match": None,
        "override": None,
        "sum": None,
    }


def test_agenda__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_x_agenda = agendaunit_shop(_healer=bob_text)
    assert len(bob_x_agenda._originunit._links) == 0

    # WHEN
    bob_x_agenda._meld_originlinks(party_pid=sue_text, party_weight=sue_weight)

    # THEN
    assert len(bob_x_agenda._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(pid=sue_text, weight=sue_weight)
    assert bob_x_agenda._originunit == bob_sue_originunit


def test_agenda_meld_OriginUnitsCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob_x_agenda = agendaunit_shop(_healer=bob_text)

    swim_text = "swim"
    swim_road = bob_x_agenda.make_road(bob_x_agenda._economy_id, swim_text)
    free_text = "freestyle"
    free_road = bob_x_agenda.make_road(swim_road, free_text)
    back_text = "backstroke"
    back_road = bob_x_agenda.make_road(swim_road, back_text)
    bob_x_agenda.add_idea(idea_kid_shop(free_text), parent_road=swim_road)

    sue_text = "Sue"
    sue_weight = 4
    sue_x_agenda = agendaunit_shop(_healer=sue_text)
    sue_x_agenda.add_idea(idea_kid_shop(free_text), parent_road=swim_road)
    sue_x_agenda.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_agenda.add_idea(idea_kid_shop(back_text), parent_road=swim_road)
    assert len(bob_x_agenda._originunit._links) == 0

    # WHEN
    bob_x_agenda.meld(sue_x_agenda, party_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(pid=sue_text, weight=sue_weight)
    assert len(bob_x_agenda._originunit._links) == 1
    assert bob_x_agenda._originunit == sue_originunit
    bob_free_idea = bob_x_agenda.get_idea_obj(free_road)
    bob_back_idea = bob_x_agenda.get_idea_obj(back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
