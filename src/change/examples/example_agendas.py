from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import reasonunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop


def get_agenda_with_4_levels() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    idea_kid_casa = ideaunit_shop(casa, _weight=30, pledge=True)
    sue_agenda.add_l1_idea(idea_kid_casa)

    cat = "feed cat"
    idea_kid_feedcat = ideaunit_shop(cat, _weight=30, pledge=True)
    sue_agenda.add_l1_idea(idea_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    idea_kid_weekdays = ideaunit_shop(week_text, _weight=40)
    sue_agenda.add_l1_idea(idea_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    idea_grandkidU = ideaunit_shop(sun_text, _weight=20)
    idea_grandkidM = ideaunit_shop(mon_text, _weight=20)
    idea_grandkidT = ideaunit_shop(tue_text, _weight=20)
    idea_grandkidW = ideaunit_shop(wed_text, _weight=20)
    idea_grandkidR = ideaunit_shop(thu_text, _weight=30)
    idea_grandkidF = ideaunit_shop(fri_text, _weight=40)
    idea_grandkidA = ideaunit_shop(sat_text, _weight=50)

    sue_agenda.add_idea(idea_grandkidU, week_road)
    sue_agenda.add_idea(idea_grandkidM, week_road)
    sue_agenda.add_idea(idea_grandkidT, week_road)
    sue_agenda.add_idea(idea_grandkidW, week_road)
    sue_agenda.add_idea(idea_grandkidR, week_road)
    sue_agenda.add_idea(idea_grandkidF, week_road)
    sue_agenda.add_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    idea_kid_states = ideaunit_shop(states_text, _weight=30)
    sue_agenda.add_l1_idea(idea_kid_states)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = ideaunit_shop(usa_text, _weight=50)
    idea_grandkid_france = ideaunit_shop(france_text, _weight=50)
    idea_grandkid_brazil = ideaunit_shop(brazil_text, _weight=50)
    sue_agenda.add_idea(idea_grandkid_france, states_road)
    sue_agenda.add_idea(idea_grandkid_brazil, states_road)
    sue_agenda.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = ideaunit_shop(texas_text, _weight=50)
    idea_grandgrandkid_usa_oregon = ideaunit_shop(oregon_text, _weight=50)
    sue_agenda.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return sue_agenda


def get_agenda_with_4_levels_and_2reasons() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    week_reason = reasonunit_shop(week_road)
    week_reason.set_premise(wed_road)

    nation_text = "nation-state"
    nation_road = sue_agenda.make_l1_road(nation_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(nation_road, usa_text)
    nation_reason = reasonunit_shop(nation_road)
    nation_reason.set_premise(usa_road)

    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    sue_agenda.edit_idea_attr(road=casa_road, reason=week_reason)
    sue_agenda.edit_idea_attr(road=casa_road, reason=nation_reason)
    return sue_agenda


def get_agenda_with_4_levels_and_2reasons_2beliefs() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    sue_agenda.set_belief(base=week_road, pick=wed_road)
    sue_agenda.set_belief(base=states_road, pick=usa_road)
    return sue_agenda
