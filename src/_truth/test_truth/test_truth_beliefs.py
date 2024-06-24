from src._road.road import get_default_real_id_roadnode
from src._truth.belief import (
    BeliefID,
    balancelink_shop,
    beliefunit_shop,
    get_others_relevant_beliefs,
    get_other_relevant_beliefs,
)
from src._truth.other import OtherID, otherunit_shop, otherlink_shop
from src._truth.idea import ideaunit_shop
from src._truth.truth import truthunit_shop
from src._truth.examples.example_truths import truth_v001 as examples_truth_v001
from pytest import raises as pytest_raises


def test_TruthUnit_beliefs_get_beliefunit_ReturnsCorrectObj():
    # GIVEN
    x_truth = truthunit_shop()
    swim_text = ",swimmers"
    # x_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))
    swim_beliefs = {swim_text: beliefunit_shop(belief_id=swim_text)}
    x_truth._beliefs = swim_beliefs

    # WHEN
    swim_beliefunit = x_truth.get_beliefunit(swim_text)

    # THEN
    assert swim_beliefunit == beliefunit_shop(belief_id=swim_text)


def test_TruthUnit_beliefs_set_beliefunit_CorrectlySetAttr():
    # GIVEN
    swim_text = ",swimmers"
    x_truth = truthunit_shop()

    # WHEN
    x_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))

    # THEN
    assert len(x_truth._beliefs) == 1
    swim_beliefs = {swim_text: beliefunit_shop(belief_id=swim_text)}
    assert len(x_truth._beliefs) == len(swim_beliefs)
    assert x_truth.get_beliefunit(swim_text) != None
    swim_beliefunit = x_truth.get_beliefunit(swim_text)
    assert swim_beliefunit._others == swim_beliefs.get(swim_text)._others
    assert x_truth.get_beliefunit(swim_text) == swim_beliefs.get(swim_text)
    assert x_truth._beliefs == swim_beliefs


def test_TruthUnit_beliefs_set_beliefunit_CorrectlyReplacesBelief():
    # GIVEN
    swim_text = ",swimmers"
    x_truth = truthunit_shop()
    swim1_belief = beliefunit_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_otherlink(otherlink_shop(bob_text))
    x_truth.set_beliefunit(swim1_belief)
    assert len(x_truth.get_beliefunit(swim_text)._others) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefunit_shop(swim_text)
    swim2_belief.set_otherlink(otherlink_shop(bob_text))
    swim2_belief.set_otherlink(otherlink_shop(yao_text))
    x_truth.set_beliefunit(swim2_belief, replace=False)

    # THEN
    assert len(x_truth.get_beliefunit(swim_text)._others) == 1

    # WHEN / THEN
    x_truth.set_beliefunit(swim2_belief, replace=True)
    assert len(x_truth.get_beliefunit(swim_text)._others) == 2


# def test_TruthUnit_beliefs_set_beliefunit_RaisesErrorWhen_other_mirrorSubmitted():
#     # GIVEN
#     yao_truth = truthunit_shop("Yao")
#     bob_text = "Bob"
#     yao_truth.set_otherunit(otherunit_shop(bob_text))
#     bob_beliefunit = yao_truth.get_beliefunit(bob_text)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         yao_truth.set_beliefunit(bob_beliefunit)
#     assert (
#         str(excinfo.value)
#         == f"TruthUnit.set_beliefunit('{bob_text}') fails because belief is _other_mirror."
#     )


def test_TruthUnit_beliefs_set_beliefunit_CorrectlySets_otherlinks():
    # GIVEN
    swim_text = ",swimmers"
    x_truth = truthunit_shop()
    swim1_belief = beliefunit_shop(swim_text)
    bob_text = "Bob"
    swim1_belief.set_otherlink(otherlink_shop(bob_text))
    x_truth.set_beliefunit(swim1_belief)
    assert len(x_truth.get_beliefunit(swim_text)._others) == 1

    # WHEN
    yao_text = "Yao"
    swim2_belief = beliefunit_shop(swim_text)
    swim2_belief.set_otherlink(otherlink_shop(bob_text))
    swim2_belief.set_otherlink(otherlink_shop(yao_text))
    x_truth.set_beliefunit(swim2_belief, add_otherlinks=True)

    # THEN
    assert len(x_truth.get_beliefunit(swim_text)._others) == 2


def test_TruthUnit_beliefs_del_beliefunit_casasCorrectly():
    # GIVEN
    x_truth = truthunit_shop()
    swim_text = "swimmers"
    swim_belief = beliefunit_shop(belief_id=BeliefID(swim_text))
    x_truth.set_beliefunit(y_beliefunit=swim_belief)
    assert x_truth.get_beliefunit(swim_text) != None

    # WHEN
    x_truth.del_beliefunit(belief_id=swim_text)
    assert x_truth.get_beliefunit(swim_text) is None
    assert x_truth._beliefs == {}


def test_examples_truth_v001_HasBeliefs():
    # GIVEN / WHEN
    x_truth = examples_truth_v001()

    # THEN
    assert x_truth._beliefs != None
    assert len(x_truth._beliefs) == 34
    everyone_others_len = None
    everyone_belief = x_truth.get_beliefunit(",Everyone")
    everyone_others_len = len(everyone_belief._others)
    assert everyone_others_len == 22

    # WHEN
    x_truth.calc_truth_metrics()
    idea_dict = x_truth._idea_dict

    # THEN
    print(f"{len(idea_dict)=}")
    db_idea = idea_dict.get(x_truth.make_l1_road("D&B"))
    print(f"{db_idea._label=} {db_idea._balancelinks=}")
    assert len(db_idea._balancelinks) == 3
    # for idea_key in idea_dict:
    #     print(f"{idea_key=}")
    #     if idea._label == "D&B":
    #         print(f"{idea._label=} {idea._balancelinks=}")
    #         db_balancelink_len = len(idea._balancelinks)
    # assert db_balancelink_len == 3


def test_TruthUnit_set_balancelink_correctly_sets_balancelinks():
    # GIVEN
    sue_text = "Sue"
    sue_truth = truthunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))

    assert len(sue_truth._others) == 3
    assert len(sue_truth._beliefs) == 3
    swim_text = "swim"
    sue_truth.add_l1_idea(ideaunit_shop(swim_text))
    balancelink_rico = balancelink_shop(belief_id=BeliefID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(belief_id=BeliefID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(belief_id=BeliefID(patr_text), credor_weight=10)
    swim_road = sue_truth.make_l1_road(swim_text)
    sue_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    sue_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    sue_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    street_text = "streets"
    sue_truth.add_idea(ideaunit_shop(street_text), parent_road=swim_road)
    assert sue_truth._idearoot._balancelinks in (None, {})
    assert len(sue_truth._idearoot._kids[swim_text]._balancelinks) == 3

    # WHEN
    idea_dict = sue_truth.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=} {get_default_real_id_roadnode()=}")
    root_idea = idea_dict.get(get_default_real_id_roadnode())
    swim_idea = idea_dict.get(swim_road)
    street_idea = idea_dict.get(sue_truth.make_road(swim_road, street_text))

    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3
    assert street_idea._balancelinks in (None, {})
    assert len(street_idea._balanceheirs) == 3

    print(f"{len(idea_dict)}")
    print(f"{swim_idea._balancelinks}")
    print(f"{swim_idea._balanceheirs}")
    print(f"{swim_idea._balanceheirs}")
    assert len(sue_truth._idearoot._kids["swim"]._balanceheirs) == 3


def test_TruthUnit_set_balancelink_correctly_deletes_balancelinks():
    # GIVEN
    prom_text = "prom"
    x_truth = truthunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))

    swim_text = "swim"
    swim_road = x_truth.make_road(prom_text, swim_text)

    x_truth.add_l1_idea(ideaunit_shop(swim_text))
    balancelink_rico = balancelink_shop(belief_id=BeliefID(rico_text), credor_weight=10)
    balancelink_carm = balancelink_shop(belief_id=BeliefID(carm_text), credor_weight=10)
    balancelink_patr = balancelink_shop(belief_id=BeliefID(patr_text), credor_weight=10)

    swim_idea = x_truth.get_idea_obj(swim_road)
    x_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_rico)
    x_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_carm)
    x_truth.edit_idea_attr(road=swim_road, balancelink=balancelink_patr)

    assert len(swim_idea._balancelinks) == 3
    assert len(swim_idea._balanceheirs) == 3

    # print(f"{len(idea_list)}")
    # print(f"{idea_list[0]._balancelinks}")
    # print(f"{idea_list[0]._balanceheirs}")
    # print(f"{idea_list[1]._balanceheirs}")
    assert len(x_truth._idearoot._kids[swim_text]._balancelinks) == 3
    assert len(x_truth._idearoot._kids[swim_text]._balanceheirs) == 3

    # WHEN
    x_truth.edit_idea_attr(road=swim_road, balancelink_del=rico_text)

    # THEN
    swim_idea = x_truth.get_idea_obj(swim_road)
    print(f"{swim_idea._label=}")
    print(f"{swim_idea._balancelinks=}")
    print(f"{swim_idea._balanceheirs=}")

    assert len(x_truth._idearoot._kids[swim_text]._balancelinks) == 2
    assert len(x_truth._idearoot._kids[swim_text]._balanceheirs) == 2


def test_TruthUnit_set_balancelink_CorrectlyCalculatesInheritedBalanceLinkTruthImportance():
    # GIVEN
    sue_text = "Sue"
    sue_truth = truthunit_shop(sue_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    sue_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))
    blink_rico = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    blink_carm = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    blink_patr = balancelink_shop(belief_id=patr_text, credor_weight=10)
    sue_truth._idearoot.set_balancelink(balancelink=blink_rico)
    sue_truth._idearoot.set_balancelink(balancelink=blink_carm)
    sue_truth._idearoot.set_balancelink(balancelink=blink_patr)
    assert len(sue_truth._idearoot._balancelinks) == 3

    # WHEN
    idea_dict = sue_truth.get_idea_dict()

    # THEN
    print(f"{idea_dict.keys()=}")
    idea_prom = idea_dict.get(get_default_real_id_roadnode())
    assert len(idea_prom._balanceheirs) == 3

    bheir_rico = idea_prom._balanceheirs.get(rico_text)
    bheir_carm = idea_prom._balanceheirs.get(carm_text)
    bheir_patr = idea_prom._balanceheirs.get(patr_text)
    assert bheir_rico._truth_cred == 0.5
    assert bheir_rico._truth_debt == 0.75
    assert bheir_carm._truth_cred == 0.25
    assert bheir_carm._truth_debt == 0.125
    assert bheir_patr._truth_cred == 0.25
    assert bheir_patr._truth_debt == 0.125
    assert bheir_rico._truth_cred + bheir_carm._truth_cred + bheir_patr._truth_cred == 1
    assert bheir_rico._truth_debt + bheir_carm._truth_debt + bheir_patr._truth_debt == 1

    # truth_cred_sum = 0
    # truth_debt_sum = 0
    # for belief in x_truth._idearoot._balanceheirs.values():
    #     print(f"{belief=}")
    #     assert belief._truth_cred != None
    #     assert belief._truth_cred in [0.25, 0.5]
    #     assert belief._truth_debt != None
    #     assert belief._truth_debt in [0.75, 0.125]
    #     truth_cred_sum += belief._truth_cred
    #     truth_debt_sum += belief._truth_debt

    # assert truth_cred_sum == 1
    # assert truth_debt_sum == 1


def test_TruthUnit_get_idea_list_CorrectlyCalculates1LevelTruthBeliefTruthImportance():
    # GIVEN
    prom_text = "prom"
    x_truth = truthunit_shop(prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    sele_text = "selena"
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))
    blink_rico = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    blink_carm = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    blink_patr = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_truth._idearoot.set_balancelink(balancelink=blink_rico)
    x_truth._idearoot.set_balancelink(balancelink=blink_carm)
    x_truth._idearoot.set_balancelink(balancelink=blink_patr)

    assert len(x_truth._beliefs) == 3

    # WHEN
    x_truth.calc_truth_metrics()

    # THEN
    belief_rico = x_truth.get_beliefunit(rico_text)
    belief_carm = x_truth.get_beliefunit(carm_text)
    belief_patr = x_truth.get_beliefunit(patr_text)
    assert belief_rico._truth_cred == 0.5
    assert belief_rico._truth_debt == 0.75
    assert belief_carm._truth_cred == 0.25
    assert belief_carm._truth_debt == 0.125
    assert belief_patr._truth_cred == 0.25
    assert belief_patr._truth_debt == 0.125
    assert (
        belief_rico._truth_cred + belief_carm._truth_cred + belief_patr._truth_cred == 1
    )
    assert (
        belief_rico._truth_debt + belief_carm._truth_debt + belief_patr._truth_debt == 1
    )

    # WHEN
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(sele_text)))
    bl_sele = balancelink_shop(belief_id=sele_text, credor_weight=37)
    x_truth._idearoot.set_balancelink(balancelink=bl_sele)
    assert len(x_truth._beliefs) == 4
    x_truth.calc_truth_metrics()

    # THEN
    belief_sele = x_truth.get_beliefunit(sele_text)
    assert belief_rico._truth_cred != 0.5
    assert belief_rico._truth_debt != 0.75
    assert belief_carm._truth_cred != 0.25
    assert belief_carm._truth_debt != 0.125
    assert belief_patr._truth_cred != 0.25
    assert belief_patr._truth_debt != 0.125
    assert belief_sele._truth_cred != None
    assert belief_sele._truth_debt != None
    assert (
        belief_rico._truth_cred
        + belief_carm._truth_cred
        + belief_patr._truth_cred
        + belief_sele._truth_cred
        == 1
    )
    assert (
        belief_rico._truth_debt
        + belief_carm._truth_debt
        + belief_patr._truth_debt
        + belief_sele._truth_debt
        == 1
    )


def test_TruthUnit_get_idea_list_CorrectlyCalculates3levelTruthBeliefTruthImportance():
    # GIVEN
    prom_text = "prom"
    x_truth = truthunit_shop(prom_text)
    swim_text = "swim"
    x_truth.add_l1_idea(ideaunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))
    rico_balancelink = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)
    assert len(x_truth._beliefs) == 3

    # WHEN
    x_truth.calc_truth_metrics()

    # THEN
    belief_rico = x_truth.get_beliefunit(rico_text)
    belief_carm = x_truth.get_beliefunit(carm_text)
    belief_patr = x_truth.get_beliefunit(patr_text)
    assert belief_rico._truth_cred == 0.5
    assert belief_rico._truth_debt == 0.75
    assert belief_carm._truth_cred == 0.25
    assert belief_carm._truth_debt == 0.125
    assert belief_patr._truth_cred == 0.25
    assert belief_patr._truth_debt == 0.125
    assert (
        belief_rico._truth_cred + belief_carm._truth_cred + belief_patr._truth_cred == 1
    )
    assert (
        belief_rico._truth_debt + belief_carm._truth_debt + belief_patr._truth_debt == 1
    )


def test_TruthUnit_get_idea_list_CorrectlyCalculatesBeliefTruthImportanceLWwithBeliefEmptyAncestors():
    # GIVEN
    prom_text = "prom"
    x_truth = truthunit_shop(prom_text)
    swim_text = "swim"
    x_truth.add_l1_idea(ideaunit_shop(swim_text))

    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(rico_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(carm_text)))
    x_truth.set_otherunit(otherunit=otherunit_shop(other_id=OtherID(patr_text)))
    rico_balancelink = balancelink_shop(
        belief_id=rico_text, credor_weight=20, debtor_weight=6
    )
    carm_balancelink = balancelink_shop(
        belief_id=carm_text, credor_weight=10, debtor_weight=1
    )
    parm_balancelink = balancelink_shop(belief_id=patr_text, credor_weight=10)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=rico_balancelink)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=carm_balancelink)
    x_truth._idearoot._kids[swim_text].set_balancelink(balancelink=parm_balancelink)

    # no balancelinks attached to this one
    x_truth.add_l1_idea(ideaunit_shop("hunt", _weight=3))

    # WHEN
    x_truth.calc_truth_metrics()

    # THEN

    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._balancelinks[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._balancelinks[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._balancelinks[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"
    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._kids["hunt"]._balanceheirs[rico_text]
    assert str(excinfo.value) == f"'{rico_text}'"
    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._kids["hunt"]._balanceheirs[carm_text]
    assert str(excinfo.value) == f"'{carm_text}'"
    with pytest_raises(Exception) as excinfo:
        x_truth._idearoot._kids["hunt"]._balanceheirs[patr_text]
    assert str(excinfo.value) == f"'{patr_text}'"

    # THEN
    belief_rico = x_truth.get_beliefunit(rico_text)
    belief_carm = x_truth.get_beliefunit(carm_text)
    belief_patr = x_truth.get_beliefunit(patr_text)
    assert belief_rico._truth_cred == 0.125
    assert belief_rico._truth_debt == 0.1875
    assert belief_carm._truth_cred == 0.0625
    assert belief_carm._truth_debt == 0.03125
    assert belief_patr._truth_cred == 0.0625
    assert belief_patr._truth_debt == 0.03125
    assert (
        belief_rico._truth_cred + belief_carm._truth_cred + belief_patr._truth_cred
        == 0.25
    )
    assert (
        belief_rico._truth_debt + belief_carm._truth_debt + belief_patr._truth_debt
        == 0.25
    )


def test_TruthUnit_edit_beliefunit_belief_id_CorrectlyCreatesNewPersonID():
    # GIVEN
    truth = truthunit_shop("prom")
    rico_text = "rico"
    truth.add_otherunit(other_id=rico_text)
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_otherlink(otherlink=otherlink_shop(other_id=rico_text))
    truth.set_beliefunit(swim_belief)
    assert len(truth._others) == 1
    assert len(truth._beliefs) == 2
    assert truth.get_beliefunit(swim_text) != None
    assert truth.get_beliefunit(swim_text)._other_mirror is False
    assert len(truth.get_beliefunit(swim_text)._others) == 1

    # WHEN
    jog_text = ",jog"
    truth.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=False
    )

    # THEN
    assert truth.get_beliefunit(jog_text) != None
    assert truth.get_beliefunit(swim_text) is None
    assert len(truth._others) == 1
    assert len(truth._beliefs) == 2
    assert truth.get_beliefunit(jog_text)._other_mirror is False
    assert len(truth.get_beliefunit(jog_text)._others) == 1


def test_TruthUnit_edit_Beliefunit_belief_id_raiseErrorNewPersonIDPreviouslyExists():
    # GIVEN
    truth = truthunit_shop("prom")
    rico_text = "rico"
    truth.add_otherunit(other_id=rico_text)
    swim_text = ",swimmers"
    truth.set_beliefunit(beliefunit_shop(belief_id=swim_text))
    jog_text = ",jog"
    truth.set_beliefunit(beliefunit_shop(belief_id=jog_text))

    # WHEN
    with pytest_raises(Exception) as excinfo:
        truth.edit_beliefunit_belief_id(
            old_belief_id=swim_text,
            new_belief_id=jog_text,
            allow_belief_overwite=False,
        )
    assert (
        str(excinfo.value)
        == f"Belief '{swim_text}' modify to '{jog_text}' failed since '{jog_text}' exists."
    )


def test_TruthUnit_edit_beliefunit_belief_id_CorrectlyMeldPersonIDs():
    # GIVEN
    truth = truthunit_shop("prom")
    rico_text = "rico"
    truth.add_otherunit(other_id=rico_text)
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    swim_belief.set_otherlink(
        otherlink=otherlink_shop(other_id=rico_text, credor_weight=5, debtor_weight=3)
    )
    truth.set_beliefunit(swim_belief)
    jog_text = ",jog"
    jog_belief = beliefunit_shop(belief_id=jog_text)
    jog_belief.set_otherlink(
        otherlink=otherlink_shop(other_id=rico_text, credor_weight=7, debtor_weight=10)
    )
    truth.set_beliefunit(jog_belief)
    print(f"{truth.get_beliefunit(jog_text)._others.get(rico_text)=}")
    assert truth.get_beliefunit(jog_text) != None

    # WHEN
    truth.edit_beliefunit_belief_id(
        old_belief_id=swim_text,
        new_belief_id=jog_text,
        allow_belief_overwite=True,
    )

    # THEN
    assert truth.get_beliefunit(jog_text) != None
    assert truth.get_beliefunit(swim_text) is None
    assert len(truth._others) == 1
    assert len(truth._beliefs) == 2
    assert truth.get_beliefunit(jog_text)._other_mirror is False
    assert len(truth.get_beliefunit(jog_text)._others) == 1
    assert truth.get_beliefunit(jog_text)._others.get(rico_text).credor_weight == 12
    assert truth.get_beliefunit(jog_text)._others.get(rico_text).debtor_weight == 13


def test_TruthUnit_edit_beliefunit_belief_id_CorrectlyModifiesBalanceLinks():
    # GIVEN
    x_truth = truthunit_shop("prom")
    rico_text = "rico"
    x_truth.add_otherunit(other_id=rico_text)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    x_truth.set_beliefunit(swim_beliefunit)
    outdoor_text = "outdoors"
    outdoor_road = x_truth.make_road(x_truth._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_truth.make_road(outdoor_road, camping_text)
    x_truth.add_idea(ideaunit_shop(camping_text), parent_road=outdoor_road)

    camping_idea = x_truth.get_idea_obj(camping_road)
    swim_balancelink = balancelink_shop(
        belief_id=swim_beliefunit.belief_id, credor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).credor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3

    # WHEN
    jog_text = ",jog"
    x_truth.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=False
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 5
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 3


def test_TruthUnit_edit_beliefunit_belief_id_CorrectlyMeldsBalanceLinesBalanceLinksBalanceHeirs():
    # GIVEN
    x_truth = truthunit_shop("prom")
    rico_text = "rico"
    x_truth.add_otherunit(other_id=rico_text)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    x_truth.set_beliefunit(swim_beliefunit)

    jog_text = ",jog"
    jog_beliefunit = beliefunit_shop(belief_id=jog_text)
    x_truth.set_beliefunit(jog_beliefunit)

    outdoor_text = "outdoors"
    outdoor_road = x_truth.make_road(x_truth._owner_id, outdoor_text)
    camping_text = "camping"
    camping_road = x_truth.make_road(outdoor_road, camping_text)
    x_truth.add_idea(ideaunit_shop(camping_text), parent_road=outdoor_road)

    camping_idea = x_truth.get_idea_obj(camping_road)
    swim_balancelink = balancelink_shop(
        belief_id=swim_beliefunit.belief_id, credor_weight=5, debtor_weight=3
    )
    camping_idea.set_balancelink(swim_balancelink)
    jog_balancelink = balancelink_shop(
        belief_id=jog_beliefunit.belief_id, credor_weight=7, debtor_weight=10
    )
    camping_idea.set_balancelink(jog_balancelink)
    assert camping_idea._balancelinks.get(swim_text) != None
    assert camping_idea._balancelinks.get(swim_text).credor_weight == 5
    assert camping_idea._balancelinks.get(swim_text).debtor_weight == 3
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 7
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 10

    # WHEN
    x_truth.edit_beliefunit_belief_id(
        old_belief_id=swim_text, new_belief_id=jog_text, allow_belief_overwite=True
    )

    # THEN
    assert camping_idea._balancelinks.get(swim_text) is None
    assert camping_idea._balancelinks.get(jog_text) != None
    assert camping_idea._balancelinks.get(jog_text).credor_weight == 12
    assert camping_idea._balancelinks.get(jog_text).debtor_weight == 13


def test_TruthUnit_add_idea_CreatesMissingBeliefs():
    # GIVEN
    bob_text = "Bob"
    x_truth = truthunit_shop(bob_text)
    casa_road = x_truth.make_l1_road("casa")
    new_idea_parent_road = x_truth.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    balancelink_z = balancelink_shop(belief_id=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)
    assert len(x_truth._beliefs) == 0
    assert x_truth.get_beliefunit(family_text) is None

    # WHEN
    x_truth.add_l1_idea(clean_cookery_idea, create_missing_beliefs=True)

    # THEN
    assert len(x_truth._beliefs) == 1
    assert x_truth.get_beliefunit(family_text) != None
    assert x_truth.get_beliefunit(family_text)._others in (None, {})


def test_TruthUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_truth = truthunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_truth.add_otherunit(other_id=xia_text)
    x1_truth.add_otherunit(other_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_truth.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_truth.make_l1_road(swim_text)
    x1_truth.add_l1_idea(ideaunit_shop(casa_text))
    x1_truth.add_l1_idea(ideaunit_shop(swim_text))
    x1_truth.edit_idea_attr(swim_road, balancelink=balancelink_shop(xia_text))
    x1_truth.edit_idea_attr(swim_road, balancelink=balancelink_shop(zoa_text))
    x1_truth_swim_idea = x1_truth.get_idea_obj(swim_road)
    assert len(x1_truth_swim_idea._balancelinks) == 2
    x_truth = truthunit_shop(noa_text)
    x_truth.add_otherunit(other_id=xia_text)

    # WHEN
    filtered_idea = x_truth._get_filtered_balancelinks_idea(x1_truth_swim_idea)

    # THEN
    assert len(filtered_idea._balancelinks) == 1
    assert list(filtered_idea._balancelinks.keys()) == [xia_text]


def test_TruthUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa_text = "Noa"
    x1_truth = truthunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    x1_truth.add_otherunit(other_id=xia_text)
    x1_truth.add_otherunit(other_id=zoa_text)

    casa_text = "casa"
    casa_road = x1_truth.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = x1_truth.make_l1_road(swim_text)
    x1_truth.add_l1_idea(ideaunit_shop(casa_text))
    x1_truth.add_l1_idea(ideaunit_shop(swim_text))
    x1_truth.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(belief_id=xia_text)
    )
    x1_truth.edit_idea_attr(
        road=swim_road, balancelink=balancelink_shop(belief_id=zoa_text)
    )
    x1_truth_swim_idea = x1_truth.get_idea_obj(swim_road)
    assert len(x1_truth_swim_idea._balancelinks) == 2

    # WHEN
    x_truth = truthunit_shop(noa_text)
    x_truth.add_otherunit(other_id=xia_text)
    x_truth.add_l1_idea(x1_truth_swim_idea, create_missing_ideas=False)

    # THEN
    x_truth_swim_idea = x_truth.get_idea_obj(swim_road)
    assert len(x_truth_swim_idea._balancelinks) == 1
    assert list(x_truth_swim_idea._balancelinks.keys()) == [xia_text]


def test_TruthUnit_add_idea_DoesNotOverwriteBeliefs():
    # GIVEN
    bob_text = "Bob"
    bob_truth = truthunit_shop(bob_text)
    casa_road = bob_truth.make_l1_road("casa")
    new_idea_parent_road = bob_truth.make_road(casa_road, "cleaning")
    clean_cookery_text = "clean_cookery"
    clean_cookery_idea = ideaunit_shop(
        _weight=40, _label=clean_cookery_text, pledge=True
    )

    family_text = ",family"
    balancelink_z = balancelink_shop(belief_id=family_text)
    clean_cookery_idea.set_balancelink(balancelink=balancelink_z)

    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_otherlink(otherlink=otherlink_shop(other_id="ann1"))
    beliefunit_z.set_otherlink(otherlink=otherlink_shop(other_id="bet1"))
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_z)

    # assert len(bob_truth._beliefs) == 0
    # assert bob_truth.get_beliefunit(family_text) is None
    assert len(bob_truth._beliefs) == 1
    assert len(bob_truth.get_beliefunit(family_text)._others) == 2

    # WHEN
    bob_truth.add_idea(
        idea_kid=clean_cookery_idea,
        parent_road=new_idea_parent_road,
        create_missing_beliefs=True,
    )

    # THEN

    # assert len(bob_truth._beliefs) == 1
    # assert len(bob_truth.get_beliefunit(family_text)._others) == 0
    # beliefunit_z = beliefunit_shop(belief_id=family_text)
    # beliefunit_z.set_otherlink(otherlink=otherlink_shop(other_id="ann2"))
    # beliefunit_z.set_otherlink(otherlink=otherlink_shop(other_id="bet2"))
    # bob_truth.set_beliefunit(y_beliefunit=beliefunit_z)

    assert len(bob_truth._beliefs) == 1
    assert len(bob_truth.get_beliefunit(family_text)._others) == 2


def test_TruthUnit_set_beliefunit_create_missing_others_DoesCreateMissingOthers():
    # GIVEN
    bob_truth = truthunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_otherlink(
        otherlink=otherlink_shop(other_id=anna_text, credor_weight=3, debtor_weight=7)
    )
    beliefunit_z.set_otherlink(
        otherlink=otherlink_shop(other_id=beto_text, credor_weight=5, debtor_weight=11)
    )

    assert beliefunit_z._others.get(anna_text).credor_weight == 3
    assert beliefunit_z._others.get(anna_text).debtor_weight == 7

    assert beliefunit_z._others.get(beto_text).credor_weight == 5
    assert beliefunit_z._others.get(beto_text).debtor_weight == 11

    assert len(bob_truth._others) == 0
    assert len(bob_truth._beliefs) == 0

    # WHEN
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_z, create_missing_others=True)

    # THEN
    assert len(bob_truth._others) == 2
    assert len(bob_truth._beliefs) == 3
    assert bob_truth._others.get(anna_text).credor_weight == 3
    assert bob_truth._others.get(anna_text).debtor_weight == 7

    assert bob_truth._others.get(beto_text).credor_weight == 5
    assert bob_truth._others.get(beto_text).debtor_weight == 11


def test_TruthUnit_set_beliefunit_create_missing_others_DoesNotReplaceOthers():
    # GIVEN
    bob_truth = truthunit_shop("Bob")
    family_text = ",family"
    anna_text = "anna"
    beto_text = "beto"
    bob_truth.set_otherunit(
        otherunit_shop(other_id=anna_text, credor_weight=17, debtor_weight=88)
    )
    bob_truth.set_otherunit(
        otherunit_shop(other_id=beto_text, credor_weight=46, debtor_weight=71)
    )
    beliefunit_z = beliefunit_shop(belief_id=family_text)
    beliefunit_z.set_otherlink(
        otherlink=otherlink_shop(other_id=anna_text, credor_weight=3, debtor_weight=7)
    )
    beliefunit_z.set_otherlink(
        otherlink=otherlink_shop(other_id=beto_text, credor_weight=5, debtor_weight=11)
    )

    assert beliefunit_z._others.get(anna_text).credor_weight == 3
    assert beliefunit_z._others.get(anna_text).debtor_weight == 7
    assert beliefunit_z._others.get(beto_text).credor_weight == 5
    assert beliefunit_z._others.get(beto_text).debtor_weight == 11
    assert len(bob_truth._others) == 2
    assert bob_truth._others.get(anna_text).credor_weight == 17
    assert bob_truth._others.get(anna_text).debtor_weight == 88
    assert bob_truth._others.get(beto_text).credor_weight == 46
    assert bob_truth._others.get(beto_text).debtor_weight == 71

    # WHEN
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_z, create_missing_others=True)

    # THEN
    assert len(bob_truth._others) == 2
    assert bob_truth._others.get(anna_text).credor_weight == 17
    assert bob_truth._others.get(anna_text).debtor_weight == 88
    assert bob_truth._others.get(beto_text).credor_weight == 46
    assert bob_truth._others.get(beto_text).debtor_weight == 71


def test_TruthUnit_get_beliefunits_dict_ReturnsCorrectObj():
    # GIVEN
    bob_truth = truthunit_shop("Bob")
    swim_text = ",swimmers"
    run_text = ",runners"
    fly_text = ",flyers"
    yao_text = "Yao"
    bob_truth.set_otherunit(otherunit_shop(yao_text))
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swim_text))
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=run_text))
    bob_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=fly_text))
    assert len(bob_truth._beliefs) == 4

    # WHEN
    x_beliefunits_dict = bob_truth.get_beliefunits_dict()

    # THEN
    assert x_beliefunits_dict.get(fly_text) != None
    assert x_beliefunits_dict.get(run_text) != None
    assert x_beliefunits_dict.get(swim_text) != None
    assert x_beliefunits_dict.get(yao_text) is None
    assert len(x_beliefunits_dict) == 3


def test_get_others_relevant_beliefs_ReturnsEmptyDict():
    # GIVEN
    bob_text = "Bob"
    truth_with_others = truthunit_shop(bob_text)

    sam_text = "sam"
    wil_text = "wil"
    truth_with_others.set_otherunit(otherunit=otherunit_shop(other_id=bob_text))
    truth_with_others.set_otherunit(otherunit=otherunit_shop(other_id=sam_text))

    truth_with_beliefs = truthunit_shop()

    # WHEN
    print(f"{len(truth_with_others._others)=} {len(truth_with_beliefs._beliefs)=}")
    relevant_x = get_others_relevant_beliefs(
        truth_with_beliefs._beliefs, truth_with_others._others
    )

    # THEN
    assert relevant_x == {}


def test_get_others_relevant_beliefs_Returns2SingleOtherBeliefs():
    # GIVEN
    bob_text = "Bob"
    sam_text = "Sam"
    wil_text = "Wil"
    truth_3beliefs = truthunit_shop(bob_text)
    truth_3beliefs.set_otherunit(otherunit=otherunit_shop(other_id=bob_text))
    truth_3beliefs.set_otherunit(otherunit=otherunit_shop(other_id=sam_text))
    truth_3beliefs.set_otherunit(otherunit=otherunit_shop(other_id=wil_text))

    truth_2others = truthunit_shop(bob_text)
    truth_2others.set_otherunit(otherunit=otherunit_shop(other_id=bob_text))
    truth_2others.set_otherunit(otherunit=otherunit_shop(other_id=sam_text))

    # WHEN
    print(f"{len(truth_2others._others)=} {len(truth_3beliefs._beliefs)=}")
    mrg_x = get_others_relevant_beliefs(truth_3beliefs._beliefs, truth_2others._others)

    # THEN
    assert mrg_x == {bob_text: {bob_text: -1}, sam_text: {sam_text: -1}}


def test_get_other_relevant_beliefs_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_truth = truthunit_shop(jes_text)
    bob_text = "Bob"
    jes_truth.set_otherunit(otherunit_shop(other_id=jes_text))
    jes_truth.set_otherunit(otherunit_shop(other_id=bob_text))

    hike_text = "hikers"
    jes_truth.set_beliefunit(beliefunit_shop(belief_id=hike_text))
    hike_belief = jes_truth.get_beliefunit(hike_text)
    hike_belief.set_otherlink(otherlink_shop(bob_text))

    # WHEN
    noa_text = "Noa"
    noa_mrg = get_other_relevant_beliefs(jes_truth._beliefs, noa_text)

    # THEN
    assert noa_mrg == {}


def test_get_other_relevant_beliefs_ReturnsCorrectDict():
    # GIVEN
    jes_text = "Jessi"
    jes_truth = truthunit_shop(jes_text)
    bob_text = "Bob"
    noa_text = "Noa"
    eli_text = "Eli"
    jes_truth.set_otherunit(otherunit_shop(other_id=jes_text))
    jes_truth.set_otherunit(otherunit_shop(other_id=bob_text))
    jes_truth.set_otherunit(otherunit_shop(other_id=noa_text))
    jes_truth.set_otherunit(otherunit_shop(other_id=eli_text))

    swim_text = ",swimmers"
    jes_truth.set_beliefunit(beliefunit_shop(belief_id=swim_text))
    swim_belief = jes_truth.get_beliefunit(swim_text)
    swim_belief.set_otherlink(otherlink_shop(bob_text))

    hike_text = ",hikers"
    jes_truth.set_beliefunit(beliefunit_shop(belief_id=hike_text))
    hike_belief = jes_truth.get_beliefunit(hike_text)
    hike_belief.set_otherlink(otherlink_shop(bob_text))
    hike_belief.set_otherlink(otherlink_shop(noa_text))

    hunt_text = ",hunters"
    jes_truth.set_beliefunit(beliefunit_shop(belief_id=hunt_text))
    hike_belief = jes_truth.get_beliefunit(hunt_text)
    hike_belief.set_otherlink(otherlink_shop(noa_text))
    hike_belief.set_otherlink(otherlink_shop(eli_text))

    # WHEN
    print(f"{len(jes_truth._others)=} {len(jes_truth._beliefs)=}")
    bob_mrg = get_other_relevant_beliefs(jes_truth._beliefs, bob_text)

    # THEN
    assert bob_mrg == {bob_text: -1, swim_text: -1, hike_text: -1}
