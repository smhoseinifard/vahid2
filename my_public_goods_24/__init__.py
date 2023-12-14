from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'my_public_goods_24'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 10
    ENDOWMENT = 100
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    individual_share = models.IntegerField()
    #total_others = models.IntegerField()
    #average_others = models.IntegerField()

class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=C.ENDOWMENT, label="چقدر در کالای عمومی مشارکت میکنید؟(بین 0 تا 100)"
    )



# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = round(
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )

    #group.total_others = group.total_contribution - players.contribution
    #group.average_others = round(group.total_contribution - players.contribution) / 3
    #return dict(average_others=average_others, total_others=total_others)
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


def creating_session(subsession):
    # new_structure = [[1, 3, 5, 7], [2, 4, 6, 8], [9, 11, 13, 15], [10, 12, 14, 16], [17, 19, 21, 23], [18, 20, 22, 24],
    # [25, 27, 29, 31], [26, 28, 30, 32], [33, 35, 37, 39], [34, 36, 38, 40], [41, 43, 45, 47],
    # [42, 44, 46, 48]]
    new_structure = [[1, 3, 5, 7], [2, 4, 6, 8], [9, 11, 13, 15], [10, 12, 14, 16], [17, 19, 21, 23], [18, 20, 22, 24]]
    subsession.set_group_matrix(new_structure)
    # new_structure = [[1, 3, 5, 7], [2, 4, 6, 8],[9,11,13,15],[10,12,14,16],[17,19,21,23],[18,20,22,24],[25,27,29,31],[26,28,30,32],[33,35,37,39],[34,36,38,40],[41,43,45,47],[42,44,46,48],[49,51,53,55],[50,52,54,56]]
    print(subsession.get_group_matrix())
# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        total_others = group.total_contribution - player.contribution
        average_others = round((group.total_contribution - player.contribution)/3)
        return dict(average_others=average_others, total_others=total_others)




page_sequence = [Contribute, ResultsWaitPage, Results]
