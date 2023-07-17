#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
  
    spread_plan = Sequence(name='Spread Strategy')
    is_neutral = Check(if_neutral_planet_available)
    not_attacked = Check(if_not_being_attacked)
    spread_close = Action(spread_to_closest)
    spread_value = Action(spread_to_value)
    close_or_value = Selector(name='close or value')
    should_value = Sequence(name='should spread value')
    should_value.child_nodes = [not_attacked, spread_value]
    close_or_value.child_nodes = [should_value.copy(), spread_close]
    spread_plan.child_nodes = [is_neutral,  close_or_value.copy()]

    offensive_plan = Selector(name='Offensive Strategy')
    attack_close = Action(attack_closest_enemy_planet)

    offensive_plan.child_nodes = [attack_close]
    
    root.child_nodes = [spread_plan, offensive_plan]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
