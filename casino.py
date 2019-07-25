from game import Game
from student import StudentPlayer
from multiprocessing import Pool
from ModelBuilder import Model
from randomplayer import RandomPlayer
import time

INIT_MONEY = 100
GAMES = 2500
ITER = 4
GENERATIONS = 1

def runGame(ID):
    print("Running iteration %d" % (ID,))
    players = [StudentPlayer("Versao2", INIT_MONEY, GAMES)]
    for i in range(GAMES):
        g = Game(players, min_bet=1, max_bet= 500, verbose=False)
        #print("Game nº: ",i)
        g.run()
    #for p in players:
    #         p.history_to_csv("newPlays.csv")

    print("wins: %d | losses: %d -> r %f" %(players[0].wins, players[0].losses, float(players[0].wins)/float(players[0].losses)))
    #print( "lucro-> ",((players[0].pocket - INIT_MONEY)))
    return ((players[0].pocket - INIT_MONEY))

if __name__ == '__main__':
    inicio = time.time()
    last_profit = 0
    for i in range(GENERATIONS):
        pool = Pool(processes=8)
        lucros = pool.map(runGame, range(ITER))
        print("Lucros: ", lucros)
        profit = sum(lucros) / float(len(lucros))
        last_profit = lucros[-1]
        print("Last_Profit: ", last_profit)
        print("%d games in %d seconds" % (GAMES * ITER, time.time() - inicio))
        print("Average profit in %d iterations: %.1f%%" % (ITER, profit ))
        print("Last Profit: %.1f%%" % (float(last_profit)) )
        print("Training\n")
        model = Model(debug=True, num_estimators=300, file_plays='newPlays.csv')
        model.train()
        inicio = time.time()
