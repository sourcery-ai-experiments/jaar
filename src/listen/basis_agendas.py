from src._road.road import PersonID
from src.agenda.agenda import AgendaUnit, agendaunit_shop


def _is_empty_agenda(x_agenda: AgendaUnit) -> bool:
    empty_agenda = create_empty_agenda(x_agenda)
    return x_agenda.get_dict() == empty_agenda.get_dict()


def create_empty_agenda(
    ref_agenda: AgendaUnit, x_owner_id: PersonID = None
) -> AgendaUnit:
    if x_owner_id is None:
        x_owner_id = ref_agenda._owner_id
    x_road_delimiter = ref_agenda._road_delimiter
    x_planck = ref_agenda._planck
    x_penny = ref_agenda._penny
    return agendaunit_shop(
        x_owner_id, ref_agenda._real_id, x_road_delimiter, x_planck, x_penny
    )


def create_listen_basis(x_role: AgendaUnit) -> AgendaUnit:
    x_listen = create_empty_agenda(x_role, x_owner_id=x_role._owner_id)
    x_listen._partys = x_role._partys
    x_listen._ideas = x_role._ideas
    x_listen.set_monetary_desc(x_role._monetary_desc)
    x_listen.set_max_tree_traverse(x_role._max_tree_traverse)
    if x_role._party_credor_pool != None:
        x_listen.set_party_credor_pool(x_role._party_credor_pool)
    if x_role._party_debtor_pool != None:
        x_listen.set_party_debtor_pool(x_role._party_debtor_pool)
    for x_partyunit in x_listen._partys.values():
        x_partyunit.reset_listen_calculated_attrs()
    return x_listen


def get_default_work_agenda(duty: AgendaUnit) -> AgendaUnit:
    default_work_agenda = create_listen_basis(duty)
    default_work_agenda._last_atom_id = duty._last_atom_id
    default_work_agenda._party_credor_pool = None
    default_work_agenda._party_debtor_pool = None
    return default_work_agenda
