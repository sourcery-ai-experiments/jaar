from src._world.healer import healerhold_shop
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.hubunit import hubunit_shop
from src.real.real import realunit_shop
from src.real.examples.real_env import get_test_reals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_RealUnit_generate_doing_world_Sets_doing_WorldFile(env_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(None, music_text, sue_text, None)
    x_sue_doing_path = f"{music_real._owners_dir}/{sue_text}/doing/{sue_text}.json"
    assert os_path_exists(x_sue_doing_path) is False
    music_real.init_owner_econs(sue_text)
    assert sue_hubunit.doing_path() == x_sue_doing_path
    assert os_path_exists(x_sue_doing_path)

    # WHEN
    sue_doing = music_real.generate_doing_world(sue_text)

    # THEN
    example_world = worldunit_shop(sue_text, music_text)
    assert sue_doing._real_id == example_world._real_id
    assert sue_doing._owner_id == example_world._owner_id


def test_RealUnit_generate_doing_world_ReturnsRegeneratedObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    sue_text = "Sue"
    music_real.init_owner_econs(sue_text)
    sue_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, sue_text, None)
    before_sue_world = sue_hubunit.get_doing_world()
    bob_text = "Bob"
    before_sue_world.add_charunit(bob_text)
    sue_hubunit.save_doing_world(before_sue_world)
    assert sue_hubunit.get_doing_world().char_exists(bob_text)

    # WHEN
    after_sue_world = music_real.generate_doing_world(sue_text)

    # THEN method should wipe over doing world
    assert after_sue_world.char_exists(bob_text) is False


def test_RealUnit_generate_doing_world_SetsCorrectFileWithout_healerhold(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    bob_text = "Bob"
    music_real.init_owner_econs(bob_text)
    bob_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    before_bob_doing_world = music_real.generate_doing_world(bob_text)
    sue_text = "Sue"
    assert before_bob_doing_world.char_exists(sue_text) is False

    # WHEN
    bob_suis_world = bob_hubunit.get_suis_world()
    bob_suis_world.add_charunit(sue_text)
    bob_hubunit.save_suis_world(bob_suis_world)

    # WHEN
    after_bob_doing_world = music_real.generate_doing_world(bob_text)

    # THEN
    assert after_bob_doing_world.char_exists(sue_text)


def test_RealUnit_generate_doing_world_SetsFileWith_healerhold(env_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    music_real.init_owner_econs(bob_text)
    bob_hubunit = hubunit_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    after_bob_doing_world = music_real.generate_doing_world(bob_text)
    assert after_bob_doing_world.char_exists(bob_text) is False

    # WHEN
    bob_suis_world = bob_hubunit.get_suis_world()
    bob_suis_world.add_charunit(bob_text)
    bob_suis_world.set_char_pool(100)
    texas_text = "Texas"
    texas_road = bob_suis_world.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_suis_world.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_suis_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_suis_world.add_idea(elpaso_idea, texas_road)
    bob_hubunit.save_suis_world(bob_suis_world)
    after_bob_doing_world = music_real.generate_doing_world(bob_text)

    # THEN
    assert after_bob_doing_world.char_exists(bob_text)


def test_RealUnit_generate_all_doing_worlds_SetsCorrectFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    music_real.init_owner_econs(bob_text)
    reals_dir = music_real.reals_dir
    bob_hubunit = hubunit_shop(reals_dir, music_real.real_id, bob_text, None)
    music_real.init_owner_econs(sue_text)
    sue_hubunit = hubunit_shop(reals_dir, music_real.real_id, sue_text, None)
    bob_suis_world = music_real.generate_doing_world(bob_text)
    sue_suis_world = music_real.generate_doing_world(sue_text)

    texas_text = "Texas"
    texas_road = bob_suis_world.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_suis_world.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_suis_world = bob_hubunit.get_suis_world()
    bob_suis_world.add_charunit(bob_text)
    bob_suis_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_suis_world.add_idea(elpaso_idea, texas_road)
    bob_hubunit.save_suis_world(bob_suis_world)

    sue_suis_world = sue_hubunit.get_suis_world()
    sue_suis_world.add_charunit(sue_text)
    sue_suis_world.add_charunit(bob_text)
    sue_suis_world.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_suis_world.add_idea(elpaso_idea, texas_road)
    sue_hubunit.save_suis_world(sue_suis_world)

    before_bob_doing_world = music_real.get_doing_file_world(bob_text)
    before_sue_doing_world = music_real.get_doing_file_world(sue_text)
    assert before_bob_doing_world.char_exists(bob_text) is False
    assert before_sue_doing_world.char_exists(sue_text) is False

    # WHEN
    music_real.generate_all_doing_worlds()

    # THEN
    after_bob_doing_world = music_real.get_doing_file_world(bob_text)
    after_sue_doing_world = music_real.get_doing_file_world(sue_text)
    assert after_bob_doing_world.char_exists(bob_text)
    assert after_sue_doing_world.char_exists(sue_text)
