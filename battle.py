import random
import time
import sys
import math


class Battle():

    def __init__(self, pokemon1, pokemon2) -> None:
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.delay_print('LOADING...')
        self.pokemon1.get_attrs()
        self.pokemon2.get_attrs()

    def damage_multiplier(self, defending_mon, quicker_mon, move):
        d_resistences = defending_mon.resistances
        d_weaknesses = defending_mon.weaknesses
        d_ineffectives = defending_mon.ineffectives

        m_type = quicker_mon.move_dict[move].get('type')

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

        if m_type in quicker_mon.types:
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
        
        dmg = (((2*attacking_mon.level*crit) / 5 + 2)
                * attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['power'] * atk_def_mult) / 50 + 2
        dmg *= (stab * multiplier)
        dmg = int(dmg * random.randint(217, 255) / 255) # random multiplier

        return dmg, multiplier, crit

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


    def battle_turn1(self, quicker_mon, slower_mon):
        print("Go", quicker_mon.name, "!")
        for i, x in enumerate(quicker_mon.moves):
            print(
                i+1, x, f"--- {quicker_mon.move_dict[x]['power']} power, {quicker_mon.move_dict[x]['type']}")

        print('\n')
        index = self.input_validation("Pick a move: ")

        print(quicker_mon.name, "used", list(quicker_mon.moves)[index-1])

        acc = quicker_mon.move_dict[list(quicker_mon.moves)[index-1]]['accuracy']
        miss = False
        if acc:
            miss = self.check_miss(quicker_mon.move_dict[list(quicker_mon.moves)[index-1]]['accuracy'])

        time.sleep(1)
        if miss:
            print(f"{slower_mon.name} avoided the attack!")
            dmg = 0
        
        else:
            dmg, multiplier, crit = self.damage_calc(quicker_mon, slower_mon, index)

            print(quicker_mon.name,
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
                    print(f"It doesn't effect the opposing {slower_mon.name}...")

        slower_mon.bars -= dmg
        slower_mon.health = ""

        # for i in range(int(slower_mon.bars)):
        #     slower_mon.health += "="
        slower_mon.health = '=' * math.ceil((slower_mon.bars / slower_mon.max_bars) * 10)

        print('\n')
        print(quicker_mon.name, "health:", quicker_mon.health)
        print(slower_mon.name, "health:", slower_mon.health, '\n')

    def battle_turn2(self, quicker_mon, slower_mon):
        print("Go", slower_mon.name, "!")
        for i, x in enumerate(slower_mon.moves):
            print(
                i+1, x, f"--- {slower_mon.move_dict[x]['power']} power, {slower_mon.move_dict[x]['type']}")

        print('\n')
        index = self.input_validation("Pick a move: ")

        print(slower_mon.name, "used", list(slower_mon.moves)[index-1])

        acc = slower_mon.move_dict[list(slower_mon.moves)[index-1]]['accuracy']
        miss = False
        if acc:
            miss = self.check_miss(slower_mon.move_dict[list(slower_mon.moves)[index-1]]['accuracy'])

        time.sleep(1)
        if miss:
            print(f"{quicker_mon.name} avoided the attack!")
            dmg = 0
        
        else:
            dmg, multiplier, crit = self.damage_calc(slower_mon, quicker_mon, index)
    
            print(slower_mon.name,
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
                    print(f"It doesn't effect the opposing {quicker_mon.name}...")

        quicker_mon.bars -= dmg
        quicker_mon.health = ""

        # for i in range(int(quicker_mon.bars)):
        #     quicker_mon.health += "="
        quicker_mon.health = '=' * math.ceil((quicker_mon.bars / quicker_mon.max_bars) * 10)

        print('\n')
        print(slower_mon.name, "health:", slower_mon.health)
        print(quicker_mon.name, "health:", quicker_mon.health, '\n')

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
            quicker_mon = self.pokemon1
            slower_mon = self.pokemon2

        else:
            slower_mon = self.pokemon1
            quicker_mon = self.pokemon2

        while (quicker_mon.bars > 0) and (slower_mon.bars > 0):

            self.battle_turn1(quicker_mon, slower_mon)

            if slower_mon.bars <= 0:
                self.delay_print("\n..." + slower_mon.name + ' fainted.')
                break

        # mirroring the attack pattern of the quicker mon but for the slower mon

            self.battle_turn2(quicker_mon, slower_mon)

            if quicker_mon.bars <= 0:
                self.delay_print("\n..." + quicker_mon.name + ' fainted.')
                break
