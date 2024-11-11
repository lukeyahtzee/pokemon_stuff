import time

def print_health(iteration, total, old_bars, name, condition):
    """Dynamically decrease health bar from previous level to current level."""
    current_bars = (old_bars - iteration) * '=' # current ='s
    missing_bars = (total - (old_bars - iteration)) * '-' # current -'s

    if condition:
        print(f'{name} hp: |{current_bars}{missing_bars}| {condition}', end='\r')
    else:
        print(f'{name} hp: |{current_bars}{missing_bars}|', end='\r')

    time.sleep(0.5)
    
    return

def finish_print(iteration, old_bars, name, condition):
    current_bars = (old_bars - iteration) * '=' # current ='s
    missing_bars = (10 - (old_bars - iteration)) * '-' # current -'s
    if condition:
        print(f'{name} hp: |{current_bars}{missing_bars}| {condition}')
    else:
        print(f'{name} hp: |{current_bars}{missing_bars}|')


if __name__ == "__main__":
    print_health(0, 10, 9, 6)
    for i in range(1, (9 - 6 + 1)):
        print_health(i, 10, 9, 6) 