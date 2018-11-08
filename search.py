import random
import numpy as np
import pandas as pd


class Game:

    def genMap(self, dimen):
        map = [['0' for i in range(dimen)] for i in range(dimen)]

        for i in range(dimen):
            for j in range(dimen):

                num = random.random()
                if num <= 0.2:
                    map[i][j] = 0  # flat terrain less than 0.2
                elif num > 0.2 and num <= 0.5:
                    map[i][j] = 1  # hilly terrain between 0.2 and 0.5
                elif num > 0.5 and num <= 0.8:
                    map[i][j] = 2  # forested terrain betwwen 0.5 and 0.8
                elif num > 0.8 and num <= 1:
                    map[i][j] = 3  # caves terrain graeter than 0.8
        return map

    def create_random_target(self, dimen):
        x = np.random.randint(0, dimen)
        y = np.random.randint(0, dimen)
        return tuple(x, y)

        return map

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief

    def game_master(self, dimen, map, user_target, target):

        if target == y:
            num1 = random.random()
            terrain_type = map[target[0]][target[1]]
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

    def update_belief_matrix(self, dimen, map, user_cell, belief):
        if map[user_cell[0]][user_cell[1]] == '0':
            fnr = 0.1
        elif map[user_cell[0]][user_cell[1]] == '1':
            fnr = 0.3
        elif map[user_cell[0]][user_cell[1]] == '2':
            fnr = 0.7
        elif map[user_cell[0]][user_cell[1]] == '3':
            fnr = 0.9
        belief[user_cell[0]][user_cell[1]] *= fnr
        scaling_fac = 0
        sum = 0
        for i in range(dimen):
            for j in range(dimen):
                sum += belief[i][j]
        scaling_fac = 1 / sum
        for i in range(dimen):
            for j in range(dimen):
                belief[i][j] *= scaling_fac
        self.printMap(10, belief)
        self.dummy_player(dimen, map, user_cell, belief)

    def dummy_player(self, dimen, map, target, belief):

        y = max(map(max, belief))
        for i in range(dimen):
            for j in range(dimen):
                if map[i][j] == y:
                    user_cell = tuple(i, j)
        xyz = self.game_master(dimen, map, target, user_cell)

        if xyz is True:
            print("you win")
            exit()
        else:
            self.update_belief_matrix(dimen, map, user_cell, belief)

    def printMap(self, dim, map):
        print(np.matrix(map))


# x=Game()
# map=x.genMap(10,(x.genMap(10),10))
# target = x.create_random_target(dimen)
#print("target")
# x.dummy_player(10,map,target,x.create_belief_matrix(10))