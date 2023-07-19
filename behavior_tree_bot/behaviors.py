import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy(state):
    targets = [planets for planets in state.enemy_planets() if not any(fleets.destination_planet == planets.ID for fleets in state.my_fleets())]
    strongest = max(state.my_planets(), key=lambda p:p.num_ships, default=None)
    weakest = min(targets, key=lambda p: p.num_ships, default=None)
    if not strongest and not weakest:
        return False
    required_ships = weakest.num_ships + state.distance(strongest.ID, weakest.ID) * weakest.growth_rate + 1
    if strongest.num_ships > required_ships:
        return issue_order(state, strongest.ID, weakest.ID, required_ships)
    return False

def counterattack_enemy_spread(state):
    possible_neutral_id = [planets.ID for planets in state.neutral_planets() if not any(fleets.destination_planet == planets.ID for fleets in state.my_fleets())]
    spreading_fleets = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet in possible_neutral_id]
    strongest = max(state.my_planets(), key=lambda p:p.num_ships, default=None)
    if not spreading_fleets or not strongest:
        return False
    
    for sf in spreading_fleets:
        target_planet = state.planets[sf.destination_planet]
        distance = state.distance(strongest.ID, target_planet.ID)
        distance_till_fleet = sf.turns_remaining
        required_ships = (sf.num_ships - target_planet.num_ships) + (distance - distance_till_fleet) * target_planet.growth_rate + 1
        if strongest.num_ships > required_ships:
            if distance >= distance_till_fleet + 1:
                return issue_order(state, strongest.ID, target_planet.ID, required_ships)
    return False


def spread_weakest(state):
    targets = [planets for planets in state.neutral_planets() if not any(fleets.destination_planet == planets.ID for fleets in state.my_fleets())]
    strongest = max(state.my_planets(), key=lambda p:p.num_ships, default=None)
    weakest = min(targets, key=lambda p: p.num_ships, default=None)
    if not strongest or not weakest:
        return False
    required_ships = weakest.num_ships + 1
    if strongest.num_ships > required_ships:
        return issue_order(state, strongest.ID, weakest.ID, required_ships)
    return False