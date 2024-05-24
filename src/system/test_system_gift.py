# from src.agenda.atom import get_atom_columns_build
# from src.system.system import systemunit_shop
# from src.system.examples.system_env_kit import (
#     get_test_systems_dir,
#     systems_dir_setup_cleanup,
# )
# from src.system.examples.example_gifts import (
#     yao_sue_giftunit as example_yao_sue_giftunit,
# )
# from os import path as os_path


# def test_systemUnit_set_giftunit_CorrectSetsAttr(systems_dir_setup_cleanup):
#     # GIVEN
#     oregon_system = systemunit_shop("Oregon", get_test_systems_dir(), in_memory_journal=True)
#     assert oregon_system._giftunits == {}

#     # WHEN
#     yao_sue_uid = oregon_system.set_giftunit(x_giftunit=example_yao_sue_giftunit())

#     # THEN
#     assert oregon_system._giftunits != {}
#     assert oregon_system._giftunits == {1: example_yao_sue_giftunit()}
#     assert yao_sue_uid == 1


# def test_systemUnit_get_giftunit_ReturnsCorrectObj(systems_dir_setup_cleanup):
#     # GIVEN
#     oregon_system = systemunit_shop("Oregon", get_test_systems_dir(), in_memory_journal=True)
#     yao_sue_uid = oregon_system.set_giftunit(example_yao_sue_giftunit())

#     # WHEN
#     yao_sue_giftunit = oregon_system.get_giftunit(yao_sue_uid)

#     # THEN
#     assert yao_sue_giftunit == example_yao_sue_giftunit()


# def test_systemUnit_giftunit_file_exists_ReturnsCorrectObj(systems_dir_setup_cleanup):
#     # GIVEN
#     oregon_system = systemunit_shop("Oregon", get_test_systems_dir(), in_memory_journal=True)
#     static_yao_sue_uid = 1
#     assert oregon_system.giftunit_file_exists(static_yao_sue_uid) == False

#     # WHEN
#     gen_yao_sue_uid = oregon_system.set_giftunit(example_yao_sue_giftunit())
#     assert static_yao_sue_uid == gen_yao_sue_uid

#     # THEN
#     assert oregon_system.giftunit_file_exists(static_yao_sue_uid)


# def test_systemUnit_del_giftunit_CorrectChangesAttr(systems_dir_setup_cleanup):
#     # GIVEN
#     oregon_system = systemunit_shop("Oregon", get_test_systems_dir(), in_memory_journal=True)
#     yao_sue_uid = oregon_system.set_giftunit(example_yao_sue_giftunit())
#     assert oregon_system.giftunit_file_exists(yao_sue_uid)

#     # WHEN
#     oregon_system.del_giftunit(yao_sue_uid)

#     # THEN
#     assert oregon_system.giftunit_file_exists(yao_sue_uid) == False


# def test_systemUnit_apply_requestunit_CorrectlyCreates_role_agendas(
#     systems_dir_setup_cleanup,
# ):
#     # GIVEN requester and requestee role_agendas does not exist
#     w1_text = "w1"
#     system = systemunit_shop(w1_text, get_test_systems_dir(), in_memory_journal=True)
#     yao_text = "Yao"
#     system.add_personunit(yao_text)
#     yao_person = system.get_personunit_from_memory(yao_text)
#     texas_text = "Texas"
#     yao_person.set_econunit(texas_text)
#     texas_econ = yao_person.get_econunit(texas_text)
#     texas_jobs_dir = texas_econ.get_jobs_dir()

#     highwaay_needunit = create_needunit(
#         econdeleteme=econdeleteme_shop("war", yao_text, texas_text),
#         fix="flying in 737s",
#         positive="Do not fly",
#         negative="Continue flying",
#         isssue="global environment",
#         good="healthy",
#         bad="boiling",
#     )
#     tim_text = "Tim"
#     xio_text = "Xio"
#     highwaay_requestunit = create_requestunit(
#         needunit=highwaay_needunit, requestee_party_id=tim_text, requester_person_id=xio_text
#     )
#     assert system.get_personunit_from_memory(tim_text) is None
#     assert system.get_personunit_from_memory(xio_text) is None
#     jobs_tim_file_path = f"{texas_jobs_dir}/{tim_text}.json"
#     jobs_xio_file_path = f"{texas_jobs_dir}/{xio_text}.json"
#     jobs_yao_file_path = f"{texas_jobs_dir}/{yao_text}.json"
#     assert os_path.exists(jobs_tim_file_path) is False
#     assert os_path.exists(jobs_xio_file_path) is False
#     assert os_path.exists(jobs_yao_file_path) is False

#     # WHEN
#     system.apply_requestunit(highwaay_requestunit)

#     # THEN
#     assert system.get_personunit_from_memory(tim_text) != None
#     assert system.get_personunit_from_memory(xio_text) != None
#     print(f"{jobs_tim_file_path=}")
#     assert os_path.exists(jobs_tim_file_path)
#     assert os_path.exists(jobs_xio_file_path)
#     assert os_path.exists(jobs_yao_file_path)
#     assert texas_econ.create_job_file_from_role_file(tim_text).get_role() != None
#     assert texas_econ.create_job_file_from_role_file(xio_text).get_role() != None
#     assert texas_econ.create_job_file_from_role_file(yao_text).get_role() != None


# def test_systemUnit_apply_requestunit_CorrectlyAddsTaskTo_requester_role_agenda(
#     systems_dir_setup_cleanup,
# ):
#     system = systemunit_shop("w1", get_test_systems_dir(), in_memory_journal=True)
#     yao_text = "Yao"
#     system.add_personunit(yao_text)
#     yao_person = system.get_personunit_from_memory(yao_text)
#     texas_text = "Texas"
#     yao_person.set_econunit(texas_text)
#     texas_econ = yao_person.get_econunit(texas_text)

#     flying_text = "flying in 737s"
#     no_fly_text = "Do not fly"
#     yesfly_text = "Continue flying"
#     weather_text = "global weather"
#     healthy_text = "healthy"
#     boiling_text = "boiling"

#     highwaay_needunit = create_needunit(
#         econdeleteme=econdeleteme_shop("war", yao_text, texas_text),
#         fix=flying_text,
#         positive=no_fly_text,
#         negative=yesfly_text,
#         isssue=weather_text,
#         good=healthy_text,
#         bad=boiling_text,
#     )
#     tim_text = "Tim"
#     xio_text = "Xio"
#     fix_weight = 7
#     highwaay_requestunit = create_requestunit(
#         needunit=highwaay_needunit,
#         requestee_party_id=tim_text,
#         requester_party_id=xio_text,
#         fix_weight=fix_weight,
#     )

#     # WHEN
#     system.apply_requestunit(highwaay_requestunit)

#     # THEN
#     xio_role = texas_econ.create_job_file_from_role_file(xio_text).get_role()
#     xio_partyunit = xio_role.get_party(xio_text)
#     tim_partyunit = xio_role.get_party(tim_text)
#     assert xio_partyunit != None
#     assert tim_partyunit != None
#     assert tim_partyunit.creditor_weight == 1
#     assert tim_partyunit.debtor_weight == 1
#     flying_road = econunit.build_econ_road(texas_econ.econ_id, flying_text)
#     no_fly_road = econunit.build_econ_road(flying_road, no_fly_text)
#     yesfly_road = econunit.build_econ_road(flying_road, yesfly_text)
#     weather_road = econunit.build_econ_road(texas_econ.econ_id, weather_text)
#     healthy_road = econunit.build_econ_road(weather_road, healthy_text)
#     boiling_road = econunit.build_econ_road(weather_road, boiling_text)
#     print(f"{xio_role._idea_dict.keys()=}")
#     print(f"{flying_road=}")
#     print(f"{no_fly_road=}")
#     flying_idea = xio_role.get_idea_obj(flying_road)
#     no_fly_idea = xio_role.get_idea_obj(no_fly_road)
#     yesfly_idea = xio_role.get_idea_obj(yesfly_road)
#     weather_idea = xio_role.get_idea_obj(weather_road)
#     healthy_idea = xio_role.get_idea_obj(healthy_road)
#     boiling_idea = xio_role.get_idea_obj(boiling_road)
#     assert flying_idea != None
#     assert no_fly_idea != None
#     assert yesfly_idea != None
#     assert weather_idea != None
#     assert healthy_idea != None
#     assert boiling_idea != None

#     assert flying_idea.pledge == False
#     assert no_fly_idea.pledge
#     assert yesfly_idea.pledge == False
#     assert weather_idea.pledge == False
#     assert healthy_idea.pledge == False
#     assert boiling_idea.pledge == False

#     assert len(flying_idea._reasonunits) == 0
#     assert len(no_fly_idea._reasonunits) == 1
#     assert len(yesfly_idea._reasonunits) == 0
#     assert len(weather_idea._reasonunits) == 0
#     assert len(healthy_idea._reasonunits) == 0
#     assert len(boiling_idea._reasonunits) == 0

#     assert no_fly_idea._reasonunits.get(weather_road) != None
#     weather_reasonunit = no_fly_idea._reasonunits.get(weather_road)
#     assert len(weather_reasonunit.premises) == 1
#     assert weather_reasonunit.premises.get(boiling_road) != None

#     assert flying_idea._weight == 1
#     assert no_fly_idea._weight != 1
#     assert no_fly_idea._weight == fix_weight
#     assert yesfly_idea._weight == 1
#     assert weather_idea._weight == 1
#     assert healthy_idea._weight == 1
#     assert boiling_idea._weight == 1

#     assert flying_idea._assignedunit.get_suffgroup(tim_text) != None
#     assert no_fly_idea._assignedunit.get_suffgroup(tim_text) != None
#     assert yesfly_idea._assignedunit.get_suffgroup(tim_text) != None
#     assert weather_idea._assignedunit.get_suffgroup(tim_text) != None
#     assert healthy_idea._assignedunit.get_suffgroup(tim_text) != None
#     assert boiling_idea._assignedunit.get_suffgroup(tim_text) != None

#     assert flying_idea._balancelinks.get(tim_text) != None
#     assert no_fly_idea._balancelinks.get(tim_text) != None
#     assert yesfly_idea._balancelinks.get(tim_text) != None
#     assert weather_idea._balancelinks.get(tim_text) != None
#     assert healthy_idea._balancelinks.get(tim_text) != None
#     assert boiling_idea._balancelinks.get(tim_text) != None

#     xio_beliefunits = xio_role._idearoot._beliefunits
#     assert len(xio_beliefunits) == 1
#     static_weather_beliefunit = beliefunit_shop(weather_road, pick=boiling_road)
#     assert xio_beliefunits.get(weather_road) == static_weather_beliefunit
#     assert len(xio_role.get_intent_dict()) == 0

#     # check tim role
#     tim_role = texas_econ.create_job_file_from_role_file(tim_text).get_role()
#     assert tim_role.get_party(xio_text) != None
#     assert tim_role.get_party(xio_text).debtor_weight == 7
#     # check tim jobs
#     tim_jobs = texas_econ.get_job_agenda(tim_text)
#     assert len(tim_jobs.get_intent_dict()) == 1
#     assert tim_jobs.get_intent_dict()[0].get_road() == no_fly_road


# def test_systemUnit_apply_requestunit_CorrectlyAppliesGroup(systems_dir_setup_cleanup):
#     system = systemunit_shop("w1", get_test_systems_dir(), in_memory_journal=True)
#     yao_text = "Yao"
#     system.add_personunit(yao_text)
#     yao_person = system.get_personunit_from_memory(yao_text)
#     texas_text = "Texas"
#     yao_person.set_econunit(texas_text)
#     texas_econ = yao_person.get_econunit(texas_text)

#     flying_text = "flying in 737s"
#     no_fly_text = "Do not fly"
#     yesfly_text = "Continue flying"
#     weather_text = "global weather"
#     healthy_text = "healthy"
#     boiling_text = "boiling"

#     highwaay_needunit = create_needunit(
#         econdeleteme=econdeleteme_shop("war", yao_text, texas_text),
#         fix=flying_text,
#         positive=no_fly_text,
#         negative=yesfly_text,
#         isssue=weather_text,
#         good=healthy_text,
#         bad=boiling_text,
#     )
#     tim_text = "Tim"
#     xio_text = "Xio"
#     environmentalist_text = "Environmentalist"
#     fix_weight = 7
#     highwaay_requestunit = create_requestunit(
#         needunit=highwaay_needunit,
#         requestee_party_id=tim_text,
#         requestee_group=environmentalist_text,
#         requester_person_id=xio_text,
#         fix_weight=fix_weight,
#     )

#     # WHEN
#     system.apply_requestunit(highwaay_requestunit)

#     # THEN
#     xio_role = texas_econ.create_job_file_from_role_file(xio_text).get_role()
#     xio_partyunit = xio_role.get_party(xio_text)
#     tim_partyunit = xio_role.get_party(tim_text)
#     assert xio_partyunit != None
#     assert tim_partyunit != None
#     assert tim_partyunit.creditor_weight == 1
#     assert tim_partyunit.debtor_weight == 1
#     assert xio_role._groups.get(environmentalist_text) != None
#     environmentalist_group = xio_role.get_groupunit(environmentalist_text)
#     assert len(environmentalist_group._partys) == 1
#     assert environmentalist_group.get_partylink(tim_text) != None

#     flying_road = econunit.build_econ_road(texas_econ.econ_id, flying_text)
#     no_fly_road = econunit.build_econ_road(flying_road, no_fly_text)
#     yesfly_road = econunit.build_econ_road(flying_road, yesfly_text)
#     weather_road = econunit.build_econ_road(texas_econ.econ_id, weather_text)
#     healthy_road = econunit.build_econ_road(weather_road, healthy_text)
#     boiling_road = econunit.build_econ_road(weather_road, boiling_text)
#     flying_idea = xio_role.get_idea_obj(flying_road)
#     no_fly_idea = xio_role.get_idea_obj(no_fly_road)
#     yesfly_idea = xio_role.get_idea_obj(yesfly_road)
#     weather_idea = xio_role.get_idea_obj(weather_road)
#     healthy_idea = xio_role.get_idea_obj(healthy_road)
#     boiling_idea = xio_role.get_idea_obj(boiling_road)

#     assert flying_idea._assignedunit.get_suffgroup(tim_text) is None
#     assert no_fly_idea._assignedunit.get_suffgroup(tim_text) is None
#     assert yesfly_idea._assignedunit.get_suffgroup(tim_text) is None
#     assert weather_idea._assignedunit.get_suffgroup(tim_text) is None
#     assert healthy_idea._assignedunit.get_suffgroup(tim_text) is None
#     assert boiling_idea._assignedunit.get_suffgroup(tim_text) is None

#     assert flying_idea._assignedunit.get_suffgroup(environmentalist_text) != None
#     assert no_fly_idea._assignedunit.get_suffgroup(environmentalist_text) != None
#     assert yesfly_idea._assignedunit.get_suffgroup(environmentalist_text) != None
#     assert weather_idea._assignedunit.get_suffgroup(environmentalist_text) != None
#     assert healthy_idea._assignedunit.get_suffgroup(environmentalist_text) != None
#     assert boiling_idea._assignedunit.get_suffgroup(environmentalist_text) != None

#     xio_beliefunits = xio_role._idearoot._beliefunits
#     assert len(xio_beliefunits) == 1
#     static_weather_beliefunit = beliefunit_shop(weather_road, pick=boiling_road)
#     assert xio_beliefunits.get(weather_road) == static_weather_beliefunit
#     assert len(xio_role.get_intent_dict()) == 0

#     # check tim role
#     tim_role = texas_econ.create_job_file_from_role_file(tim_text).get_role()
#     assert tim_role.get_party(xio_text) != None
#     assert tim_role.get_party(xio_text).debtor_weight == 7
#     # check tim jobs
#     tim_jobs = texas_econ.get_job_agenda(tim_text)
#     assert len(tim_jobs.get_intent_dict()) == 1
#     assert tim_jobs.get_intent_dict()[0].get_road() == no_fly_road


# # def test_systemUnit_apply_requestunit_Multiple_requestunitsCreateMultiple_intent_items(
# #     systems_dir_setup_cleanup,
# # ):
# #     system = systemunit_shop("w1", get_test_systems_dir(), in_memory_journal=True)
# #     yao_text = "Yao"
# #     system.add_personunit(yao_text)
# #     yao_person = system.get_personunit_from_memory(yao_text)
# #     texas_text = "Texas"
# #     yao_person.set_econunit(texas_text)
# #     texas_econ = yao_person.get_econunit(texas_text)

# #     fly_needunit = create_needunit(
# #         econdeleteme=econdeleteme_shop("war", yao_text, texas_text),
# #         fix="flying in 737s",
# #         positive="Do not fly",
# #         negative="Continue flying",
# #         isssue="global weather",
# #         good="healthy",
# #         bad="boiling",
# #     )
# #     sue_text = "Sue"
# #     tim_text = "Tim"
# #     xio_text = "Xio"
# #     fix_weight = 7
# #     fly_requestunit = create_requestunit(fly_needunit, tim_text, xio_text, fix_weight)
# #     fly_requestunit = create_requestunit(fly_needunit, tim_text, xio_text, fix_weight)
# #     fly_requestunit = create_requestunit(fly_needunit, yao_text, xio_text, fix_weight)

# #     # WHEN
# #     system.apply_requestunit(fly_requestunit)
# #     system.apply_requestunit(fly_requestunit)
