import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

#attack behavior
def attack_weakest_enemy_planet(state):
    targets = [planet for planet in state.not_my_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    # (2) Find my strongest planet.
    strongest_planet = max(targets, key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

#attack closest
def attack_closest_enemy_planet(state):
    targets = [planet for planet in state.not_my_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    for p in state.my_planets():
        closest_enemy_to_p = min(targets, key=lambda o: state.distance(p.ID, o.ID), default=None)
        if closest_enemy_to_p is not None:
            dist = state.distance(p.ID, closest_enemy_to_p.ID)
            required_ships = closest_enemy_to_p.num_ships + dist * closest_enemy_to_p.growth_rate + 1
            if p.num_ships > required_ships:
                return issue_order(state, p.ID, closest_enemy_to_p.ID, required_ships)
    return False

#spread behavior
def spread_to_weakest_neutral_planet(state):
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        required_ships = weakest_planet.num_ships + 1
        if strongest_planet.num_ships > required_ships:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
            return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)

def spread_to_gr_neutral_planet(state):
    
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    highest_gr_planet = max(state.neutral_planets(), key=lambda p: p.growth_rate, default=None)
    if not strongest_planet or not highest_gr_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        required_ships = highest_gr_planet.num_ships + 1
        if strongest_planet.num_ships > required_ships:
            return issue_order(state, strongest_planet.ID, highest_gr_planet.ID, required_ships)