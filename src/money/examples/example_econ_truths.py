from src._instrument.file import delete_dir
from src._truth.truth import TruthUnit, truthunit_shop, ideaunit_shop, RealID
from src._truth.examples.example_truths import (
    get_truth_with7amCleanTableReason,
    get_truth_base_time_example,
    get_truth_x1_3levels_1reason_1facts,
)
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import temp_real_id, get_texas_userhub
from random import randrange


def get_1node_truth() -> TruthUnit:
    x_truth = truthunit_shop("A")
    x_truth.set_real_id(temp_real_id())
    x_truth.calc_truth_metrics()
    return x_truth


def get_Jnode2node_truth() -> TruthUnit:
    x_truth = truthunit_shop("J")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("A"))
    x_truth.calc_truth_metrics()
    return x_truth


def get_2node_truth(real_id: RealID = None) -> TruthUnit:
    if real_id is None:
        real_id = temp_real_id()
    a_text = "A"
    b_text = "B"
    x_truth = truthunit_shop(_owner_id=a_text)
    x_truth.set_real_id(real_id)
    idea_b = ideaunit_shop(b_text)
    x_truth.add_idea(idea_b, parent_road=temp_real_id())
    x_truth.calc_truth_metrics()
    return x_truth


def get_3node_truth() -> TruthUnit:
    a_text = "A"
    x_truth = truthunit_shop(a_text)
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("B"))
    x_truth.add_l1_idea(ideaunit_shop("C"))
    x_truth.calc_truth_metrics()
    return x_truth


def get_3node_D_E_F_truth() -> TruthUnit:
    d_text = "D"
    x_truth = truthunit_shop(d_text)
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("E"))
    x_truth.add_l1_idea(ideaunit_shop("F"))
    x_truth.calc_truth_metrics()
    return x_truth


def get_6node_truth() -> TruthUnit:
    x_truth = truthunit_shop("A")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("B"))
    x_truth.add_l1_idea(ideaunit_shop("C"))
    c_road = x_truth.make_l1_road("C")
    x_truth.add_idea(ideaunit_shop("D"), c_road)
    x_truth.add_idea(ideaunit_shop("E"), c_road)
    x_truth.add_idea(ideaunit_shop("F"), c_road)
    x_truth.calc_truth_metrics()
    return x_truth


def get_7nodeInsertH_truth() -> TruthUnit:
    x_truth = truthunit_shop("A")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("B"))
    x_truth.add_l1_idea(ideaunit_shop("C"))
    c_road = x_truth.make_l1_road("C")
    x_truth.add_idea(ideaunit_shop("H"), c_road)
    x_truth.add_idea(ideaunit_shop("D"), c_road)
    x_truth.add_idea(ideaunit_shop("E"), c_road)
    x_truth.add_idea(ideaunit_shop("F"), x_truth.make_road(c_road, "H"))
    x_truth.calc_truth_metrics()
    return x_truth


def get_5nodeHG_truth() -> TruthUnit:
    x_truth = truthunit_shop("A")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("B"))
    x_truth.add_l1_idea(ideaunit_shop("C"))
    c_road = x_truth.make_l1_road("C")
    x_truth.add_idea(ideaunit_shop("H"), c_road)
    x_truth.add_idea(ideaunit_shop("G"), c_road)
    x_truth.calc_truth_metrics()
    return x_truth


def get_7nodeJRoot_truth() -> TruthUnit:
    x_truth = truthunit_shop("J")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("A"))

    a_road = x_truth.make_l1_road("A")
    x_truth.add_idea(ideaunit_shop("B"), a_road)
    x_truth.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_truth.make_l1_road("C")
    x_truth.add_idea(ideaunit_shop("D"), c_road)
    x_truth.add_idea(ideaunit_shop("E"), c_road)
    x_truth.add_idea(ideaunit_shop("F"), c_road)
    x_truth.calc_truth_metrics()
    return x_truth


def get_7nodeJRootWithH_truth() -> TruthUnit:
    x_truth = truthunit_shop("J")
    x_truth.set_real_id(temp_real_id())
    x_truth.add_l1_idea(ideaunit_shop("A"))

    a_road = x_truth.make_l1_road("A")
    x_truth.add_idea(ideaunit_shop("B"), a_road)
    x_truth.add_idea(ideaunit_shop("C"), a_road)
    c_road = x_truth.make_l1_road("C")
    x_truth.add_idea(ideaunit_shop("E"), c_road)
    x_truth.add_idea(ideaunit_shop("F"), c_road)
    x_truth.add_idea(ideaunit_shop("H"), c_road)
    x_truth.calc_truth_metrics()
    return x_truth


def get_truth_2CleanNodesRandomWeights(_owner_id: str = None) -> TruthUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_truth = truthunit_shop(owner_id)
    casa_text = "casa"
    x_truth.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_truth.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    x_truth.add_idea(cookery_idea, parent_road=casa_road)
    x_truth.add_idea(bedroom_idea, parent_road=casa_road)
    x_truth.calc_truth_metrics()
    return x_truth


def get_truth_3CleanNodesRandomWeights(_owner_id: str = None) -> TruthUnit:
    owner_id = _owner_id if _owner_id != None else "ernie"
    x_truth = truthunit_shop(owner_id)
    casa_text = "casa"
    x_truth.add_l1_idea(ideaunit_shop(casa_text))
    casa_road = x_truth.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    nursery_text = "clean nursery"
    cookery_idea = ideaunit_shop(cookery_text, _weight=randrange(1, 50), pledge=True)
    bedroom_idea = ideaunit_shop(bedroom_text, _weight=randrange(1, 50), pledge=True)
    nursery_idea = ideaunit_shop(nursery_text, _weight=randrange(1, 50), pledge=True)
    x_truth.add_idea(cookery_idea, parent_road=casa_road)
    x_truth.add_idea(bedroom_idea, parent_road=casa_road)
    x_truth.add_idea(nursery_idea, parent_road=casa_road)
    x_truth.calc_truth_metrics()
    return x_truth


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
    x_money.userhub.save_job_truth(get_7nodeJRootWithH_truth())
    x_money.userhub.save_job_truth(get_truth_with7amCleanTableReason())
    x_money.userhub.save_job_truth(get_truth_base_time_example())
    x_money.userhub.save_job_truth(get_truth_x1_3levels_1reason_1facts())


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

    sal_truth = truthunit_shop(_owner_id=sal_text)
    sal_truth.add_otherunit(other_id=bob_text, credor_weight=2)
    sal_truth.add_otherunit(other_id=tom_text, credor_weight=7)
    sal_truth.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_truth(sal_truth)

    bob_truth = truthunit_shop(_owner_id=bob_text)
    bob_truth.add_otherunit(other_id=sal_text, credor_weight=3)
    bob_truth.add_otherunit(other_id=ava_text, credor_weight=1)
    x_money.userhub.save_job_truth(bob_truth)

    tom_truth = truthunit_shop(_owner_id=tom_text)
    tom_truth.add_otherunit(other_id=sal_text, credor_weight=2)
    x_money.userhub.save_job_truth(tom_truth)

    ava_truth = truthunit_shop(_owner_id=ava_text)
    ava_truth.add_otherunit(other_id=elu_text, credor_weight=2)
    x_money.userhub.save_job_truth(ava_truth)

    elu_truth = truthunit_shop(_owner_id=elu_text)
    elu_truth.add_otherunit(other_id=ava_text, credor_weight=19)
    elu_truth.add_otherunit(other_id=sal_text, credor_weight=1)
    x_money.userhub.save_job_truth(elu_truth)

    x_money.refresh_treasury_job_truths_data()
    x_money.set_cred_flow_for_truth(owner_id=sal_text, max_blocks_count=100)

    return x_money
