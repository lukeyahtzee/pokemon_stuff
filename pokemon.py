import requests
import json
import numpy as np
import pandas as pd
import concurrent.futures
import random


class Pokemon():
    """
    An individual Pokemon

    Args:
        name (string): the name of your pokemon. spelling is important, capitalization is not
        speed (int): movement speed of the pokemon
    """

    def __init__(self, name: str):
        self.name = name
        self.types = []
        self.moves = []
        self.health = '=========='
        self.bars = 30
        self.pokemon_url = 'https://pokeapi.co/api/v2/pokemon/' + \
            str.lower(self.name).strip()+'/'
        self.weaknesses = []
        self.resistances = []
        self.ineffectives = []
        self.move_dict = {}
        self.get_base_stats()
        self.hp = int(self.base_stats['hp'].iloc[0])
        self.attack = int(self.base_stats['attack'].iloc[0])
        self.defense = int(self.base_stats['defense'].iloc[0])
        self.special_attack = int(self.base_stats['special-attack'].iloc[0])
        self.special_defense = int(self.base_stats['special-defense'].iloc[0])
        self.speed = int(self.base_stats['speed'].iloc[0])

    def api_call(self, url):
        """Makes api call to the Pokemon type endpoint and returns json text"""
        response = requests.get(url)
        response_json = json.loads(response.text)
        return response_json

    def get_moves(self):
        """Creates a list of moves for battle. The moves are random
        assignments from all available moves in the api"""
        response_json = self.api_call(self.pokemon_url)
        num_of_moves = len(response_json['moves'])
        # randomly selects 8 out of all moves available
        # 8 because some moves have 0 attack which is lame
        # and I want to filter down to 4 useable moves
        if num_of_moves > 8:
            move_index = random.sample(range(num_of_moves), 8)
        else:
            move_index = range(num_of_moves)

        for i in move_index:
            self.moves.append(
                response_json['moves'][i]['move']['name'])

    def poke_types(self):
        """Updates types list for the Pokemon's type(s)"""
        self.types.clear()  # empty the list so that duplicates are not created if ran multiple times
        response_json = self.api_call(self.pokemon_url)
        for i in range(len(response_json['types'])):
            type_resp = response_json['types'][i]['type']['name']
            self.types.append(type_resp)

    def factors(self):
        """Finds the weaknesses and resistance types for this Pokemon"""
        self.poke_types()
        for i in self.types:
            type_url = 'https://pokeapi.co/api/v2/type/'+i+'/'
            type_response_json = self.api_call(type_url)

            for j in range(len(type_response_json['damage_relations']['double_damage_from'])):
                self.weaknesses.append(
                    type_response_json['damage_relations']['double_damage_from'][j]['name'])

            for k in range(len(type_response_json['damage_relations']['half_damage_from'])):
                self.resistances.append(
                    type_response_json['damage_relations']['half_damage_from'][k]['name'])
                
            for l in range(len(type_response_json['damage_relations']['no_damage_from'])):
                self.ineffectives.append(
                    type_response_json['damage_relations']['no_damage_from'][l]['name'])

            self.weaknesses = np.unique(np.array(self.weaknesses)).tolist()
            self.resistances = np.unique(np.array(self.resistances)).tolist()
            self.ineffectives = np.unique(np.array(self.ineffectives)).tolist()

    def delete_no_damage(self):
        """
        Removes any move with a 0 damage value from the move_dict and moves
        """
        del_list = []
        for m in self.move_dict:
            if self.move_dict[m]['power'] == 0:
                del_list.append(m)
        for n in del_list:
            if len(self.move_dict) > 1:
                del self.move_dict[n]

        # remove excess moves from move_dict
        for k, v in enumerate(self.move_dict.copy()):
            if k > 3:
                del self.move_dict[v]

        # remove the extra moves from moves
        self.moves = self.move_dict.keys()

    def move_info(self):
        """Finds type and power attributes for each of the pokemons moves.  The results
        fill in the move_dict attribute. """
        for moves in self.moves:
            move = moves.replace(' ', '-').lower()
            url = 'https://pokeapi.co/api/v2/move/'+move+'/'
            response_json = self.api_call(url)

            move_type = response_json['type']['name']
            damage_class = response_json['damage_class']['name']
            move_accuracy = response_json['accuracy']
            move_power = 0 if response_json['power'] == None else response_json['power'] // 10
            self.move_dict[move] = {'type': move_type, 'power': move_power, 'accuracy': move_accuracy,
                                    'damage_class': damage_class}

        self.delete_no_damage()

    def get_move_info(self, move):
        """Same as move_info but without the loop. To be used with the concurrent.futures module"""
        move = move.replace(' ', '-').lower()
        url = 'https://pokeapi.co/api/v2/move/'+move+'/'
        response_json = self.api_call(url)

        move_type = response_json['type']['name']
        damage_class = response_json['damage_class']['name']
        move_accuracy = response_json['accuracy']
        move_power = 0 if response_json['power'] == None else response_json['power'] // 10
        self.move_dict[move] = {'type': move_type, 'power': move_power, 'accuracy': move_accuracy,
                        'damage_class': damage_class}

    def get_attrs(self):
        """Retrieves all the pokemons attributes to prepare for battle"""
        self.get_moves()
        self.poke_types()
        self.factors()
        # self.move_info
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.get_move_info, self.moves)

        self.delete_no_damage()

    def get_base_stats(self):

        data = self.api_call(self.pokemon_url)

        stats_num = [x['base_stat'] for x in data['stats']]
        stats = [x['stat']['name'] for x in data['stats']]

        name = data['forms'][0]['name']
        # target = stats.index('special-attack')

        self.base_stats = pd.DataFrame(
            dict(zip(stats, stats_num)), index=[name])
