# from src._prime.road import PartyRoad, create_road


# def get_adam_party_road() -> PartyRoad:
#     jack_text = "Yao"
#     mess_problem_road = create_road(jack_text, "mess")
#     femi_healer_road = create_road(mess_problem_road, "Femi")
#     ohio_economy_road = create_road(femi_healer_road, "Ohio")
#     jack_agent_road = create_road(ohio_economy_road, jack_text)
#     adam_party_road = create_road(jack_agent_road, "Adam")
#     return adam_party_road
from src._prime.road import create_road_from_nodes as roadnodes, PersonRoad


def get_bob_personroad() -> PersonRoad:
    bob_text = "Bob"
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    return roadnodes([bob_text, food_text, yao_text, ohio_text])


def get_sue_personroad() -> PersonRoad:
    sue_text = "Sue"
    yao_text = "Yao"
    food_text = "Hunger"
    ohio_text = "Ohio"
    return roadnodes([sue_text, food_text, yao_text, ohio_text])
