from collections import Counter
def get_worst_enemie(matches_loose):
    list_win = []
    for match_l in matches_loose:
        list_win.append(match_l.winner.competitor.name)

    nb_win_max = 0
    worst_enemie = []
    for player,nb_win in Counter(list_win).items():
        if nb_win_max < nb_win:
            worst_enemie = [player]
            nb_win_max = nb_win
        elif nb_win_max == nb_win:
            worst_enemie.append(player)
    
    return ", ".join(worst_enemie)


class OnePlStatistics():

    def __init__(self, list_matches):
        self.matches = list_matches