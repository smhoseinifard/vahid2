from otree.api import *




doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class C(BaseConstants):
    NAME_IN_URL = 'my_trust_16'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    INSTRUCTIONS_TEMPLATE = 'trust/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = 100
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.IntegerField(
        min=0,
        max=C.ENDOWMENT,
        doc="""Amount sent by P1""",
        label="از این 100 امتیاز چه میزان را به فرد (ب) میدهید؟",
    )
    sent_back_amount = models.IntegerField(doc="""Amount sent back by P2""", min=0)


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.sent_amount * C.MULTIPLIER


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount


def creating_session(subsession):
    if subsession.round_number == 1:

        new_structure = [[1, 2], [3, 4], [5, 6], [7, 8],[9,10],[11,12],[13,14],[15,16]]
        # new_structure = [[1, 2], [3, 4], [5, 6], [7, 8],[9,10],[11,12],[13,14],[15,16],[17,18],[19,20],[21,22],[23,24],[25,26],[27,28],[29,30],[31,32],[33,34],[35,36],[37,38],[39,40],[41,42],[43,44],[45,46],[47,48],[49,50],[51,52]]
        subsession.set_group_matrix(new_structure)
        print(subsession.get_group_matrix())
    else:
        new2_structure = [[2, 3], [4, 1], [6, 7], [8, 5],[10,11],[12,9],[14,15],[16,13]]

        # new2_structure = [[2,3], [4,1],[6,7],[8,5],[10,11],[12,9],[14,15],[16,13],[18,19],[20,17],[22,23],[24,21],[26,27],[28,25],[30,31],[32,29],[34,35],[36,33],[38,39],[40,37],[42,43],[44,41],[46,47],[48,45],[50,51],[52,49]]
        subsession.set_group_matrix(new2_structure)

        print(subsession.get_group_matrix())
# PAGES
class Introduction(Page):
    pass


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
