from src._road.road import RoadUnit, get_terminus_node
from src.agenda.agenda import AgendaUnit, GroupID


def create_promise(
    x_agenda: AgendaUnit, promise_road: RoadUnit, x_suffgroup: GroupID = None
):
    x_terminus_node = get_terminus_node(promise_road)
    if x_terminus_node != "":
        x_idea = x_agenda.get_idea_obj(promise_road, if_missing_create=True)
        x_idea.promise = True
        x_idea._assignedunit.set_suffgroup(x_suffgroup)

        if x_agenda.get_groupunit(x_suffgroup) is None:
            x_agenda.add_partyunit(x_suffgroup)
