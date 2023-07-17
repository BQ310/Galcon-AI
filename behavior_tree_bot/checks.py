

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def too_large(state):
    biggest = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    if biggest.num_ships > 100:
        return True
    

def if_own_less_than_neutral(state):
    if len(state.my_planets()) < len(state.neutral_planets()):
        return True