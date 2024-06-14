from src.agenda.fact import factunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop


def get_agenda_with_4_levels() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    fact_kid_casa = factunit_shop(casa, _weight=30, pledge=True)
    sue_agenda.add_l1_fact(fact_kid_casa)

    cat = "feed cat"
    fact_kid_feedcat = factunit_shop(cat, _weight=30, pledge=True)
    sue_agenda.add_l1_fact(fact_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    fact_kid_weekdays = factunit_shop(week_text, _weight=40)
    sue_agenda.add_l1_fact(fact_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    fact_grandkidU = factunit_shop(sun_text, _weight=20)
    fact_grandkidM = factunit_shop(mon_text, _weight=20)
    fact_grandkidT = factunit_shop(tue_text, _weight=20)
    fact_grandkidW = factunit_shop(wed_text, _weight=20)
    fact_grandkidR = factunit_shop(thu_text, _weight=30)
    fact_grandkidF = factunit_shop(fri_text, _weight=40)
    fact_grandkidA = factunit_shop(sat_text, _weight=50)

    sue_agenda.add_fact(fact_grandkidU, week_road)
    sue_agenda.add_fact(fact_grandkidM, week_road)
    sue_agenda.add_fact(fact_grandkidT, week_road)
    sue_agenda.add_fact(fact_grandkidW, week_road)
    sue_agenda.add_fact(fact_grandkidR, week_road)
    sue_agenda.add_fact(fact_grandkidF, week_road)
    sue_agenda.add_fact(fact_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    fact_kid_states = factunit_shop(states_text, _weight=30)
    sue_agenda.add_l1_fact(fact_kid_states)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    fact_grandkid_usa = factunit_shop(usa_text, _weight=50)
    fact_grandkid_france = factunit_shop(france_text, _weight=50)
    fact_grandkid_brazil = factunit_shop(brazil_text, _weight=50)
    sue_agenda.add_fact(fact_grandkid_france, states_road)
    sue_agenda.add_fact(fact_grandkid_brazil, states_road)
    sue_agenda.add_fact(fact_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    fact_grandgrandkid_usa_texas = factunit_shop(texas_text, _weight=50)
    fact_grandgrandkid_usa_oregon = factunit_shop(oregon_text, _weight=50)
    sue_agenda.add_fact(fact_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_fact(fact_grandgrandkid_usa_oregon, usa_road)
    return sue_agenda
