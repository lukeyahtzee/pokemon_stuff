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
    if 'confuses' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'cfn'
    
    return move

def status_effect_calc(attacking_mon, defending_mon, index):
    move_fx = attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['status-effects']
    
    if move_fx['target'] == 'user':
        if move_fx['effect'] == 'def':
            x = stat_mod(attacking_mon.def_stage, True)
            attacking_mon.defense = round(attacking_mon.defense * x)
            attacking_mon.def_stage += 1
            print_stat('defense', attacking_mon, True)
        if move_fx['effect'] == 'atk':
            x = stat_mod(attacking_mon.atk_stage, True)
            attacking_mon.attack = round(attacking_mon.attack * x)
            attacking_mon.atk_stage += 1
            print_stat('attack', attacking_mon, True)
        if move_fx['effect'] == 'spatk':
            x = stat_mod(attacking_mon.spatk_stage, True)
            attacking_mon.special_attack = round(attacking_mon.special_attack * x)
            attacking_mon.spatk_stage += 1
            print_stat('special attack', attacking_mon, True)
        if move_fx['effect'] == 'spdef':
            x = stat_mod(attacking_mon.spdef_stage, True)
            attacking_mon.special_defense = round(attacking_mon.special_defense * x)
            attacking_mon.spdef_stage += 1
            print_stat('special defense', attacking_mon, True)
        if move_fx['effect'] == 'spd':
            x = stat_mod(attacking_mon.speed_stage, True)
            attacking_mon.speed = round(attacking_mon.speed * x)
            attacking_mon.speed_stage += 1
            print_stat('speed', attacking_mon, True)
        if move_fx['effect'] == 'eva':
            attacking_mon.evasion = max(attacking_mon.evasion - 20, 25)
            print_stat('evasion', attacking_mon, True)
        if move_fx['effect'] == 'acc':
            attacking_mon.accuracy = min((attacking_mon.accuracy + 50),400)
            print_stat('accuracy', attacking_mon, True)
    
    elif move_fx['target'] == 'opponent':
        if move_fx['effect'] == 'def':
            x = stat_mod(defending_mon.def_stage, False)
            defending_mon.defense = round(defending_mon.defense * x)
            defending_mon.def_stage -= 1
            print_stat('defense', defending_mon, False)
        if move_fx['effect'] == 'atk':
            x = stat_mod(defending_mon.atk_stage, False)
            defending_mon.attack = round(defending_mon.attack * x)
            defending_mon.atk_stage -= 1
            print_stat('attack', defending_mon, False)
        if move_fx['effect'] == 'spatk':
            x = stat_mod(defending_mon.spatk_stage, False)
            defending_mon.special_attack = round(defending_mon.special_attack * x)
            defending_mon.spatk_stage -= 1
            print_stat('special attack', defending_mon, False)
        if move_fx['effect'] == 'spdef':
            x = stat_mod(defending_mon.spdef_stage, False)
            defending_mon.special_defense = round(defending_mon.special_defense * x)
            defending_mon.spdef_stage -= 1
            print_stat('special defense', defending_mon, False)
        if move_fx['effect'] == 'spd':
            x = stat_mod(defending_mon.speed_stage, False)
            defending_mon.speed = round(defending_mon.speed * x)
            defending_mon.speed_dtage -= 1
            print_stat('speed', defending_mon, False)
        if move_fx['effect'] == 'eva':
            defending_mon.evasion = min(defending_mon.evasion + 50, 400)
            print_stat('evasion', defending_mon, False)
        if move_fx['effect'] == 'acc':
            defending_mon.accuracy = max((defending_mon.accuracy - 20),25)
            print_stat('accuracy', defending_mon, False)
        if defending_mon.condition and move_fx['condition']:
            print("But it failed!")
        elif move_fx['condition']:
            defending_mon.condition = move_fx['condition']
            if defending_mon.condition != None:
                print_condition(defending_mon.condition, defending_mon)



def stat_mod(stat_stage, buff):
    if buff:
        if stat_stage > 0:
            return (2 / (2 + stat_stage)) * ((2 + stat_stage + 1)/ 2)
        elif stat_stage < 0:
            return ((2 - stat_stage) / 2) * (2 / (2 - stat_stage + 1))# multiply base stat by new stage
        else:
            stat_stage += 1
            return ((2 + stat_stage) / 2)
    else:
        if stat_stage > 0:
            return (2 / (2 + stat_stage)) * ((2 + stat_stage - 1)/ 2)
        elif stat_stage < 0:
            return ((2 - stat_stage) / 2) * (2 / (2 - stat_stage + 1))# multiply base stat by new stage
        else:
            stat_stage -= 1
            return (2 / (2 - stat_stage))

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
    if condition == 'cfn':
        print(defending_mon.name, 'became confused!')
        defending_mon.condition_limit = random.randint(2, 5)

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
