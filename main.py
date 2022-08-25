
from pokemon import Pokemon
from battle import Battle
from pokedex import check_pokedex, pokedex


choice1 = check_pokedex(pokedex, 'Please pick a Pokemon: ')
choice2 = check_pokedex(pokedex, 'Please select a second Pokemon: ')


pokemon1 = Pokemon(choice1)
pokemon2 = Pokemon(choice2)

print('\n')

battle = Battle(pokemon1, pokemon2)

battle.commence_battle()
