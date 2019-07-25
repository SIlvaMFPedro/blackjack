# encoding: utf8
import card
import random

import numpy as np
from player import Player
from ModelBuilder import Model
from multiprocessing import Lock
import math

file_write_lock = Lock()


class StudentPlayer(Player):
    def __repr__(self):
        return "StudentPlayer"

    def __init__(self, name="Meu nome", money=0, games=0):
        super(StudentPlayer, self).__init__(name, money)
        self.rules = None
        self.plays = []
        self.plays_history = []
        self.model = Model()
        self.model.load()
        self.last_game_win = None
        self.loss_value = 0
        self.pocket = money
        self.initial_pocket = money
        self.number_games = games
        self.wins = 0
        self.losses = 0
        self.martingale_count = 0
        self.paroli_count = 0
        self.prog_count = 0
        self.min_bet_count = 0
        self.max_bet_count = 0
        self.total_rounds = 0
        self.dealer_numCards = 0
        self.dealer_didntHit = 0
        self.round_number = 0
        self.double_down = 0
        self.amount_to_bet = 1

    def play(self, dealer, players):
        val_dealer = card.value(dealer.hand)
        numCards_dealer = len(dealer.hand)
        if self.dealer_numCards == numCards_dealer:
            self.dealer_didntHit = 1
        else:
            self.dealer_didntHit = 0

        self.dealer_numCards = numCards_dealer
        ases_dealer = len([x for x in dealer.hand if x.rank == 1])
        for player_state in players:
            if player_state.player == self:
                self.round_number += 1
                val_player = card.value(player_state.hand)
                numCards_player = len(player_state.hand)
                ases_player = len([x for x in player_state.hand if x.rank == 1])

                #if self.round_number ==  1:	#double-down only on the 1st turn
                #    if self.pocket >= self.amount_to_bet*2:
                #        self.double_down = 1
                #    else:
                #        self.double_down = 0

                if val_player == 11:
                    if self.round_number == 1:  #double-down only on the 1st turn
                        self.double_down = 1

                # calcular probabilidades com o modelo
                #ver os maximos. se for para perder, usar surrender
                prob_stand = self.model.get_classifier().predict_proba(
                    np.array([[val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit , ases_dealer, 0]]))  # stand
                prob_hit = self.model.get_classifier().predict_proba(
                    np.array([[val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit , ases_dealer, 1]]))  # hit


                class_hit = np.argmax(prob_hit)
                class_stand = np.argmax(prob_stand)
                class_hit_prob = np.max(prob_hit)
                class_stand_prob = np.max(prob_stand)

                if class_hit_prob < 0.1 and class_stand_prob < 0.1:
                    play = Play(val_player, numCards_dealer, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                    return "u"  #SURRENDER

                #if(self.want_to_play(rules = self.rules) == False):
                #    play = Play(val_player, numCards_dealer, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                #    return "u"  # SURRENDER

                if class_hit == class_stand:

                    if class_hit == 1:
                        if class_hit_prob > class_stand_prob:
                            if self.double_down != 0:
                                play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                                self.plays.append(play)
                                return "d"  #DOUBLE_DOWN
                            else:
                                self.double_down = 0
                                play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                                self.plays.append(play)
                                return "h"  #HIT
                        else:
                            self.double_down = 0
                            play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 0)
                            self.plays.append(play)
                            return "s"  #STAND
                    else:
                        if class_hit_prob < class_stand_prob:
                            if self.double_down != 0:
                                play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_player, 1)
                                self.plays.append(play)
                                return "d"  #DOUBLE_DOWN
                            else:
                                self.double_down = 0
                                play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                                self.plays.append(play)
                                return "h"  #HIT
                        else:
                            self.double_down = 0
                            play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 0)
                            self.plays.append(play)
                            return "s"  #STAND


                else:
                    self.double_down = 0
                    if class_hit == 1:
                        play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 1)
                        self.plays.append(play)
                        return "h"  #HIT
                    else:
                        play = Play(val_player, numCards_player, ases_player, val_dealer, numCards_dealer, self.dealer_didntHit, ases_dealer, 0)
                        self.plays.append(play)
                        return "s"  #STAND



        return "s"  #STAND

    def bet(self, dealer, players):
        if self.number_games > 1000:
            if self.rules.max_bet < 100:
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            #elif self.martingale_count != 0:
            #     # print("MARTINGALE\n")
            #     amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.max_bet_count != 0 and (2*self.initial_pocket < self.pocket <= self.rules.max_bet):
                #print("MAX_BET\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_max_bet(dealer=dealer, players=players)

            elif self.martingale_count != 0 and ((self.initial_pocket + 0.80*self.initial_pocket) < self.pocket <= 2*self.initial_pocket):
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.paroli_count != 0 and ((self.initial_pocket + 0.60*self.initial_pocket) < self.pocket <= (self.initial_pocket + 0.80*self.initial_pocket)):
                #print("PAROLI\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_paroli(dealer=dealer, players=players)
            elif self.prog_count != 0 and ((self.initial_pocket + 0.40*self.initial_pocket) < self.pocket <= (self.initial_pocket + 0.60*self.initial_pocket)):
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            elif self.martingale_count != 0 and (0.80*self.initial_pocket < self.pocket <= (self.initial_pocket + 0.40*self.initial_pocket)):
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.paroli_count != 0 and (0.60*self.initial_pocket < self.pocket <= 0.80*self.initial_pocket):
                #print("PAROLI\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_paroli(dealer=dealer, players=players)
            elif self.prog_count != 0 and (0.40*self.initial_pocket < self.pocket <= 0.60*self.initial_pocket):
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            elif self.min_bet_count != 0 and (0 < self.pocket <= 0.40*self.initial_pocket):
                #print("MIN_BET\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_min_bet(dealer=dealer, players=players)
            else:
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            return amount_to_bet
        else:
            if self.rules.max_bet < 100:
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            #elif self.martingale_count != 0:
            #     # print("MARTINGALE\n")
            #     amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.martingale_count != 0 and ((self.initial_pocket + 0.80*self.initial_pocket) < self.pocket <= 2*self.initial_pocket):
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.paroli_count != 0 and ((self.initial_pocket + 0.60*self.initial_pocket) < self.pocket <= (self.initial_pocket + 0.80*self.initial_pocket)):
                #print("PAROLI\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_paroli(dealer=dealer, players=players)
            elif self.prog_count != 0 and ((self.initial_pocket + 0.40*self.initial_pocket) < self.pocket <= (self.initial_pocket + 0.60*self.initial_pocket)):
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            elif self.martingale_count != 0 and (0.80*self.initial_pocket < self.pocket <= (self.initial_pocket + 0.40*self.initial_pocket)):
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            elif self.paroli_count != 0 and (0.60*self.initial_pocket < self.pocket <= 0.80*self.initial_pocket):
                #print("PAROLI\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_paroli(dealer=dealer, players=players)
            elif self.prog_count != 0 and (0.40*self.initial_pocket < self.pocket <= 0.60*self.initial_pocket):
                #print("PROGRESSIVE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_progressive(dealer=dealer, players=players)
            else:
                #print("MARTINGALE\n")
                if not self.want_to_play(rules=self.rules):
                    amount_to_bet = 0
                    print("Amount_to_bet: ", amount_to_bet)
                else:
                    amount_to_bet = self.bet_martingale(dealer=dealer, players=players)
            return amount_to_bet


    def bet_martingale(self, dealer, players):
        martingale_multiplier = math.pow(2, self.martingale_count)
        amount_to_bet = 1 * martingale_multiplier
        mart_count = self.martingale_count
        #if (self.martingale_count == 0) and ((50 - self.total_rounds) < 10): # Inhibit martingale system if we're on the last 9 games <- only possible if we know how many games we'll play
        #	amount_to_bet = 1
        if amount_to_bet > self.rules.max_bet:
            self.martingale_count = 0
            amount_to_bet = 1
        print("Amount_to_bet: ", amount_to_bet)
        print("Martingale_Count: ", mart_count)
        #self.amount_to_bet = amount_to_bet
        return amount_to_bet

    def bet_paroli(self, dealer, players):
        paroli_multiplier = self.paroli_count + 2
        amount_to_bet = 1 * paroli_multiplier
        parol_count = self.paroli_count
        if amount_to_bet > self.rules.max_bet:
            self.paroli_count = 0
            amount_to_bet = 1
        print("Amount_to_bet: ", amount_to_bet)
        print("Paroli Count: ", parol_count)
        return amount_to_bet

    def bet_min_bet(self, dealer, players): #só convem utilizar esta estratégia quando temos muitos jogos;
        amount_to_bet = (self.rules.min_bet + self.min_bet_count) #o player nao chega a apostar o minimo
        #amount_to_bet = self.rules.min_bet
        min_count = self.min_bet_count
        print("Amount_to_bet: ", amount_to_bet)
        print("Min_Bet_Count: ", min_count)
        return amount_to_bet

    def bet_max_bet(self, dealer, players): #só convem utilizar esta estrategia quando temos muitos jogos;
        amount_to_bet = (self.rules.max_bet - self.max_bet_count) #o player nao chega a apostar o maximo
        #amount_to_bet = self.rules.max_bet
        max_count = self.max_bet_count
        print("Amount_to_bet: ", amount_to_bet)
        print("Max_Bet_Count: ", max_count)
        return amount_to_bet

    def bet_progressive(self, dealer, players):
        amount_to_bet = self.prog_count
        p_count = self.prog_count
        if self.last_game_win != None:  #progressive v1
            amount_to_bet += 1
        else:
            amount_to_bet = 1     #progressive v2
        print("Amount_to_bet: ", amount_to_bet)
        print("Prog Count: ", p_count)
        return amount_to_bet

    def history_to_csv(self, file='Agent_history.csv'):
        file_write_lock.acquire()
        with open(file, 'a') as f:
            #f.write("val_player, numCards_player, ases_player, val_dealer, numCards_dealer, dealer_didntHit, ases_dealer, action_player, result\n")
            for play in self.plays_history:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (play.val_player, play.numCards_player, play.ases_player, play.val_dealer,
                                                       play.numCards_dealer, play.dealer_didntHit, play.ases_dealer, play.action_player, play.result))
            f.flush()
            f.close()
        file_write_lock.release()

    def payback(self, prize):
        #print("ENTREI NO PAYBACK\n")
        super(StudentPlayer, self).payback(prize)
        self.total_rounds += 1
        #print("Prize: ", prize)
        #print("Martingale_count: ", self.martingale_count)
        #print("Amount_to_Bet: ", self.amount_to_bet)
        if prize >= 0:
            if prize > 0:
                self.wins += 1
                self.martingale_count = 0
                self.paroli_count = 0
                self.prog_count = 0
                self.min_bet_count = 0
                self.max_bet_count = 0
                self.pocket += prize
            ganhou = 1
            self.loss_value = 0
            print("Ganhou: ", prize)
        else:
            self.losses += 1
            if self.double_down != 0:
                self.martingale_count += 1
                self.paroli_count += 1
                self.prog_count += 1
                self.max_bet_count += 1
                self.min_bet_count += 1
            self.martingale_count += 1
            self.paroli_count += 1
            self.prog_count += 1
            self.min_bet_count += 1
            self.max_bet_count += 1
            ganhou = 0
            self.loss_value += math.fabs(prize)
            self.pocket -= self.loss_value
            print("Perdeu: ", prize)

        self.last_game_win = ganhou == 1
        self.round_number = 0
        self.dealer_numCards = 0
        self.dealer_didntHit = 0
        self.plays_history.extend(map(lambda x: x.set_result(ganhou), self.plays))
        self.plays = []

    def want_to_play(self, rules):
        self.rules = rules
        #if self.wins > 1000 and ((self.pocket - self.initial_pocket) > self.initial_pocket) and self.last_game_win == 1:
        #   return False
        if self.wins > 1000 and ((self.pocket - self.initial_pocket) > 0) and self.last_game_win == 1:
            return False
        else:
            return True


class Play(object):
    def __init__(self, val_player, numCards_player, ases_player, val_dealer, numCards_dealer, dealer_didntHit, ases_dealer, action_player, result=None):
        self.val_player = val_player
        self.numCards_player = numCards_player
        self.ases_player = ases_player
        self.val_dealer = val_dealer
        self.numCards_dealer = numCards_dealer
        self.dealer_didntHit = dealer_didntHit
        self.ases_dealer = ases_dealer
        self.action_player = action_player
        self.result = result

    def set_result(self, result):
        self.result = result
        return self
