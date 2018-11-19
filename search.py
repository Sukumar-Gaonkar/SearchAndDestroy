import random
import time, math
from itertools import count
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from collections import Counter

case_str = ["", "Proportional Terrain Selection", "Unbiased Terrain Selection"]
rule_str = ["", "Belief Matrix", "Confidence Matrix"]


class TerrainType(Enum):
    PLAINS = 0
    HILLY = 1
    FOREST = 2
    CAVES = 3


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
        # while True:
        x = np.random.randint(0, len(self.game_map))
        y = np.random.randint(0, len(self.game_map))
            # if self.game_map[x][y] == TerrainType.PLAINS.value:
            #     break
        return (x, y)

    def search_cell(self, user_target):

        if self.target == user_target:
            num1 = random.random()
            terrain_type = self.game_map[self.target[0]][self.target[1]]
            if terrain_type == TerrainType.PLAINS.value:
                if num1 <= 0.1:
                    return False
                else:
                    return True
            elif terrain_type == TerrainType.HILLY.value:
                if num1 <= 0.3:
                    return False
                else:
                    return True
            elif terrain_type == TerrainType.FOREST.value:
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

    def __init__(self, game_map, case, rule, iteration):
        self.map = game_map
        self.dimen = len(game_map)
        self.rule = rule
        self.case = case
        self.hit_freq = [[0 for j in range(self.dimen)] for i in range(self.dimen)]
        self.belief = self.create_belief_matrix(self.dimen)
        self.confidence_mat = self.create_belief_matrix(self.dimen)

        self.terrain_counts = [0, 0, 0, 0]
        for x in range(self.dimen):
            for y in range(self.dimen):
                self.terrain_counts[self.map[x][y]] += 1

        min_val = float('inf')
        for x in self.terrain_counts:
            if x is not 0 and x < min_val:
                min_val = x
        self.terrain_counts = list(map(lambda n: math.ceil(n / min_val), self.terrain_counts))

        # self.plaincount=sum(x.count(TerrainType.PLAINS.value) for x in map)
        # self.hillcount=sum(x.count(TerrainType.HILLY.value) for x in map)
        # self.forestcount=sum(x.count(TerrainType.FOREST.value) for x in map)
        # self.cavecount=sum(x.count(TerrainType.CAVES.value) for x in map)
        # self.arr1=[[TerrainType.PLAINS.value]*self.plaincount,[TerrainType.HILLY.value]*self.hillcount,[TerrainType.FOREST.value]*self.forestcount,[TerrainType.CAVES.value]*self.cavecount]
        # self.arr=[item for sublist in self.arr1 for item in sublist]
        # self.k=0
        # self.sort_arr=[item for items, c in Counter(self.arr).most_common() for item in [items] * c]

        self.marker = 5
        game_map[0][0] += self.marker
        self.prev_cell = (0, 0)

        plt.ion()
        self.fig = plt.figure(figsize=(10, 6))
        self.fig.suptitle("Iteration: {}  Case: {}  Rule: {}".format(iteration, case_str[case], rule_str[rule]))
        # self.ax = plt.subplot(1, 3, 1)
        self.belief_plot = plt.subplot(1, 3, 1).matshow(self.belief, cmap='Greys')
        plt.colorbar(self.belief_plot)

        cdict1 = {'red': ((0.0, 1.0, 1.0),
                          (0.2, 0.8, 0.8),
                          (0.4, 0.6, 0.6),
                          (0.6, 0.4, 0.4),
                          (0.8, 0.2, 0.2),
                          (1, 0, 0)),
                  'green': ((0.0, 1.0, 1.0),
                            (0.2, 0.8, 0.8),
                            (0.4, 0.6, 0.6),
                            (0.6, 0.4, 0.4),
                            (0.8, 0.2, 0.2),
                            (1, 0, 0)),
                  'blue': ((0.0, 1.0, 1.0),
                           (0.2, 0.8, 0.8),
                           (0.4, 0.6, 0.6),
                           (0.6, 0.4, 0.4),
                           (0.8, 0.2, 0.2),
                           (1, 0, 0))
                  }

        cm = LinearSegmentedColormap('BlueRed1', cdict1)
        self.terrain_plot = self.fig.add_subplot(1, 3, 2).matshow(game_map, cmap=cm)

        self.freq_ax = self.fig.add_subplot(1, 3, 3)
        self.freq_plot = self.freq_ax.matshow(self.hit_freq)

        self.hit_freq_texts = [[None for i in range(self.dimen)] for i in range(self.dimen)]

        for (i, j), z in np.ndenumerate(self.hit_freq):
            self.hit_freq_texts[i][j] = self.freq_ax.text(j, i, '{}'.format(z), ha='center', va='center')

        plt.show()

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief

    def print_mat(self, mat):
        print(np.matrix(mat))

    def update_belief_matrix(self, user_cell):

        if self.map[user_cell[0]][user_cell[1]] > 3:
            cell_val = self.map[user_cell[0]][user_cell[1]] - self.marker
        else:
            cell_val = self.map[user_cell[0]][user_cell[1]]

        if cell_val == TerrainType.PLAINS.value:     # Plains
            fnr = 0.1
        elif cell_val == TerrainType.HILLY.value:   # Hilly
            fnr = 0.3
        elif cell_val == TerrainType.FOREST.value:   # Forest
            fnr = 0.7
        elif cell_val == TerrainType.CAVES.value:   # Caves
            fnr = 0.9

        sum = 1 - (1 - fnr) * self.belief[user_cell[0]][user_cell[1]]
        # scaling_fac = (1 - fnr) * self.belief[user_cell[0]][user_cell[1]] / sum
        self.belief[user_cell[0]][user_cell[1]] *= fnr


        # Renormalize the Grid
        for i in range(self.dimen):
            for j in range(self.dimen):
                    self.belief[i][j] /= sum
                    self.confidence_mat[i][j] = (self.belief[i][j] / sum) * (1 - fnr)

    def next_move(self):

        move_counter = 0
        for move_counter in count():

            if self.case == 1:
                # Proportional Terrain Selection

                # Terrain Selection
                curr_sum = self.terrain_counts[0]
                active_terrain = 0
                temp_counter = move_counter % sum(self.terrain_counts) + 1
                while temp_counter > curr_sum:
                    active_terrain += 1
                    curr_sum += self.terrain_counts[active_terrain]

                maxm = 0

                # TODO: if the max of one of the terrains is too low then dont search it

                for i in range(self.dimen):
                    for j in range(self.dimen):
                     #   print(self.k)
                        if self.map[i][j] == active_terrain:
                            if self.rule == 1:
                                # Belief Matrix
                                if self.belief[i][j] > maxm:

                                    maxm = self.belief[i][j]
                                    user_cell = (i, j)
                            elif self.rule == 2:
                                # Confidence Matrix
                                if self.confidence_mat[i][j] > maxm:

                                    maxm = self.confidence_mat[i][j]
                                    user_cell = (i, j)
                # self.k=self.k+1

            if(self.case==2):
                # Unbiased Terrain Selection
                if(self.rule==1):
                    # Belief Matrix
                    y = max(map(max, self.belief))
                    for i in range(self.dimen):
                        for j in range(self.dimen):
                            if self.belief[i][j] == y:
                                user_cell = (i, j)
                elif(self.rule==2):
                    # Confidence Matrix
                    y = max(map(max, self.confidence_mat))
                    for i in range(self.dimen):
                        for j in range(self.dimen):
                            if self.confidence_mat[i][j] == y:
                                user_cell = (i, j)

            if self.prev_cell is not None:
                self.map[self.prev_cell[0]][self.prev_cell[1]] -= self.marker

            self.prev_cell = user_cell
            self.map[user_cell[0]][user_cell[1]] += self.marker

            self.hit_freq[user_cell[0]][user_cell[1]] += 1
            hit_count = self.hit_freq[user_cell[0]][user_cell[1]]
            # self.freq_ax.text(user_cell[0], user_cell[1], '{}'.format(hit_count), ha='center', va='center')
            self.hit_freq_texts[user_cell[0]][user_cell[1]].set_text(str(hit_count))


            move_counter += 1
            yield user_cell


if __name__ == "__main__":
    # dimen = 3
    iterations = 1
    fileName = "results/profilerResults_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    f = open(fileName, "a", 1)
    f.write("Gridsize;IterationNo;Case;Rule;Searches\n")

    for itr in range(1, iterations+1):
        # Iteration Loop
        for dimen in range(5, 11):
            game_master = GameMaster(dimen)

            for case in range(1, 3):
                for rule in range(1, 3):

                    dummy_player = DummyPlayer(game_master.game_map, case, rule, itr)
                    move_generator = dummy_player.next_move()
                    game_won = False
                    game_master.printMap()
                    dummy_player.print_mat(dummy_player.belief)
                    terrains = ["Plains", "Hilly", "Forest", "Caves"]
                    print(dummy_player.map[game_master.target[0]][game_master.target[1]])
                    print("Dimen: {}  Target: {},{} : {}".format(dimen, game_master.target[0], game_master.target[1], terrains[(dummy_player.map[game_master.target[0]][game_master.target[1]])%5]))
                  #  input("Press 'Y' Key to continue")      # just to stop the execution before entering while loop
                    i = 0

                    while not game_won:
                        i += 1
                        user_cell = next(move_generator)
                        game_won = game_master.search_cell(user_cell)
                        dummy_player.update_belief_matrix(user_cell)
                        print("\nMove - {}: {},{}\n".format(i,user_cell[0],user_cell[1]))
                        dummy_player.print_mat(dummy_player.belief)
                        dummy_player.terrain_plot.set_data(dummy_player.map)
                        dummy_player.belief_plot.set_data(dummy_player.belief)
                        dummy_player.freq_plot.set_data(dummy_player.hit_freq)
                        dummy_player.fig.canvas.draw()
                        plt.pause(0.0001)
                        # time.sleep(0.1)
                    else:
                        game_master.game_map[game_master.target[0]][game_master.target[1]] -= dummy_player.marker
                        plt.close(dummy_player.fig)

                    print("Kudos you Won!!!\n{} cells Searched".format(i))

                    f.write("{0};{1};{2};{3};{4}\n".format(dimen, itr, case_str[case], rule_str[rule], i))
                    #input()

