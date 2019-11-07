import math

class Elo_Sytem():

    def __init__(self):
        self.k = 40
        self.k_winner = 40
        self.k_looser = 40

    def calc(self, elo_winner, elo_loser, type_match):
        elodif = self.elo_dif(elo_winner, elo_loser)
        self.update_k_factor(elo_winner, True)
        self.update_k_factor(elo_loser, False)
        prob_winner = self.probability(elodif)
        prob_loser = 1 - prob_winner
        mod_match = self.get_value_of_match(type_match)
        modif_winner = math.trunc(self.k_winner*(1-prob_winner)*mod_match)
        modif_loser = math.trunc(self.k_looser*(0-prob_loser)*mod_match)

        return (modif_winner, modif_loser)

    #TODO A réfléchir à réduire le K pour les grands elos ! 1900 ? 
    def update_k_factor(self,elo_player, is_winner):
        if elo_player.elo > 1900 and elo_player.elo < 2200 :
            if is_winner:
                self.k_winner = 30
            else: 
                self.k_looser = 30

    def probability(self, diff):
        return 1 / (1 + ( 10**(diff/-400)))

    def elo_dif(self, elo_winner, elo_loser,):
        elodif = elo_winner.elo - elo_loser.elo
        if elodif > 400:
            elodif = 400
        elif elodif < -400:
            elodif = -400
        return elodif
    
    def get_value_of_match(self, match_type):
        value = 1

        if 'Winners' in match_type:
            value = 1
        else:
            value = 0.85

        return value

    def get_metal_rank(self, nb_player, rank_player):
        percent = (rank_player/nb_player)*100
        if percent < 5:
            return 'Diamond'
        elif percent < 20:
            return 'Platine'
        elif percent < 45:
            return 'Gold'
        elif percent < 75:
            return 'Silver'
        else:
            return 'Bronze'