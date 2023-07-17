import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

#helper functions
def closest(state, source, target_planets):
    target_planets.sort(key=lambda o:state.distance(source.ID, o.ID))
    return target_planets[:3]

# attack behavior
def attack_closest_enemy_planet(state):
    targets = [planet for planet in state.enemy_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for p in state.my_planets():
        closest_planets = closest(state, p, targets)
        for cp in closest_planets:
            dist = state.distance(p.ID, cp.ID)
            required_ships = cp.num_ships + dist * cp.growth_rate + 1
            if p.num_ships > required_ships:
                return issue_order(state, p.ID, cp.ID, required_ships)
    return False

# spread behavior
def spread_to_closest(state):
    targets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for p in state.my_planets():
        closest_planets = closest(state, p, targets)
        for cp in closest_planets:
            dist = state.distance(p.ID, cp.ID)
            required_ships = cp.num_ships + 1
            if p.num_ships > required_ships:
                return issue_order(state, p.ID, cp.ID, required_ships)
    return False

def spread_to_value(state):
    targets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    highest_value = max(targets, key=lambda p: p.growth_rate, default=None)
    strongest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    
    if highest_value is None or strongest is None:
        return False
    required_ships = highest_value.num_ships + 1
    if strongest.num_ships > required_ships:
        return issue_order(state, strongest.ID, highest_value.ID, required_ships)
    return False           