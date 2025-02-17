class Offer:
    def __init__(self, link1, link2, coef1, coef2,
                 team1="", team2="", tournament="",
                 match_time="", bet_amount1="",
                 bet_amount2="", profit="", url=""):
        self.link1 = link1
        self.link2 = link2
        self.coef1 = coef1
        self.coef2 = coef2
        self.team1 = team1
        self.team2 = team2
        self.tournament = tournament
        self.match_time = match_time
        self.bet_amount1 = bet_amount1
        self.bet_amount2 = bet_amount2
        self.profit = profit
        self.url = url

    def __str__(self):
        if self.coef1 != '0.0':
            return (
                    '[' + self.team1
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + '\n' +
                    'vs\n' +
                    self.team2
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ']' +
                    '(' + self.url + ')' +
                    '\n\n' +
                    self.tournament
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`") + '\n' +
                    self.match_time + '\n\n' +
                    self.coef1 + '\n' +
                    self.coef2 + '\n' +
                    '[' + self.team1
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ' bet link' + ']' + '(' + self.link1 + ')' + '\n' +
                    '[' + self.team2
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ' bet link' + ']' + '(' + self.link2 + ')' + '\n' +
                    self.team1
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ' bet amount :  ' + self.bet_amount1 + '\n' +
                    self.team2
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ' bet amount :  ' + self.bet_amount2 + '\n\n' +
                    'Profit :  ' + '**' + self.profit + '**'
            )
        else:
            return (
                    '[' + self.team1
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + '\n' +
                    'vs\n' +
                    self.team2
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`")
                    + ']' +
                    '(' + self.url + ')' +
                    '\n\n' +
                    self.tournament
                    .replace("_", "\\_")
                    .replace("*", "\\*")
                    .replace("[", "\\[")
                    .replace("`", "\\`") + '\n' +
                    self.match_time + '\n\n' +
                    'No offers for this match!'
            )


def count_profit(coef1, coef2, bet_amount):
    return round(min(coef1 * bet_amount[0], coef2 * bet_amount[1]) - 100, 2)


def count_bet_amount(coef1, coef2):
    if coef1 == 0.0:
        return 0.0, 0.0
    bet1 = coef2 * 100 / (coef1 + coef2)
    bet2 = 100 - bet1
    return round(bet1, 2), round(bet2, 2)


def add_offer_info_to_container(team1, team2, tournament, match_time, offers_list, url, offers_container):
    best_offer = get_best_offer(offers_list)
    bet_amount = count_bet_amount(best_offer.coef1, best_offer.coef2)
    profit = count_profit(best_offer.coef1, best_offer.coef2, bet_amount)

    offers_container.append(
        Offer(best_offer.link1, best_offer.link2, str(best_offer.coef1), str(best_offer.coef2),
              team1, team2, tournament, match_time.strftime('%Y-%m-%d - %A %H:%M'),
              str(bet_amount[0]) + '%', str(bet_amount[1]) + '%',
              str(profit) + '%', url))


def get_best_offer(offers):
    max_first_coef = 0
    max_second_coef = 0
    best_offer_first = None
    best_offer_second = None

    if offers:
        for o in offers:
            if float(o.coef1) > max_first_coef:
                max_first_coef = o.coef1
                best_offer_first = o
            if float(o.coef2) > max_second_coef:
                max_second_coef = o.coef2
                best_offer_second = o

        return Offer(best_offer_first.link1, best_offer_second.link1, best_offer_first.coef1, best_offer_second.coef2)
    else:
        return Offer('', '', 0.0, 0.0)
