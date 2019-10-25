import requests
import json
from math import ceil


class Smashgg():

    def __init__(self, api_token):
        self.token = api_token
        format_sort_64 = ['WR1','LR1','WR2','LR2','LR3','WR3','LR4','LR5','WQ','LR6','LR7','WS','LQ', 'LS', 'WF', 'LF', 'GF', 'GFR']
        format_sort_48 = ['WR1','WR2','LR1','LR2','WR3','LR3','LR4','WQ','LR5','LR6','WS','LQ', 'LS', 'WF', 'LF', 'GF', 'GFR']
        format_sort_32 = ['WR1','LR1','WR2','LR2','LR3','WQ','LR4','LR5','WS','LQ', 'LS', 'WF', 'LF', 'GF', 'GFR']
        format_sort_24 = ['WR1','WR2','LR1','LR2','WQ','LR3','LR4','WS','LQ', 'LS', 'WF', 'LF', 'GF', 'GFR'] # A revoir
        format_sort_16 = ['WR1','LR1','WQ','LR2','LR3','WS','LQ', 'LS', 'WF', 'LF', 'GF', 'GFR']

        self.format_sort = {
            "16" : format_sort_16,
            "24" : format_sort_24,
            "32" : format_sort_32,
            "48" : format_sort_48,
            "64" : format_sort_64
        }

    def run_query(self, query): # A simple function to use requests.post to make the API call. Note the json= section.
        headers = {"Authorization": f"Bearer {self.token}"}
        request = requests.post('https://api.smash.gg/gql/alpha', json=query, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


    def get_number_entrant(self, tn_slug, event_id):
        query = {
            "query" : """query TournamentQuery($slug: String, $eventIds:[ID]) {
                tournament(slug: $slug){
                    id
                    name
                    participants(query:{
                        filter:{
                        eventIds:$eventIds
                        }}){
                        pageInfo{
                            total
                        }
                    }
                }
            }""",
            "variables" : {"slug": f"{tn_slug}", "eventIds":event_id}
        }
        data = self.run_query(query)
        return data['data']['tournament']['participants']['pageInfo']['total']

    def get_tournament(self, tournament_slug, event_name, speed_crawl = 100):
        event_id = self.get_event_id_from_tournament(tournament_slug,event_name)
        nb_entrant = self.get_number_entrant(tournament_slug,event_id)
        tourna = Tournament(tournament_slug,event_name,event_id, nb_entrant, entrants=[],sets=[])
        print(tourna.entrants)
        phases_group = self.get_phases_group_from_event(event_id,1,speed_crawl)
        sets = self.phases_group_to_smashsets(phases_group, tourna)
        tourna.sets = sets
        return tourna

    def get_event_id_from_tournament(self, tournament, event):
        query = {
            "query" : """query TournamentQuery($slug: String) {
                tournament(slug: $slug){
                    id
                    name
                    events {
                        id
                        name
                    }
                }
            }""",
            "variables" : {"slug": f"{tournament}"}
        }
        data = self.run_query(query)
        events = data['data']['tournament']['events']
        id = -1
        for e in events :
            if e['name'] == event :
                id = e['id']
        return id
    
    def get_phases_group_from_event(self, event_id, page, per_page):
        query = {
            "query" : """query EventSets($eventId: ID!, $page:Int!, $perPage:Int!){
                        event(id:$eventId){
                            id
                            name
                            phaseGroups{
                                id
                                bracketType
                                standings(query:{}){
                                    pageInfo{
                                        total
                                    }
                                }
                                sets(page: $page
                                    perPage: $perPage
                                    sortType: STANDARD){
                                    pageInfo{
                                        total
                                        totalPages
                                        page
                                        perPage
                                    }
                                    nodes{
                                        id
                                        displayScore
                                        fullRoundText
                                        winnerId
                                        slots{
                                            entrant{
                                                id
                                                name
                                                participants{
                                                    prefix
                                                    gamerTag
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        }""",
            "variables" : {
                "eventId": event_id,
                "page": page,
                "perPage": per_page
                }
        }
        failed = True
        while per_page > 1 and failed:
            try:
                print(f"Try {query['variables']['perPage']}")
                data = self.run_query(query)
                failed = False
            except Exception:
                failed = True
                per_page = ceil(per_page / 2) 
                query['variables']['perPage'] = per_page
                print(f"Error PerPage => {query['variables']['perPage']}")
        
        max_page = 0
        for pg in data['data']['event']['phaseGroups'] :
            if pg['sets']['pageInfo']['totalPages'] > max_page:
                max_page = pg['sets']['pageInfo']['totalPages']
        if page >= max_page:
            return data['data']['event']['phaseGroups']
        else:
            pgplus = self.get_phases_group_from_event(event_id,page+1,per_page)
            total_pg = data['data']['event']['phaseGroups']
            
            for index,pg in enumerate(pgplus):
                if pg['sets']['nodes']:
                    total_pg[index]['sets']['nodes'] = total_pg[index]['sets']['nodes'] + pg['sets']['nodes']

            return total_pg

    def phases_group_to_smashsets(self, phases, tournament, sort=True):
        data = []
        for pg in phases : 
            stand = pg['standings']
            if stand:
                nb_pl = stand['pageInfo']['total']
            else:
                break
            item = {
                "id" : pg['id'],
                "nb_player" : nb_pl,
                "sets" : [],
                "sorted_sets" : []
            }
            for sets in pg['sets']['nodes']:
                item['sets'].append(Smashset(sets, tournament))
            if sort:
                item['sorted_sets'] = self.__sort_sets(item['sets'], item['nb_player'])
            data.append(item)
        return data

    def __sort_sets(self, list_sets, nb_entrant):
        """[summary]
        
        Args:
            list_sets ([type]): [description]
            nb_entrant ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        sets = list_sets
        sets_sort = []
        count = 0
        for type_set in self.__find_sort_format(nb_entrant):
            for match in sets:
                if match.round == type_set:
                    count = count +1
                    sets_sort.append(match)
            count = 0
        return sets_sort
    
    def __find_sort_format(self, nb_entrant):
        """[summary]
        
        Args:
            nb_entrant ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        if nb_entrant <= 16 :
            return self.format_sort['16']
        elif nb_entrant > 16 and nb_entrant <= 24 :
            return self.format_sort['24']
        elif nb_entrant > 24 and nb_entrant <= 32 :
            return self.format_sort['32']
        elif nb_entrant > 32 and nb_entrant <= 48 :
            return self.format_sort['48']
        elif nb_entrant > 48 and nb_entrant <= 64 :
            return self.format_sort['64']
        else:
            return self.format_sort['64']

class Entrant():

    def __init__(self, infos):
        if infos['participants'][0]['gamerTag'] == 'Lomens' :
            print(infos)
        self.name = infos['participants'][0]['gamerTag']
        self.team = infos['participants'][0]['prefix']
        self.id = infos['id']
    
    def __str__(self):
        if self.team:
            return f"{self.team} | {self.name}"
        else:
            return f"{self.name}"

class Smashset():
    """ 
    Representation of a set 
    id (int) : Set ID 
    fullRoundText (str) : Complet round text 
    round (str) = Accronym round text
    winner (entrant) : Winner of set
    looser (entrant) : Looser of set
    score (tuple) = Score (winner,looser)
    """

    def __init__(self, dictdata, tournament):
        
        self.id = dictdata['id']
        self.fullRoundText = dictdata['fullRoundText']
        self.round = self.roundText(dictdata['fullRoundText'])
        self.winner , self.looser = self.winner_and_looser(dictdata['slots'], dictdata['winnerId'], tournament)
        self.score = self.find_score(dictdata['displayScore'])

    def __str__(self):
        return f"{self.fullRoundText} / {self.round} >> {self.winner} {self.score} {self.looser} "

    def roundText(self, fullRoundText):
        r = ""
        for word in fullRoundText.split():
            r = r + word[0]
        return r
    
    def winner_and_looser(self, entrants, idwinner, tournament):
        if entrants[0]['entrant']['id'] == idwinner:
            winner = self.should_add(entrants[0]['entrant'], tournament)
            looser = self.should_add(entrants[1]['entrant'], tournament)
        else:
            looser = self.should_add(entrants[0]['entrant'], tournament)
            winner = self.should_add(entrants[1]['entrant'], tournament)

        return (winner,looser)

    def find_score(self, str_score):
        if str_score == 'DQ':
            return ('DQ', 'DQ')
        str_sc = str_score.split(' - ')
        score_un = str_sc[0][-1:]
        score_deux = str_sc[1][-1:]
        tuple_scr = tuple(sorted((int(score_un), int(score_deux)), reverse=True))
        return tuple_scr

    
    def should_add(self, entrant_infos, tournament):
        exist = [x for x in tournament.entrants if x.name == entrant_infos['participants'][0]['gamerTag']]
        if not exist:
            exist = Entrant(entrant_infos)
            tournament.entrants.append(exist)
        else:
            exist = exist[0]
        return exist

class Tournament():

    def __init__(self, slug, event_name, event_id, nb_entrant, entrants= [], sets=[]):
        self.slug = slug
        self.event_name = event_name
        self.event_id = event_id
        self.nb_entrant = nb_entrant
        self.entrants = entrants
        self.sets = sets


