import random
import time
import sys
import math
from status import status_effect_calc


class Battle():

    def __init__(self, pokemon1, pokemon2) -> None:
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.delay_print('LOADING...')
        self.pokemon1.get_attrs()
        self.pokemon2.get_attrs()
        self.attacking_mon = None
        self.defending_mon = None
        self.bottom_of_turn = False
        self.first_turn_poke1 = True
        self.first_turn_poke2 = True

    def damage_multiplier(self, defending_mon, attacking_mon, move):
        d_resistences = defending_mon.resistances
        d_weaknesses = defending_mon.weaknesses
        d_ineffectives = defending_mon.ineffectives

        m_type = attacking_mon.move_dict[move].get('type')

        multiplier = 1

        # this method allows 4x or .25x type multiplier if move -
        # type is a weakness/resistance of both the defending mons type
        if m_type in d_weaknesses:
            multiplier *= (2 * d_weaknesses.count(m_type))
        if m_type in d_resistences:
            multiplier *= (0.5 * d_resistences.count(m_type))
        if m_type in d_ineffectives:
            multiplier *= 0

        stab = 1

        if m_type in attacking_mon.types:
            # same type attack bonus is 1.5
            stab = 1.5

        return multiplier, stab

    def damage_calc(self, attacking_mon, defending_mon, index):
        """Calculates the actual damage done by selected move during battle"""
        multiplier, stab = self.damage_multiplier(defending_mon,
                                           attacking_mon,
                                           list(attacking_mon.moves)[index-1])
        
        crit = 1
        atk_def_mult = 1

        if attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['damage_class'] == 'special':
            atk_def_mult = attacking_mon.special_attack / defending_mon.special_defense
        else:
            atk_def_mult = attacking_mon.attack / defending_mon.defense

        if random.randint(0, 255) < attacking_mon.crit_val and multiplier != 0:
            crit = 2

        dmg = self.damage_math(attacking_mon.level, crit, attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['power'],
                                 atk_def_mult, stab, multiplier)

        return dmg, multiplier, crit


    def damage_math(self, level, crit, power, atk_def_mult, stab, type_multiplier):
        dmg = (((2*level*crit) / 5 + 2)
            * power * atk_def_mult) / 50 + 2
        dmg *= (stab * type_multiplier)
        return int(dmg * random.randint(217, 255) / 255) # random multiplier

    def input_validation(self, prompt):
        """Validates user input for attack choice in battle"""
        while True:
            try:
                try:
                    val = int(input(prompt))
                except ValueError:
                    print('Please input a number')
                    continue

                if val not in [1, 2, 3, 4]:
                    print(
                        'Please input a number corresponding to the attack you wish to use')
                    continue
                else:
                    break
            except KeyboardInterrupt:
                break

        return val
    
    def check_miss(self, acc):
        """Random roll to determine if move misses or hits"""
        missed = False
        if random.randint(0, 100) > acc:
            missed = True
        return missed
    
    def check_cfn(self, name):
        print(f"{name} is confused!")
        if random.randint(0, 100) < 50:
            return True
        return False
    
    def test_mons_stats(self, mon_1, mon_2):
        print(f"{mon_1.name} stats:\n")
        print(f"attack: {mon_1.attack}")
        print(f"defense: {mon_1.defense}")
        print(f"special attack: {mon_1.special_attack}")
        print(f"special defense: {mon_1.special_defense}")
        print(f"speed: {mon_1.speed}")
        print(f"accuracy: {mon_1.accuracy}")
        print(f"evasion: {mon_1.evasion}")

        print(f"{mon_2.name} stats:\n")
        print(f"attack: {mon_2.attack}")
        print(f"defense: {mon_2.defense}")
        print(f"special attack: {mon_2.special_attack}")
        print(f"special defense: {mon_2.special_defense}")
        print(f"speed: {mon_2.speed}")
        print(f"accuracy: {mon_2.accuracy}")
        print(f"evasion: {mon_2.evasion}")

        

    def battle_turn(self, attacking_mon, defending_mon):

        print("Go", attacking_mon.name, "!")
        for i, x in enumerate(attacking_mon.moves):
            print(
                i+1, x, f"--- {attacking_mon.move_dict[x]['power']} power, {attacking_mon.move_dict[x]['type']}")
            
        if not self.bottom_of_turn and self.first_turn_poke1 or self.bottom_of_turn and self.first_turn_poke2:
            while attacking_mon.rerolls_left > 0:
                try:
                    try:
                        val = str(input("\nReroll moves? (1-y, 2-n) ")).lower()
                    except ValueError:
                        print('Please input a name')
                        continue

                    if val not in ['1', '2']:
                            print('Please choose 1 or 2')
                    elif val == '1':
                        attacking_mon.rerolls_left -= 1
                        print(f"Rerolling...({attacking_mon.rerolls_left} rerolls remaining!)\n")
                        attacking_mon.moves.clear()
                        attacking_mon.move_dict.clear()
                        attacking_mon.get_moves()
                        for i, x in enumerate(attacking_mon.moves):
                            attacking_mon.get_move_info(x)
                            print(
                                i+1, x, f"--- {attacking_mon.move_dict[x]['power']} power, {attacking_mon.move_dict[x]['type']}")
                    elif val == '2':
                        break
                except KeyboardInterrupt:
                    break
            if self.bottom_of_turn:
                self.first_turn_poke2 = False
            else:
                self.first_turn_poke1 = False

        print('\n')
        index = self.input_validation("Pick a move: ")

        print(attacking_mon.name, "used", list(attacking_mon.moves)[index-1])

        acc = attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['accuracy']
        miss = False
        if acc:
            miss = self.check_miss((attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['accuracy'] * 
                                   (attacking_mon.accuracy / 100)) - defending_mon.evasion)

        if attacking_mon.condition == 'slp' and attacking_mon.condition_turns == attacking_mon.condition_limit:
            print(f"{attacking_mon.name} woke up!")
            attacking_mon.condition_turns = 0
            attacking_mon.condition = None
        
        if attacking_mon.condition == 'cfn' and attacking_mon.condition_turns == attacking_mon.condition_limit:
            print(f"{attacking_mon.name} snapped out of confusion!")
            attacking_mon.condition_turns = 0
            attacking_mon.condition = None
        
        time.sleep(1)

        if attacking_mon.condition == 'plz' and random.randint(0, 100) < 25:
            print(f"{attacking_mon.name} is paralyzed! It can't move!")
            dmg = 0

        elif attacking_mon.condition == 'cfn' and self.check_cfn(attacking_mon.name):
            print(f"It hurt itself in confusion!")
            attacking_mon.bars -= (((2 * attacking_mon.level) / 5) + 2) * 40 * (attacking_mon.attack / attacking_mon.defense) / 50
            dmg = 0

        elif attacking_mon.condition == 'slp':
            print(f"{attacking_mon.name} is fast asleep.")
            dmg = 0
            attacking_mon.condition_turns += 1
        
        elif attacking_mon.condition == 'frz':
            if random.randint(0, 100) < 20:
                print(f"{attacking_mon.name} thawed out!")
                attacking_mon.condition = None
            else:
                print(f"{attacking_mon.name} is frozen solid!")
        
        elif miss:
            print(f"{defending_mon.name} avoided the attack!")
            dmg = 0

        elif attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['power'] == 0:
            status_effect_calc(attacking_mon, defending_mon, index)
            dmg = 0

        else:
            dmg, multiplier, crit = self.damage_calc(attacking_mon, defending_mon, index)

            print(attacking_mon.name,
                "did",
                dmg,
                "damage!")
            
            if crit == 2:
                print("A critical hit!")

            match multiplier:
                case 2 | 4:
                    print("It's super effective!")
                case 0.5 | 0.25:
                    print("It's not very effective...")
                case 0:
                    print(f"It doesn't effect the opposing {defending_mon.name}...")

        defending_mon.bars -= dmg
        defending_mon.health = ""

        # for i in range(int(defending_mon.bars)):
        #     defending_mon.health += "="
        attacking_mon.health = '=' * math.ceil((attacking_mon.bars / attacking_mon.max_bars) * 10)
        defending_mon.health = '=' * math.ceil((defending_mon.bars / defending_mon.max_bars) * 10)

        if self.bottom_of_turn:
            if defending_mon.condition == 'psn':
                defending_mon.bars -= (1/16)*defending_mon.max_bars
                print(f"\n{defending_mon.name} is hurt by poison!")
            if attacking_mon.condition == ('psn' or 'brn'):
                attacking_mon.bars -= (1/16)*attacking_mon.max_bars
                print(f"\n{attacking_mon.name} is hurt by poison!")

            if attacking_mon.condition:
                attacking_mon.condition_turns += 1
            if defending_mon.condition:
                defending_mon.condition_turns += 1

            # self.test_mons_stats(attacking_mon, defending_mon) # test function, prints pokemons stats each turn

        print('\n')
        print(self.pokemon1.name, "health:", self.pokemon1.health)
        print(self.pokemon2.name, "health:", self.pokemon2.health, '\n')

        self.bottom_of_turn = not self.bottom_of_turn

    def delay_print(self, s):
        for c in s:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)

    def commence_battle(self):

        print('\n')
        print("-----POKEMON BATTLE-----")
        print("Pokemon 1:", self.pokemon1.name)
        print("TYPE/", self.pokemon1.types)
        print("\nVS\n")
        print("Pokemon 2:", self.pokemon2.name)
        print("TYPE/", self.pokemon2.types, '\n')

    # evaluate speed of pokemon

        while self.pokemon1.speed > self.pokemon2.speed == True:
            self.attacking_mon = self.pokemon1
            self.defending_mon = self.pokemon2

        else:
            self.defending_mon = self.pokemon1
            self.attacking_mon = self.pokemon2

        while (self.pokemon1.bars > 0) and (self.pokemon2.bars > 0):

            self.battle_turn(self.attacking_mon, self.defending_mon)

            if self.defending_mon.bars <= 0:
                self.delay_print("\n..." + self.defending_mon.name + ' fainted.')
                break
            if self.attacking_mon.bars <= 0:
                self.delay_print("\n..." + self.attacking_mon.name + ' fainted.')
                break

        # mirroring the attack pattern of the quicker mon but for the slower mon
            temp_mon = self.attacking_mon
            self.attacking_mon = self.defending_mon
            self.defending_mon = temp_mon
