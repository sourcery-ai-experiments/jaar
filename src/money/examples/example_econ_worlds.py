from src._instrument.file import delete_dir
from src._world.world import WorldUnit, worldunit_shop, ideaunit_shop, RealID
from src._world.examples.example_worlds import (
    get_world_with7amCleanTableReason,
    get_world_base_time_example,
    get_world_x1_3levels_1reason_1facts,
)
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import temp_real_id, get_texas_userhub
from random import randrange


def get_1node_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.calc_world_metrics()
    return x_world


def get_Jnode2node_world() -> WorldUnit:
    x_world = worldunit_shop("J")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("A"))
    x_world.calc_world_metrics()
    return x_world


def get_2node_world(real_id: RealID = None) -> WorldUnit:
    if real_id is None:
        real_id = temp_real_id()
    a_text = "A"
    b_text = "B"
    x_world = worldunit_shop(_owner_id=a_text)
    x_world.set_real_id(real_id)
    idea_b = ideaunit_shop(b_text)
    x_world.add_idea(idea_b, parent_road=temp_real_id())
    x_world.calc_world_metrics()
    return x_world


def get_3node_world() -> WorldUnit:
    a_text = "A"
    x_world = worldunit_shop(a_text)
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    x_world.calc_world_metrics()
    return x_world


def get_3node_D_E_F_world() -> WorldUnit:
    d_text = "D"
    x_world = worldunit_shop(d_text)
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("E"))
    x_world.add_l1_idea(ideaunit_shop("F"))
    x_world.calc_world_metrics()
    return x_world


def get_6node_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), c_road)
    x_world.calc_world_metrics()
    return x_world


def get_7nodeInsertH_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("H"), c_road)
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), x_world.make_road(c_road, "H"))
    x_world.calc_world_metrics()
    return x_world


def get_5nodeHG_world() -> WorldUnit:
    x_world = worldunit_shop("A")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("B"))
    x_world.add_l1_idea(ideaunit_shop("C"))
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("H"), c_road)
    x_world.add_idea(ideaunit_shop("G"), c_road)
    x_world.calc_world_metrics()
    return x_world


def get_7nodeJRoot_world() -> WorldUnit:
    x_world = worldunit_shop("J")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("A"))

    a_road = x_world.make_l1_road("A")
    x_world.add_idea(ideaunit_shop("B"), a_road)
    x_world.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("D"), c_road)
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), c_road)
    x_world.calc_world_metrics()
    return x_world


def get_7nodeJRootWithH_world() -> WorldUnit:
    x_world = worldunit_shop("J")
    x_world.set_real_id(temp_real_id())
    x_world.add_l1_idea(ideaunit_shop("A"))

    a_road = x_world.make_l1_road("A")
    x_world.add_idea(ideaunit_shop("B"), a_road)
    x_world.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_world.make_l1_road("C")
    x_world.add_idea(ideaunit_shop("E"), c_road)
    x_world.add_idea(ideaunit_shop("F"), c_road)
    x_world.add_idea(ideaunit_shop("H"), c_road)
    x_world.calc_world_metrics()
    return x_world


def get_world_2CleanNodesRandomWeights(_owner_id: str = None) -> WorldUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_world = worldunit_shop(owner_id)
    casa_text = "casa"
    x_world.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_world.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    x_world.add_idea(cookery_idea, parent_road=casa_road)
    x_world.add_idea(bedroom_idea, parent_road=casa_road)
    x_world.calc_world_metrics()
    return x_world


def get_world_3CleanNodesRandomWeights(_owner_id: str = None) -> WorldUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_world = worldunit_shop(owner_id)
    casa_text = "casa"
    x_world.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_world.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    nursery_text = "clean nursery"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    nursery_idea = ideaunit_shop(nursery_text, _weight=randrange(1, 50), pledge=True)
    x_world.add_idea(cookery_idea, parent_road=casa_road)
    x_world.add_idea(bedroom_idea, parent_road=casa_road)
    x_world.add_idea(nursery_idea, parent_road=casa_road)
    x_world.calc_world_metrics()
    return x_world


def setup_test_example_environment():
    # _delete_and_set_ex3()
    _delete_and_set_ex4()
    # _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex4():
    ex4_id = "ex4"
    ex4_userhub = get_texas_userhub()
    ex4_userhub.real_id = ex4_id
    x_money = moneyunit_shop(ex4_userhub)
    delete_dir(x_money.userhub.econ_dir())
    x_money.create_treasury_db(in_memory=True)
    x_money.userhub.save_job_world(get_7nodeJRootWithH_world())
    x_money.userhub.save_job_world(get_world_with7amCleanTableReason())
    x_money.userhub.save_job_world(get_world_base_time_example())
    x_money.userhub.save_job_world(get_world_x1_3levels_1reason_1facts())


def _delete_and_set_ex6(ex6_id: str = None):
    if ex6_id is None:
        ex6_id = "ex6"
    ex6_userhub = get_texas_userhub()
    ex6_userhub.real_id = ex6_id
    x_money = moneyunit_shop(ex6_userhub)
    delete_dir(x_money.userhub.econ_dir())
    x_money.create_treasury_db(in_memory=False)

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_world = worldunit_shop(_owner_id=sal_text)
    sal_world.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_world.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(sal_world)

    bob_world = worldunit_shop(_owner_id=bob_text)
    bob_world.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_world.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_world(bob_world)

    tom_world = worldunit_shop(_owner_id=tom_text)
    tom_world.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_world(tom_world)

    ava_world = worldunit_shop(_owner_id=ava_text)
    ava_world.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_world(ava_world)

    elu_world = worldunit_shop(_owner_id=elu_text)
    elu_world.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_world.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_world(elu_world)

    x_money.refresh_treasury_job_worlds_data()
    x_money.set_cred_flow_for_world(owner_id=sal_text, max_blocks_count=100)

    return x_money
