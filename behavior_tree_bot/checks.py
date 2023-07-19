
def if_enemy_spread(state):
    target_id = [planet.ID for planet in state.neutral_planets()]
    spreaders = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet in target_id]
    if len(spreaders) > 0:
        return True
    return False

def if_enemy_attack(state):
    target_id = [planet.ID for planet in state.my_planets()]
    attackers = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet in target_id]