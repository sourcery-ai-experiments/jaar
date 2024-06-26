from src._instrument.file import save_file
from src._world.examples.world_env import get_world_examples_dir as env_dir
from src._world.examples.example_worlds import world_v001, world_v002

save_file(env_dir(), "example_world3.json", world_v001().get_json())
save_file(env_dir(), "example_world4.json", world_v002().get_json())
