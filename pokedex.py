
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

                print(
                    'Please choose one of the original 151 Pokemon. Spelling is important.')
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
