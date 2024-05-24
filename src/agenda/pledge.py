from src._road.road import RoadUnit, get_terminus_node
from src.agenda.agenda import AgendaUnit, GroupID


def create_pledge(
    x_agenda: AgendaUnit, pledge_road: RoadUnit, x_suffgroup: GroupID = None
):
    if pledge_road is not None and get_terminus_node(pledge_road) != "":
        x_idea = x_agenda.get_idea_obj(pledge_road, if_missing_create=True)
        x_idea.pledge = True
        x_idea._assignedunit.set_suffgroup(x_suffgroup)

        if x_agenda.get_groupunit(x_suffgroup) is None:
            x_agenda.add_partyunit(x_suffgroup)
