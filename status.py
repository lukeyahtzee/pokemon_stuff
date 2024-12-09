import requests
import json
import random

def status_effect_check(move_name):
    move_url = 'https://pokeapi.co/api/v2/move/' + str.lower(move_name)
    response = requests.get(move_url)
    response_json = json.loads(response.text)
    move = {'accuracy': response_json['accuracy'], 'target': 'user', 'effect': None, 'stage-change': 0, 'condition': None}

    # detect if it effects opponent or self
    if 'target' in response_json['effect_entries'][0]['effect']:
        move['target'] = 'opponent'

    if len(response_json['stat_changes']) > 0:
        move['effect'] = response_json['stat_changes'][0]['stat']['name']
        move['stage-change'] = response_json['stat_changes'][0]['change']
    
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
    if 'flinch' in str.lower(response_json['effect_entries'][0]['effect']):
        move['condition'] = 'flinch'
    return move

def status_effect_calc(attacking_mon, defending_mon, index):
    move_fx = attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['status-effects']
    move_chance = attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['effect-chance']

    if move_chance:
        if random.randint(0, 100) > move_chance:
            return
    
    if move_fx['condition'] == 'flinch':
        defending_mon.flinch = True
        return
    
    if move_fx['target'] == 'user':
        if move_fx['effect'] == 'defense':
            x = stat_mod(attacking_mon.def_stage, True)
            attacking_mon.defense = round(attacking_mon.defense * x)
            attacking_mon.def_stage += move_fx['stage-change']
            print_stat('defense', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'attack':
            x = stat_mod(attacking_mon.atk_stage, True)
            attacking_mon.attack = round(attacking_mon.attack * x)
            attacking_mon.atk_stage += move_fx['stage-change']
            print_stat('attack', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'special-attack':
            x = stat_mod(attacking_mon.spatk_stage, True)
            attacking_mon.special_attack = round(attacking_mon.special_attack * x)
            attacking_mon.spatk_stage += move_fx['stage-change']
            print_stat('special attack', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'special-defense':
            x = stat_mod(attacking_mon.spdef_stage, True)
            attacking_mon.special_defense = round(attacking_mon.special_defense * x)
            attacking_mon.spdef_stage += move_fx['stage-change']
            print_stat('special defense', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'speed':
            x = stat_mod(attacking_mon.speed_stage, True)
            attacking_mon.speed = round(attacking_mon.speed * x)
            attacking_mon.speed_stage += move_fx['stage-change']
            print_stat('speed', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'evasion':
            attacking_mon.evasion = max(attacking_mon.evasion - 20, 25)
            print_stat('evasion', attacking_mon, True, move_fx['stage-change'])
        if move_fx['effect'] == 'accuracy':
            attacking_mon.accuracy = min((attacking_mon.accuracy + 50),400)
            print_stat('accuracy', attacking_mon, True, move_fx['stage-change'])
    
    elif move_fx['target'] == 'opponent':
        if defending_mon.mist > 0:
            print(f'{defending_mon.name} was protected by mist!')
            return
        if move_fx['effect'] == 'defense':
            x = stat_mod(defending_mon.def_stage, False)
            defending_mon.defense = round(defending_mon.defense * x)
            defending_mon.def_stage += move_fx['stage-change']
            print_stat('defense', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'attack':
            x = stat_mod(defending_mon.atk_stage, False)
            defending_mon.attack = round(defending_mon.attack * x)
            defending_mon.atk_stage += move_fx['stage-change']
            print_stat('attack', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'special-attack':
            x = stat_mod(defending_mon.spatk_stage, False)
            defending_mon.special_attack = round(defending_mon.special_attack * x)
            defending_mon.spatk_stage += move_fx['stage-change']
            print_stat('special attack', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'special-defense':
            x = stat_mod(defending_mon.spdef_stage, False)
            defending_mon.special_defense = round(defending_mon.special_defense * x)
            defending_mon.spdef_stage += move_fx['stage-change']
            print_stat('special defense', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'speed':
            x = stat_mod(defending_mon.speed_stage, False)
            defending_mon.speed = round(defending_mon.speed * x)
            defending_mon.speed_stage += move_fx['stage-change']
            print_stat('speed', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'evasion':
            defending_mon.evasion = min(defending_mon.evasion + 50, 400)
            print_stat('evasion', defending_mon, False, move_fx['stage-change'])
        if move_fx['effect'] == 'accuracy':
            defending_mon.accuracy = max((defending_mon.accuracy - 20),25)
            print_stat('accuracy', defending_mon, False, move_fx['stage-change'])
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

def print_stat(stat, mon, buff, stage):
    sharp = ' '
    if abs(stage) > 1:
        sharp = ' sharply '
    if abs(stage) > 2:
        sharp = ' severely '
    if buff:
        buff = 'rose!'
    else:
        buff = 'fell!'
    print(f"{mon.name}'s {stat}{sharp}{buff}")



if __name__ == '__main__':
    status_effect_check('sleep-powder')
    status_effect_check('harden')
    status_effect_check('string-shot')
