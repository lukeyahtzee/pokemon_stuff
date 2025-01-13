import random
import requests
import json
import time

def check_type(poke_type):
    types = ['fire', 'bug', 'dragon', 'electric', 'fighting', 'flying', 'ghost', 'grass', 'ground', 'ice',
             'normal', 'poison', 'psychic', 'rock', 'water']
    if poke_type in types:
        return True
    else:
        return False

def check_pokedex(pokedex, prompt):

    while True:
        try:
            try:
                val = str(input(prompt)).lower()
            except ValueError:
                print('Please input a name')
                continue

            if val not in pokedex:
                if val == 'list':
                    print(pokedex)
                
                if 'rand' in val:
                    if len(val.split()) == 1:
                        val = random.choice(pokedex)
                        print(f'\nRandom choice - {val}\n')
                        break
                    elif len(val.split()) == 2 and val.split()[0] == 'rand' and check_type(val.split()[1]):
                        poke_type = val.split()[1]
                        types = []
                        dex_copy = pokedex
                        while poke_type not in types:
                            time.sleep(0.1)
                            print("Generating.  ", end='\r')
                            time.sleep(0.1)
                            print("Generating.. ", end='\r')
                            val = random.choice(dex_copy)
                            dex_copy.pop(dex_copy.index(val))
                            url = 'https://pokeapi.co/api/v2/pokemon/' + val
                            response = requests.get(url)
                            if response.status_code != 200:
                                continue
                            response_json = json.loads(response.text)
                            for i in range(len(response_json['types'])):
                                types.append(response_json['types'][i]['type']['name'])
                            print("Generating...", end='\r')
                        print(f'\nRandom choice - {val}\n')
                        break
                    else:
                        print("Please enter 'rand' for a random pokemon, followed by an optional type parameter")
                        

                else:
                    print('Please choose one of the original 151 Pokemon. Spelling is important.',
                          '\nIf you need help, type: list.\n For a random choice, type: rand\n',
                          'For a random choice of a specific type, type: rand { type }')
                continue
            else:
                break
        except KeyboardInterrupt:
            break

    return val


with open('pokedex.txt', 'r') as fl:
    pokemons = fl.readlines()

    pokedex = []

    for n in pokemons:
        name = n.strip().lower()
        pokedex.append(name)
