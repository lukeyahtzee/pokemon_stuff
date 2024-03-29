import random
import time
import sys


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
        m_type = quicker_mon.move_dict[move].get('type')
        # move_types = set(m_type)

        if m_type in d_weaknesses:
            multiplier = 2
        elif m_type in d_resistences:
            multiplier = .5
        else:
            multiplier = 1

        return multiplier

    def damage_calc(self, attacking_mon, defending_mon, index):
        """Calculates the actual damage done by selected move during battle"""
        dmg = int(attacking_mon.move_dict[list(attacking_mon.moves)[index-1]]['power']
                  * self.damage_multiplier(defending_mon,
                                           attacking_mon,
                                           list(attacking_mon.moves)[index-1]))
        return dmg

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

    def battle_turn1(self, quicker_mon, slower_mon):
        print("Go", quicker_mon.name, "!")

        for i, x in enumerate(quicker_mon.moves):
            print(
                i+1, x, f"--- does {quicker_mon.move_dict[x]['power']} damage")

        print('\n')
        index = self.input_validation("Pick a move: ")

        print(quicker_mon.name, "used", list(quicker_mon.moves)[index-1])
        time.sleep(1)
        print(quicker_mon.name,
              "did",
              self.damage_calc(quicker_mon, slower_mon, index),
              "damage!")

        slower_mon.bars -= self.damage_calc(quicker_mon, slower_mon, index)
        slower_mon.health = ""

        # for i in range(int(slower_mon.bars)):
        #     slower_mon.health += "="
        slower_mon.health = '=' * round(slower_mon.bars / 3)

        print('\n')
        print(quicker_mon.name, "health:", quicker_mon.health)
        print(slower_mon.name, "health:", slower_mon.health, '\n')

    def battle_turn2(self, quicker_mon, slower_mon):
        print("Go", slower_mon.name, "!")
        for i, x in enumerate(slower_mon.moves):
            print(
                i+1, x, f"--- does {slower_mon.move_dict[x]['power']} damage")

        print('\n')
        index = self.input_validation("Pick a move: ")

        print(slower_mon.name, "used", list(slower_mon.moves)[index-1])
        time.sleep(1)
        print(slower_mon.name,
              "did",
              self.damage_calc(slower_mon, quicker_mon, index),
              "damage!")

        quicker_mon.bars -= self.damage_calc(slower_mon, quicker_mon, index)
        quicker_mon.health = ""

        # for i in range(int(quicker_mon.bars)):
        #     quicker_mon.health += "="
        quicker_mon.health = '=' * round(quicker_mon.bars / 3)

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
