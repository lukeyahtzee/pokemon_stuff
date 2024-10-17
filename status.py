import requests
import json
import random

def status_effect_check(move_name):
    move_url = 'https://pokeapi.co/api/v2/move/' + str.lower(move_name)
    response = requests.get(move_url)
    response_json = json.loads(response.text)
    move = {'accuracy': response_json['accuracy'], 'target': 'user', 'effect': None, 'condition': None}

    # detect if it effects opponent or self
    if 'target' in response_json['effect_entries'][0]['effect']:
        move['target'] = 'opponent'


    # status buffs/debuffs
    if 'defense' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'def'
    if 'attack' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'atk'
    if 'special attack' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'spatk'
    if 'special defense' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'spdef'
    if 'speed' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'spd'
    if 'evasion' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'eva'
    if 'accuracy' in str.lower(response_json['effect_entries'][0]['effect']):
        move['effect'] = 'acc'   
    
    # status conditions
    if 'sleep' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'slp'
    if 'poison' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'psn'
    if 'paralyze' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'plz'
    if 'burn' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'brn'
    
    return move

def status_effect_calc(attacking_mon, defending_mon, index):
    move_fx = attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['status-effects']
    if move_fx['target'] == 'user':
        if move_fx['effect'] == 'def':
            stat_mod(attacking_mon.defense, attacking_mon.def_stage, True)
            print_stat('defense', attacking_mon, True)
        if move_fx['effect'] == 'atk':
            stat_mod(attacking_mon.attack, attacking_mon.atk_stage, True)
            print_stat('attack', attacking_mon, True)
        if move_fx['effect'] == 'spatk':
            stat_mod(attacking_mon.special_attack, attacking_mon.spatk_stage, True)
            print_stat('special attack', attacking_mon, True)
        if move_fx['effect'] == 'spdef':
            stat_mod(attacking_mon.special_defense, attacking_mon.spdef_stage, True)
            print_stat('special defense', attacking_mon, True)
        if move_fx['effect'] == 'spd':
            stat_mod(attacking_mon.speed, attacking_mon.speed_stage, True)
            print_stat('speed', attacking_mon, True)
        if move_fx['effect'] == 'eva':
            min(attacking_mon.evasion + 5, 100)
            print_stat('evasion', attacking_mon, True)
        if move_fx['effect'] == 'acc':
            min((attacking_mon.accuracy + 5),100)
            print_stat('accuracy', attacking_mon, True)
    
    elif move_fx['target'] == 'opponent':
        if move_fx['effect'] == 'def':
            stat_mod(defending_mon.defense, defending_mon.def_stage, False)
            print_stat('defense', defending_mon, False)
        if move_fx['effect'] == 'atk':
            stat_mod(defending_mon.attack, defending_mon.atk_stage, False)
            print_stat('attack', defending_mon, False)
        if move_fx['effect'] == 'spatk':
            stat_mod(defending_mon.special_attack, defending_mon.spatk_stage, False)
            print_stat('special attack', defending_mon, False)
        if move_fx['effect'] == 'spdef':
            stat_mod(defending_mon.special_defense, defending_mon.spdef_stage, False)
            print_stat('special defense', defending_mon, False)
        if move_fx['effect'] == 'spd':
            stat_mod(defending_mon.speed, defending_mon.speed_stage, False)
            print_stat('speed', defending_mon, False)
        if move_fx['effect'] == 'eva':
            min(defending_mon.evasion - 5, 50)
            print_stat('evasion', defending_mon, False)
        if move_fx['effect'] == 'acc':
            min((defending_mon.accuracy - 5),50)
            print_stat('accuracy', defending_mon, False)
        defending_mon.condition = move_fx['condition']
        if defending_mon.condition != None:
            print_condition(defending_mon.condition, defending_mon)



def stat_mod(stat, stat_stage, buff):
    if buff:
        x = 2 / 2 + stat_stage
        stat *= x
        stat_stage += 1
        stat *= (2 + stat_stage / 2)
    else:
        x = 2 / 2 + stat_stage
        stat *= x
        stat_stage -= 1
        stat *= (2 + stat_stage / 2)

def print_condition(condition, defending_mon):
    if condition == 'slp':
        print(defending_mon.name, 'fell asleep!')
        defending_mon.condition_limit = random.randint(1, 7)
    if condition == 'psn':
        print(defending_mon.name, 'was poisoned!')
    if condition == 'plz':
        print(defending_mon.name, 'was paralyzed! It may be unable to move!')
    if condition == 'brn':
        print(defending_mon.name, 'was badly burned!')

def print_stat(stat, mon, buff):
    if buff:
        buff = 'rose!'
    else:
        buff = 'fell!'
    print(f"{mon.name}'s {stat} {buff}")



if __name__ == '__main__':
    status_effect_check('sleep-powder')
    status_effect_check('harden')
    status_effect_check('string-shot')
