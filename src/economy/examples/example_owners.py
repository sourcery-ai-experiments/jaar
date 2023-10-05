from src.contract.contract import ContractUnit, IdeaKid, assigned_unit_shop
from src.economy.owner import ownerunit_shop, OwnerUnit
from src.economy.examples.owner_env_kit import get_temp_economy_title

from random import randrange


def get_1node_contract() -> ContractUnit:
    a_text = "A"
    contract_x = ContractUnit(_owner=a_text)
    contract_x.set_economy_title(get_temp_economy_title())
    contract_x.set_contract_metrics()
    return contract_x


def get_Jnode2node_contract() -> ContractUnit:
    owner_text = "J"
    contract_x = ContractUnit(_owner=owner_text)
    contract_x.set_economy_title(get_temp_economy_title())
    a_text = "A"
    idea_a = IdeaKid(_label=a_text)
    contract_x.add_idea(idea_kid=idea_a, walk=get_temp_economy_title())
    contract_x.set_contract_metrics()
    return contract_x


def get_2node_contract() -> ContractUnit:
    owner_text = "A"
    b_text = "B"
    contract_x = ContractUnit(_owner=owner_text)
    contract_x.set_economy_title(get_temp_economy_title())
    idea_b = IdeaKid(_label=b_text)
    contract_x.add_idea(idea_kid=idea_b, walk=get_temp_economy_title())
    contract_x.set_contract_metrics()
    return contract_x


def get_3node_contract() -> ContractUnit:
    a_text = "A"
    a_road = a_text
    contract_x = ContractUnit(_owner=a_text)
    contract_x.set_economy_title(get_temp_economy_title())
    b_text = "B"
    idea_b = IdeaKid(_label=b_text)
    c_text = "C"
    idea_c = IdeaKid(_label=c_text)
    contract_x.add_idea(idea_kid=idea_b, walk=a_road)
    contract_x.add_idea(idea_kid=idea_c, walk=a_road)
    contract_x.set_contract_metrics()
    return contract_x


def get_3node_D_E_F_contract() -> ContractUnit:
    d_text = "D"
    d_road = d_text
    contract_x = ContractUnit(_owner=d_text)
    contract_x.set_economy_title(get_temp_economy_title())
    b_text = "E"
    idea_b = IdeaKid(_label=b_text)
    c_text = "F"
    idea_c = IdeaKid(_label=c_text)
    contract_x.add_idea(idea_kid=idea_b, walk=d_road)
    contract_x.add_idea(idea_kid=idea_c, walk=d_road)
    contract_x.set_contract_metrics()
    return contract_x


def get_6node_contract() -> ContractUnit:
    contract_x = ContractUnit(_owner="A")
    contract_x.set_economy_title(get_temp_economy_title())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    contract_x.add_idea(idea_kid=idea_b, walk="A")
    contract_x.add_idea(idea_kid=idea_c, walk="A")
    contract_x.add_idea(idea_kid=idea_d, walk="A,C")
    contract_x.add_idea(idea_kid=idea_e, walk="A,C")
    contract_x.add_idea(idea_kid=idea_f, walk="A,C")
    contract_x.set_contract_metrics()
    return contract_x


def get_7nodeInsertH_contract() -> ContractUnit:
    contract_x = ContractUnit(_owner="A")
    contract_x.set_economy_title(get_temp_economy_title())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    contract_x.add_idea(idea_kid=idea_b, walk="A")
    contract_x.add_idea(idea_kid=idea_c, walk="A")
    contract_x.add_idea(idea_kid=idea_e, walk="A,C")
    contract_x.add_idea(idea_kid=idea_f, walk="A,C")
    contract_x.add_idea(idea_kid=idea_h, walk="A,C")
    contract_x.add_idea(idea_kid=idea_d, walk="A,C,H")
    contract_x.set_contract_metrics()
    return contract_x


def get_5nodeHG_contract() -> ContractUnit:
    contract_x = ContractUnit(_owner="A")
    contract_x.set_economy_title(get_temp_economy_title())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_g = IdeaKid(_label="G")
    contract_x.add_idea(idea_kid=idea_b, walk="A")
    contract_x.add_idea(idea_kid=idea_c, walk="A")
    contract_x.add_idea(idea_kid=idea_h, walk="A,C")
    contract_x.add_idea(idea_kid=idea_g, walk="A,C")
    contract_x.set_contract_metrics()
    return contract_x


def get_7nodeJRoot_contract() -> ContractUnit:
    contract_x = ContractUnit(_owner="J")
    contract_x.set_economy_title(get_temp_economy_title())
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    contract_x.add_idea(idea_kid=idea_a, walk="J")
    contract_x.add_idea(idea_kid=idea_b, walk="J,A")
    contract_x.add_idea(idea_kid=idea_c, walk="J,A")
    contract_x.add_idea(idea_kid=idea_d, walk="J,A,C")
    contract_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    contract_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    contract_x.set_contract_metrics()
    return contract_x


def get_7nodeJRootWithH_contract() -> ContractUnit:
    contract_x = ContractUnit(_owner="J")
    contract_x.set_economy_title(get_temp_economy_title())
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    idea_h = IdeaKid(_label="H")
    contract_x.add_idea(idea_kid=idea_a, walk="J")
    contract_x.add_idea(idea_kid=idea_b, walk="J,A")
    contract_x.add_idea(idea_kid=idea_c, walk="J,A")
    contract_x.add_idea(idea_kid=idea_e, walk="J,A,C")
    contract_x.add_idea(idea_kid=idea_f, walk="J,A,C")
    contract_x.add_idea(idea_kid=idea_h, walk="J,A,C")
    contract_x.set_contract_metrics()
    return contract_x


def get_owner_2contract(env_dir, economy_title) -> OwnerUnit:
    yao_text = "Xio"
    yao_owner = ownerunit_shop(yao_text, env_dir, economy_title)
    yao_owner.set_depot_contract(get_1node_contract(), depotlink_type="blind_trust")
    yao_owner.set_depot_contract(
        get_Jnode2node_contract(), depotlink_type="blind_trust"
    )
    return yao_owner


def get_contract_2CleanNodesRandomWeights(_owner: str = None) -> ContractUnit:
    owner_text = _owner if _owner != None else "ernie"
    contract_x = ContractUnit(_owner=owner_text)
    casa_text = "casa"
    contract_x.add_idea(idea_kid=IdeaKid(_label=casa_text), walk="")
    casa_road = f"{contract_x._economy_title},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    contract_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    contract_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    contract_x.set_contract_metrics()
    return contract_x


def get_contract_3CleanNodesRandomWeights(_owner: str = None) -> ContractUnit:
    owner_text = _owner if _owner != None else "ernie"
    contract_x = ContractUnit(_owner=owner_text)
    casa_text = "casa"
    contract_x.add_idea(idea_kid=IdeaKid(_label=casa_text), walk="")
    casa_road = f"{contract_x._economy_title},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = IdeaKid(_label=hallway_text, _weight=randrange(1, 50), promise=True)
    contract_x.add_idea(idea_kid=cookery_idea, walk=casa_road)
    contract_x.add_idea(idea_kid=bedroom_idea, walk=casa_road)
    contract_x.add_idea(idea_kid=hallway_idea, walk=casa_road)
    contract_x.set_contract_metrics()
    return contract_x


def get_contract_assignment_laundry_example1() -> ContractUnit:
    america_text = "America"
    america_cx = ContractUnit(_owner=america_text)
    joachim_text = "Joachim"
    america_cx.add_partyunit(america_text)
    america_cx.add_partyunit(joachim_text)

    root_road = america_cx._economy_title
    casa_text = "casa"
    casa_road = f"{root_road},{casa_text}"
    america_cx.add_idea(IdeaKid(_label=casa_text), walk=root_road)

    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    america_cx.add_idea(IdeaKid(_label=basket_text), walk=casa_road)

    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    america_cx.add_idea(IdeaKid(_label=b_full_text), walk=basket_road)

    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    america_cx.add_idea(IdeaKid(_label=b_smel_text), walk=basket_road)

    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    america_cx.add_idea(IdeaKid(_label=b_bare_text), walk=basket_road)

    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    america_cx.add_idea(IdeaKid(_label=b_fine_text), walk=basket_road)

    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    america_cx.add_idea(IdeaKid(_label=b_half_text), walk=basket_road)

    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    america_cx.add_idea(IdeaKid(_label=laundry_task_text, promise=True), walk=casa_road)

    # make laundry requirement
    basket_idea = america_cx.get_idea_kid(road=basket_road)
    america_cx.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_full_road
    )
    # make laundry requirement
    america_cx.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_smel_road
    )
    # assign Joachim to task
    joachim_assignunit = assigned_unit_shop()
    joachim_assignunit.set_suffgroup(joachim_text)
    america_cx.edit_idea_attr(road=laundry_task_road, assignedunit=joachim_assignunit)
    america_cx.set_acptfact(base=basket_road, pick=b_full_road)

    return america_cx
