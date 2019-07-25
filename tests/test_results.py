#encoding: utf8
import sys
sys.path.insert(0,"..")
from game import Game
from player import Player
from card import Card
from test_shoe import TestShoe
from student import StudentPlayer

#class TestPlayer(Player):
#    def __init__(self, name="TestPlayer", money=0, default_bet=1):
#        super(TestPlayer, self).__init__(name, money)
#        self.default_bet = default_bet

#    def play(self, dealer, players):
#        print("HIT\n")
#        return "h"

#    def bet(self, dealer, players):
#        return self.default_bet

if __name__ == '__main__':

    players = [StudentPlayer("PEDRO",2000)]

    print("Players: ", players)
    rules = Game.Rules()
    print("Game Rules: ", rules.__str__())
    g = Game(players, debug=True, shoe=TestShoe([Card(0,1), Card(0,2), Card(1,1), Card(1,12),
                                                 Card(0, 1), Card(0, 12), Card(1, 1), Card(1, 6), Card(2, 10),
                                                 Card(0, 1), Card(0, 12), Card(1, 1), Card(1, 12),
                                                 Card(0, 1), Card(0, 5), Card(1, 1), Card(1, 5), Card(2, 3), Card(3, 5),
                                                 Card(3, 9), Card(1, 8), Card(1, 7), Card(2, 4), Card(3, 9),
                                                 Card(3, 8), Card(1, 10), Card(1, 13), Card(2, 3), Card(3, 9),
                                                 Card(3, 12), Card(3, 6), Card(1, 2), Card(1, 8), Card(2, 4), Card(3, 3)] ))

    g1 = Game(players, debug=True, shoe=TestShoe([Card(3,3), Card(2,4), Card(1,8), Card(1,2), Card(3,6), Card(3,12),
                                                 Card(3,9), Card(2,3), Card(1,13), Card(1,10), Card(3,8),
                                                 Card(3,9), Card(2,4), Card(1,7), Card(1,8), Card(3,9),
                                                 Card(3,5), Card(2,3), Card(1,5), Card(1,1), Card(0,5), Card(0,1),
                                                 Card(1,12), Card(1,1), Card(0,12), Card(0,1),
                                                 Card(2,10), Card(1,6), Card(1,1), Card(0,12), Card(0,1),
                                                 Card(1,12), Card(1,1), Card(0,2), Card(0,1)] ))


    g2 = Game(players, debug=True, shoe=TestShoe([Card(1,12), Card(1,1), Card(0,2), Card(0,1),
                                                  Card(2,10), Card(1,6), Card(1,1), Card(0,12), Card(0,1),
                                                  Card(1,12), Card(1,1), Card(0,12), Card(0,1),
                                                  Card(3,5), Card(2,3), Card(1,5), Card(1,1), Card(0,5), Card(0,1),
                                                  Card(3,9), Card(2,4), Card(1,7), Card(1,8), Card(3,9),
                                                  Card(3,9), Card(2,3), Card(1,13), Card(1,10), Card(3,8),
                                                  Card(3,3), Card(2,4), Card(1,8), Card(1,2), Card(3,6), Card(3,12)] ))

    g3 = Game(players, debug=True, shoe=TestShoe([Card(3, 12), Card(3, 6), Card(1, 2), Card(1, 8), Card(2, 4), Card(3, 3),
                                                  Card(3, 8), Card(1, 10), Card(1, 13), Card(2, 3), Card(3, 9),
                                                  Card(3, 9), Card(1, 8), Card(1, 7), Card(2, 4), Card(3, 9),
                                                  Card(0, 1), Card(0, 5), Card(1, 1), Card(1, 5), Card(2, 3), Card(3, 5),
                                                  Card(0, 1), Card(0, 12), Card(1, 1), Card(1, 12),
                                                  Card(0, 1), Card(0, 12), Card(1, 1), Card(1, 6), Card(2, 10),
                                                  Card(0, 1), Card(0, 2), Card(1, 1), Card(1, 12)] ))


    g.run()
    print("#############################################################################################################################################################\n")
    g1.run()
    print("#############################################################################################################################################################\n")
    g2.run()
    print("#############################################################################################################################################################\n")
    g3.run()
    print("#############################################################################################################################################################\n")

    print("OVERALL: ", players)
    if str(players) == "[PEDRO (4000€)]":
        sys.exit(0)
    sys.exit(1)


