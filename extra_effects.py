from move_records import Record
from status import status_effect_check
import requests
import json
import random


extra_effects_moves = [
    'recover',
    'reflect',
    'mimic',
    'protect',
    'bide',
    'dragon-rage',
    'rest',
    'whirlwind',
    'fly',
    'dig',
    'psywave',
    'haze',
    'substitute',
    'seismic-toss',
    'counter',
    'double-edge',
    'focus-energy',
    'super-fang',
    'leech-life',
    'mega-drain',
    'explosion',
    'conversion',
    'sonic-boom',
    'mist',
    'fury-attack',
    'horn-drill',
    'rage',
    'night-shade',
    'splash'
]

def unique_effects(move):
    if move in extra_effects_moves:
        return True
    else: return False

def apply_effects(mon, defending_mon, move, r, bottom_of_turn, dmg):
    if move == 'recover':
        mon.hp += min(mon.hp + (mon.max_hp / 2), mon.max_hp)
    if move == 'leech-life' or move == 'mega-drain':
        mon.hp = min(mon.hp + (dmg / 2), mon.max_hp)
        print(f"{defending_mon.name} had its energy drained!")
        return dmg
    
    if move == 'night-shade':
        dmg = mon.level
        if 'normal' or 'fighting' in defending_mon.types:
            print(f"it doesn't effect the opposing {defending_mon.name}...")
            return 0
        return dmg
    
    if move == 'rage':
        mon.enraged = True
        return dmg
    
    if move == 'splash':
        print("nothing happened!")

    if move == 'transform':
        print("but it failed!")
    
    if move == 'fury-attack':
        x = random.randint(0, 7)
        if x < 3:
            print("hit 2 times!")
            return 2 * dmg
        if x < 6:
            print("hit 3 times!")
            return 3 * dmg
        if x < 7:
            print("hit 4 times!")
            return 4 * dmg
        if x == 7:
            print("hit 5 times!")
            return 5 * dmg
        
    if move == 'horn-drill':
        dmg = defending_mon.max_hp
        return dmg

    if move == 'mist':
        mon.mist = 5
        print(f'{mon.name} became immune to stat-lowering effects!')
        return 0

    if move == 'reflect':
        if mon.reflect_barrier > 0:
            print(f'{mon.name} already has a barrier active!')
        else:
            print(f'{mon.name} put up a barrier! damage from physical attacks is weakened!')
            mon.reflect_barrier = 5
        return 0

    if move == 'fly':
        print(f'{mon.name} flew up high!')
        mon.fly_dig = True
        return 0
    
    if move == 'dig':
        print(f'{mon.name} dug into the ground!')
        mon.fly_dig = True
        return 0
    
    if move == 'self-destruct' or move == 'explosion':
        print(f'{mon.name} self destructed!')
        mon.hp = 0
        return 200
    
    if move == 'rest':
        if mon.hp == mon.max_hp or mon.condition == 'slp':
            print('But it failed!')
            return 0
        else:
            mon.condition = 'slp'
            mon.hp = mon.max_hp
            print(f'{mon.name} fell asleep and regained health!')
        return 0
    
    if move == 'super-fang':
        return round(defending_mon.hp / 2)
    
    if move == 'seismic-toss':
        return 50
    
    if move == 'dragon-rage':
        return 40
    
    if move == 'counter':
        # deal back twice the physical damage the user received this turn, or nothing if n/a
        # will be a little tricky to implement
        if not r.get_previous_enemy_atk(bottom_of_turn)[3]:
            print("but it failed!")
            return 0
        else:
            return 2 * r.get_previous_enemy_atk(bottom_of_turn)[2]
    
    if move == 'haze':
        # resets all pokemons stats to base
        mon.reset_stats()
        defending_mon.reset_stats()
        print("all stat modifications have been erased!")
        return 0
    
    if move == 'sonic-boom':
        return 20
    
    if move == 'double-edge':
        mon.hp -= ((1/3) * dmg)
        print(f"{mon.name} was hurt by recoil!")
        return dmg
        # applies 1/3 the damage inflicted as recoil
        # TODO: this move should deal recoil even if it misses
        # currently nothing executes if this attack misses. may require a refactor

    if move == 'focus-energy':
        if not mon.focus_energy:
            print(f"{mon.name} is getting pumped!")
            mon.focus_energy = True
            mon.crit_rate = mon.crit_rate * 2
            return 0
        else:
            print("But it failed!")
            return 0
        
    if move == 'psywave':
        x = random.randrange(50, 150, 10)
        dmg = (x / 100) * 15
        return round(dmg)

    if move == 'mimic':
        if not r.get_previous_enemy_atk(bottom_of_turn)[3]:
            print("But it failed!")
            return 0
        else:
            print(f"{mon.name} learned {r.get_previous_enemy_atk(bottom_of_turn)[1]}!")
            mon.move_dict['mimic'].clear()
            mon.moves.remove('mimic')
            mon.moves.append(r.get_previous_enemy_atk(bottom_of_turn)[1])
            # collect move info for attacking mons move dict
            url = 'https://pokeapi.co/api/v2/move/'+r.get_previous_enemy_atk(bottom_of_turn)[1]+'/'
            response = requests.get(url)
            response_json = json.loads(response.text)
            status = status_effect_check(r.get_previous_enemy_atk(bottom_of_turn)[1])

            move_type = response_json['type']['name']
            damage_class = response_json['damage_class']['name']
            move_accuracy = response_json['accuracy']
            move_power = 0 if response_json['power'] == None else response_json['power']
            effect_chance = response_json['effect_chance']
            mon.move_dict[r.get_previous_enemy_atk(bottom_of_turn)[1]] = {'type': move_type, 'power': move_power, 'accuracy': move_accuracy,
                            'damage_class': damage_class, 'status-effects': status, 'effect-chance': effect_chance}
            # do api call on the previous move and replace mimic with the new move in the mon's move dict
            return 0
        
    if move == 'conversion':
        arr = [0, 1, 2, 3]
        random.shuffle(arr)
        for i in arr:
            if mon.move_dict[list(mon.moves)[i]]['type'] not in mon.types:
                mon.types = [mon.move_dict[list(mon.moves)[i]]['type']]
                print(f"{mon.name} converted to {mon.types[0]} type!")
                return 0
        print("No valid types to convert to!")
        return 0
    
    print('it had no effect...')
    return 0

