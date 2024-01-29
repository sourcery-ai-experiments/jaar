from src._prime.road import get_single_roadnode
from src._prime.meld import get_meld_default
from src.agenda.group import balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.learn import (
    learnunit_shop,
    grain_update,
    grain_delete,
    grain_insert,
    grainunit_shop,
)
from src.agenda.examples.example_learns import (
    get_sue_personroad,
    get_sue_learnunit_example1,
    get_yao_example_roadunit as yao_roadunit,
)


# Given before_agenda, after_agenda
# Go to every element of before_agenda, check if it exists in after_agenda
# If the element is missing in after_agenda: create delete grainunit
# If the element is changed in after_agenda: create update grainunit (optional args in config)
# Go to every element in after_agenda, check if it exists in before_agenda
# If the element does not exist, create insert grainunit

# Use python's ability to compare custom class objects. Don't start at a smallest detail.
# Given before_agenda, after_agenda
# create deepcopy of before_agenda, call it learning_agenda
# if learning_agenda != after_agenda: check something if different find grainunits.
#   Apply grainunits to learning_agenda
# if learning_agenda != after_agenda again: check something else if different
# all the way down the line for all 15 elements

# check "AgendaUnit_weight" unequal => build_update_grain
# check "_max_tree_traverse" unequal => build_update_grain
# check "_party_creditor_pool" unequal => build_update_grain
# check "_party_debtor_pool" unequal => build_update_grain
# check "_auto_output_to_forum" unequal => build_update_grain
# check "_meld_strategy" unequal => build_update_grain
# check "partyunit" unequal => build_party_grains
# check "groupunit_partylink" => build_groupunit_partylink_grains
# check "groupunit" => build_groupunit_grains
# check "idea_reasonunit_premiseunit" => build_idea_reasonunit_premiseunit_grains
# check "idea_reasonunit" => build_idea_reasonunit_grains
# check "idea_beliefunit" => build_idea_beliefunit_grains
# check "idea_suffgroup" => build_idea_suffgroup_grains
# check "idea_balancelink" => build_idea_balancelink_grains
# check "idea" => build_idea_grains
