import random, math, time
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

case_str = ["", "Proportional Terrain Selection", "Unbiased Terrain Selection"]
rule_str = ["", "Belief Matrix", "Confidence Matrix"]


def get_fnr(cell_val):
    if cell_val == 0:  # Plains
        fnr = 0.1
    elif cell_val == 1:  # Hilly
        fnr = 0.3
    elif cell_val == 2:  # Forest
        fnr = 0.7
    elif cell_val == 3:  # Caves
        fnr = 0.9
    return fnr


class GameMaster:

    def __init__(self, dimen, moving_target, visualize):
        self.target_hit_counter = 0
        self.target_marker = 20
        self.moving_target = moving_target
        self.visualize = visualize

        self.game_map = self.genMap(dimen)
        self.target = self.create_random_target()
        self.dummy_player = None

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
        # return [[0, 2, 3], [2, 2, 1], [1, 2, 3]]
        return gamemap

    def create_random_target(self):
        # while True:
        x = np.random.randint(0, len(self.game_map))
        y = np.random.randint(0, len(self.game_map))
            # if self.game_map[x][y] == 3:
                # break
        return (x, y)

    def search_cell(self, user_target):

        if tuple(self.target) == user_target:
            reqd_hits = [2, 2, 4, 10]
            if self.target_hit_counter == reqd_hits[self.game_map[user_target[0]][user_target[1]] % 5]:
                self.target_hit_counter = 0
                return True
            else:
                self.target_hit_counter += 1
                return False

            # num1 = random.random()
            # terrain_type = self.game_map[self.target[0]][self.target[1]]
            # terrain_type = terrain_type - 5 if terrain_type >= 5 else terrain_type
            # if terrain_type == 0:
            #     if num1 > 0.1:
            #         return True
            # elif terrain_type == 1:
            #     if num1 > 0.3:
            #         return True
            # elif terrain_type == 2:
            #     if num1 > 0.7:
            #         return True
            # elif terrain_type == 3:
            #     if num1 > 0.9:
            #         return True

        # You got False

        if not self.moving_target:
            return False
        else:
            crossing = [0, 0]

            if visualize:
                self.dummy_player.hit_freq[self.target[0]][self.target[1]] -= self.target_marker
                self.dummy_player.hit_freq_texts[self.target[0]][self.target[1]].set_text(str(self.dummy_player.hit_freq[self.target[0]][self.target[1]]))

            crossing[0] = self.game_map[self.target[0]][self.target[1]]

            temp_target = self.target
            moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            move = moves[random.randint(0, 7)]
            temp_target = [move[0] + self.target[0], move[1] + self.target[1]]
            while not self.isvalid(temp_target):
                move = moves[random.randint(0, 7)]
                temp_target = [move[0] + self.target[0], move[1] + self.target[1]]

            self.target = temp_target
            crossing[1] = self.game_map[self.target[0]][self.target[1]]
            if visualize:
                self.dummy_player.hit_freq[temp_target[0]][temp_target[1]] += self.target_marker
                self.dummy_player.hit_freq_texts[temp_target[0]][temp_target[1]].set_text(
                    str(self.dummy_player.hit_freq[temp_target[0]][temp_target[1]]))

            return crossing

    def isvalid(self, target):
        if target[0] > -1 and target[0] < len(self.game_map) and target[1] > -1 and target[1] < len(self.game_map):
            return True
        else:
            return False

    def printMap(self):
        print(np.matrix(self.game_map))

    def set_player(self, player):
        self.dummy_player = player
        if visualize:
            self.dummy_player.hit_freq[self.target[0]][self.target[1]] += self.target_marker


class DummyPlayer:

    def __init__(self, game_map, moving_target, case, rule, iteration, visualize):
        self.map = game_map
        self.dimen = len(game_map)
        self.rule = rule
        self.case = case
        if visualize:
            self.hit_freq = [[0 for j in range(self.dimen)] for i in range(self.dimen)]
        self.belief = self.create_belief_matrix(self.dimen)
        self.moving_target = moving_target
        self.confidence_mat = self.create_belief_matrix(self.dimen)

        for x in range(dimen):
            for y in range(dimen):
                self.confidence_mat[x][y] *= (1 - get_fnr(self.map[x][y]))

        self.terrain_counts = [0, 0, 0, 0]
        for x in range(self.dimen):
            for y in range(self.dimen):
                self.terrain_counts[self.map[x][y]] += 1

        min_val = float('inf')
        for x in self.terrain_counts:
            if x is not 0 and x < min_val:
                min_val = x
        self.terrain_counts = list(map(lambda n: math.ceil(n / min_val), self.terrain_counts))

        self.marker = 5
        game_map[0][0] += self.marker
        self.prev_cell = (0, 0)

        if visualize:
            plt.ion()
            self.fig = plt.figure(figsize=(10, 6))
            self.fig.suptitle("Iteration: {}  Case: {}  Rule: {}".format(iteration, case_str[case], rule_str[rule]))
            # self.ax = plt.subplot(1, 3, 1)
            self.belief_plot = plt.subplot(2, 2, 1).matshow(self.belief, cmap='Greys')
            # self.belief_plot.set_clim(0, 1)
            plt.colorbar(self.belief_plot)

            self.confidence_plot = plt.subplot(2, 2, 2).matshow(self.confidence_mat, cmap='Greys')
            # self.confidence_plot.set_clim(0, 1)
            plt.colorbar(self.confidence_plot)

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
            # cm = matplotlib.colors.ListedColormap(terrain_colors)
            self.terrain_plot = self.fig.add_subplot(2, 2, 3).matshow(game_map, cmap=cm)

            self.freq_ax = self.fig.add_subplot(2, 2, 4)
            self.freq_plot = self.freq_ax.matshow(self.hit_freq, cmap="Oranges")

            self.hit_freq_texts = [[None for i in range(self.dimen)] for i in range(self.dimen)]

            for (i, j), z in np.ndenumerate(self.hit_freq):
                self.hit_freq_texts[i][j] = self.freq_ax.text(j, i, '{}'.format(z), ha='center', va='center')

            plt.show()

    def isvalid(self, target):
        if target[0] > -1 and target[0] < len(self.map) and target[1] > -1 and target[1] < len(self.map):
            return True
        else:
            return False

    def create_belief_matrix(self, dimen):
        belief = [[1 / (dimen * dimen) for j in range(dimen)] for i in range(dimen)]
        return belief

    def printBelief(self):
        print(np.matrix(self.belief))

    def update_borders(self, i, j, dst, holder_mat):
        count = 0
        moves = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        valid_cells = []
        for move in moves:
            cell = [i + move[0], j + move[1]]
            if self.isvalid((cell[0], cell[1])) and self.map[cell[0]][cell[1]] % self.marker == dst:
                valid_cells.append(cell)
                count += 1

        for cell in valid_cells:
            holder_mat[cell[0]][cell[1]] = holder_mat[cell[0]][cell[1]] + self.belief[i][j] / count

        return count

    def border_cross_detected(self, user_cell, cross):
        # print(cross)

        if cross is not False:
            cross[0] = cross[0] % self.marker
            cross[1] = cross[1] % self.marker

        if self.map[user_cell[0]][user_cell[1]] > 3:
            cell_val = self.map[user_cell[0]][user_cell[1]] - self.marker
        else:
            cell_val = self.map[user_cell[0]][user_cell[1]]

        fnr = get_fnr(cell_val)

        sum = 1 - (1 - fnr) * self.belief[user_cell[0]][user_cell[1]]
        self.belief[user_cell[0]][user_cell[1]] *= fnr

        if self.moving_target:

            holder_mat = [[0 for j in range(dimen)] for i in range(dimen)]
            for i in range(dimen):
                for j in range(dimen):
                    if self.map[i][j] % self.marker == cross[0]:
                        self.update_borders(i, j, cross[1], holder_mat)
                    elif self.map[i][j] % self.marker == cross[1]:
                        self.update_borders(i, j, cross[0], holder_mat)
                    else:
                        sum -= self.belief[i][j]
                        holder_mat[i][j] = 0

            self.belief = holder_mat

        sum = 0
        for i in range(dimen):
            for j in range(dimen):
                sum += self.belief[i][j]

        confidence_sum = 0

        # Renormalize the Grid
        for i in range(self.dimen):
            for j in range(self.dimen):
                self.belief[i][j] /= sum
                self.confidence_mat[i][j] = self.belief[i][j] * (1 - get_fnr(self.map[i][j] % self.marker))
                confidence_sum += self.confidence_mat[i][j]

        # Renormalize the Confidence Matrix
        for i in range(self.dimen):
            for j in range(self.dimen):
                self.confidence_mat[i][j] /= confidence_sum

    def next_move(self):

        # y = max(map(max, self.belief))

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
                        if self.map[i][j] % self.marker == active_terrain:
                            if self.rule == 1:
                                # Belief Matrix
                                if self.belief[i][j] >= maxm:
                                    maxm = self.belief[i][j]
                                    user_cell = (i, j)
                            elif self.rule == 2:
                                # Confidence Matrix
                                if self.confidence_mat[i][j] >= maxm:
                                    maxm = self.confidence_mat[i][j]
                                    user_cell = (i, j)

            if (self.case == 2):
                # Unbiased Terrain Selection
                if (self.rule == 1):
                    # Belief Matrix
                    y = max(map(max, self.belief))
                    for i in range(self.dimen):
                        for j in range(self.dimen):
                            if self.belief[i][j] == y:
                                user_cell = (i, j)
                elif (self.rule == 2):
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

            if visualize:
                self.hit_freq[user_cell[0]][user_cell[1]] += 1
                hit_count = self.hit_freq[user_cell[0]][user_cell[1]]
                # self.freq_ax.text(user_cell[0], user_cell[1], '{}'.format(hit_count), ha='center', va='center')
                self.hit_freq_texts[user_cell[0]][user_cell[1]].set_text(str(hit_count))

            move_counter += 1
            yield user_cell


if __name__ == "__main__":
    # dimen = 15

    moving_target = False
    visualize = False

    iterations = 10
    fileName = "results/profilerResults_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
    f = open(fileName, "a", 1)
    f.write("Gridsize;IterationNo;Terrain;Case;Rule;Searches\n")

    for dimen in range(3, 30):
        for itr in range(1, iterations+1):
            # Iteration Loop
            game_master = GameMaster(dimen, moving_target, visualize)

            for case in range(1, 3):
                for rule in range(1, 3):

                    dummy_player = DummyPlayer(game_master.game_map, moving_target, case, rule, iterations, visualize)
                    game_master.set_player(dummy_player)
                    move_generator = dummy_player.next_move()
                    game_won = False

                    # dummy_player.hit_freq[game_master.target[0]][game_master.target[1]] += game_master.target_marker
                    # game_master.printMap()
                    # dummy_player.printBelief()

                    terrains = ["Plains", "Hilly", "Forest", "Caves"]
                    print("Dimen: {}  Target: {},{} : {}".format(dimen, game_master.target[0], game_master.target[1], terrains[dummy_player.map[game_master.target[0]][game_master.target[1]] % 5]))

                    # input("Press 'Y' Key to continue")      # just to stop the execution before entering while loop
                    i = 0

                    while True:
                        i += 1
                        user_cell = next(move_generator)
                        status = game_master.search_cell(user_cell)
                        crossing = None
                        if status == True:
                            break
                        else:
                            crossing = status

                        dummy_player.border_cross_detected(user_cell, crossing)
                        # dummy_player.update_belief_matrix(user_cell)
                        # print("\nMove - {}: {},{}\n".format(i, user_cell[0], user_cell[1]))

                        # dummy_player.printBelief()
                        if visualize:
                            dummy_player.terrain_plot.set_data(dummy_player.map)
                            dummy_player.belief_plot.set_data(dummy_player.belief)
                            dummy_player.confidence_plot.set_data(dummy_player.confidence_mat)
                            dummy_player.freq_plot.set_data(dummy_player.hit_freq)
                            dummy_player.freq_plot.set_clim(0, game_master.target_marker)
                            dummy_player.fig.canvas.draw()
                            plt.pause(0.001)
                        # time.sleep(0.9)

                    game_master.game_map[game_master.target[0]][game_master.target[1]] -= dummy_player.marker
                    if visualize:
                        plt.close(dummy_player.fig)

                    target = game_master.target

                    target_terrain = terrains[game_master.game_map[target[0]][target[1]]]
                    print("Kudos you Won!!!\n{} cells Searched".format(i))
                    f.write("{0};{1};{2};{3};{4};{5}\n".format(dimen, itr, target_terrain, case_str[case], rule_str[rule], i))
                    # input()
