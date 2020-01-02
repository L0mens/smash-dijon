from collections import Counter
def get_worst_enemie(matches_loose):
    list_win = []
    for match_l in matches_loose:
        list_win.append(match_l.winner.competitor.name)

    nb_win_max = 0
    worst_enemie = ""
    for player,nb_win in Counter(list_win).items():
        if nb_win_max < nb_win:
            worst_enemie = player
            nb_win_max = nb_win
    
    return worst_enemie