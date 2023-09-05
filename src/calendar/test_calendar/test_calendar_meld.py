from src.calendar.idea import IdeaKid
from src.calendar.calendar import CalendarUnit
from src.calendar.group import groupunit_shop
from src.calendar.member import memberunit_shop
from src.calendar.road import get_global_root_label as root_label
from pytest import raises as pytest_raises
from src.calendar.examples.example_calendars import calendar_v001
from src.calendar.x_func import get_on_meld_weight_actions


def test_calendar_meld_BaseScenario():
    # GIVEN
    calendar_text = "x_calendar"
    ax1 = CalendarUnit(_owner=calendar_text)
    ax2 = CalendarUnit(_owner=calendar_text)

    # WHEN
    ax1.meld(other_calendar=ax2)

    # THEN
    assert ax1
    assert ax1._owner == calendar_text


def test_calendar_meld_WeightDoesNotCombine():
    # GIVEN
    calendar_text = "x_calendar"
    ax1 = CalendarUnit(_owner=calendar_text)
    ax1._weight = 3
    ax2 = CalendarUnit(_owner=calendar_text)
    ax2._weight = 5

    # WHEN
    ax1.meld(other_calendar=ax2)

    # THEN
    assert ax1._weight == 3


def test_calendar_meld_MemberUnits():
    # GIVEN
    x1_name = "x1_member"
    x1_member = memberunit_shop(name=x1_name)

    calendar_text = "x_calendar"
    ax1 = CalendarUnit(_owner=calendar_text)
    ax1.set_memberunit(memberunit=x1_member)

    ax2 = CalendarUnit(_owner=calendar_text)
    ax2.set_memberunit(memberunit=x1_member)
    x2_name = "x2_member"
    x2_member = memberunit_shop(name=x2_name)
    ax2.set_memberunit(memberunit=x2_member)
    assert len(ax1._members) == 1

    # WHEN
    ax1.meld(other_calendar=ax2)

    # THEN
    assert len(ax1._members) == 2
    assert ax1._members.get(x1_name) != None
    assert ax1._members.get(x2_name) != None


def test_calendar_meld_GroupUnits():
    # GIVEN
    x1_name = "x1_group"
    x1_group = groupunit_shop(name=x1_name)

    calendar_text = "x_calendar"
    ax1 = CalendarUnit(_owner=calendar_text)
    ax1.set_groupunit(groupunit=x1_group)

    ax2 = CalendarUnit(_owner=calendar_text)
    ax2.set_groupunit(groupunit=x1_group)
    x2_name = "x2_group"
    x2_group = groupunit_shop(name=x2_name, uid=5)
    ax2.set_groupunit(groupunit=x2_group)
    assert len(ax1._groups) == 1

    # WHEN
    ax1.meld(other_calendar=ax2)

    # THEN
    # for group_name in ax1._groups.values():
    #     print(f"ax1 {group_name.name=}")

    assert len(ax1._groups) == 2
    assert ax1._groups.get(x1_name) != None
    assert ax1._groups.get(x2_name) != None
    # assert ax1._groups.get(x2_name).uid == 5


def test_calendar_idearoot_meld_IdeaRootAttrCorrectlyMelded():
    # GIVEN
    ax1 = CalendarUnit(_owner="spirit")
    ax2 = CalendarUnit(_owner="spirit")
    ax2._idearoot._uid = 4
    assert ax1._idearoot._uid == 1
    assert ax2._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        ax1.meld(ax2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea=None,{root_label()} _uid:1 with None,{root_label()} _uid:4"
    )


def test_calendar_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"
    free_road = f"{root_label()},{swim_text},{free_text}"

    ax1 = CalendarUnit(_owner="spirit")

    ax2 = CalendarUnit(_owner="spirit")
    ax2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1.get_idea_list()) == 5
    assert ax1.get_idea_kid(road=tech_road)._label == tech_text
    assert ax1.get_idea_kid(road=bowl_road)._label == bowl_text
    assert ax1.get_idea_kid(road=swim_road)._label == swim_text
    assert ax1.get_idea_kid(road=free_road)._label == free_text


def test_calendar_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"

    owner_text = "Yoa"
    ax1 = CalendarUnit(_owner=owner_text)
    ax1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    ax2 = CalendarUnit(_owner=owner_text)
    ax2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    assert ax1.get_idea_kid(road=bowl_road)._weight == 1
    # WHEN
    ax1.meld(ax2)

    # THEN
    assert ax1.get_idea_kid(road=bowl_road)._weight == 1
    assert len(ax1.get_idea_list()) == 3


def test_calendar_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"

    ax1 = CalendarUnit(_owner="test7")
    ax1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    ax1.set_acptfact(base=tech_road, pick=bowl_road)

    ax2 = CalendarUnit(_owner="test7")
    ax2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    ax2.set_acptfact(base=tech_road, pick=bowl_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1._idearoot._acptfactunits) == 1
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_calendar_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"

    ax1 = CalendarUnit(_owner="test7")
    ax1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    ax1.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    ax1.set_acptfact(base=tech_road, pick=bowl_road)

    ax2 = CalendarUnit(_owner="test7")
    ax2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    ax2.set_acptfact(base=tech_road, pick=bowl_road)
    ax2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1._idearoot._acptfactunits) == 2
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_calendar_acptfactunits_meld_IdeasMeldedBeforeAcptFacts():
    # GIVEN
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"

    ax1 = CalendarUnit(_owner="test7")

    ax2 = CalendarUnit(_owner="test7")
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    ax2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    print()
    assert len(ax1._idearoot._acptfactunits) == 1
    assert ax1.get_idea_kid(swim_road)._label == swim_text
    assert ax1._idearoot._kids[swim_text]._label == swim_text
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_calendar_acptfactunits_meld_GroupsMeldedBefore_Members():
    # GIVEN
    owner_text = "Yoa"
    ax1 = CalendarUnit(_owner=owner_text)
    ax2 = CalendarUnit(_owner=owner_text)
    bob = "bob"
    ax2.set_memberunit(memberunit_shop(name=bob))
    assert ax2._groups.get(bob) != None
    assert ax2._groups.get(bob).uid is None
    ax2.set_groupunit(groupunit_shop(name=bob, uid=13))
    assert ax2._groups.get(bob).uid == 13

    # WHEN/THEN
    assert ax1.meld(ax2) is None  # No error raised
    # with pytest_raises(Exception) as excinfo:
    #     ax1.meld(ax2)
    # assert (
    #     str(excinfo.value)
    #     == f"Meld fail GroupUnit bob .uid='None' not the same as .uid='13"
    # )


def test_calendar_acptfactunits_meld_AcptFactsAttributeCorrectlySet():
    # GIVEN
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"
    free_road = f"{root_label()},{free_text}"

    ax1 = CalendarUnit(_owner="test7")
    ax1.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))

    ax2 = CalendarUnit(_owner="test7")
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    ax2.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)

    # WHEN
    ax1.meld(ax2)

    # THEN
    print()
    assert len(ax1._idearoot._acptfactunits) == 1
    assert ax1._idearoot._acptfactunits[swim_road].base == swim_road
    assert ax1._idearoot._acptfactunits[swim_road].pick == free_road
    assert ax1._idearoot._acptfactunits[swim_road].open == 23
    assert ax1._idearoot._acptfactunits[swim_road].nigh == 27


def test_calendar_meld_worksCorrectlyForLargeExample():
    # GIVEN
    owner_text = "TlME"
    ax1 = CalendarUnit(_owner=owner_text)
    ax1._idearoot._uid = 1
    ax2 = calendar_v001()

    ax2r_bl = ax2._idearoot._grouplines
    fam_text = "Family"

    print(
        f"Before {ax2r_bl.get(fam_text)._calendar_credit=} {ax2._idearoot._kids_total_weight=}"
    )

    # WHEN
    ax1.meld(ax2)
    ax1.get_tree_metrics()

    # THEN
    print(
        f"After    {ax2r_bl.get(fam_text)._calendar_debt=} {ax2._idearoot._kids_total_weight=}"
    )
    assert ax1._weight == ax2._weight
    assert ax1._idearoot._kids == ax2._idearoot._kids
    assert ax1._idearoot._uid == ax2._idearoot._uid
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits
    assert ax1._groups == ax2._groups
    assert ax1._members == ax2._members

    assert len(ax1._idearoot._acptfactunits) == 2
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._owner == ax2._owner
    print(f"{len(ax1._groups.items())=}")
    # for ax1_group_key, ax1_group_obj in ax1._groups.items():
    #     print(f"{ax1_group_key=}")
    #     assert ax1_group_obj.uid == ax2._groups[ax1_group_key].uid
    #     assert ax1_group_obj == ax2._groups[ax1_group_key]
    assert ax1._groups == ax2._groups
    assert len(ax1.get_idea_list()) == len(ax2.get_idea_list())

    ax1r_bl = ax1._idearoot._grouplines
    print(
        f"Melded   {ax1r_bl.get(fam_text)._calendar_debt=} {ax1._idearoot._kids_total_weight=}"
    )

    assert ax1r_bl.get(fam_text) != None
    # assert ax1r_bl.get(fam_text) == ax2r_bl.get(fam_text)
    # assert ax1r_bl.get(fam_text).calendar_credit == ax2r_bl.get(fam_text).calendar_credit
    print(
        f"{ax1r_bl.get(fam_text)._calendar_credit=} {ax1._idearoot._kids_total_weight=}"
    )
    print(
        f"{ax2r_bl.get(fam_text)._calendar_credit=} {ax1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {ax1r_bl.get(fam_text)._calendar_debt=} {ax1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {ax2r_bl.get(fam_text)._calendar_debt=} {ax1._idearoot._kids_total_weight=}"
    )
    assert (
        abs(
            ax1r_bl.get(fam_text)._calendar_credit
            - ax2r_bl.get(fam_text)._calendar_credit
        )
        < 0.0001
    )
    assert (
        abs(ax1r_bl.get(fam_text)._calendar_debt - ax2r_bl.get(fam_text)._calendar_debt)
        < 0.0001
    )

    # for groupline in ax1r_bl.values():
    #     if groupline.name != fam_text:
    #         assert groupline == ax2r_bl.get(groupline.name)
    assert ax1r_bl == ax2r_bl
    # assert ax1._idearoot._grouplines == ax2._idearoot._grouplines
    # assert ax1._idearoot == ax2._idearoot


def test_get_on_meld_weight_actions_HasCorrectItems():
    assert len(get_on_meld_weight_actions()) == 5
    assert get_on_meld_weight_actions() == {
        "accept": None,
        "default": None,
        "match": None,
        "override": None,
        "sum": None,
    }
