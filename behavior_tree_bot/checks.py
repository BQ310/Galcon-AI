
def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def if_not_being_attacked(state):
    enemies = [fleet for fleet in state.enemy_fleets() if fleet.destination_planet in state.my_planets()]
    if len(enemies) > 0:
        return False
    return True