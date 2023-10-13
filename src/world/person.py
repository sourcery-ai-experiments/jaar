from dataclasses import dataclass
from src.goal.goal import GoalUnit, GoalTag, goalunit_shop


class PersonName(str):
    pass


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _goals: dict[GoalTag:GoalUnit] = None

    def set_goals_empty_if_none(self):
        if self._goals is None:
            self._goals = {}

    def create_goal(self, goal_tag: GoalTag):
        goals_dir = f"{self.person_dir}/goals"
        self._goals[goal_tag] = goalunit_shop(tag=goal_tag, goals_dir=goals_dir)

    def get_goal_obj(self, goal_tag: GoalTag) -> GoalUnit:
        return self._goals.get(goal_tag)


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_goals_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
