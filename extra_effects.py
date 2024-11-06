extra_effects_moves = [
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
    'counter'
]

def unique_effects(move):
    if move in extra_effects_moves:
        return True
    else: return False

def apply_effects(mon, defending_mon, move):
    if move == 'reflect':
        print(f'{mon.name} put up a barrier! damage from physical attacks is weakened!')
        mon.reflect_barrier = 5
        return 0

    if move == 'fly':
        print(f'{mon.name} flew up high!')
        return 0
    
    if move == 'dig':
        print(f'{mon.name} dug into the ground!')
        return 0
    
    if move == 'rest':
        if mon.bars == mon.max_bars or mon.condition == 'slp':
            print('But it failed!')
            return 0
        else:
            mon.condition = 'slp'
            mon.bars = mon.max_bars
            print(f'{mon.name} fell asleep and regained health!')
        return 0
    
    if move == 'seismic-toss':
        # should do 50 damage strictly but would be too imbalanced
        return 17
    
    if move == 'dragon-rage':
        # should do 40 damage strictly but would be too imbalanced
        return 15
    
    if move == 'counter':
        # deal back twice the physical damage the user received this turn, or nothing if n/a
        # will be a little tricky to implement
        return 5
    
    if move == 'haze':
        # resets all pokemons stats to base
        mon.reset_stats()
        defending_mon.reset_stats()
        print("all stat modifications have been erased!")

    if move == 'mimic':
        # claims the targets most recently used move in this slot. will also be kind hard to implement
        # will need to maybe keep a record somehow of moves used throughout the battle or something
        return 0
    
    print('it had no effect...')
    return 0

