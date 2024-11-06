class Record():
    def __init__(self):
        self.first_moves = []
        self.second_moves = []

    def record_first_move(self, mon_name, attack, dmg, success):
        self.first_moves.append([mon_name, attack, dmg, success])

    def record_second_move(self, mon_name, attack, dmg, success):
        self.second_moves.append([mon_name, attack, dmg, success])

    def get_previous_self_atk(self, bottom_of_turn):
        if bottom_of_turn:
            if len(self.second_moves) == 0:
                return [None, None, None, None]
            return self.second_moves[len(self.second_moves) - 1]
        else: 
            if len(self.first_moves) == 0:
                return [None, None, None, None]
            return self.first_moves[len(self.first_moves) - 1]

    def get_previous_enemy_atk(self, bottom_of_turn):
        if bottom_of_turn:
            if len(self.first_moves) == 0:
                return [None, None, None, None]
            return self.first_moves[len(self.first_moves) - 1]
        else: 
            if len(self.second_moves) == 0:
                return [None, None, None, None]
            return self.second_moves[len(self.second_moves) - 1]
        
