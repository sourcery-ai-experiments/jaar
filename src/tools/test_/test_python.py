from src.tools.python import (
    get_1_if_None,
    add_dict_if_missing,
    place_obj_in_dict,
    get_all_nondictionary_objs,
    get_nested_value,
)
from pytest import raises as pytest_raises


def test_get_1_if_None():
    # GIVEN / WHEN / THEN
    assert get_1_if_None(None) == 1
    assert get_1_if_None(2) == 2
    assert get_1_if_None(-3) == -3


def test_add_dict_if_missing_CorrectAddsDict():
    # GIVEN
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    add_dict_if_missing(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3])

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: {}}}}


def test_place_obj_in_dict_CorrectAddsDict():
    # GIVEN
    y_dict = {}

    # WHEN
    y_key1 = "sports"
    y_key2 = "running"
    y_key3 = "fun running"
    fly_text = "flying"
    place_obj_in_dict(x_dict=y_dict, x_keylist=[y_key1, y_key2, y_key3], x_obj=fly_text)

    # THEN
    assert y_dict == {y_key1: {y_key2: {y_key3: fly_text}}}


def test_get_all_nondictionary_objs_ReturnsCorrectDict():
    # GIVEN
    y_dict = {}
    sports_text = "sports"
    run_text = "running"
    run_list = [sports_text, run_text]
    fun_text = "fun running"
    fun_list = [sports_text, run_text, fun_text]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_text = "mountains"
    mount_list = [sports_text, run_text, mount_text]
    mount_obj = "hard"

    frank_text = "franklin mountain"
    day_text = "day"
    night_text = "night"
    day_list = [sports_text, run_text, frank_text, day_text]
    day_obj = "is hot"
    night_list = [sports_text, run_text, frank_text, night_text]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    print(y_dict)

    assert y_dict == {
        sports_text: {
            run_text: {
                fun_text: fun_obj,
                mount_text: mount_obj,
                frank_text: {day_text: day_obj, night_text: night_obj},
            }
        }
    }

    # WHEN
    childless_objs = get_all_nondictionary_objs(y_dict)

    # THEN
    assert childless_objs == {sports_text: [fun_obj, mount_obj, day_obj, night_obj]}
    assert get_nested_value(y_dict, day_list) == day_obj
    assert get_nested_value(y_dict, mount_list) == mount_obj


def test_get_nested_value_RaisesReadableException():
    y_dict = {}
    sports_text = "sports"
    run_text = "running"
    run_list = [sports_text, run_text]
    fun_text = "fun running"
    fun_list = [sports_text, run_text, fun_text]
    fun_obj = "weird"
    # print(f"{run_list=} {fun_list=}")
    mount_text = "mountains"
    mount_list = [sports_text, run_text, mount_text]
    mount_obj = "hard"

    frank_text = "franklin mountain"
    day_text = "day"
    night_text = "night"
    day_list = [sports_text, run_text, frank_text, day_text]
    day_obj = "is hot"
    night_list = [sports_text, run_text, frank_text, night_text]
    night_obj = "is cool"

    place_obj_in_dict(x_dict=y_dict, x_keylist=fun_list, x_obj=fun_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=mount_list, x_obj=mount_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=day_list, x_obj=day_obj)
    place_obj_in_dict(x_dict=y_dict, x_keylist=night_list, x_obj=night_obj)
    assert get_nested_value(y_dict, day_list) == day_obj

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [swim_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 0."

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_text, swim_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 1."

    # WHEN / THEN
    swim_text = "swim"
    with pytest_raises(Exception) as excinfo:
        get_nested_value(y_dict, [sports_text, swim_text, day_text])
    assert str(excinfo.value) == f"'{swim_text}' failed at level 1."
