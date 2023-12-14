from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'my_environment_game'
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
    exrtaction = models.IntegerField(
        min=0, max=C.ENDOWMENT, label="از سهم 100 واحدی خود از این منبع طبیعی به چه میزان استخراج خواهید کرد؟(بین 0 تا 100)"
    )
    #e= models.IntegerField()



# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    exrtactions = [p.exrtaction for p in players] #ehtemelen tabe sigma ast ke jam zade
    #xxx = C.ENDOWMENT - contributions
    group.total_contribution = (C.PLAYERS_PER_GROUP*C.ENDOWMENT) - sum( exrtactions) # in jam mizanad va ghabli moghadame boode
    #group.total_exrtaction = sum(contributions)
    group.individual_share = round(
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = p.exrtaction + group.individual_share


# PAGES
#class test(Page):
   # form_model = 'player'
   # form_fields = ['e']

class Contribute(Page):
    form_model = 'player'
    form_fields = ['exrtaction']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        total_others = 400 - group.total_contribution - player.exrtaction
        average_others = round((400 - group.total_contribution - player.exrtaction) / 3)
        return dict(average_others=average_others, total_others=total_others)



page_sequence = [Contribute, ResultsWaitPage, Results]
