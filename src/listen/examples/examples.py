from src.agenda.oath import oathunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop


def get_agenda_with_4_levels() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    oath_kid_casa = oathunit_shop(casa, _weight=30, pledge=True)
    sue_agenda.add_l1_oath(oath_kid_casa)

    cat = "feed cat"
    oath_kid_feedcat = oathunit_shop(cat, _weight=30, pledge=True)
    sue_agenda.add_l1_oath(oath_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    oath_kid_weekdays = oathunit_shop(week_text, _weight=40)
    sue_agenda.add_l1_oath(oath_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    oath_grandkidU = oathunit_shop(sun_text, _weight=20)
    oath_grandkidM = oathunit_shop(mon_text, _weight=20)
    oath_grandkidT = oathunit_shop(tue_text, _weight=20)
    oath_grandkidW = oathunit_shop(wed_text, _weight=20)
    oath_grandkidR = oathunit_shop(thu_text, _weight=30)
    oath_grandkidF = oathunit_shop(fri_text, _weight=40)
    oath_grandkidA = oathunit_shop(sat_text, _weight=50)

    sue_agenda.add_oath(oath_grandkidU, week_road)
    sue_agenda.add_oath(oath_grandkidM, week_road)
    sue_agenda.add_oath(oath_grandkidT, week_road)
    sue_agenda.add_oath(oath_grandkidW, week_road)
    sue_agenda.add_oath(oath_grandkidR, week_road)
    sue_agenda.add_oath(oath_grandkidF, week_road)
    sue_agenda.add_oath(oath_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    oath_kid_states = oathunit_shop(states_text, _weight=30)
    sue_agenda.add_l1_oath(oath_kid_states)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    oath_grandkid_usa = oathunit_shop(usa_text, _weight=50)
    oath_grandkid_france = oathunit_shop(france_text, _weight=50)
    oath_grandkid_brazil = oathunit_shop(brazil_text, _weight=50)
    sue_agenda.add_oath(oath_grandkid_france, states_road)
    sue_agenda.add_oath(oath_grandkid_brazil, states_road)
    sue_agenda.add_oath(oath_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    oath_grandgrandkid_usa_texas = oathunit_shop(texas_text, _weight=50)
    oath_grandgrandkid_usa_oregon = oathunit_shop(oregon_text, _weight=50)
    sue_agenda.add_oath(oath_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_oath(oath_grandgrandkid_usa_oregon, usa_road)
    return sue_agenda
