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

def spread_to_weakest_neutral(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))
    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    weakest = min(neutral_planets, key=lambda p: p.num_ships, default=None)
    for p in my_planets:
        required_ships = weakest.num_ships + 1
        if p.num_ships > required_ships:
            return issue_order(state, p.ID, weakest.ID, required_ships)
    return False
