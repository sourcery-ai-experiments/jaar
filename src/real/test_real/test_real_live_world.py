from src._world.healer import healerhold_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.userhub import userhub_shop
from src.real.real import realunit_shop
from src.real.examples.real_env import get_test_reals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_RealUnit_generate_live_world_Sets_live_WorldFile(env_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_userhub = userhub_shop(None, music_text, sue_text, None)
    x_sue_live_path = f"{music_real._persons_dir}/{sue_text}/live/{sue_text}.json"
    assert os_path_exists(x_sue_live_path) is False
    music_real.init_person_econs(sue_text)
    assert sue_userhub.live_path() == x_sue_live_path
    assert os_path_exists(x_sue_live_path)

    # WHEN
    sue_live = music_real.generate_live_world(sue_text)

    # THEN
    example_world = worldunit_shop(sue_text, music_text)
    assert sue_live._real_id == example_world._real_id
    assert sue_live._owner_id == example_world._owner_id


def test_RealUnit_generate_live_world_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    sue_text = "Sue"
    music_real.init_person_econs(sue_text)
    sue_userhub = userhub_shop(music_real.reals_dir, music_real.real_id, sue_text, None)
    before_sue_world = sue_userhub.get_live_world()
    bob_text = "Bob"
    before_sue_world.add_otherunit(bob_text)
    sue_userhub.save_live_world(before_sue_world)
    assert sue_userhub.get_live_world().other_exists(bob_text)

    # WHEN
    after_sue_world = music_real.generate_live_world(sue_text)

    # THEN method should wipe over live world
    assert after_sue_world.other_exists(bob_text) is False


def test_RealUnit_generate_live_world_SetsCorrectFileWithout_healerhold(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    bob_text = "Bob"
    music_real.init_person_econs(bob_text)
    bob_userhub = userhub_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    before_bob_live_world = music_real.generate_live_world(bob_text)
    sue_text = "Sue"
    assert before_bob_live_world.other_exists(sue_text) is False

    # WHEN
    bob_same_world = bob_userhub.get_same_world()
    bob_same_world.add_otherunit(sue_text)
    bob_userhub.save_same_world(bob_same_world)

    # WHEN
    after_bob_live_world = music_real.generate_live_world(bob_text)

    # THEN
    assert after_bob_live_world.other_exists(sue_text)


def test_RealUnit_generate_live_world_SetsFileWith_healerhold(env_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    music_real.init_person_econs(bob_text)
    bob_userhub = userhub_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    after_bob_live_world = music_real.generate_live_world(bob_text)
    assert after_bob_live_world.other_exists(bob_text) is False

    # WHEN
    bob_same_world = bob_userhub.get_same_world()
    bob_same_world.add_otherunit(bob_text)
    bob_same_world.set_other_pool(100)
    texas_text = "Texas"
    texas_road = bob_same_world.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_same_world.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_same_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_same_world.add_idea(elpaso_idea, texas_road)
    bob_userhub.save_same_world(bob_same_world)
    after_bob_live_world = music_real.generate_live_world(bob_text)

    # THEN
    assert after_bob_live_world.other_exists(bob_text)


def test_RealUnit_generate_all_live_worlds_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    music_real.init_person_econs(bob_text)
    reals_dir = music_real.reals_dir
    bob_userhub = userhub_shop(reals_dir, music_real.real_id, bob_text, None)
    music_real.init_person_econs(sue_text)
    sue_userhub = userhub_shop(reals_dir, music_real.real_id, sue_text, None)
    bob_same_world = music_real.generate_live_world(bob_text)
    sue_same_world = music_real.generate_live_world(sue_text)

    texas_text = "Texas"
    texas_road = bob_same_world.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_same_world.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_same_world = bob_userhub.get_same_world()
    bob_same_world.add_otherunit(bob_text)
    bob_same_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_same_world.add_idea(elpaso_idea, texas_road)
    bob_userhub.save_same_world(bob_same_world)

    sue_same_world = sue_userhub.get_same_world()
    sue_same_world.add_otherunit(sue_text)
    sue_same_world.add_otherunit(bob_text)
    sue_same_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_same_world.add_idea(elpaso_idea, texas_road)
    sue_userhub.save_same_world(sue_same_world)

    before_bob_live_world = music_real.get_live_file_world(bob_text)
    before_sue_live_world = music_real.get_live_file_world(sue_text)
    assert before_bob_live_world.other_exists(bob_text) is False
    assert before_sue_live_world.other_exists(sue_text) is False

    # WHEN
    music_real.generate_all_live_worlds()

    # THEN
    after_bob_live_world = music_real.get_live_file_world(bob_text)
    after_sue_live_world = music_real.get_live_file_world(sue_text)
    assert after_bob_live_world.other_exists(bob_text)
    assert after_sue_live_world.other_exists(sue_text)
