import random
import numpy as np
import pandas as pd


class GameMaster:

    def __init__(self, dimen):
        self.game_map = self.genMap(dimen)
        self.target = self.create_random_target()

    def genMap(self, dimen):
        gamemap = [[0 for i in range(dimen)] for i in range(dimen)]

        for i in range(dimen):
            for j in range(dimen):
                num = random.random()
                if num <= 0.2:
                    gamemap[i][j] = 0  # flat terrain less than 0.2
                elif num > 0.2 and num <= 0.5:
                    gamemap[i][j] = 1  # hilly terrain between 0.2 and 0.5
                elif num > 0.5 and num <= 0.8:
                    gamemap[i][j] = 2  # forested terrain betwwen 0.5 and 0.8
                elif num > 0.8 and num <= 1:
                    gamemap[i][j] = 3  # caves terrain graeter than 0.8
        return gamemap

    def create_random_target(self):
        x = np.random.randint(0, len(self.game_map))
        y = np.random.randint(0, len(self.game_map))
        return (x, y)

    def search_cell(self, user_target):

        if self.target == user_target:
            num1 = random.random()
            terrain_type = self.game_map[self.target[0]][self.target[1]]
            if terrain_type == 0:
                if num1 <= 0.1:
                    return False
                else:
                    return True
            elif terrain_type == 1:
                if num1 <= 0.3:
                    return False
                else:
                    return True
            elif terrain_type == 2:
                if num1 <= 0.7:
                    return False
                else:
                    return True
            else:
                if num1 <= 0.9:
                    return False
                else:
                    return True
        else:
            return False

    def printMap(self):
        print(np.matrix(self.game_map))


class DummyPlayer:

    def __init__(self, map):
        self.map = map
        self.dimen = len(map)
        self.belief = self.create_belief_matrix(self.dimen)

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief

    def printBelief(self):
        print(np.matrix(self.belief))

    def update_belief_matrix(self, user_cell):
        if self.map[user_cell[0]][user_cell[1]] == 0:
            fnr = 0.1
        elif self.map[user_cell[0]][user_cell[1]] == 1:
            fnr = 0.3
        elif self.map[user_cell[0]][user_cell[1]] == 2:
            fnr = 0.7
        elif self.map[user_cell[0]][user_cell[1]] == 3:
            fnr = 0.9
        self.belief[user_cell[0]][user_cell[1]] *= fnr
        scaling_fac = 0
        sum = 0
        for i in range(self.dimen):
            for j in range(self.dimen):
                sum += self.belief[i][j]
        sum -= self.belief[user_cell[0]][user_cell[1]]
        scaling_fac = (1 - fnr) * self.belief[user_cell[0]][user_cell[1]] / sum

        for i in range(self.dimen):
            for j in range(self.dimen):
                if (i, j) != user_cell:
                    self.belief[i][j] *= scaling_fac
        # self.printMap(10, self.belief)
        # self.dummy_player(self.dimen, self.map, user_cell, self.belief)

    def next_move(self):

        y = max(map(max, self.belief))

        for i in range(self.dimen):
            for j in range(self.dimen):
                if self.belief[i][j] == y:
                    user_cell = (i, j)

        return user_cell
        # xyz = self.game_master(self.dimen, map, target, user_cell)
        #
        #
        # if xyz is True:
        #     print("you win")
        #     exit()
        # else:
        #     self.update_belief_matrix(dimen, map, user_cell, belief)


if __name__ == "__main__":
    dimen = 10
    game_master = GameMaster(dimen)
    dummy_player = DummyPlayer(game_master.game_map)
    game_won = False

    i = 0

    while not game_won:
        i += 1
        user_cell = dummy_player.next_move()
        game_won = game_master.search_cell(user_cell)
        dummy_player.update_belief_matrix(user_cell)
        print("\nMove : {}\n".format(i))
        dummy_player.printBelief()

    print("Kudos you Won!!!")
# x=Game()
# map=x.genMap(10,(x.genMap(10),10))
# target = x.create_random_target(dimen)
#print("target")
# x.dummy_player(10,map,target,x.create_belief_matrix(10))